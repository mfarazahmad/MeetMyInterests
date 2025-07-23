import os
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from config.logger import log


class PlaidClient:
    """Plaid API client for financial data integration."""
    
    def __init__(self, client_id: str = None, secret: str = None, environment: str = "sandbox"):
        self.client_id = client_id or os.getenv('PLAID_CLIENT_ID')
        self.secret = secret or os.getenv('PLAID_SECRET')
        self.environment = environment or os.getenv('PLAID_ENVIRONMENT', 'sandbox')
        
        if self.environment == "sandbox":
            self.base_url = "https://sandbox.plaid.com"
        elif self.environment == "development":
            self.base_url = "https://development.plaid.com"
        elif self.environment == "production":
            self.base_url = "https://production.plaid.com"
        else:
            self.base_url = "https://sandbox.plaid.com"
        
        if not self.client_id or not self.secret:
            log.warning("Plaid credentials not found. Set PLAID_CLIENT_ID and PLAID_SECRET environment variables.")
        
        log.info(f"Plaid client initialized for {self.environment} environment")
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make a request to the Plaid API."""
        try:
            url = f"{self.base_url}/{endpoint}"
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            log.error(f"Plaid API request failed: {e}")
            return None
        except Exception as e:
            log.error(f"Plaid request error: {e}")
            return None
    
    def create_link_token(self, user_id: str, client_name: str = "Analytics Engine") -> Optional[str]:
        """Create a link token for Plaid Link."""
        try:
            data = {
                'client_id': self.client_id,
                'secret': self.secret,
                'client_name': client_name,
                'country_codes': ['US'],
                'language': 'en',
                'user': {'client_user_id': user_id},
                'products': ['auth', 'transactions']
            }
            
            response = self._make_request('link/token/create', data)
            
            if response and 'link_token' in response:
                log.info(f"Created link token for user {user_id}")
                return response['link_token']
            else:
                log.error(f"Failed to create link token: {response}")
                return None
                
        except Exception as e:
            log.error(f"Link token creation error: {e}")
            return None
    
    def exchange_public_token(self, public_token: str) -> Optional[str]:
        """Exchange public token for access token."""
        try:
            data = {
                'client_id': self.client_id,
                'secret': self.secret,
                'public_token': public_token
            }
            
            response = self._make_request('item/public_token/exchange', data)
            
            if response and 'access_token' in response:
                log.info("Successfully exchanged public token for access token")
                return response['access_token']
            else:
                log.error(f"Failed to exchange public token: {response}")
                return None
                
        except Exception as e:
            log.error(f"Token exchange error: {e}")
            return None
    
    def get_accounts(self, access_token: str) -> Optional[List[Dict[str, Any]]]:
        """Get accounts for an access token."""
        try:
            data = {
                'client_id': self.client_id,
                'secret': self.secret,
                'access_token': access_token
            }
            
            response = self._make_request('accounts/get', data)
            
            if response and 'accounts' in response:
                accounts = response['accounts']
                log.info(f"Retrieved {len(accounts)} accounts")
                return accounts
            else:
                log.error(f"Failed to get accounts: {response}")
                return None
                
        except Exception as e:
            log.error(f"Get accounts error: {e}")
            return None
    
    def get_transactions(self, access_token: str, start_date: str = None, end_date: str = None, 
                        count: int = 100, offset: int = 0) -> Optional[List[Dict[str, Any]]]:
        """Get transactions for an access token."""
        try:
            # Default to last 30 days if no dates provided
            if not start_date:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            data = {
                'client_id': self.client_id,
                'secret': self.secret,
                'access_token': access_token,
                'start_date': start_date,
                'end_date': end_date,
                'options': {
                    'count': count,
                    'offset': offset
                }
            }
            
            response = self._make_request('transactions/get', data)
            
            if response and 'transactions' in response:
                transactions = response['transactions']
                log.info(f"Retrieved {len(transactions)} transactions from {start_date} to {end_date}")
                return transactions
            else:
                log.error(f"Failed to get transactions: {response}")
                return None
                
        except Exception as e:
            log.error(f"Get transactions error: {e}")
            return None
    
    def get_balance(self, access_token: str) -> Optional[List[Dict[str, Any]]]:
        """Get account balances."""
        try:
            data = {
                'client_id': self.client_id,
                'secret': self.secret,
                'access_token': access_token
            }
            
            response = self._make_request('accounts/balance/get', data)
            
            if response and 'accounts' in response:
                accounts = response['accounts']
                log.info(f"Retrieved balances for {len(accounts)} accounts")
                return accounts
            else:
                log.error(f"Failed to get balances: {response}")
                return None
                
        except Exception as e:
            log.error(f"Get balance error: {e}")
            return None
    
    def get_income(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Get income information."""
        try:
            data = {
                'client_id': self.client_id,
                'secret': self.secret,
                'access_token': access_token
            }
            
            response = self._make_request('income/get', data)
            
            if response and 'income' in response:
                log.info("Retrieved income information")
                return response['income']
            else:
                log.error(f"Failed to get income: {response}")
                return None
                
        except Exception as e:
            log.error(f"Get income error: {e}")
            return None
    
    def get_identity(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Get identity information."""
        try:
            data = {
                'client_id': self.client_id,
                'secret': self.secret,
                'access_token': access_token
            }
            
            response = self._make_request('identity/get', data)
            
            if response and 'accounts' in response:
                log.info("Retrieved identity information")
                return response
            else:
                log.error(f"Failed to get identity: {response}")
                return None
                
        except Exception as e:
            log.error(f"Get identity error: {e}")
            return None
    
    def get_investments(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Get investment holdings and transactions."""
        try:
            data = {
                'client_id': self.client_id,
                'secret': self.secret,
                'access_token': access_token
            }
            
            response = self._make_request('investments/holdings/get', data)
            
            if response and 'holdings' in response:
                log.info("Retrieved investment holdings")
                return response
            else:
                log.error(f"Failed to get investments: {response}")
                return None
                
        except Exception as e:
            log.error(f"Get investments error: {e}")
            return None
    
    def get_liabilities(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Get liability information."""
        try:
            data = {
                'client_id': self.client_id,
                'secret': self.secret,
                'access_token': access_token
            }
            
            response = self._make_request('liabilities/get', data)
            
            if response and 'accounts' in response:
                log.info("Retrieved liability information")
                return response
            else:
                log.error(f"Failed to get liabilities: {response}")
                return None
                
        except Exception as e:
            log.error(f"Get liabilities error: {e}")
            return None
    
    def refresh_transactions(self, access_token: str) -> bool:
        """Refresh transactions for an access token."""
        try:
            data = {
                'client_id': self.client_id,
                'secret': self.secret,
                'access_token': access_token
            }
            
            response = self._make_request('transactions/refresh', data)
            
            if response and response.get('request_id'):
                log.info("Successfully initiated transaction refresh")
                return True
            else:
                log.error(f"Failed to refresh transactions: {response}")
                return False
                
        except Exception as e:
            log.error(f"Refresh transactions error: {e}")
            return False 