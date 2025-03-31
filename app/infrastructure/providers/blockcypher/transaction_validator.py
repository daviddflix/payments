"""
Transaction Validator Utility

A utility for verifying and validating blockchain transactions using the BlockCypher API.
This can be used to:
1. Verify a transaction exists
2. Check the number of confirmations
3. Calculate the total value sent to a specific address
4. Verify transaction details like sender, recipient, and fees
"""

import os
import json
import argparse
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file (if available)
load_dotenv()

class TransactionValidator:
    """
    Utility for validating blockchain transactions using BlockCypher API
    """
    
    def __init__(self, coin_symbol="btc-testnet", token=None):
        """
        Initialize the validator
        
        Args:
            coin_symbol (str): The cryptocurrency to use (default: btc-testnet)
                Options: btc (Bitcoin), btc-testnet, ltc (Litecoin), doge (Dogecoin), etc.
            token (str): BlockCypher API token (optional)
        """
        self.coin_symbol = coin_symbol
        self.token = token or os.getenv("BLOCKCYPHER_TOKEN")
        self.base_url = f"https://api.blockcypher.com/v1/{self.coin_symbol}"
        
    def get_transaction(self, tx_hash):
        """
        Get detailed information about a transaction
        
        Args:
            tx_hash (str): Transaction hash/ID
            
        Returns:
            dict: Transaction details or None if not found
        """
        params = {"token": self.token} if self.token else {}
        url = f"{self.base_url}/txs/{tx_hash}"
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching transaction: {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"Error fetching transaction: {str(e)}")
            return None
            
    def verify_transaction(self, tx_hash, recipient_address=None, min_confirmations=0):
        """
        Verify a transaction exists and optionally check recipient and confirmations
        
        Args:
            tx_hash (str): Transaction hash/ID
            recipient_address (str, optional): Verify this address received funds
            min_confirmations (int, optional): Minimum confirmations required
            
        Returns:
            tuple: (is_valid, message, transaction_data)
        """
        tx_data = self.get_transaction(tx_hash)
        
        if not tx_data:
            return False, "Transaction not found", None
            
        # Check confirmation count
        confirmations = tx_data.get('confirmations', 0)
        if confirmations < min_confirmations:
            return False, f"Transaction has only {confirmations} confirmations, {min_confirmations} required", tx_data
            
        # If recipient address provided, verify it received funds
        if recipient_address:
            # Check if recipient is in outputs
            found = False
            amount = 0
            for output in tx_data.get('outputs', []):
                if recipient_address in output.get('addresses', []):
                    found = True
                    amount += output.get('value', 0)
                    
            if not found:
                return False, f"Transaction does not include payments to {recipient_address}", tx_data
            
            # Return success with amount
            return True, f"Valid transaction with {confirmations} confirmations. Amount: {amount/100000000:.8f} {self.coin_symbol.split('-')[0].upper()}", tx_data
        
        # If we get here, transaction is valid and meets confirmation requirement
        return True, f"Valid transaction with {confirmations} confirmations", tx_data
        
    def calculate_received_amount(self, tx_hash, address):
        """
        Calculate the total amount received by an address in a transaction
        
        Args:
            tx_hash (str): Transaction hash/ID
            address (str): The address to check
            
        Returns:
            tuple: (amount_satoshis, amount_in_coin_units)
        """
        tx_data = self.get_transaction(tx_hash)
        if not tx_data:
            return 0, 0
            
        total_received = 0
        for output in tx_data.get('outputs', []):
            if address in output.get('addresses', []):
                total_received += output.get('value', 0)
                
        # Convert to coin units (e.g., BTC, LTC)
        amount_in_coin = total_received / 100000000.0
        
        return total_received, amount_in_coin
        
    def format_transaction_details(self, tx_hash):
        """
        Format transaction details in a human-readable format
        
        Args:
            tx_hash (str): Transaction hash/ID
            
        Returns:
            str: Formatted transaction details
        """
        tx_data = self.get_transaction(tx_hash)
        if not tx_data:
            return "Transaction not found"
            
        # Get basic info
        confirmed = tx_data.get('confirmed', 'Unconfirmed')
        received = tx_data.get('received', 'Unknown')
        confirmations = tx_data.get('confirmations', 0)
        fees = tx_data.get('fees', 0)
        size = tx_data.get('size', 0)
        
        # Format date/time if available
        if confirmed != 'Unconfirmed':
            try:
                confirmed_dt = datetime.fromisoformat(confirmed.replace('Z', '+00:00'))
                confirmed = confirmed_dt.strftime('%Y-%m-%d %H:%M:%S UTC')
            except:
                pass
                
        # Format received time
        try:
            received_dt = datetime.fromisoformat(received.replace('Z', '+00:00'))
            received = received_dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        except:
            pass
            
        # Get total input/output values
        total_input = sum(input_data.get('output_value', 0) for input_data in tx_data.get('inputs', []))
        total_output = sum(output.get('value', 0) for output in tx_data.get('outputs', []))
        
        # Get input addresses (senders)
        input_addresses = set()
        for input_data in tx_data.get('inputs', []):
            addresses = input_data.get('addresses', [])
            for addr in addresses:
                input_addresses.add(addr)
                
        # Get output addresses (recipients)
        output_details = []
        for output in tx_data.get('outputs', []):
            addresses = output.get('addresses', [])
            value = output.get('value', 0)
            for addr in addresses:
                output_details.append((addr, value))
                
        # Create formatted output
        coin_symbol = self.coin_symbol.split('-')[0].upper()
        result = [
            f"Transaction: {tx_hash}",
            f"Status: {'Confirmed' if confirmations > 0 else 'Unconfirmed'} ({confirmations} confirmations)",
            f"Received Time: {received}",
            f"Confirmed Time: {confirmed if confirmed != 'Unconfirmed' else 'Pending'}",
            f"Total Input: {total_input/100000000:.8f} {coin_symbol}",
            f"Total Output: {total_output/100000000:.8f} {coin_symbol}",
            f"Fees: {fees/100000000:.8f} {coin_symbol}",
            f"Size: {size} bytes",
            f"Fee Rate: {fees/size:.2f} satoshis/byte",
            "\nSender Addresses:",
        ]
        
        for addr in input_addresses:
            result.append(f"  {addr}")
            
        result.append("\nRecipient Addresses:")
        for addr, value in output_details:
            result.append(f"  {addr}: {value/100000000:.8f} {coin_symbol}")
            
        return "\n".join(result)

def main():
    """Command line interface for the transaction validator"""
    parser = argparse.ArgumentParser(description="Blockchain Transaction Validator")
    parser.add_argument('tx_hash', type=str, help='Transaction hash/ID to verify')
    parser.add_argument('--address', '-a', type=str, help='Verify funds were sent to this address')
    parser.add_argument('--confirmations', '-c', type=int, default=0, 
                        help='Minimum confirmations required (default: 0)')
    parser.add_argument('--network', '-n', type=str, default='btc-testnet',
                        help='Blockchain network (default: btc-testnet)')
    parser.add_argument('--verbose', '-v', action='store_true', 
                        help='Show detailed transaction information')
    
    args = parser.parse_args()
    
    validator = TransactionValidator(coin_symbol=args.network)
    
    if args.verbose:
        print(validator.format_transaction_details(args.tx_hash))
    else:
        is_valid, message, _ = validator.verify_transaction(
            args.tx_hash, 
            args.address, 
            args.confirmations
        )
        
        print(f"Transaction status: {'VALID' if is_valid else 'INVALID'}")
        print(message)
    
if __name__ == "__main__":
    main() 