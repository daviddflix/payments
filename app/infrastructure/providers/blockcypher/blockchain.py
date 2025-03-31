from typing import Dict, Any, Optional, List
import blockcypher
import os
from .blockcypher_types import (
    WalletInfo,
    TransactionInfo,
    TransactionStatus,
    BlockInfo,
    AddressInfo,
    TokenInfo
)

class BlockCypherProvider:
    """Bitcoin implementation of the cryptocurrency provider."""
    
    def __init__(self, coin_symbol: str = 'btc-testnet'):
        self.api_token = os.getenv("BLOCKCYPHER_API_TOKEN")
        self.coin_symbol = coin_symbol

    def get_satoshi_multiplier(self) -> int:
        return 100000000  # 1 BTC = 100,000,000 satoshis
    
    def create_wallet(self, address: str) -> WalletInfo:
        try:
            wallet = blockcypher.create_wallet_from_address(
                address=address,
                api_key=self.api_token,
                coin_symbol=self.coin_symbol
            )
            return {
                "address": address,
                "private_key": wallet.get("private"),
                "public_key": wallet.get("public"),
                "wif": wallet.get("wif")
            }
        except Exception as e:
            raise Exception(f"Failed to create Bitcoin wallet: {str(e)}")
    
    def get_address_balance(self, address: str) -> float:
        try:
            address_info = blockcypher.get_address_details(
                address,
                coin_symbol=self.coin_symbol
            )
            return float(address_info.get("balance", 0)) / self.get_satoshi_multiplier()
        except Exception as e:
            raise Exception(f"Failed to get Bitcoin address balance: {str(e)}")
    
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
            raise Exception(f"Failed to get Bitcoin address details: {str(e)}")
    
    def get_total_balance(self, address: str) -> int:
        try:
            address_info = blockcypher.get_address_details(
                address,
                coin_symbol=self.coin_symbol
            )
            return address_info.get("balance", 0)
        except Exception as e:
            raise Exception(f"Failed to get Bitcoin total balance: {str(e)}")
    
    def create_transaction(
        self,
        from_address: str,
        to_address: str,
        amount: float,
        private_key: str
    ) -> TransactionInfo:
        try:
            satoshis = int(amount * self.get_satoshi_multiplier())
            
            tx = blockcypher.create_unsigned_tx(
                inputs=[{"address": from_address}],
                outputs=[{"address": to_address, "value": satoshis}],
                coin_symbol=self.coin_symbol
            )
            
            signed_tx = blockcypher.sign_transaction(
                tx,
                private_key,
                coin_symbol=self.coin_symbol
            )
            
            result = blockcypher.push_unsigned_tx(
                signed_tx,
                coin_symbol=self.coin_symbol
            )
            
            return {
                "transaction_hash": result.get("tx", {}).get("hash"),
                "status": "success"
            }
        except Exception as e:
            raise Exception(f"Failed to create Bitcoin transaction: {str(e)}")
    
    def get_transaction_status(self, tx_hash: str) -> TransactionStatus:
        try:
            tx = blockcypher.get_transaction_details(
                tx_hash,
                coin_symbol=self.coin_symbol
            )
            return {
                "hash": tx_hash,
                "confirmations": tx.get("confirmations", 0),
                "status": "confirmed" if tx.get("confirmations", 0) > 0 else "pending"
            }
        except Exception as e:
            raise Exception(f"Failed to get Bitcoin transaction status: {str(e)}")
    
    def get_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        try:
            return blockcypher.get_transaction_details(
                tx_hash,
                coin_symbol=self.coin_symbol
            )
        except Exception as e:
            raise Exception(f"Failed to get Bitcoin transaction details: {str(e)}")
    
    def get_latest_block_height(self) -> int:
        try:
            return blockcypher.get_latest_block_height(coin_symbol=self.coin_symbol)
        except Exception as e:
            raise Exception(f"Failed to get Bitcoin latest block height: {str(e)}")
    
    def get_block_details(self, block_height: int) -> BlockInfo:
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
            raise Exception(f"Failed to get Bitcoin block details: {str(e)}")
    
    def get_block_overview(self, block_height: int) -> Dict[str, Any]:
        try:
            return blockcypher.get_block_overview(block_height, coin_symbol=self.coin_symbol)
        except Exception as e:
            raise Exception(f"Failed to get Bitcoin block overview: {str(e)}")
    
    def get_token_balance(self, address: str, token_address: str) -> float:
        """Bitcoin doesn't support tokens natively, so this is not implemented."""
        raise NotImplementedError("Bitcoin does not support tokens natively")

    def get_token_details(self, token_address: str) -> TokenInfo:
        """Bitcoin doesn't support tokens natively, so this is not implemented."""
        raise NotImplementedError("Bitcoin does not support tokens natively")

    def create_token_transaction(
        self,
        from_address: str,
        to_address: str,
        token_address: str,
        amount: float,
        private_key: str
    ) -> TransactionInfo:
        """Bitcoin doesn't support tokens natively, so this is not implemented."""
        raise NotImplementedError("Bitcoin does not support tokens natively")

    def get_token_transactions(
        self,
        address: str,
        token_address: str,
        limit: int = 50
    ) -> List[TransactionInfo]:
        """Bitcoin doesn't support tokens natively, so this is not implemented."""
        raise NotImplementedError("Bitcoin does not support tokens natively")

# Example usage
if __name__ == "__main__":
    # Initialize the provider with your API token
    provider = BlockCypherProvider(api_token="your_api_token_here", use_testnet=True)
    
    # Get the latest block height
    latest_block = provider.get_latest_block_height()
    print(f"Latest block height: {latest_block}")
    
    # Get network information
    print(f"Network: {provider.get_network_name()} ({provider.get_network_symbol()})")
    
    # Example: Get address details (replace with a valid Bitcoin address)
    # address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    # details = provider.get_address_details(address)
    # print(f"Address details: {details}")


