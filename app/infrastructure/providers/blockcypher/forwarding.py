from requests.exceptions import RequestException
from typing import Dict, Any, List, Optional, Union, Tuple
import requests
import os

class ForwardingManager:
    """
    Class to handle BlockCypher's Address Forwarding and Events/Hooks functionality.
    
    This allows for automatic forwarding of payments from one address to another, 
    as well as setting up webhooks and websocket events for blockchain notifications.
    """
    
    # Mapping of coin_symbol to (coin, chain) tuple used in BlockCypher API URL
    COIN_SYMBOL_MAPPING = {
        'btc': ('btc', 'main'),
        'btc-testnet': ('btc', 'test3'),
        'ltc': ('ltc', 'main'),
        'doge': ('doge', 'main'),
        'dash': ('dash', 'main'),
        'bcy': ('bcy', 'test')
    }
    
    # Valid event types for webhooks and websockets
    VALID_EVENT_TYPES = [
        'unconfirmed-tx',
        'new-block',
        'confirmed-tx',
        'tx-confirmation',
        'double-spend-tx',
        'tx-confidence'
    ]
    
    def __init__(self, coin_symbol: str = 'btc-testnet'):
        self.api_token = os.getenv("BLOCKCYPHER_API_TOKEN")
        if not self.api_token:
            raise ValueError("BLOCKCYPHER_API_TOKEN is not set")
        
        if coin_symbol not in self.COIN_SYMBOL_MAPPING:
            raise ValueError(f"Invalid coin symbol: {coin_symbol}")
        
        self.coin_symbol = coin_symbol
        coin, chain = self.COIN_SYMBOL_MAPPING[coin_symbol]
        self.base_url = f"https://api.blockcypher.com/v1/{coin}/{chain}"
        
    # ======== Address Forwarding ========
    
    def create_forwarding_address(
        self, 
        destination_address: str,
        callback_url: Optional[str] = None,
        process_fee_satoshis: Optional[int] = None,
        process_fee_address: Optional[str] = None,
        process_fee_percent: Optional[float] = None,
        transaction_value_satoshis: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create an address that automatically forwards payments to a destination address.
        
        Args:
            destination_address: The address where funds will be forwarded to
            callback_url: Optional URL to receive notifications when a payment is forwarded
            process_fee_satoshis: Optional fixed processing fee (in satoshis)
            process_fee_address: Optional address to send the processing fee to
            process_fee_percent: Optional processing fee as a percentage (0-100)
            transaction_value_satoshis: Optional minimum transaction value to process (in satoshis)
            
        Returns:
            Dictionary with forwarding address details
        """
        try:
            # Build the forwarding request data
            data = {
                "destination": destination_address,
                "token": self.api_token
            }
            
            # Add optional parameters if provided
            if callback_url:
                data["callback_url"] = callback_url
                
            if process_fee_satoshis:
                data["process_fee_satoshis"] = process_fee_satoshis
                
            if process_fee_address:
                data["process_fee_address"] = process_fee_address
                
            if process_fee_percent:
                if not 0 <= process_fee_percent <= 100:
                    raise ValueError("process_fee_percent must be between 0 and 100")
                data["process_fee_percent"] = process_fee_percent
                
            if transaction_value_satoshis:
                data["transaction_value_satoshis"] = transaction_value_satoshis
                
            # Make the API request
            url = f"{self.base_url}/forwards"
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to create forwarding address: {str(e)}")
    
    def list_forwarding_addresses(self, start: int = 0) -> List[Dict[str, Any]]:
        """
        List active address forwarding addresses associated with the API token.
        
        Args:
            start: Starting index for paging (default 0)
            
        Returns:
            List of forwarding address details
        """
        try:
            url = f"{self.base_url}/forwards"
            params = {
                'token': self.api_token,
                'start': start
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to list forwarding addresses: {str(e)}")
    
    def delete_forwarding_address(self, forwarding_id: str) -> bool:
        """
        Delete an address forwarding setup by its ID.
        
        Args:
            forwarding_id: The ID of the forwarding address to delete
            
        Returns:
            True if deletion was successful
        """
        try:
            url = f"{self.base_url}/forwards/{forwarding_id}"
            params = {'token': self.api_token}
            response = requests.delete(url, params=params)
            response.raise_for_status()
            
            # The API returns 204 No Content for successful deletion
            return True
        except RequestException as e:
            raise Exception(f"Failed to delete forwarding address: {str(e)}")
    
    # ======== Events and Hooks ========
    
    def create_webhook(
        self,
        event_type: str,
        url: str, 
        address: Optional[str] = None,
        hash_or_height: Optional[str] = None,
        confirmations: Optional[int] = None,
        confidence: Optional[float] = None,
        script: Optional[str] = None,
        wallet_name: Optional[str] = None,
        signkey: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a webhook to receive notifications for blockchain events.
        
        Args:
            event_type: Type of event to listen for (see VALID_EVENT_TYPES)
            url: URL to receive webhook notifications
            address: Optional address to monitor
            hash_or_height: Optional transaction hash or block height to monitor
            confirmations: Optional number of confirmations to monitor (max 10, default 6)
            confidence: Optional confidence threshold (0.0-1.0)
            script: Optional script to monitor
            wallet_name: Optional wallet name to monitor
            signkey: Optional signing key for webhook signatures
            
        Returns:
            Dictionary with webhook details including ID
        """
        if event_type not in self.VALID_EVENT_TYPES:
            raise ValueError(f"Invalid event type. Must be one of: {', '.join(self.VALID_EVENT_TYPES)}")
            
        try:
            # Build the webhook request data
            data = {
                "event": event_type,
                "url": url,
                "token": self.api_token
            }
            
            # Add optional parameters if provided
            if address:
                data["address"] = address
                
            if hash_or_height:
                data["hash"] = hash_or_height
                
            if confirmations is not None:
                if not 0 <= confirmations <= 10:
                    raise ValueError("confirmations must be between 0 and 10")
                data["confirmations"] = confirmations
                
            if confidence is not None:
                if not 0 <= confidence <= 1:
                    raise ValueError("confidence must be between 0.0 and 1.0")
                data["confidence"] = confidence
                
            if script:
                data["script"] = script
                
            if wallet_name:
                data["wallet_name"] = wallet_name
                
            if signkey:
                data["signkey"] = signkey
                
            # Make the API request
            url = f"{self.base_url}/hooks"
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to create webhook: {str(e)}")
    
    def list_webhooks(self) -> List[Dict[str, Any]]:
        """
        List all webhooks associated with the API token.
        
        Returns:
            List of webhook details
        """
        try:
            url = f"{self.base_url}/hooks"
            params = {'token': self.api_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to list webhooks: {str(e)}")
    
    def get_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """
        Get details of a specific webhook by its ID.
        
        Args:
            webhook_id: ID of the webhook to retrieve
            
        Returns:
            Dictionary with webhook details
        """
        try:
            url = f"{self.base_url}/hooks/{webhook_id}"
            params = {'token': self.api_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to get webhook details: {str(e)}")
    
    def delete_webhook(self, webhook_id: str) -> bool:
        """
        Delete a webhook by its ID.
        
        Args:
            webhook_id: ID of the webhook to delete
            
        Returns:
            True if deletion was successful
        """
        try:
            url = f"{self.base_url}/hooks/{webhook_id}"
            params = {'token': self.api_token}
            response = requests.delete(url, params=params)
            response.raise_for_status()
            
            # The API returns 204 No Content for successful deletion
            return True
        except RequestException as e:
            raise Exception(f"Failed to delete webhook: {str(e)}")
    
    # ======== Utility Methods ========
    
    def get_websocket_url(self) -> str:
        """
        Get the WebSocket URL for the selected blockchain.
        
        Returns:
            WebSocket URL for real-time blockchain event monitoring
        """
        coin, chain = self.COIN_SYMBOL_MAPPING[self.coin_symbol]
        return f"wss://socket.blockcypher.com/v1/{coin}/{chain}?token={self.api_token}"
    
    def create_address_webhook(
        self, 
        address: str, 
        url: str, 
        event_type: str = 'unconfirmed-tx',
        confirmations: int = 6
    ) -> Dict[str, Any]:
        """
        Convenience method to create a webhook for a specific address.
        
        Args:
            address: The address to monitor
            url: URL to receive webhook notifications
            event_type: Type of event to listen for
            confirmations: Number of confirmations to monitor (for tx-confirmation events)
            
        Returns:
            Dictionary with webhook details
        """
        return self.create_webhook(
            event_type=event_type,
            url=url,
            address=address,
            confirmations=confirmations
        )
    
    def create_transaction_webhook(
        self, 
        transaction_hash: str, 
        url: str, 
        event_type: str = 'tx-confirmation',
        confirmations: int = 6
    ) -> Dict[str, Any]:
        """
        Convenience method to create a webhook for a specific transaction.
        
        Args:
            transaction_hash: The transaction hash to monitor
            url: URL to receive webhook notifications
            event_type: Type of event to listen for
            confirmations: Number of confirmations to monitor
            
        Returns:
            Dictionary with webhook details
        """
        return self.create_webhook(
            event_type=event_type,
            url=url,
            hash_or_height=transaction_hash,
            confirmations=confirmations
        )
    
    def create_confidence_webhook(
        self,
        address: str,
        url: str,
        confidence_threshold: float = 0.99
    ) -> Dict[str, Any]:
        """
        Convenience method to create a webhook for transaction confidence monitoring.
        
        Args:
            address: The address to monitor
            url: URL to receive webhook notifications
            confidence_threshold: Confidence threshold (0.0-1.0)
            
        Returns:
            Dictionary with webhook details
        """
        return self.create_webhook(
            event_type='tx-confidence',
            url=url,
            address=address,
            confidence=confidence_threshold
        )


if __name__ == "__main__":
    # How to use the ForwardingManager
    manager = ForwardingManager(coin_symbol="btc-testnet")
    
    # Example usage
    try:
        print("\n===== ADDRESS FORWARDING =====")
        # Create a forwarding address
        # Replace with your actual destination address
        destination = "REPLACE_WITH_DESTINATION_ADDRESS"
        forwarding = manager.create_forwarding_address(
            destination_address=destination,
            callback_url="https://example.com/payment/callback"
        )
        print(f"Forwarding address created: {forwarding}")
        
        # List active forwarding addresses
        forwards = manager.list_forwarding_addresses()
        print(f"Active forwarding addresses count: {len(forwards)}")
        
        # Create a forwarding address with a processing fee
        forwarding_with_fee = manager.create_forwarding_address(
            destination_address=destination,
            process_fee_percent=1.0,  # 1% fee
            process_fee_address=destination  # Fee goes to same destination
        )
        print(f"Forwarding address with fee created: {forwarding_with_fee}")
        
        print("\n===== WEBHOOKS =====")
        # Create an address webhook
        monitor_address = "REPLACE_WITH_ADDRESS_TO_MONITOR"
        webhook = manager.create_address_webhook(
            address=monitor_address,
            url="https://example.com/webhook/callback",
            event_type="unconfirmed-tx"
        )
        print(f"Webhook created: {webhook}")
        
        # List active webhooks
        webhooks = manager.list_webhooks()
        print(f"Active webhooks count: {len(webhooks)}")
        
        # Get WebSocket URL
        ws_url = manager.get_websocket_url()
        print(f"WebSocket URL: {ws_url}")
        print("To use WebSockets, connect to this URL and send a JSON Event object")
        
    except Exception as e:
        print(f"\nError: {e}") 