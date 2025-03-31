from typing import Dict, Any, Optional, List
import blockcypher
import os
from app.infrastructure.providers.blockcypher.common.types import (
    CoinSymbol,
    Address, 
    TransactionHash,
    TransactionInfo,
    TransactionStatus,
    AddressInfo,
    WalletInfo
)

class BlockchainService:
    """
    High-level service for interacting with blockchain data through BlockCypher API.
    
    This class provides access to blockchain data like blocks, transactions,
    and network information, without handling wallets or transactions directly.
    """
    
    def __init__(self, coin_symbol: CoinSymbol = 'btc-testnet'):
        self.api_token = os.getenv("BLOCKCYPHER_API_TOKEN")
        self.coin_symbol = coin_symbol

    def get_satoshi_multiplier(self) -> int:
        return 100000000  # 1 BTC = 100,000,000 satoshis
    
    def get_address_balance(self, address: str) -> float:
        try:
            address_info = blockcypher.get_address_details(
                address,
                coin_symbol=self.coin_symbol
            )
            return float(address_info.get("balance", 0)) / self.get_satoshi_multiplier()
        except Exception as e:
            raise Exception(f"Failed to get address balance: {str(e)}")
    
    def get_address_details(self, address: str) -> AddressInfo:
        try:
            details = blockcypher.get_address_details(
                address,
                coin_symbol=self.coin_symbol
            )
            return {
                "address": address,
                "balance": details.get("balance", 0),
                "total_received": details.get("total_received", 0),
                "total_sent": details.get("total_sent", 0),
                "n_tx": details.get("n_tx", 0),
                "unconfirmed_balance": details.get("unconfirmed_balance", 0),
                "final_balance": details.get("final_balance", 0)
            }
        except Exception as e:
            raise Exception(f"Failed to get address details: {str(e)}")
    
    def get_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        try:
            return blockcypher.get_transaction_details(
                tx_hash,
                coin_symbol=self.coin_symbol
            )
        except Exception as e:
            raise Exception(f"Failed to get transaction details: {str(e)}")
    
    def get_latest_block_height(self) -> int:
        try:
            return blockcypher.get_latest_block_height(coin_symbol=self.coin_symbol)
        except Exception as e:
            raise Exception(f"Failed to get latest block height: {str(e)}")
    
    def get_block_details(self, block_height: int) -> Dict[str, Any]:
        try:
            details = blockcypher.get_block_details(block_height, coin_symbol=self.coin_symbol)
            return {
                "hash": details.get("hash"),
                "height": details.get("height"),
                "time": details.get("time"),
                "n_tx": details.get("n_tx"),
                "total": details.get("total"),
                "fees": details.get("fees"),
                "size": details.get("size"),
                "ver": details.get("ver"),
                "prev_block": details.get("prev_block"),
                "mrkl_root": details.get("mrkl_root"),
                "txids": details.get("txids", [])
            }
        except Exception as e:
            raise Exception(f"Failed to get block details: {str(e)}")
    
    def get_block_overview(self, block_height: int) -> Dict[str, Any]:
        try:
            return blockcypher.get_block_overview(block_height, coin_symbol=self.coin_symbol)
        except Exception as e:
            raise Exception(f"Failed to get block overview: {str(e)}")
    
    def get_network_info(self) -> Dict[str, Any]:
        """
        Get information about the current network.
        
        Returns:
            Dictionary with network information
        """
        try:
            return blockcypher.get_blockchain_overview(coin_symbol=self.coin_symbol)
        except Exception as e:
            raise Exception(f"Failed to get network information: {str(e)}")

    def get_fee_estimates(self) -> Dict[str, int]:
        """
        Get fee estimates for different priority levels.
        
        Returns:
            Dictionary with fee estimates in satoshis per kilobyte
        """
        try:
            info = blockcypher.get_blockchain_overview(coin_symbol=self.coin_symbol)
            return {
                "high_fee_per_kb": info.get("high_fee_per_kb", 0),
                "medium_fee_per_kb": info.get("medium_fee_per_kb", 0),
                "low_fee_per_kb": info.get("low_fee_per_kb", 0)
            }
        except Exception as e:
            raise Exception(f"Failed to get fee estimates: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Initialize the provider with your API token
    provider = BlockchainService(api_token="your_api_token_here", use_testnet=True)
    
    # Get the latest block height
    latest_block = provider.get_latest_block_height()
    print(f"Latest block height: {latest_block}")
    
    # Get network information
    print(f"Network: {provider.get_network_name()} ({provider.get_network_symbol()})")
    
    # Example: Get address details (replace with a valid Bitcoin address)
    # address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    # details = provider.get_address_details(address)
    # print(f"Address details: {details}")


