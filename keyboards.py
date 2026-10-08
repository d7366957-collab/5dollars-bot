"""
Botoneras del bot
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard():
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
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 EMPEZAR", callback_data="start_deposit")],
        [InlineKeyboardButton("⬅️ ATRÁS", callback_data="back")]
    ])


def deposit_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 VINCULAR MI WALLET", callback_data="setup_wallet")],
        [InlineKeyboardButton("📸 YA ENVIÉ EL PAGO", callback_data="sent_payment")],
        [
            InlineKeyboardButton("📋 COPIAR", callback_data="copy_address"),
            InlineKeyboardButton("🔄 VERIFICAR", callback_data="check_payment")
        ],
        [InlineKeyboardButton("⬅️ ATRÁS", callback_data="back")]
    ])


def wallet_setup_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 VINCULAR MI WALLET", callback_data="setup_wallet")],
        [InlineKeyboardButton("⬅️ ATRÁS", callback_data="back")]
    ])


def after_deposit_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📤 COMPARTIR", callback_data="share_link"),
            InlineKeyboardButton("📋 COPIAR LINK", callback_data="copy_link")
        ],
        [InlineKeyboardButton("🏠 MENÚ", callback_data="menu")]
    ])


def withdrawal_keyboard(balance, is_premium):
    buttons = []
    
    min_w = 5.0 if is_premium else 10.0
    
    if balance >= 5 and is_premium:
        buttons.append([InlineKeyboardButton("💵 RETIRAR $5", callback_data="withdraw_5")])
    
    if balance > min_w:
        buttons.append([InlineKeyboardButton(f"💵 RETIRAR TODO (${balance:.2f})", callback_data="withdraw_all")])
    
    buttons.append([InlineKeyboardButton("📝 OTRO MONTO", callback_data="withdraw_custom")])
    buttons.append([InlineKeyboardButton("⬅️ ATRÁS", callback_data="back")])
    
    return InlineKeyboardMarkup(buttons)


def activate_premium_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 ACTIVAR PREMIUM $5", callback_data="start_deposit")],
        [InlineKeyboardButton("⬅️ ATRÁS", callback_data="menu")]
    ])


def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 MENÚ", callback_data="menu")]
    ])


def admin_deposit_keyboard(ticket):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ APROBAR", callback_data=f"approve_dep_{ticket}"),
            InlineKeyboardButton("❌ RECHAZAR", callback_data=f"reject_dep_{ticket}")
        ]
    ])


def admin_withdrawal_keyboard(ticket):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ PAGADO", callback_data=f"approve_wd_{ticket}"),
            InlineKeyboardButton("❌ RECHAZAR", callback_data=f"reject_wd_{ticket}")
        ]
    ])


def admin_panel_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📥 Depósitos", callback_data="admin_deposits"),
            InlineKeyboardButton("📤 Retiros", callback_data="admin_withdrawals")
        ],
        [
            InlineKeyboardButton("📊 Stats", callback_data="admin_stats"),
            InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")
        ]
    ])
