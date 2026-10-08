"""
Depósitos automáticos via Etherscan V2 API
"""
import requests
from config import (
    BSCSCAN_API_KEY, BSCSCAN_API_URL,
    DEPOSIT_WALLET, USDT_CONTRACT, ENTRY_PRICE, BSC_CHAIN_ID
)

# Cache de TX procesadas (evita duplicados)
processed_txs = set()


def get_usdt_transactions(wallet_address, limit=100):
    """Obtiene las últimas transacciones USDT BEP20"""
    params = {
        "chainid": BSC_CHAIN_ID,
        "module": "account",
        "action": "tokentx",
        "contractaddress": USDT_CONTRACT,
        "address": wallet_address,
        "page": 1,
        "offset": limit,
        "sort": "desc",
        "apikey": BSCSCAN_API_KEY
    }
    
    try:
        response = requests.get(BSCSCAN_API_URL, params=params, timeout=10)
        data = response.json()
        
        if data.get("status") == "1":
            return data.get("result", [])
        return []
    
    except Exception as e:
        print(f"❌ Error Etherscan: {e}")
        return []


def check_new_deposits():
    """Verifica nuevas transacciones entrantes"""
    txs = get_usdt_transactions(DEPOSIT_WALLET)
    new_deposits = []
    
    for tx in txs:
        tx_hash = tx.get("hash")
        
        # Evitar duplicados
        if tx_hash in processed_txs:
            continue
        
        # Solo entrantes (to = tu wallet)
        if tx.get("to", "").lower() != DEPOSIT_WALLET.lower():
            continue
        
        # Solo USDT
        if tx.get("contractAddress", "").lower() != USDT_CONTRACT.lower():
            continue
        
        # Monto (18 decimales para BEP20)
        try:
            value = int(tx.get("value", "0")) / (10 ** 18)
        except:
            continue
        
        # Solo depósitos de $5
        if abs(value - ENTRY_PRICE) > 0.01:
            continue
        
        # Confirmaciones mínimas
        confirmations = int(tx.get("confirmations", "0"))
        if confirmations < 3:
            continue
        
        new_deposits.append({
            "tx_hash": tx_hash,
            "from": tx.get("from", ""),
            "amount": value,
            "timestamp": int(tx.get("timeStamp", "0")),
        })
        
        processed_txs.add(tx_hash)
    
    return new_deposits
