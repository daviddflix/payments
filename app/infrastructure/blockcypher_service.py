from typing import Optional
import blockcypher
from blockcypher import create_wallet_from_address

from app.core.config import settings


class BlockCypherService:
    def __init__(self):
        blockcypher.api_key = settings.BLOCKCYPHER_TOKEN

    def create_wallet(self, address: str) -> dict:
        """Create a new Bitcoin wallet using BlockCypher."""
        try:
            wallet = create_wallet_from_address(
                address=address,
                api_key=settings.BLOCKCYPHER_TOKEN
            )
            return {
                "address": address,
                "private_key": wallet.get("private"),
                "public_key": wallet.get("public"),
                "wif": wallet.get("wif")
            }
        except Exception as e:
            raise Exception(f"Failed to create wallet: {str(e)}")

    def get_address_balance(self, address: str) -> float:
        """Get the balance of a Bitcoin address."""
        try:
            address_info = blockcypher.get_address_details(address)
            return float(address_info.get("balance", 0)) / 100000000  # Convert satoshis to BTC
        except Exception as e:
            raise Exception(f"Failed to get address balance: {str(e)}")

    def create_transaction(
        self,
        from_address: str,
        to_address: str,
        amount: float,
        private_key: str
    ) -> dict:
        """Create and send a Bitcoin transaction."""
        try:
            # Convert BTC to satoshis
            satoshis = int(amount * 100000000)
            
            # Create the transaction
            tx = blockcypher.create_unsigned_tx(
                inputs=[{"address": from_address}],
                outputs=[{"address": to_address, "value": satoshis}],
                coin_symbol="btc"
            )
            
            # Sign and send the transaction
            signed_tx = blockcypher.sign_transaction(
                tx,
                private_key,
                coin_symbol="btc"
            )
            
            # Push the transaction to the network
            result = blockcypher.push_unsigned_tx(
                signed_tx,
                coin_symbol="btc"
            )
            
            return {
                "transaction_hash": result.get("tx", {}).get("hash"),
                "status": "success"
            }
        except Exception as e:
            raise Exception(f"Failed to create transaction: {str(e)}")

    def get_transaction_status(self, tx_hash: str) -> dict:
        """Get the status of a Bitcoin transaction."""
        try:
            tx = blockcypher.get_transaction_details(tx_hash)
            return {
                "hash": tx_hash,
                "confirmations": tx.get("confirmations", 0),
                "status": "confirmed" if tx.get("confirmations", 0) > 0 else "pending"
            }
        except Exception as e:
            raise Exception(f"Failed to get transaction status: {str(e)}") 