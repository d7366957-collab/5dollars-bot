"""
Comandos de administración
"""
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID, ADMIN_IDS
from database import get_user, update_user, get_connection


def is_admin(user_id):
    """Verifica si es admin"""
    return user_id in ADMIN_IDS


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envía mensaje masivo"""
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
        f"📢 *Broadcast completado*\n\n✅ Enviados: {success}\n❌ Fallidos: {failed}",
        parse_mode="Markdown"
    )


async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Banea usuario"""
    if not is_admin(update.effective_user.id):
        return
    
    if not context.args:
        await update.message.reply_text("Uso: `/ban <user_id>`", parse_mode="Markdown")
        return
    
    try:
        user_id = int(context.args[0])
        update_user(user_id, is_banned=1)
        await update.message.reply_text(f"✅ Usuario {user_id} baneado.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def user_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info de usuario"""
    if not is_admin(update.effective_user.id):
        return
    
    if not context.args:
        await update.message.reply_text("Uso: `/userinfo <user_id>`", parse_mode="Markdown")
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
✅ Activos: {user['total_active']}
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
    
    from datetime import datetime
    
    try:
        with open('bot.db', 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename=f"bot_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
                caption="💾 Backup de la base de datos"
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
