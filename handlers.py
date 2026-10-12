"""
Manejadores de eventos del bot 5DOLLARS
"""
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import (
    ADMIN_ID, ADMIN_IDS, ENTRY_PRICE, REFERRAL_COMMISSION,
    REFERRAL_REGISTRATION_FEE, MIN_WITHDRAWAL,
    MIN_WITHDRAWAL_FREE, DEPOSIT_WALLET, BOT_NAME
)
from database import (
    get_user, create_user, update_user, add_balance,
    get_user_by_referral_code, process_referral_registration,
    process_premium_commission, check_bonuses,
    get_referrals, get_commissions, create_withdrawal,
    get_withdrawals, get_ranking, get_global_stats,
    get_pending_withdrawals, approve_withdrawal, reject_withdrawal,
    link_wallet_to_user, get_user_by_wallet,
    give_premium, remove_premium
)
from keyboards import (
    main_menu_keyboard, welcome_keyboard, how_it_works_keyboard,
    deposit_keyboard, wallet_setup_keyboard, wallet_linked_keyboard,
    after_premium_keyboard, withdrawal_keyboard,
    activate_premium_keyboard, back_keyboard, ranking_keyboard,
    support_keyboard, admin_panel_keyboard,
    admin_withdrawal_keyboard
)
from messages import (
    welcome_message, how_it_works_message, deposit_message,
    wallet_setup_message, wallet_linked_message,
    premium_activated_message, main_menu_message,
    my_link_message, my_referrals_message, withdraw_message,
    wallet_request_message, withdrawal_created_message,
    bonuses_message, bonus_unlocked_message, ranking_message,
    help_message, support_message,
    new_referral_notification, referral_premium_notification,
    withdrawal_paid_notification
)


def is_admin(user_id):
    """Verifica si es admin"""
    return user_id in ADMIN_IDS


