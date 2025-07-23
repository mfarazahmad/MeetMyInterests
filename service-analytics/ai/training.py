import datetime
import os
import torch
from transformers.models.auto.modeling_auto import AutoModelForCausalLM
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.trainer import Trainer
from transformers.training_args import TrainingArguments
from transformers.data.data_collator import DataCollatorForLanguageModeling
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType as PEFTTaskType

from ai.pipelines.financial import initialize_financial_index
from ai.pipelines.pdf import initialize_pdf_index
from ai.utils import ModelLoader

from config.bootstrap import s3
from config.logger import log


def train_pdf_data():
    """Train model with PDF data using PyTorch + Hugging Face."""
    try:
        chunks = initialize_pdf_index()
        
        # Load model with S3 support
        model_loader = ModelLoader('microsoft/DialoGPT-medium', os.getenv('MODEL_PATH'))
        model, tokenizer = model_loader.load_model()
        
        # Prepare dataset
        def tokenize_function(examples):
            return tokenizer(
                examples['text'],
                truncation=True,
                padding=True,
                max_length=512
            )
        
        # Create dataset
        dataset_dict = {'text': chunks}
        dataset = Dataset.from_dict(dataset_dict)
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        
        # Configure LoRA for efficient fine-tuning
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.1,
            bias="none",
            task_type=PEFTTaskType.CAUSAL_LM
        )
        
        model = get_peft_model(model, lora_config)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir="./pdf_model",
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir="./logs",
            logging_steps=10,
            save_steps=1000,
            eval_steps=500,
            evaluation_strategy="steps",
            load_best_model_at_end=True,
            save_total_limit=2,
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )
        
        # Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator,
        )
        
        # Train
        trainer.train()
        
        # Save model
        model.save_pretrained('pdf_model')
        tokenizer.save_pretrained('pdf_model')
        
        # Upload to S3
        s3_bucket = os.getenv('S3_BUCKET', 'default-bucket')
        s3.upload('pdf_model', s3_bucket, os.getenv('MODEL_PATH'))
        log.info("PDF model trained and saved to S3.")
        
    except Exception as e:
        log.error(f"Error training PDF model: {e}")
        raise


def train_financial_data():
    """Train model with financial data using PyTorch + Hugging Face."""
    try:
        insights = initialize_financial_index()
        
        # Create multiple samples from insights for better training
        insights_list = []
        for category, amount in insights.items():
            insights_list.append(f"{category}: ${amount:.2f}")
        
        # If no insights, create a default sample
        if not insights_list:
            insights_list = ["No financial data available"]
        
        # Load model with S3 support
        model_loader = ModelLoader('microsoft/DialoGPT-medium', os.getenv('MODEL_PATH'))
        model, tokenizer = model_loader.load_model()
        
        # Prepare dataset
        def tokenize_function(examples):
            return tokenizer(
                examples['text'],
                truncation=True,
                padding=True,
                max_length=512
            )
        
        # Create dataset with multiple samples
        dataset_dict = {'text': insights_list}
        dataset = Dataset.from_dict(dataset_dict)
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        
        # Configure LoRA
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.1,
            bias="none",
            task_type=PEFTTaskType.CAUSAL_LM
        )
        
        model = get_peft_model(model, lora_config)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir="./financial_model",
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir="./logs",
            logging_steps=10,
            save_steps=1000,
            eval_steps=500,
            evaluation_strategy="steps",
            load_best_model_at_end=True,
            save_total_limit=2,
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )
        
        # Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator,
        )
        
        # Train
        trainer.train()
        
        # Save model
        model.save_pretrained('financial_model')
        tokenizer.save_pretrained('financial_model')
        
        # Upload to S3
        s3_bucket = os.getenv('S3_BUCKET', 'default-bucket')
        s3.upload('financial_model', s3_bucket, os.getenv('MODEL_PATH'))
        log.info("Financial model trained and saved to S3.")
        
    except Exception as e:
        log.error(f"Error training financial model: {e}")
        raise


def train_trip_model(new_only=False):
    """Train model with trip data using PyTorch + Hugging Face."""
    try:
        from config.bootstrap import database
        
        # Get training data from database
        try:
            if new_only:
                last_night = datetime.datetime.utcnow() - datetime.timedelta(days=1)
                cur = database.cursor()
                cur.execute('SELECT query, context, answer FROM questions WHERE timestamp >= %s', (last_night,))
            else:
                cur = database.cursor()
                cur.execute('SELECT query, context, answer FROM questions')
            
            questions = cur.fetchall()
            cur.close()
            
            if not questions:
                log.info("No new data to train on.")
                return
            
            # Prepare training data - access by index since fetchall returns tuples
            train_data = {
                'question': [q[0] for q in questions],  # query is first column
                'context': [q[1] for q in questions],   # context is second column
                'answers': [q[2] for q in questions]    # answer is third column
            }
        except Exception as e:
            log.error(f"Database query failed: {e}")
            return
        
        # Load model with S3 support
        model_loader = ModelLoader('microsoft/DialoGPT-medium', os.getenv('MODEL_PATH'))
        model, tokenizer = model_loader.load_model()
        
        # Prepare dataset
        def tokenize_function(examples):
            # Combine question and context
            texts = [f"Q: {q} Context: {c} A: {a}" for q, c, a in zip(
                examples['question'], examples['context'], examples['answers']
            )]
            return tokenizer(
                texts,
                truncation=True,
                padding=True,
                max_length=512
            )
        
        # Create dataset
        dataset = Dataset.from_dict(train_data)
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        
        # Configure LoRA
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.1,
            bias="none",
            task_type=PEFTTaskType.CAUSAL_LM
        )
        
        model = get_peft_model(model, lora_config)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir="./trip_model",
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir="./logs",
            logging_steps=10,
            save_steps=1000,
            eval_steps=500,
            evaluation_strategy="steps",
            load_best_model_at_end=True,
            save_total_limit=2,
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )
        
        # Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator,
        )
        
        # Train
        trainer.train()
        
        # Save model
        model.save_pretrained('trip_model')
        tokenizer.save_pretrained('trip_model')
        
        # Upload to S3
        s3_bucket = os.getenv('S3_BUCKET', 'default-bucket')
        s3.upload('trip_model', s3_bucket, os.getenv('MODEL_PATH'))
        log.info("Trip model trained and saved to S3.")
        
    except Exception as e:
        log.error(f"Error training trip model: {e}")
        raise