"""
Type definitions for BlockCypher API integration.

This module contains type definitions and constants used by the BlockCypher provider.
"""

from enum import Enum
from typing import Dict, List, Any, Literal, Optional, Union

# Currency symbols and constants
CoinSymbol = Literal['btc', 'btc-testnet', 'ltc', 'doge', 'dash', 'bcy']

# Transaction related types
TxConfirmationLevel = Literal[0, 1, 2, 3, 6]

class TransactionStatus(str, Enum):
    """Transaction status options"""
    UNCONFIRMED = "unconfirmed"
    CONFIRMED = "confirmed"
    DOUBLE_SPEND = "double-spend"
    FAILED = "failed"
    UNKNOWN = "unknown"

class WebhookEventType(str, Enum):
    """Webhook event types supported by BlockCypher"""
    UNCONFIRMED_TX = "unconfirmed-tx"
    CONFIRMED_TX = "confirmed-tx"
    TX_CONFIRMATION = "tx-confirmation"
    NEW_BLOCK = "new-block"
    DOUBLE_SPEND = "double-spend-tx"

class ScriptType(str, Enum):
    """Script types for multi-signature wallets"""
    MULTISIG_2_OF_3 = "multisig-2-of-3"
    MULTISIG_2_OF_2 = "multisig-2-of-2"
    MULTISIG_3_OF_5 = "multisig-3-of-5"
    
# Type aliases for better semantic meaning
Address = str
TransactionHash = str
Satoshi = int  # Bitcoin's smallest unit (1 BTC = 100,000,000 satoshis)
BTCAmount = float  # Amount in BTC

# Common data structures
AddressInfo = Dict[str, Any]
TransactionInfo = Dict[str, Any]
WebhookInfo = Dict[str, Any]
WalletInfo = Dict[str, Any] 