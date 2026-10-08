"""
Manejadores de eventos del bot
"""
import random
import re
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import (
    ADMIN_ID, ADMIN_IDS, ENTRY_PRICE, REFERRAL_COMMISSION,
    REFERRAL_REGISTRATION_FEE, MIN_WITHDRAWAL,
    MIN_WITHDRAWAL_FREE, DEPOSIT_WALLET, BOT_NAME
)
from database import (
    get_user, create_user, update_user, add_balance,
    get_user_by_referral_code, create_deposit,
    process_referral_registration, process_referral_commission,
    check_bonuses, get_referrals, get_commissions,
    create_withdrawal, get_withdrawals, get_ranking,
    get_global_stats, get_pending_deposits, get_pending_withdrawals,
    approve_deposit, reject_deposit, approve_withdrawal, reject_withdrawal,
    link_wallet_to_user, get_user_by_wallet, create_auto_deposit
)
from keyboards import (
    main_menu_keyboard, welcome_keyboard, how_it_works_keyboard,
    deposit_keyboard, after_deposit_keyboard, withdrawal_keyboard,
    back_keyboard, admin_deposit_keyboard, admin_withdrawal_keyboard,
    admin_panel_keyboard, activate_premium_keyboard, wallet_setup_keyboard
)
from messages import (
    welcome_message, how_it_works_message, deposit_message,
    send_proof_message, proof_received_message, deposit_approved_message,
    main_menu_message, my_link_message, my_referrals_message,
    withdraw_message, wallet_request_message, withdrawal_created_message,
    bonuses_message, bonus_unlocked_message, ranking_message,
    help_message, new_referral_notification, referral_deposited_notification,
    withdrawal_paid_notification
)


