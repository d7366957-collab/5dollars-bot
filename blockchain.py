"""
Depósitos automáticos via Etherscan V2 API (BSC)
"""
import requests
from config import (
    BSCSCAN_API_KEY, BSCSCAN_API_URL,
    DEPOSIT_WALLET, USDT_CONTRACT, ENTRY_PRICE, BSC_CHAIN_ID
)

# Cache de TX procesadas (evita duplicados)
processed_txs = set()


def get_usdt_transactions(wallet_address, limit=100):
    """
    Obtiene las últimas transacciones USDT BEP20 de una wallet
    
    Args:
        wallet_address: Dirección de la wallet a consultar
        limit: Número máximo de transacciones a obtener
    
    Returns:
        Lista de transacciones o lista vacía si hay error
    """
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
        
        # Si no hay transacciones o hay error
        if data.get("message") == "No transactions found":
            return []
        
        print(f"⚠️ Etherscan respuesta: {data.get('message', 'Unknown')}")
        return []
    
    except requests.exceptions.Timeout:
        print("❌ Etherscan: timeout")
        return []
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Etherscan: error de red - {e}")
        return []
    
    except Exception as e:
        print(f"❌ Etherscan: error inesperado - {e}")
        return []


def check_new_deposits():
    """
    Verifica nuevas transacciones USDT entrantes a DEPOSIT_WALLET
    
    Returns:
        Lista de diccionarios con las nuevas transacciones válidas
    """
    txs = get_usdt_transactions(DEPOSIT_WALLET)
    new_deposits = []
    
    if not txs:
        return new_deposits
    
    for tx in txs:
        tx_hash = tx.get("hash")
        
        # Evitar duplicados
        if tx_hash in processed_txs:
            continue
        
        # Solo transacciones entrantes (to = tu wallet)
        if tx.get("to", "").lower() != DEPOSIT_WALLET.lower():
            continue
        
        # Solo USDT
        if tx.get("contractAddress", "").lower() != USDT_CONTRACT.lower():
            continue
        
        # Convertir valor (18 decimales para BEP20)
        try:
            value = int(tx.get("value", "0")) / (10 ** 18)
        except (ValueError, TypeError):
            continue
        
        # Solo depósitos del monto esperado (con tolerancia)
        if abs(value - ENTRY_PRICE) > 0.01:
            continue
        
        # Confirmaciones mínimas (evita transacciones no confirmadas)
        try:
            confirmations = int(tx.get("confirmations", "0"))
        except (ValueError, TypeError):
            confirmations = 0
        
        if confirmations < 3:
            continue
        
        # TX válida
        new_deposits.append({
            "tx_hash": tx_hash,
            "from": tx.get("from", "").lower(),
            "amount": value,
            "timestamp": int(tx.get("timeStamp", "0")),
        })
        
        processed_txs.add(tx_hash)
    
    return new_deposits


def get_tx_url(tx_hash):
    """Devuelve la URL de BscScan para una transacción"""
    return f"https://bscscan.com/tx/{tx_hash}"
