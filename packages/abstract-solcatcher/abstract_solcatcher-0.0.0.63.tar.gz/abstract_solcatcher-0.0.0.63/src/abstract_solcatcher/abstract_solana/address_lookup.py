from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from ..abstract_async_rate_limit import *
import base64
from typing import List, Dict, Any
from abstract_utilities import *
import asyncio
from .abstract_transactions import get_account_keys,get_loaded_addresses,get_read_only_addresses,get_writable_addresses
def get_pubkey(obj):
    return Pubkey.from_string(str(obj))

def decode_lut_data(data: bytes) -> List[str]:
    """
    Decodes LUT (Address Lookup Table) data from the account's raw binary data.
    
    Args:
        data (bytes): The binary data retrieved from the LUT account.
    
    Returns:
        List[str]: A list of base58 encoded addresses.
    """
    # Assuming the data is base64 encoded
    address_size = 32  # Public keys in Solana are 32 bytes
    addresses = []

    # Process the binary data directly
    for i in range(0, len(data), address_size):
        address_bytes = data[i:i + address_size]
        if len(address_bytes) == address_size:
            address = Pubkey.from_bytes(address_bytes)
            addresses.append(address)

    return addresses

async def fetch_lut_addresses(client: AsyncClient, lut_keys: List[Pubkey]) -> List[Pubkey]:
    luts = []
    for lut_key in lut_keys:
        response = await client.get_account_info(lut_key)
        
        account_info = response.value
        if account_info:
            decoded_data = account_info.data  # Accessing the raw data directly
            addresses = decode_lut_data(decoded_data)  # Use the implemented function here
            luts.extend([get_pubkey(address) for address in addresses])
    return luts

async def process_transaction(client: AsyncClient, txnData: Dict[str, Any]) -> List[str]:
    account_keys = get_writable_addresses(txnData) + get_account_keys(txnData) + get_read_only_addresses(txnData)
    account_keys = [get_pubkey(key) for key in account_keys]

    # Fetch and combine addresses from LUTs
    lut_keys = [Pubkey.from_string(acc['accountKey']) for acc in txnData['transaction']['message'].get('addressTableLookups', [])]
    lut_addresses = await fetch_lut_addresses(client, lut_keys)

    # Combine the original account keys with LUT addresses
    all_accs = account_keys + lut_addresses

    # Convert to base58 for consistency
    all_accs_base58 = [str(acc) for acc in all_accs]

    # Validate and sort account keys
    sorted_addresses = sorted(all_accs_base58)

    # Process each account key dynamically
    for address in sorted_addresses:
        account_index = all_accs_base58.index(address)

        # Example of fetching associated data (assuming you have a method to get it)
        account_data = txnData.get('meta', {}).get('postTokenBalances', [])
        relevant_data = next((item for item in account_data if item['accountIndex'] == account_index), None)

        #if relevant_data:
        #    print(f"Data for {address}: {relevant_data}")
        #else:
            #print(f"No data found for address: {address}")
    return sorted_addresses

async def main_sorted_addresses(txn):
    method = 'sorted_addresses'
    url = await get_rate_limit_url(method)
    client = AsyncClient(url)
    sorted_addresses = await process_transaction(client, txn)
    await client.close()
    await log_response(method, sorted_addresses)
    return sorted_addresses  # Return the sorted addresses

# Modify the main function to use asyncio's event loop directly
def get_sorted_addresses(txnData):
    return asyncio.run(main_sorted_addresses(txnData))