def is_admin(user_id):
    """Verifica si es admin"""
    return user_id in ADMIN_IDS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    
    existing = get_user(user.id)
    
    if existing:
        if existing['is_banned']:
            await update.message.reply_text("❌ Estás baneado del sistema.")
            return
        
        await update.message.reply_text(
            main_menu_message(existing),
            reply_markup=main_menu_keyboard(),
            parse_mode="Markdown"
        )
        return
    
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
                    text=new_referral_notification(
                        user.username or user.first_name,
                        referrer['has_deposited'] == 1
                    ),
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Error: {e}")
    
    await update.message.reply_text(
        welcome_message(),
        reply_markup=welcome_keyboard(),
        parse_mode="Markdown"
    )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    if not user:
        await start(update, context)
        return
    
    await update.message.reply_text(
        main_menu_message(user),
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )


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


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    user = get_user(user_id)
    
    if data == "back" or data == "menu":
        if user:
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
        context.user_data['awaiting_user_wallet'] = True
        await query.edit_message_text(
            "🔗 *VINCULA TU WALLET*\n\n"
            "Envía tu dirección USDT BEP20:\n\n"
            "⚠️ Debe empezar con `0x`\n"
            "⚠️ Es la wallet desde donde enviarás los $5\n\n"
            "📌 *Los depósitos se detectarán automáticamente.*",
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )
    
    elif data == "copy_address":
        await query.answer(f"Dirección: {DEPOSIT_WALLET}", show_alert=True)
    
    elif data == "sent_payment":
        await query.edit_message_text(
            send_proof_message(),
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )
        context.user_data['awaiting_proof'] = True
    
    elif data == "check_payment":
        await query.answer("⏳ Verificando...", show_alert=True)
    
    elif data == "my_link":
        bot_username = (await context.bot.get_me()).username
        await query.edit_message_text(
            my_link_message(user, bot_username),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📤 Compartir", url=f"https://t.me/share/url?url=https://t.me/{bot_username}?start={user['referral_code']}")],
                [InlineKeyboardButton("⬅️ Atrás", callback_data="menu")]
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
        context.user_data['awaiting_wallet'] = True
    
    elif data == "withdraw_all":
        amount = user['balance']
        context.user_data['withdraw_amount'] = amount
        await query.edit_message_text(
            wallet_request_message(amount),
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )
        context.user_data['awaiting_wallet'] = True
    
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
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Actualizar", callback_data="ranking")],
                [InlineKeyboardButton("⬅️ Atrás", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )
    
    elif data == "help" or data == "support":
        await query.edit_message_text(
            help_message(),
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )
    
    # ============ ADMIN ============
    
    elif data == "admin_deposits":
        if not is_admin(user_id):
            return
        
        deposits = get_pending_deposits()
        
        if not deposits:
            await query.edit_message_text("📥 No hay depósitos pendientes.", reply_markup=back_keyboard())
            return
        
        for dep in deposits[:5]:
            text = f"""
📥 *DEPÓSITO PENDIENTE*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 `{dep['ticket']}`
👤 @{dep['username'] or dep['first_name']} (ID: `{dep['user_id']}`)
💰 ${dep['amount']:.2f}
"""
            await query.message.reply_text(
                text,
                reply_markup=admin_deposit_keyboard(dep['ticket']),
                parse_mode="Markdown"
            )
    
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
    
    elif data.startswith("approve_dep_"):
        if not is_admin(user_id):
            return
        
        ticket = data.replace("approve_dep_", "")
        deposit = approve_deposit(ticket, user_id)
        
        if deposit:
            await query.edit_message_text(f"✅ Depósito {ticket} aprobado.")
            
            user_dep = get_user(deposit['user_id'])
            try:
                await context.bot.send_message(
                    chat_id=deposit['user_id'],
                    text=deposit_approved_message(user_dep, user_dep['referral_code']),
                    reply_markup=after_deposit_keyboard(),
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Error: {e}")
            
            if user_dep['referrer_id']:
                referrer = get_user(user_dep['referrer_id'])
                if referrer and referrer['has_deposited']:
                    bonus = check_bonuses(referrer['id'])
                    referrer = get_user(referrer['id'])
                    
                    try:
                        await context.bot.send_message(
                            chat_id=referrer['id'],
                            text=referral_deposited_notification(
                                user_dep['username'] or user_dep['first_name'],
                                REFERRAL_COMMISSION,
                                referrer['balance'],
                                referrer['total_active']
                            ),
                            parse_mode="Markdown"
                        )
                        
                        if bonus:
                            await context.bot.send_message(
                                chat_id=referrer['id'],
                                text=bonus_unlocked_message(bonus[0], bonus[1], referrer),
                                parse_mode="Markdown"
                            )
                    except Exception as e:
                        print(f"Error: {e}")
    
    elif data.startswith("reject_dep_"):
        if not is_admin(user_id):
            return
        
        ticket = data.replace("reject_dep_", "")
        reject_deposit(ticket, user_id)
        await query.edit_message_text(f"❌ Depósito {ticket} rechazado.")
    
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


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        return
    
    if context.user_data.get('awaiting_proof'):
        ticket = f"DEP-{random.randint(100000, 999999)}"
        create_deposit(user_id, ENTRY_PRICE, ticket)
        
        await update.message.reply_text(
            proof_received_message(ticket),
            reply_markup=back_keyboard(),
            parse_mode="Markdown"
        )
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"""
🔔 *NUEVO DEPÓSITO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 `{ticket}`
👤 @{user['username'] or user['first_name']}
🆔 ID: `{user_id}`
💰 ${ENTRY_PRICE:.2f}
""",
                reply_markup=admin_deposit_keyboard(ticket),
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error: {e}")
        
        context.user_data['awaiting_proof'] = False


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    text = update.message.text.strip()
    
    if not user:
        return
    
    # ============ VINCULAR WALLET ============
    if context.user_data.get('awaiting_user_wallet'):
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
            f"✅ *WALLET VINCULADA*\n\n"
            f"`{wallet}`\n\n"
            f"Ahora envía ${ENTRY_PRICE:.0f} USDT desde esta wallet.\n\n"
            f"El depósito se detectará automáticamente.",
            parse_mode="Markdown"
        )
        
        context.user_data['awaiting_user_wallet'] = False
        return
    
    # ============ RETIRO CON WALLET ============
    if context.user_data.get('awaiting_wallet'):
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
        
        context.user_data['awaiting_wallet'] = False
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
            context.user_data['awaiting_wallet'] = True
            
            await update.message.reply_text(
                wallet_request_message(amount),
                parse_mode="Markdown"
            )
        
        except ValueError:
            await update.message.reply_text("❌ Envía un número válido.")
        
        return
