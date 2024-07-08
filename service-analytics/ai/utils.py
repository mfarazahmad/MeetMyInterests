import os
import tensorflow as tf
from transformers import AutoTokenizer, TFDPRQuestionEncoder, TFDPRContextEncoder, TFAutoModelForCausalLM

from config.bootstrap import database, s3
from config.logger import log

def load_model_from_s3_or_hf(model_name, s3_path):
    try:
        # Check if the model exists in S3
        s3.download(s3_bucket, s3_path, model_name)
        model = TFAutoModelForCausalLM.from_pretrained(model_name)
        log.info("Model loaded from S3.")
    except Exception as e:
        log.info("Model not found in S3, loading from Hugging Face.")
        model = TFAutoModelForCausalLM.from_pretrained(model_name)
        model.save_pretrained(model_name)
        s3.upload(f'{model_name}', s3_bucket, s3_path)
        log.info("Model downloaded and uploaded to S3.")
    return model

# Load models
tokenizer = AutoTokenizer.from_pretrained('huggingface/llama-3b')
question_encoder = TFDPRQuestionEncoder.from_pretrained('facebook/dpr-question_encoder-single-nq-base')
context_encoder = TFDPRContextEncoder.from_pretrained('facebook/dpr-context_encoder-single-nq-base')
llama_model = load_model_from_s3_or_hf('llama3_model', os.getenv('MODEL_PATH'))

def encode_query(query):
    inputs = tokenizer(query, return_tensors='tf')
    return question_encoder(**inputs).pooler_output.numpy().squeeze()

def generate_response(augmented_input):
    llama_inputs = tokenizer(augmented_input, return_tensors='tf', truncation=True)
    outputs = llama_model.generate(**llama_inputs, max_length=200)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    database.write({'query': augmented_input, 'context': '', 'answer':answer}, '', '')
    return answer
