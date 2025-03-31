"""
Address forwarding management for BlockCypher API integration.

This module provides functionality for creating and managing forwarding addresses and webhooks.
"""

from typing import Dict, Any, List, Optional, Union
from requests.exceptions import RequestException

from app.infrastructure.providers.blockcypher.common.base import BlockCypherProvider
from app.infrastructure.providers.blockcypher.common.types import (
    Address, TransactionHash, WebhookEventType
)

class ForwardingManager(BlockCypherProvider):
    """
    Manager for handling address forwarding and webhooks through the BlockCypher API.
    
    This class provides methods for creating and managing forwarding addresses and webhooks.
    """
    
    def create_forwarding_address(
        self,
        destination: str,
        callback_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new forwarding address.
        
        Args:
            destination: Destination address to forward funds to
            callback_url: Optional URL to receive webhook notifications
            **kwargs: Additional parameters (e.g., mining_fees_satoshis, processing_fees_satoshis)
            
        Returns:
            Dictionary with forwarding address details
        """
        try:
            data = {
                "destination": destination
            }
            
            if callback_url:
                data["callback_url"] = callback_url
                
            # Add any additional parameters
            data.update(kwargs)
            
            return self.make_request('POST', 'payments', data=data)
        except RequestException as e:
            raise Exception(f"Failed to create forwarding address: {str(e)}")
    
    def list_forwarding_addresses(self) -> List[Dict[str, Any]]:
        """
        List all forwarding addresses.
        
        Returns:
            List of forwarding address details
        """
        try:
            result = self.make_request('GET', 'payments')
            return result
        except RequestException as e:
            raise Exception(f"Failed to list forwarding addresses: {str(e)}")
    
    def delete_forwarding_address(self, forward_id: str) -> Dict[str, Any]:
        """
        Delete a forwarding address.
        
        Args:
            forward_id: ID of the forwarding address to delete
            
        Returns:
            Response containing deletion status
        """
        try:
            return self.make_request('DELETE', f'payments/{forward_id}')
        except RequestException as e:
            raise Exception(f"Failed to delete forwarding address {forward_id}: {str(e)}")
    
    def create_webhook(
        self,
        url: str,
        event: str,
        address: Optional[str] = None,
        transaction: Optional[str] = None,
        confidence: Optional[float] = None,
        confirmations: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new webhook.
        
        Args:
            url: Callback URL to receive webhook notifications
            event: Event type (e.g., 'tx-confirmation', 'new-block', 'unconfirmed-tx')
            address: Optional address to monitor
            transaction: Optional transaction hash to monitor
            confidence: Optional confidence threshold for unconfirmed transactions
            confirmations: Optional number of confirmations to notify at
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with webhook details
        """
        valid_events = [
            'unconfirmed-tx', 'new-block', 'tx-confirmation', 
            'double-spend-tx', 'tx-confidence'
        ]
        
        if event not in valid_events:
            raise ValueError(f"Invalid event type. Must be one of {valid_events}")
        
        try:
            data = {
                "event": event,
                "url": url
            }
            
            if address:
                data["address"] = address
                
            if transaction:
                data["hash"] = transaction
                
            if confidence and event == 'tx-confidence':
                data["confidence"] = confidence
                
            if confirmations and event == 'tx-confirmation':
                data["confirmations"] = confirmations
                
            # Add any additional parameters
            data.update(kwargs)
            
            return self.make_request('POST', 'hooks', data=data)
        except RequestException as e:
            raise Exception(f"Failed to create webhook: {str(e)}")
    
    def list_webhooks(self) -> List[Dict[str, Any]]:
        """
        List all webhooks.
        
        Returns:
            List of webhook details
        """
        try:
            result = self.make_request('GET', 'hooks')
            return result
        except RequestException as e:
            raise Exception(f"Failed to list webhooks: {str(e)}")
    
    def get_webhook(self, hook_id: str) -> Dict[str, Any]:
        """
        Get details of a specific webhook.
        
        Args:
            hook_id: ID of the webhook to retrieve
            
        Returns:
            Webhook details
        """
        try:
            return self.make_request('GET', f'hooks/{hook_id}')
        except RequestException as e:
            raise Exception(f"Failed to get webhook {hook_id}: {str(e)}")
    
    def delete_webhook(self, hook_id: str) -> Dict[str, Any]:
        """
        Delete a webhook.
        
        Args:
            hook_id: ID of the webhook to delete
            
        Returns:
            Response containing deletion status
        """
        try:
            return self.make_request('DELETE', f'hooks/{hook_id}')
        except RequestException as e:
            raise Exception(f"Failed to delete webhook {hook_id}: {str(e)}")
    
    def create_address_webhook(
        self,
        url: str,
        address: str,
        event: str = 'unconfirmed-tx',
        **kwargs
    ) -> Dict[str, Any]:
        """
        Convenience method to create a webhook for a specific address.
        
        Args:
            url: Callback URL to receive webhook notifications
            address: Address to monitor
            event: Event type (default: 'unconfirmed-tx')
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with webhook details
        """
        return self.create_webhook(url=url, event=event, address=address, **kwargs)
    
    def create_transaction_webhook(
        self,
        url: str,
        transaction: str,
        confirmations: int = 6,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Convenience method to create a webhook for a specific transaction confirmation.
        
        Args:
            url: Callback URL to receive webhook notifications
            transaction: Transaction hash to monitor
            confirmations: Number of confirmations to notify at (default: 6)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with webhook details
        """
        return self.create_webhook(
            url=url,
            event='tx-confirmation',
            transaction=transaction,
            confirmations=confirmations,
            **kwargs
        )
    
    def create_confidence_webhook(
        self,
        url: str,
        transaction: str,
        confidence: float = 0.9,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Convenience method to create a confidence webhook for a specific transaction.
        
        Args:
            url: Callback URL to receive webhook notifications
            transaction: Transaction hash to monitor
            confidence: Confidence threshold (default: 0.9)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with webhook details
        """
        return self.create_webhook(
            url=url,
            event='tx-confidence',
            transaction=transaction,
            confidence=confidence,
            **kwargs
        )
    
    def get_websocket_url(self) -> str:
        """
        Get WebSocket URL for real-time updates.
        
        Returns:
            WebSocket URL string
        """
        base_url = self.base_url.replace('https://', 'wss://').replace('http://', 'ws://')
        return f"{base_url}/{self.coin_symbol}/ws" 