"""
Configuración del bot 5DOLLARS
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ============ TELEGRAM ============
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
ADMIN_ID_2 = int(os.getenv("ADMIN_ID_2", "0"))
ADMIN_ID_3 = int(os.getenv("ADMIN_ID_3", "0"))

# Lista de admins
ADMIN_IDS = [id for id in [ADMIN_ID, ADMIN_ID_2, ADMIN_ID_3] if id != 0]

# ============ CRIPTO ============
DEPOSIT_WALLET = os.getenv("DEPOSIT_WALLET", "0x0000000000000000000000000000000000000000")

# ============ PARÁMETROS ============
BOT_NAME = os.getenv("BOT_NAME", "5DOLLARS")
ENTRY_PRICE = float(os.getenv("ENTRY_PRICE", "5.0"))
REFERRAL_COMMISSION = float(os.getenv("REFERRAL_COMMISSION", "3.00"))
REFERRAL_REGISTRATION_FEE = float(os.getenv("REFERRAL_REGISTRATION_FEE", "0.05"))
MIN_WITHDRAWAL = float(os.getenv("MIN_WITHDRAWAL", "5.0"))
MIN_WITHDRAWAL_FREE = float(os.getenv("MIN_WITHDRAWAL_FREE", "10.0"))
BONUS_10_REFERRALS = float(os.getenv("BONUS_10_REFERRALS", "10.0"))

# ============ BONOS ESCALONADOS ============
BONUSES = {
    10: 10.0,
    50: 25.0,
    100: 50.0,
    500: 250.0,
    1000: 500.0,
}

# ============ BASE DE DATOS ============
DATABASE_PATH = os.getenv("DATABASE_PATH", "bot.db")

# ============ ETHERSCAN V2 (BSC) ============
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY", "")
BSCSCAN_API_URL = "https://api.etherscan.io/v2/api"
USDT_CONTRACT = "0x55d398326f99059fF775485246999027B3197955"
BSC_CHAIN_ID = "56"

# ============ VALIDACIONES ============
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN no está configurado en .env")

if ADMIN_ID == 0:
    raise ValueError("❌ ADMIN_ID no está configurado en .env")

if not BSCSCAN_API_KEY:
    print("⚠️ BSCSCAN_API_KEY no configurada - depósitos automáticos desactivados")

print(f"✅ Configuración cargada")
print(f"💰 Entrada: ${ENTRY_PRICE}")
print(f"💸 Comisión depósito: ${REFERRAL_COMMISSION}")
print(f"💸 Comisión registro: ${REFERRAL_REGISTRATION_FEE}")
print(f"📉 Mínimo retiro premium: ${MIN_WITHDRAWAL}")
print(f"📉 Mínimo retiro gratis: ${MIN_WITHDRAWAL_FREE}")
print(f"🔑 Admins configurados: {len(ADMIN_IDS)}")
