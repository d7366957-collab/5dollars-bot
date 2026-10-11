"""
Botoneras del bot 5DOLLARS
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard():
    """Menú principal"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔗 Mi link", callback_data="my_link"),
            InlineKeyboardButton("👥 Referidos", callback_data="my_referrals")
        ],
        [
            InlineKeyboardButton("💸 Retirar", callback_data="withdraw"),
            InlineKeyboardButton("📊 Historial", callback_data="history")
        ],
        [
            InlineKeyboardButton("🎁 Bonos", callback_data="bonuses"),
            InlineKeyboardButton("🏆 Ranking", callback_data="ranking")
        ],
        [
            InlineKeyboardButton("📖 Ayuda", callback_data="help"),
            InlineKeyboardButton("📞 Soporte", callback_data="support")
        ]
    ])


def welcome_keyboard():
    """Bienvenida"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🚀 EMPEZAR", callback_data="start_deposit"),
            InlineKeyboardButton("📖 CÓMO FUNCIONA", callback_data="how_it_works")
        ],
        [
            InlineKeyboardButton("🏆 RANKING", callback_data="ranking"),
            InlineKeyboardButton("💬 SOPORTE", callback_data="support")
        ]
    ])


def how_it_works_keyboard():
    """Cómo funciona"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 EMPEZAR", callback_data="start_deposit")],
        [InlineKeyboardButton("⬅️ ATRÁS", callback_data="back")]
    ])


def deposit_keyboard():
    """Depósito"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 VINCULAR MI WALLET", callback_data="setup_wallet")],
        [
            InlineKeyboardButton("📋 COPIAR", callback_data="copy_address"),
            InlineKeyboardButton("📞 SOPORTE", callback_data="support")
        ],
        [InlineKeyboardButton("⬅️ ATRÁS", callback_data="back")]
    ])


def wallet_setup_keyboard():
    """Vincular wallet"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 VINCULAR MI WALLET", callback_data="setup_wallet")],
        [InlineKeyboardButton("⬅️ ATRÁS", callback_data="back")]
    ])


def wallet_linked_keyboard():
    """Wallet vinculada"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 COPIAR DIRECCIÓN", callback_data="copy_address")],
        [InlineKeyboardButton("🏠 MENÚ", callback_data="menu")]
    ])


def after_premium_keyboard():
    """Después de activar premium"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📤 COMPARTIR", callback_data="share_link"),
            InlineKeyboardButton("📋 COPIAR LINK", callback_data="copy_link")
        ],
        [InlineKeyboardButton("🏠 IR AL MENÚ", callback_data="menu")]
    ])


def withdrawal_keyboard(balance, is_premium):
    """Retiro"""
    buttons = []
    
    if is_premium:
        min_w = 5.0
    else:
        min_w = 10.0
    
    if balance >= 5 and is_premium:
        buttons.append([InlineKeyboardButton("💵 RETIRAR $5", callback_data="withdraw_5")])
    
    if balance > min_w:
        buttons.append([InlineKeyboardButton(f"💵 RETIRAR TODO (${balance:.2f})", callback_data="withdraw_all")])
    
    if balance >= min_w:
        buttons.append([InlineKeyboardButton("📝 OTRO MONTO", callback_data="withdraw_custom")])
    
    buttons.append([InlineKeyboardButton("⬅️ ATRÁS", callback_data="back")])
    
    return InlineKeyboardMarkup(buttons)


def activate_premium_keyboard():
    """Activar premium (para gratis)"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 ACTIVAR PREMIUM", callback_data="start_deposit")],
        [InlineKeyboardButton("⬅️ ATRÁS", callback_data="menu")]
    ])


def back_keyboard():
    """Botón atrás"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 MENÚ", callback_data="menu")]
    ])


def ranking_keyboard():
    """Ranking"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 ACTUALIZAR", callback_data="ranking")],
        [InlineKeyboardButton("🏠 MENÚ", callback_data="menu")]
    ])


def support_keyboard():
    """Soporte"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 CONTACTAR", url="https://t.me/YordanSoporte")],
        [InlineKeyboardButton("🏠 MENÚ", callback_data="menu")]
    ])


# ============ BOTONES DE ADMIN ============

def admin_panel_keyboard():
    """Panel de admin"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📥 Depósitos", callback_data="admin_deposits"),
            InlineKeyboardButton("📤 Retiros", callback_data="admin_withdrawals")
        ],
        [
            InlineKeyboardButton("📊 Stats", callback_data="admin_stats"),
            InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")
        ],
        [
            InlineKeyboardButton("🎁 Dar Premium", callback_data="admin_give_premium"),
            InlineKeyboardButton("💰 Dar Saldo", callback_data="admin_give_balance")
        ]
    ])


def admin_withdrawal_keyboard(ticket):
    """Admin - retiro pendiente"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ PAGADO", callback_data=f"approve_wd_{ticket}"),
            InlineKeyboardButton("❌ RECHAZAR", callback_data=f"reject_wd_{ticket}")
        ]
    ])


def admin_deposit_keyboard(ticket):
    """Admin - depósito pendiente"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ APROBAR", callback_data=f"approve_dep_{ticket}"),
            InlineKeyboardButton("❌ RECHAZAR", callback_data=f"reject_dep_{ticket}")
        ]
    ])
