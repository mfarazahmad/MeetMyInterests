import os
import datetime
from typing import List, Dict, Any

from ai.utils import embedding_generator
from config.bootstrap import vectorIndex, plaid_client

# Load environment variables
# load_dotenv() # This line is removed as per the new_code, as the dotenv import is removed.

# Plaid client setup
# client = Client( # This line is removed as per the new_code, as the plaid.Client import is removed.
#     client_id=os.getenv('PLAID_CLIENT_ID'),
#     secret=os.getenv('PLAID_SECRET'),
#     environment=os.getenv('PLAID_ENVIRONMENT')
# )

# access_token = os.getenv('PLAID_ACCESS_TOKEN') # This line is removed as per the new_code, as the access_token is now directly used in get_transactions.

def get_transactions(start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """Get transactions using the new Plaid client."""
    try:
        if not plaid_client:
            print("Plaid client not initialized")
            return []
        
        # Get access token from environment
        access_token = os.getenv('PLAID_ACCESS_TOKEN')
        if not access_token:
            print("PLAID_ACCESS_TOKEN not found in environment")
            return []
        
        transactions = plaid_client.get_transactions(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
            count=500,
            offset=0
        )
        
        return transactions if transactions else []
        
    except Exception as e:
        print(f"Error retrieving transactions: {e}")
        return []

def analyze_transactions(transactions: List[Dict[str, Any]]) -> Dict[str, float]:
    """Analyze transactions and categorize spending."""
    categories = {}
    for transaction in transactions:
        category = transaction.get('category', ['Uncategorized'])[0] if transaction.get('category') else 'Uncategorized'
        amount = transaction.get('amount', 0)
        
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount
    
    return categories

def initialize_financial_index() -> Dict[str, float]:
    """Initialize financial index with transaction data."""
    start_date = (datetime.datetime.now() - datetime.timedelta(days=365 * 2)).strftime('%Y-%m-%d')
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')

    transactions = get_transactions(start_date, end_date)
    insights = analyze_transactions(transactions)

    save_financial_data_to_vector_db(insights)

    return insights

def save_financial_data_to_vector_db(insights: Dict[str, float]) -> None:
    """Save financial data to vector database using new embedding generator."""
    for category, amount in insights.items():
        context = f"Category: {category}, Amount: ${amount:.2f}"
        
        # Use new embedding generator
        embedding = embedding_generator.generate_embedding(context)
        vectorIndex.update(f"finance_{category}", embedding, context, 'finance')

