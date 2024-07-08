import os
from plaid import Client
from dotenv import load_dotenv
import datetime

from ai.utils import tokenizer, context_encoder
from config.bootstrap import vectorIndex

# Load environment variables
load_dotenv()

# Plaid client setup
client = Client(
    client_id=os.getenv('PLAID_CLIENT_ID'),
    secret=os.getenv('PLAID_SECRET'),
    environment=os.getenv('PLAID_ENVIRONMENT')
)

access_token = os.getenv('PLAID_ACCESS_TOKEN')

def get_transactions(start_date, end_date):
    try:
        response = client.Transactions.get(
            access_token,
            start_date=start_date,
            end_date=end_date,
            options={'count': 500, 'offset': 0}
        )
        return response['transactions']
    except Exception as e:
        print(f"Error retrieving transactions: {e}")
        return []

def analyze_transactions(transactions):
    categories = {}
    for transaction in transactions:
        category = transaction['category'][0] if transaction['category'] else 'Uncategorized'
        amount = transaction['amount']
        
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount
    
    return categories

def initialize_financial_index():
    start_date = (datetime.datetime.now() - datetime.timedelta(days=365 * 2)).strftime('%Y-%m-%d')
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')

    transactions = get_transactions(start_date, end_date)
    insights = analyze_transactions(transactions)

    save_financial_data_to_vector_db(insights)

    return insights

def save_financial_data_to_vector_db(insights):
    for category, amount in insights.items():
        context = f"Category: {category}, Amount: ${amount:.2f}"
        inputs = tokenizer(context, return_tensors='tf', truncation=True)
        embedding = context_encoder(**inputs).pooler_output.numpy().squeeze()
        vectorIndex.update(f"finance_{category}", embedding, context, 'finance')

