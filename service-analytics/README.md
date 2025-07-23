
# ANALYTICS ENGINE

A modern AI-powered analytics engine with advanced RAG (Retrieval-Augmented Generation) capabilities, built with PyTorch and Hugging Face, using NATS JetStream for real-time messaging.

### Health Advise
- Nutrition
- Fitness
- Recipes

### Productivity
- File Locations With Links
- Summarize Documents, Contracts
- Create Contracts, Idea Documents, Etc.

### Financials
- Build Charts & Graph
- Financial Overview
    - Business Finances
    - Personal Finances
- Category Breakdown Per Year
- Financial Advise from Books

## MACHINE LEARNING BUSINESS CASES
- Housing Market
- Bitcoin Analysis

[FEATURES]
- Voice to Text
- Real Time Reporting
- Real Time Chatbot
- Daily Training
- Real-time Message Processing with NATS JetStream

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Start NATS server (if not already running)
# Download from https://nats.io/download/
nats-server -js
```

## 🏗️ Architecture Overview

### Modern AI Stack
- **PyTorch**: Primary deep learning framework
- **Hugging Face Transformers**: State-of-the-art model loading and training
- **Sentence Transformers**: High-quality embeddings for semantic search
- **PEFT (Parameter-Efficient Fine-Tuning)**: Efficient model adaptation with LoRA
- **Hybrid RAG**: Combines dense vector search with sparse BM25 search
- **NATS JetStream**: Real-time messaging with streaming capabilities

### Key Components

#### 1. Model Management (`ai/utils.py`)
- **ModelLoader**: Handles model loading from S3 or Hugging Face with automatic device placement
- **EmbeddingGenerator**: Generates embeddings using sentence transformers
- **ResponseGenerator**: Generates responses with proper error handling and logging

#### 2. Prompt Engineering (`ai/prompt_engineer.py`)
- **Structured Prompts**: Task-specific prompt templates for different use cases
- **Context-Aware Prompting**: Intelligent context integration
- **Specialized Templates**: Financial, trip planning, PDF analysis, health advice, productivity

#### 3. RAG Pipeline (`ai/rag_pipeline.py`)
- **Hybrid Search**: Combines dense vector search with sparse BM25 search
- **Reranking**: Uses cross-encoders to improve result relevance
- **Context Management**: Intelligent context extraction and combination

#### 4. Training (`ai/training.py`)
- **LoRA Fine-Tuning**: Parameter-efficient training
- **S3 Integration**: Model persistence and sharing
- **Evaluation**: Proper training evaluation and metrics

#### 5. Message Broker (`broker/kakfa.py`)
- **NATS JetStream**: Real-time messaging with streaming capabilities
- **Async Processing**: Non-blocking message handling
- **Load Balancing**: Consumer groups for distributed processing
- **Message Persistence**: Reliable message delivery with acknowledgments

## 🎯 Business Use Cases

### Financial Analytics
- **Build Charts & Graphs**: Automated financial visualization
- **Financial Overview**: Business and personal finance analysis
- **Category Breakdown**: Yearly financial categorization
- **Financial Advice**: AI-powered financial recommendations

### Health & Wellness
- **Nutrition Guidance**: Personalized dietary recommendations
- **Fitness Planning**: Exercise and workout optimization
- **Recipe Suggestions**: AI-generated meal planning

### Trip Planning
- **Location Analysis**: Destination insights and recommendations
- **Weather Integration**: Real-time weather data for travel planning
- **Safety Information**: Travel safety and local customs
- **Activity Planning**: Personalized itinerary creation
- **Accommodation & Flights**: Booking recommendations and logistics

### Productivity Enhancement
- **Document Analysis**: PDF summarization and insights
- **Contract Generation**: AI-powered document creation
- **File Organization**: Intelligent file management
- **Workflow Optimization**: Process improvement recommendations

## 🔧 Technical Features

### NATS JetStream Messaging
```python
# Publishing messages
await broker.publish("financial.analyze", {
    'type': 'financial',
    'action': 'analyze_transactions',
    'data': {'user_id': '123', 'date_range': '2024-01-01:2024-12-31'}
})

# Subscribing to messages
async def message_handler(data):
    message_type = data.get('type')
    if message_type == 'financial':
        # Process financial data
        pass

await broker.subscribe(message_handler)
```

### Modern RAG Implementation
```python
# Hybrid search combining dense and sparse retrieval
search_results = rag_pipeline.hybrid_search(query, k=10)

