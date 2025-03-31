from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum

class TransactionStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    UNKNOWN = "unknown"

@dataclass
class WalletInfo:
    address: str
    private_key: str
    public_key: str
    network: str
    balance: float
    total_received: float
    total_sent: float
    unconfirmed_balance: float

@dataclass
class TransactionInfo:
    tx_hash: str
    from_address: str
    to_address: str
    amount: float
    fee: float
    status: TransactionStatus
    timestamp: int
    confirmations: int
    network: str
    raw_tx: Optional[str] = None

@dataclass
class BlockInfo:
    height: int
    hash: str
    timestamp: int
    size: int
    difficulty: float
    tx_count: int
    network: str
    previous_block: Optional[str] = None
    next_block: Optional[str] = None

@dataclass
class AddressInfo:
    address: str
    balance: float
    total_received: float
    total_sent: float
    unconfirmed_balance: float
    tx_count: int
    network: str
    last_updated: int

@dataclass
class TokenInfo:
    address: str
    name: str
    symbol: str
    decimals: int
    total_supply: float
    network: str
    contract_address: str
    owner: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
 