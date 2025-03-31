"""
Address forwarding and webhook management for BlockCypher API integration.

This module provides functionality for:
- Creating forwarding addresses that automatically send funds to destination addresses
- Setting up and managing webhooks for blockchain events
- Monitoring transaction confirmations and confidence levels
- Managing WebSocket connections for real-time updates
"""

from app.infrastructure.providers.blockcypher.forwarding.manager import ForwardingManager 