import os
import torch
from transformers.models.auto.modeling_auto import AutoModelForCausalLM
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.pipelines import pipeline
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from config.logger import log

from config.bootstrap import database, s3


class ModelLoader:
    """Model loader with S3 support and automatic device placement."""
    
    def __init__(self, model_name: str, s3_path: str = None, device: str = "auto"):
        self.model_name = model_name
        self.s3_path = s3_path
        self.device = device
        self.model = None
        self.tokenizer = None
    
    def load_model_from_s3_or_hf(self, model_name: str, s3_path: str) -> AutoModelForCausalLM:
        """Load model from S3 or Hugging Face with PyTorch backend."""
        try:
            # Check if the model exists in S3
            s3_bucket = os.getenv('S3_BUCKET', 'default-bucket')
            s3.download(s3_bucket, s3_path, model_name)
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            log.info("Model loaded from S3.")
        except Exception as e:
            log.info("Model not found in S3, loading from Hugging Face.")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            model.save_pretrained(model_name)
            s3_bucket = os.getenv('S3_BUCKET', 'default-bucket')
            s3.upload(f'{model_name}', s3_bucket, s3_path)
            log.info("Model downloaded and uploaded to S3.")
        return model
    
    def load_model(self) -> tuple[AutoModelForCausalLM, AutoTokenizer]:
        """Load model and tokenizer with S3 support."""
        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model with S3 support
            if self.s3_path:
                self.model = self.load_model_from_s3_or_hf(self.model_name, self.s3_path)
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16,
                    device_map="auto",
                    trust_remote_code=True,
                    low_cpu_mem_usage=True
                )
            
            log.info(f"Model {self.model_name} loaded successfully")
            return self.model, self.tokenizer
            
        except Exception as e:
            log.error(f"Error loading model {self.model_name}: {e}")
            raise


class EmbeddingGenerator:
    """Embedding generator using sentence transformers."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.embedding_model = SentenceTransformer(model_name)
        log.info(f"Embedding model {model_name} loaded successfully")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for given text."""
        try:
            embedding = self.embedding_model.encode(text)
            return embedding
        except Exception as e:
            log.error(f"Error generating embedding: {e}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a batch of texts."""
        try:
            embeddings = self.embedding_model.encode(texts)
            return embeddings
        except Exception as e:
            log.error(f"Error generating batch embeddings: {e}")
            raise


class ResponseGenerator:
    """Response generator with proper prompt handling and error recovery."""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium", s3_path: str = None):
        self.model_loader = ModelLoader(model_name, s3_path)
        self.model, self.tokenizer = self.model_loader.load_model()
        self.generation_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto"
        )
        log.info(f"Response generator initialized with {model_name}")
    
    def generate_response(self, prompt: str, max_length: int = 200, temperature: float = 0.7) -> str:
        """Generate response with proper error handling and logging."""
        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=512
            )
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the input prompt from response
            response = response[len(prompt):].strip()
            
            # Log the interaction
            self._log_interaction(prompt, response)
            
            return response
            
        except Exception as e:
            log.error(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"
    
    def _log_interaction(self, prompt: str, response: str) -> None:
        """Log the interaction to database."""
        try:
            database.write({
                'query': prompt,
                'context': '',
                'answer': response
            }, '', '')
        except Exception as e:
            log.warning(f"Failed to log interaction: {e}")


# Initialize global instances
embedding_generator = EmbeddingGenerator()
response_generator = ResponseGenerator()

# Backward compatibility functions
def load_model_from_s3_or_hf(model_name: str, s3_path: str) -> AutoModelForCausalLM:
    """Load model from S3 or Hugging Face - backward compatibility."""
    model_loader = ModelLoader(model_name, s3_path)
    model, _ = model_loader.load_model()
    return model

def encode_query(query: str) -> np.ndarray:
    """Generate embedding for query using sentence transformers."""
    return embedding_generator.generate_embedding(query)

def generate_response(augmented_input: str) -> str:
    """Generate response using response generator."""
    return response_generator.generate_response(augmented_input)
