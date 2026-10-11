"""
Comandos de administración
"""
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID, ADMIN_IDS, REFERRAL_COMMISSION, REFERRAL_REGISTRATION_FEE
from database import (
    get_user, update_user, get_connection,
    add_balance, give_premium, remove_premium
)


def is_admin(user_id):
    """Verifica si es admin"""
    return user_id in ADMIN_IDS


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envía mensaje masivo a todos los usuarios"""
    if not is_admin(update.effective_user.id):
        return
    
    if not context.args:
        await update.message.reply_text(
            "📢 *Uso:* `/broadcast Tu mensaje`",
            parse_mode="Markdown"
        )
        return
    
    message = " ".join(context.args)
    
    conn = get_connection()
    users = conn.execute("SELECT id FROM users WHERE is_banned = 0").fetchall()
    conn.close()
    
    success = 0
    failed = 0
    
    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user['id'],
                text=message,
                parse_mode="Markdown"
            )
            success += 1
        except Exception:
            failed += 1
    
    await update.message.reply_text(
        f"📢 *Broadcast completado*\n\n"
        f"✅ Enviados: {success}\n"
        f"❌ Fallidos: {failed}",
        parse_mode="Markdown"
    )


async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Banea a un usuario"""
    if not is_admin(update.effective_user.id):
        return
    
    if not context.args:
        await update.message.reply_text(
            "Uso: `/ban <user_id>`",
            parse_mode="Markdown"
        )
        return
    
    try:
        user_id = int(context.args[0])
        update_user(user_id, is_banned=1)
        await update.message.reply_text(f"✅ Usuario {user_id} baneado.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Desbanea a un usuario"""
    if not is_admin(update.effective_user.id):
        return
    
    if not context.args:
        await update.message.reply_text(
            "Uso: `/unban <user_id>`",
            parse_mode="Markdown"
        )
        return
    
    try:
        user_id = int(context.args[0])
        update_user(user_id, is_banned=0)
        await update.message.reply_text(f"✅ Usuario {user_id} desbaneado.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def user_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra info de un usuario"""
    if not is_admin(update.effective_user.id):
        return
    
    if not context.args:
        await update.message.reply_text(
            "Uso: `/userinfo <user_id>`",
            parse_mode="Markdown"
        )
        return
    
    try:
        user_id = int(context.args[0])
        user = get_user(user_id)
        
        if not user:
            await update.message.reply_text("❌ Usuario no encontrado.")
            return
        
        plan = "💎 PREMIUM" if user['has_deposited'] else "🎁 GRATIS"
        wallet = user['wallet_address'] or "No vinculada"
        
        text = f"""
👤 *INFO DE USUARIO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 `{user['id']}`
👤 @{user['username'] or 'N/A'}
📝 {user['first_name'] or 'N/A'}
{plan}

💰 Saldo: ${user['balance']:.2f}
📈 Ganado: ${user['total_earned']:.2f}
💸 Retirado: ${user['total_withdrawn']:.2f}
🎁 Bonos: ${user['total_bonuses']:.2f}

👥 Registrados: {user['total_registered']}
✅ Premium: {user['total_premium']}
⏳ Pendientes: {user['total_pending']}

🔗 Wallet: `{wallet}`

✅ Depositó: {'Sí' if user['has_deposited'] else 'No'}
🚫 Baneado: {'Sí' if user['is_banned'] else 'No'}

📅 Registro: {user['created_at'][:19]}
"""
        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def export_db_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exporta la base de datos"""
    if not is_admin(update.effective_user.id):
        return
    
    try:
        with open('bot.db', 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename=f"bot_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
                caption="💾 Backup de la base de datos"
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def give_premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Da premium a un usuario sin pago (sorteos/soporte)"""
    if not is_admin(update.effective_user.id):
        return
    
    if not context.args:
        await update.message.reply_text(
            "🎁 *Uso:* `/givepremium <user_id>`\n\n"
            "Ejemplo: `/givepremium 123456789`\n\n"
            "_Útil para sorteos y soporte_",
            parse_mode="Markdown"
        )
        return
    
    try:
        user_id = int(context.args[0])
        user = get_user(user_id)
        
        if not user:
            await update.message.reply_text(f"❌ Usuario {user_id} no encontrado.")
            return
        
        if user['has_deposited']:
            await update.message.reply_text(f"⚠️ Usuario {user_id} ya es premium.")
            return
        
        give_premium(user_id)
        
        await update.message.reply_text(
            f"✅ *PREMIUM ACTIVADO*\n\n"
            f"👤 Usuario: @{user['username'] or user['first_name']}\n"
            f"🆔 ID: `{user_id}`\n"
            f"💎 Plan: PREMIUM\n\n"
            f"_Sin costo. Otorgado por admin._",
            parse_mode="Markdown"
        )
        
        # Notificar al usuario
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"""
🎁 *¡PREMIUM ACTIVADO!*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Acceso premium otorgado

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💎 *Ahora puedes:*

→ Ganas ${REFERRAL_REGISTRATION_FEE:.2f} por cada amigo
→ +${REFERRAL_COMMISSION:.2f} por referido premium
→ Retiras desde $5
→ Bonos hasta $190

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 Comparte tu link.

*El momento es ahora.*
""",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error notificando: {e}")
    
    except ValueError:
        await update.message.reply_text("❌ Envía un ID válido.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def remove_premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quita premium a un usuario"""
    if not is_admin(update.effective_user.id):
        return
    
    if not context.args:
        await update.message.reply_text(
            "🔒 *Uso:* `/removepremium <user_id>`",
            parse_mode="Markdown"
        )
        return
    
    try:
        user_id = int(context.args[0])
        user = get_user(user_id)
        
        if not user:
            await update.message.reply_text(f"❌ Usuario {user_id} no encontrado.")
            return
        
        if not user['has_deposited']:
            await update.message.reply_text(f"⚠️ Usuario {user_id} no es premium.")
            return
        
        remove_premium(user_id)
        
        await update.message.reply_text(
            f"✅ Premium removido a {user_id}.",
            parse_mode="Markdown"
        )
    
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def add_balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Añade saldo a un usuario (premios)"""
    if not is_admin(update.effective_user.id):
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "💰 *Uso:* `/addbalance <user_id> <amount>`\n\n"
            "Ejemplo: `/addbalance 123456789 5.50`",
            parse_mode="Markdown"
        )
        return
    
    try:
        user_id = int(context.args[0])
        amount = float(context.args[1])
        
        user = get_user(user_id)
        
        if not user:
            await update.message.reply_text(f"❌ Usuario {user_id} no encontrado.")
            return
        
        add_balance(user_id, amount)
        
        await update.message.reply_text(
            f"✅ *SALDO AÑADIDO*\n\n"
            f"👤 Usuario: @{user['username'] or user['first_name']}\n"
            f"🆔 ID: `{user_id}`\n"
            f"💰 Monto: +${amount:.2f}",
            parse_mode="Markdown"
        )
        
        # Notificar al usuario
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"""
🎁 *¡SALDO AÑADIDO!*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 *+${amount:.2f}*

Otorgado por el admin.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💵 Nuevo saldo: verifícalo en tu menú

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Comparte y sigue creciendo.*
""",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error notificando: {e}")
    
    except ValueError:
        await update.message.reply_text("❌ Formato inválido. Uso: `/addbalance <id> <monto>`", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando rápido de stats"""
    if not is_admin(update.effective_user.id):
        return
    
    from database import get_global_stats
    stats = get_global_stats()
    
    text = f"""
📊 *ESTADÍSTICAS RÁPIDAS*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 Usuarios: {stats['total_users']}
💎 Premium: {stats['active_users']}
🎁 Gratis: {stats['free_users']}
💰 Depositado: ${stats['total_deposits']:.2f}
💸 Retirado: ${stats['total_withdrawals']:.2f}
💵 Saldo sistema: ${stats['total_balance']:.2f}
📥 Pendientes dep: {stats['pending_deposits']}
📤 Pendientes ret: {stats['pending_withdrawals']}
"""
    await update.message.reply_text(text, parse_mode="Markdown")