# ============ COMANDO /start ============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    
    existing = get_user(user.id)
    
    if existing:
        if existing['is_banned']:
            await update.message.reply_text("❌ Estás baneado del sistema.")
            return
        
        # ✅ SIEMPRE mostrar bienvenida si no es premium
        if existing['has_deposited']:
            # Premium → menú principal
            await update.message.reply_text(
                main_menu_message(existing),
                reply_markup=main_menu_keyboard(),
                parse_mode="Markdown"
            )
        else:
            # Gratis → bienvenida
            await update.message.reply_text(
                welcome_message(),
                reply_markup=welcome_keyboard(),
                parse_mode="Markdown"
            )
        return
    
    # Usuario nuevo
    referrer_id = None
    if args:
        referrer = get_user_by_referral_code(args[0])
        if referrer and referrer['id'] != user.id:
            referrer_id = referrer['id']
    
    new_user = create_user(
        user.id,
        user.username,
        user.first_name,
        referrer_id=referrer_id
    )
    
    if referrer_id:
        referrer = process_referral_registration(user.id)
        
        if referrer:
            try:
                await context.bot.send_message(
                    chat_id=referrer_id,
                    text=new_referral_notification(user.username or user.first_name),
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Error notificando: {e}")
    
    # Usuario nuevo → bienvenida
    await update.message.reply_text(
        welcome_message(),
        reply_markup=welcome_keyboard(),
        parse_mode="Markdown"
    )


# ============ COMANDO /menu ============

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    if not user:
        await start(update, context)
        return
    
    if user['has_deposited']:
        await update.message.reply_text(
            main_menu_message(user),
            reply_markup=main_menu_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            welcome_message(),
            reply_markup=welcome_keyboard(),
            parse_mode="Markdown"
        )


# ============ COMANDO /admin ============

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ No tienes permiso.")
        return
    
    stats = get_global_stats()
    
    text = f"""
👑 *PANEL DE ADMIN*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 *ESTADÍSTICAS*

👥 Usuarios: *{stats['total_users']}*
💎 Premium: *{stats['active_users']}*
🎁 Gratis: *{stats['free_users']}*
💰 Depositado: *${stats['total_deposits']:.2f}*
💸 Retirado: *${stats['total_withdrawals']:.2f}*
💵 Saldo: *${stats['total_balance']:.2f}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📥 Pendientes dep: *{stats['pending_deposits']}*
📤 Pendientes ret: *{stats['pending_withdrawals']}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    await update.message.reply_text(
        text,
        reply_markup=admin_panel_keyboard(),
        parse_mode="Markdown"
    )


# ============ MANEJADOR DE BOTONES ============

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    user = get_user(user_id)
    
    # ============ NAVEGACIÓN ============
    
    if data == "back" or data == "menu":
        if user and user['has_deposited']:
            await query.edit_message_text(
                main_menu_message(user),
                reply_markup=main_menu_keyboard(),
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                welcome_message(),
                reply_markup=welcome_keyboard(),
                parse_mode="Markdown"
            )
    
    elif data == "how_it_works":
        await query.edit_message_text(
            how_it_works_message(),
            reply_markup=how_it_works_keyboard(),
            parse_mode="Markdown"
        )
    
    elif data == "start_deposit":
        await query.edit_message_text(
            deposit_message(),
            reply_markup=deposit_keyboard(),
            parse_mode="Markdown"
        )
    
    elif data == "setup_wallet":
        context.user_data['awaiting_wallet'] = True
        await query.edit_message_text(
            wallet_setup_message(),
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )
    
    elif data == "copy_address":
        await query.answer(f"Dirección: {DEPOSIT_WALLET}", show_alert=True)
    
    elif data == "my_link":
        bot_username = (await context.bot.get_me()).username
        link = f"https://t.me/{bot_username}?start={user['referral_code']}"
        await query.edit_message_text(
            my_link_message(user, bot_username),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📤 COMPARTIR", url=f"https://t.me/share/url?url={link}")],
                [InlineKeyboardButton("🏠 MENÚ", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )
    
    elif data == "my_referrals":
        referrals = get_referrals(user_id)
        await query.edit_message_text(
            my_referrals_message(user, referrals),
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )
    
    elif data == "withdraw":
        await query.edit_message_text(
            withdraw_message(user),
            reply_markup=withdrawal_keyboard(user['balance'], user['has_deposited'] == 1),
            parse_mode="Markdown"
        )
    
    elif data == "withdraw_5":
        context.user_data['withdraw_amount'] = 5.0
        await query.edit_message_text(
            wallet_request_message(5.0),
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )
        context.user_data['awaiting_withdraw_wallet'] = True
    
    elif data == "withdraw_all":
        amount = user['balance']
        context.user_data['withdraw_amount'] = amount
        await query.edit_message_text(
            wallet_request_message(amount),
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )
        context.user_data['awaiting_withdraw_wallet'] = True
    
    elif data == "withdraw_custom":
        min_w = MIN_WITHDRAWAL if user['has_deposited'] else MIN_WITHDRAWAL_FREE
        await query.edit_message_text(
            f"📝 *Envía el monto*\n\n"
            f"Mínimo: ${min_w:.2f}\n"
            f"Máximo: ${user['balance']:.2f}",
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )
        context.user_data['awaiting_custom_amount'] = True
    
    elif data == "history":
        commissions = get_commissions(user_id)
        withdrawals = get_withdrawals(user_id)
        
        text = "📊 *HISTORIAL*\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n💸 *Comisiones:*\n"
        
        if commissions:
            for c in commissions[-5:]:
                tipo = "👥" if c['type'] == 'registration' else "💰"
                text += f"{tipo} @{c['username'] or 'user'} +${c['amount']:.2f}\n"
        else:
            text += "• Ninguna aún\n"
        
        text += f"\n📤 *Retiros:*\n"
        if withdrawals:
            for w in withdrawals[-5:]:
                emoji = "✅" if w['status'] == 'paid' else "⏳" if w['status'] == 'pending' else "❌"
                text += f"• {emoji} ${w['amount']:.2f}\n"
        else:
            text += "• Ninguno aún\n"
        
        text += f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n💵 *Saldo:* ${user['balance']:.2f}"
        
        await query.edit_message_text(
            text,
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )
    
    elif data == "bonuses":
        text = bonuses_message(user)
        keyboard = activate_premium_keyboard() if not user['has_deposited'] else back_keyboard()
        await query.edit_message_text(
            text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    
    elif data == "ranking":
        ranking = get_ranking(50)
        await query.edit_message_text(
            ranking_message(ranking, user_id),
            reply_markup=ranking_keyboard(),
            parse_mode="Markdown"
        )
    
    elif data == "help":
        await query.edit_message_text(
            help_message(),
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )
    
    elif data == "support":
        await query.edit_message_text(
            support_message(),
            reply_markup=support_keyboard(),
            parse_mode="Markdown"
        )
    
    # ============ ADMIN ============
    
    elif data == "admin_withdrawals":
        if not is_admin(user_id):
            return
        
        withdrawals = get_pending_withdrawals()
        
        if not withdrawals:
            await query.edit_message_text("📤 No hay retiros pendientes.", reply_markup=back_keyboard())
            return
        
        for wd in withdrawals[:5]:
            text = f"""
📤 *RETIRO PENDIENTE*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 `{wd['ticket']}`
👤 @{wd['username'] or wd['first_name']} (ID: `{wd['user_id']}`)
💰 ${wd['amount']:.2f}
📍 `{wd['wallet']}`
💵 Saldo: ${wd['balance']:.2f}
"""
            await query.message.reply_text(
                text,
                reply_markup=admin_withdrawal_keyboard(wd['ticket']),
                parse_mode="Markdown"
            )
    
    elif data == "admin_stats":
        if not is_admin(user_id):
            return
        
        stats = get_global_stats()
        text = f"""
📊 *ESTADÍSTICAS*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 Total: {stats['total_users']}
💎 Premium: {stats['active_users']}
🎁 Gratis: {stats['free_users']}
💰 Depositado: ${stats['total_deposits']:.2f}
💸 Retirado: ${stats['total_withdrawals']:.2f}
💵 Saldo: ${stats['total_balance']:.2f}
📥 Pendientes dep: {stats['pending_deposits']}
📤 Pendientes ret: {stats['pending_withdrawals']}
"""
        await query.edit_message_text(
            text,
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )
    
    elif data.startswith("approve_wd_"):
        if not is_admin(user_id):
            return
        
        ticket = data.replace("approve_wd_", "")
        withdrawal = approve_withdrawal(ticket, user_id)
        
        if withdrawal:
            await query.edit_message_text(f"✅ Retiro {ticket} pagado.")
            
            try:
                await context.bot.send_message(
                    chat_id=withdrawal['user_id'],
                    text=withdrawal_paid_notification(
                        ticket,
                        withdrawal['amount'],
                        withdrawal['wallet']
                    ),
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Error: {e}")
    
    elif data.startswith("reject_wd_"):
        if not is_admin(user_id):
            return
        
        ticket = data.replace("reject_wd_", "")
        reject_withdrawal(ticket, user_id)
        await query.edit_message_text(f"❌ Retiro {ticket} rechazado.")


# ============ MANEJADOR DE TEXTO ============

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    text = update.message.text.strip()
    
    if not user:
        return
    
    # ============ VINCULAR WALLET ============
    if context.user_data.get('awaiting_wallet'):
        wallet = text
        
        if not (wallet.startswith("0x") and len(wallet) == 42):
            await update.message.reply_text(
                "❌ Dirección inválida.\n\nDebe empezar con `0x` y tener 42 caracteres.",
                parse_mode="Markdown"
            )
            return
        
        existing = get_user_by_wallet(wallet)
        if existing and existing['id'] != user_id:
            await update.message.reply_text("❌ Esta wallet ya está vinculada a otro usuario.")
            return
        
        link_wallet_to_user(user_id, wallet)
        
        await update.message.reply_text(
            wallet_linked_message(wallet),
            reply_markup=wallet_linked_keyboard(),
            parse_mode="Markdown"
        )
        
        context.user_data['awaiting_wallet'] = False
        return
    
    # ============ RETIRO CON WALLET ============
    if context.user_data.get('awaiting_withdraw_wallet'):
        wallet = text
        
        if not (wallet.startswith("0x") and len(wallet) == 42):
            await update.message.reply_text(
                "❌ Dirección inválida.\n\nDebe empezar con `0x` y tener 42 caracteres.",
                parse_mode="Markdown"
            )
            return
        
        amount = context.user_data.get('withdraw_amount', MIN_WITHDRAWAL)
        ticket = f"WD-{random.randint(100000, 999999)}"
        
        create_withdrawal(user_id, amount, wallet, ticket)
        
        await update.message.reply_text(
            withdrawal_created_message(ticket, amount, wallet),
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )
        
        # Notificar al admin
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"""
🔔 *NUEVO RETIRO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 `{ticket}`
👤 @{user['username'] or user['first_name']}
🆔 ID: `{user_id}`
💰 ${amount:.2f}
📍 `{wallet}`
💵 Saldo: ${user['balance']:.2f}
""",
                reply_markup=admin_withdrawal_keyboard(ticket),
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error: {e}")
        
        context.user_data['awaiting_withdraw_wallet'] = False
        context.user_data['withdraw_amount'] = None
        return
    
    # ============ RETIRO MONTO PERSONALIZADO ============
    if context.user_data.get('awaiting_custom_amount'):
        try:
            amount = float(text)
            min_w = MIN_WITHDRAWAL if user['has_deposited'] else MIN_WITHDRAWAL_FREE
            
            if amount < min_w:
                await update.message.reply_text(f"❌ Mínimo ${min_w:.2f}")
                return
            
            if amount > user['balance']:
                await update.message.reply_text(f"❌ Saldo insuficiente. Tienes ${user['balance']:.2f}")
                return
            
            context.user_data['withdraw_amount'] = amount
            context.user_data['awaiting_custom_amount'] = False
            context.user_data['awaiting_withdraw_wallet'] = True
            
            await update.message.reply_text(
                wallet_request_message(amount),
                parse_mode="Markdown"
            )
        
        except ValueError:
            await update.message.reply_text("❌ Envía un número válido.")
        
        return