# Structured prompting for different tasks
prompt = prompt_engineer.create_financial_prompt(query, financial_data)
response = response_generator.generate_response(prompt)
```

### Parameter-Efficient Training
```python
# LoRA configuration for efficient fine-tuning
lora_config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=PEFTTaskType.CAUSAL_LM
)
```

### S3 Model Management
```python
# Automatic model loading from S3 or Hugging Face
model_loader = ModelLoader('microsoft/DialoGPT-medium', s3_path)
model, tokenizer = model_loader.load_model()
```

## 📊 Performance Improvements

### Why NATS over Kafka?
1. **Simpler Setup**: Single binary, no Zookeeper required
2. **Better Performance**: Lower latency and higher throughput
3. **Easier Management**: Built-in monitoring and management
4. **Streaming Built-in**: JetStream provides streaming capabilities out of the box
5. **Cloud Native**: Better integration with modern cloud platforms

### Why PyTorch + Hugging Face?
1. **Industry Standard**: 80%+ of AI research uses PyTorch
2. **Better Performance**: Optimized for modern hardware
3. **Easier Deployment**: Better cloud integration
4. **Active Community**: More frequent updates and support
5. **Memory Efficiency**: Automatic device placement and optimization

### RAG Enhancements
1. **Hybrid Search**: Combines semantic (dense) and keyword (sparse) search
2. **Reranking**: Cross-encoder models improve result relevance
3. **Structured Prompts**: Task-specific prompting for better responses
4. **Context Management**: Intelligent context extraction and combination

### Training Improvements
1. **LoRA**: Parameter-efficient fine-tuning (90% fewer parameters)
2. **Proper Evaluation**: Training metrics and validation
3. **S3 Integration**: Model persistence and sharing
4. **Error Handling**: Robust error recovery and logging

## 🛠️ Installation & Setup

### Dependencies
```bash
# Core AI dependencies
torch==2.3.1
transformers==4.41.2
sentence-transformers==2.2.2
accelerate==0.20.3
peft==0.4.0

# NATS messaging
nats-py==2.6.0
asyncio-nats-client==2.6.0

# RAG and search
rank-bm25==0.2.2
scikit-learn==1.3.0

# Data processing
datasets==2.14.0
evaluate==0.4.0
```

### Environment Variables
```bash
# NATS Configuration
BROKER_HOST=nats://localhost:4222
BROKER_TOPIC=analytics
BROKER_GROUP=analytics-consumer
BROKER_TIMEOUT=30

# S3 Configuration
S3_BUCKET=your-bucket-name
MODEL_PATH=your-model-path

# API Keys
PLAID_CLIENT_ID=your-plaid-client-id
PLAID_SECRET=your-plaid-secret
YELP_API_KEY=your-yelp-api-key
WEATHER_API_KEY=your-weather-api-key
SKYSCANNER_API_KEY=your-skyscanner-api-key
```

## 📈 Usage Examples

### NATS Message Processing
```python
import asyncio
from config.bootstrap import initialize_broker, broker

async def main():
    # Initialize NATS broker
    await initialize_broker()
    
    # Subscribe to messages
    await broker.subscribe(message_handler)
    
    # Publish a message
    await broker.publish("financial.analyze", {
        'type': 'financial',
        'action': 'analyze_transactions',
        'data': {'user_id': '123'}
    })

async def message_handler(data):
    print(f"Received: {data}")

asyncio.run(main())
```

### Financial Analysis
```python
from ai.pipelines import financial_rag_pipeline
from ai.utils import encode_query

query = "What are my spending patterns this month?"
embedding = encode_query(query)
response = financial_rag_pipeline(query, embedding)
```

### Trip Planning
```python
from ai.pipelines import trip_rag_pipeline

query = "Plan a 5-day trip to Tokyo in March"
embedding = encode_query(query)
response = trip_rag_pipeline(query, embedding)
```

### Document Analysis
```python
from ai.pipelines import pdf_rag_pipeline

query = "Summarize the key points from this contract"
embedding = encode_query(query)
response = pdf_rag_pipeline(query, embedding)
```

## 🧪 Training Your Own Models

### PDF Training
```python
from ai.training import train_pdf_data
train_pdf_data()
```

### Financial Training
```python
from ai.training import train_financial_data
train_financial_data()
```

### Trip Planning Training
```python
from ai.training import train_trip_model
train_trip_model(new_only=True)  # Train only on new data
```

## 🔍 Advanced Features

### Custom Prompt Engineering
```python
from ai.prompt_engineer import prompt_engineer, TaskType

# Create custom financial prompt
prompt = prompt_engineer.create_financial_prompt(
    query="Analyze my investment portfolio",
    financial_data=["AAPL: $10,000", "GOOGL: $15,000"]
)
```

### Hybrid Search Configuration
```python
from ai.rag_pipeline import rag_pipeline

# Initialize BM25 index for sparse search
documents = ["document1", "document2", "document3"]
rag_pipeline.initialize_bm25_index(documents)

# Perform hybrid search
results = rag_pipeline.hybrid_search("your query", k=10)
```

## 🚀 Deployment

### Docker Support
```dockerfile
FROM python:3.9-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Cloud Deployment
- **AWS**: Lambda functions with S3 model storage
- **Google Cloud**: Cloud Run with Vertex AI
- **Azure**: Container Instances with Azure ML

## 📚 Concepts Explained

### RAG (Retrieval-Augmented Generation)
RAG combines information retrieval with text generation:
1. **Retrieval**: Find relevant documents/context
2. **Augmentation**: Add context to the query
3. **Generation**: Generate response using the augmented query

### Hybrid Search
Combines two search approaches:
- **Dense Search**: Semantic similarity using embeddings
- **Sparse Search**: Keyword matching using BM25
- **Reranking**: Cross-encoder models improve final results

### LoRA (Low-Rank Adaptation)
Parameter-efficient fine-tuning technique:
- Trains only a small number of parameters
- Reduces memory usage by 90%
- Maintains model performance
- Enables quick adaptation to new tasks

### Prompt Engineering
Structured approach to creating effective prompts:
- **System Prompts**: Define AI role and behavior
- **Context Integration**: Intelligent context formatting
- **Task-Specific Templates**: Specialized prompts for different use cases
- **Output Formatting**: Structured response requirements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the code examples

**Built with ❤️ using PyTorch, Hugging Face, and modern AI best practices.**

