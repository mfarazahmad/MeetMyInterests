import datetime
import os
import tensorflow as tf
from transformers import TFAutoModelForCausalLM, create_optimizer

from ai.pipelines.financial import initialize_financial_index
from ai.pipelines.pdf import initialize_pdf_index
from utils import tokenizer, load_model_from_s3_or_hf

from config.bootstrap import s3
from config.logger import log

def train_pdf_data():
    chunks = initialize_pdf_index()
    llama_model = load_model_from_s3_or_hf('llama3_model', model_path)
    
    inputs = tokenizer(chunks, return_tensors='tf', padding=True, truncation=True)
    dataset = tf.data.Dataset.from_tensor_slices((inputs['input_ids'], inputs['attention_mask']))
    
    num_train_steps = int(len(dataset) * 3)
    optimizer, _ = create_optimizer(init_lr=3e-5, num_train_steps=num_train_steps, num_warmup_steps=0)

    llama_model.compile(optimizer=optimizer)
    llama_model.fit(dataset.batch(2), epochs=3)

    llama_model.save_pretrained('llama3_model')
    s3.upload(f'{model_path}', s3_bucket, f'{model_path}')
    log.info("Model retrained with PDF data.")

def train_financial_data():
    insights = initialize_financial_index()
    insights_text = '. '.join([f"{category}: ${amount:.2f}" for category, amount in insights.items()])

    inputs = tokenizer(insights_text, return_tensors='tf', padding=True, truncation=True)
    dataset = tf.data.Dataset.from_tensor_slices((inputs['input_ids'], inputs['attention_mask']))

    num_train_steps = int(len(dataset) * 3)
    optimizer, _ = create_optimizer(init_lr=3e-5, num_train_steps=num_train_steps, num_warmup_steps=0)

    llama_model = load_model_from_s3_or_hf('llama3_model', os.getenv('MODEL_PATH'))

    llama_model.compile(optimizer=optimizer)
    llama_model.fit(dataset.batch(2), epochs=3)

    llama_model.save_pretrained(model_path)
    s3.upload(f'{model_path}', s3_bucket, f'{model_path}')
    log.info("Financial model trained and saved.")

def train_trip_model(new_only=False):
    if new_only:
        last_night = datetime.utcnow() - datetime.timedelta(days=1)
        cur.execute('SELECT * FROM questions WHERE timestamp >= %s', (last_night,))
    else:
        cur.execute('SELECT * FROM questions')
    
    questions = cur.fetchall()

    if not questions:
        log.info("No new data to train on.")
        return

    train_data = {
        'question': [q['query'] for q in questions],
        'context': [q['context'] for q in questions],
        'answers': [{'text': q['answer']} for q in questions]
    }

    inputs = tokenizer(train_data['question'], return_tensors='tf', padding=True, truncation=True)
    dataset = tf.data.Dataset.from_tensor_slices((inputs['input_ids'], inputs['attention_mask']))

    num_train_steps = int(len(dataset) * 3)
    optimizer, _ = create_optimizer(init_lr=3e-5, num_train_steps=num_train_steps, num_warmup_steps=0)
    
    llama_model = load_model_from_s3_or_hf('llama3_model', os.getenv('MODEL_PATH'))

    llama_model.compile(optimizer=optimizer)
    llama_model.fit(dataset.batch(2), epochs=3)

    llama_model.save_pretrained(model_path)
    s3.upload(f'{model_path}', s3_bucket, f'{model_path}')
    log.info("Model retrained and saved.")