"""
Configuración del bot 5DOLLARS
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ============ TELEGRAM ============
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# ============ CRIPTO ============
DEPOSIT_WALLET = os.getenv("DEPOSIT_WALLET", "0x0000000000000000000000000000000000000000")

# ============ PARÁMETROS ============
BOT_NAME = os.getenv("BOT_NAME", "5DOLLARS")
ENTRY_PRICE = float(os.getenv("ENTRY_PRICE", "5.0"))
REFERRAL_COMMISSION = float(os.getenv("REFERRAL_COMMISSION", "3.75"))
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

# ============ VALIDACIONES ============
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN no está configurado en .env")

if ADMIN_ID == 0:
    raise ValueError("❌ ADMIN_ID no está configurado en .env")

print(f"✅ Configuración cargada")
print(f"💰 Entrada: ${ENTRY_PRICE}")
print(f"💸 Comisión depósito: ${REFERRAL_COMMISSION}")
print(f"💸 Comisión registro: ${REFERRAL_REGISTRATION_FEE}")
print(f"📉 Mínimo retiro premium: ${MIN_WITHDRAWAL}")
print(f"📉 Mínimo retiro gratis: ${MIN_WITHDRAWAL_FREE}")
