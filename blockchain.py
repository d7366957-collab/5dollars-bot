"""
Detección de depósitos USDT BEP20 via RPC directo de BSC
Sin API Key. Sin límites. Sin KYC.
"""
import json
from web3 import Web3
from config import (
    BSC_NODES, DEPOSIT_WALLET, USDT_CONTRACT,
    ENTRY_PRICE, BSC_CHAIN_ID
)

# ============ CONEXIÓN A BSC ============

_current_node_index = 0


def get_web3():
    """Obtiene conexión a un nodo BSC (rota si falla)"""
    global _current_node_index
    
    for _ in range(len(BSC_NODES)):
        try:
            node = BSC_NODES[_current_node_index]
            w3 = Web3(Web3.HTTPProvider(node, request_kwargs={'timeout': 10}))
            
            if w3.is_connected():
                return w3
            
            # Rotar al siguiente nodo
            _current_node_index = (_current_node_index + 1) % len(BSC_NODES)
        
        except Exception as e:
            print(f"⚠️ Nodo {node} falló: {e}")
            _current_node_index = (_current_node_index + 1) % len(BSC_NODES)
    
    return None


# ============ ABI MÍNIMO DE USDT ============

USDT_ABI = json.loads("""
[
    {
        "constant": true,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "name": "from", "type": "address"},
            {"indexed": true, "name": "to", "type": "address"},
            {"indexed": false, "name": "value", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]
""")


# ============ CACHE DE TX PROCESADAS ============

processed_txs = set()
_last_checked_block = 0


# ============ DETECCIÓN DE DEPÓSITOS ============

def check_new_deposits():
    """
    Verifica nuevas transacciones USDT entrantes a DEPOSIT_WALLET
    Consulta los últimos 5 bloques (~15 segundos)
    
    Returns:
        Lista de diccionarios con las nuevas transacciones válidas
    """
    global _last_checked_block
    
    w3 = get_web3()
    
    if not w3:
        print("❌ No hay nodos BSC disponibles")
        return []
    
    new_deposits = []
    
    try:
        # Último bloque
        latest_block = w3.eth.block_number
        
        # Si es la primera vez, empezar desde el bloque actual
        if _last_checked_block == 0:
            _last_checked_block = latest_block - 5
        
        # Consultar bloques desde el último chequeo
        from_block = _last_checked_block + 1
        to_block = latest_block
        
        # Máximo 20 bloques a la vez
        if to_block - from_block > 20:
            from_block = to_block - 20
        
        # Contrato USDT
        usdt = w3.eth.contract(
            address=Web3.to_checksum_address(USDT_CONTRACT),
            abi=USDT_ABI
        )
        
        # Buscar eventos Transfer hacia DEPOSIT_WALLET
        deposit_wallet_checksum = Web3.to_checksum_address(DEPOSIT_WALLET)
        
        transfer_filter = usdt.events.Transfer.create_filter(
            fromBlock=from_block,
            toBlock=to_block,
            argument_filters={'to': deposit_wallet_checksum}
        )
        
        events = transfer_filter.get_all_entries()
        
        for event in events:
            tx_hash = event['transactionHash'].hex()
            
            # Evitar duplicados
            if tx_hash in processed_txs:
                continue
            
            # Convertir monto (18 decimales para BEP20 USDT)
            try:
                value = event['args']['value'] / (10 ** 18)
            except (ValueError, TypeError):
                continue
            
            # Solo depósitos del monto esperado (con tolerancia)
            if abs(value - ENTRY_PRICE) > 0.01:
                continue
            
            # TX válida
            new_deposits.append({
                "tx_hash": tx_hash,
                "from": event['args']['from'].lower(),
                "amount": value,
                "block": event['blockNumber'],
            })
            
            processed_txs.add(tx_hash)
        
        # Actualizar último bloque chequeado
        _last_checked_block = to_block
    
    except Exception as e:
        print(f"❌ Error consultando bloques: {e}")
        return []
    
    return new_deposits


def get_tx_url(tx_hash):
    """Devuelve la URL de BscScan para una transacción"""
    return f"https://bscscan.com/tx/{tx_hash}"


def check_connection():
    """Verifica que haya conexión a BSC"""
    w3 = get_web3()
    
    if not w3:
        return False
    
    return w3.is_connected()
