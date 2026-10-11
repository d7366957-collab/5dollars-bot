"""
Monitor de depósitos automáticos
"""
import asyncio
from blockchain import check_new_deposits, get_tx_url
from database import (
    get_user_by_wallet, create_auto_deposit,
    approve_deposit, get_user, give_premium
)
from config import (
    ADMIN_ID, ENTRY_PRICE, REFERRAL_COMMISSION,
    REFERRAL_REGISTRATION_FEE, MIN_WITHDRAWAL
)
from messages import (
    premium_activated_message,
    referral_premium_notification,
    bonus_unlocked_message
)


async def monitor_deposits(bot):
    """
    Monitorea la blockchain cada 30 segundos
    Detecta depósitos y activa premium automáticamente
    """
    print("👁️ Monitor de depósitos iniciado")
    
    while True:
        try:
            new_deposits = check_new_deposits()
            
            for deposit in new_deposits:
                tx_hash = deposit['tx_hash']
                wallet = deposit['from']
                amount = deposit['amount']
                
                print(f"💰 Nuevo depósito: ${amount} de {wallet}")
                print(f"🔗 TX: {tx_hash}")
                
                # Buscar usuario por wallet
                user = get_user_by_wallet(wallet)
                
                if not user:
                    print(f"⚠️ Wallet no vinculada: {wallet}")
                    # Notificar al admin para que lo gestione
                    try:
                        await bot.send_message(
                            chat_id=ADMIN_ID,
                            text=f"""
⚠️ *DEPÓSITO SIN USUARIO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 Monto: ${amount:.2f}
📍 Wallet: `{wallet}`
🔗 TX: `{tx_hash[:20]}...`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_Esta wallet no está vinculada a ningún usuario._
_Verifica manualmente._
""",
                            parse_mode="Markdown"
                        )
                    except Exception as e:
                        print(f"Error notificando admin: {e}")
                    continue
                
                # Si ya es premium, ignorar
                if user['has_deposited']:
                    print(f"⚠️ Usuario ya es premium: {user['id']}")
                    continue
                
                # Crear depósito automático
                ticket = create_auto_deposit(user['id'], amount, tx_hash)
                
                if not ticket:
                    print(f"⚠️ Depósito ya procesado: {tx_hash}")
                    continue
                
                # Dar premium (procesa comisión al referidor)
                give_premium(user['id'])
                
                # Recargar usuario actualizado
                user = get_user(user['id'])
                
                # Notificar al usuario
                try:
                    await bot.send_message(
                        chat_id=user['id'],
                        text=premium_activated_message(user['referral_code']),
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    print(f"Error notificando usuario: {e}")
                
                # Notificar al admin
                try:
                    await bot.send_message(
                        chat_id=ADMIN_ID,
                        text=f"""
💰 *DEPÓSITO DETECTADO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 @{user['username'] or user['first_name']}
🆔 ID: `{user['id']}`
💰 Monto: ${amount:.2f}
🔗 TX: `{tx_hash[:20]}...`
✅ Estado: Premium activado
""",
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    print(f"Error notificando admin: {e}")
                
                # Procesar referidor
                if user['referrer_id']:
                    referrer = get_user(user['referrer_id'])
                    
                    if referrer and referrer['has_deposited']:
                        # Recargar referidor actualizado
                        referrer = get_user(referrer['id'])
                        
                        try:
                            await bot.send_message(
                                chat_id=referrer['id'],
                                text=referral_premium_notification(
                                    user['username'] or user['first_name'],
                                    REFERRAL_COMMISSION,
                                    referrer['balance'],
                                    referrer['total_premium']
                                ),
                                parse_mode="Markdown"
                            )
                            
                            # Verificar si desbloqueó bono
                            from database import check_bonuses
                            bonus = check_bonuses(referrer['id'])
                            
                            if bonus:
                                referrer_actualizado = get_user(referrer['id'])
                                await bot.send_message(
                                    chat_id=referrer['id'],
                                    text=bonus_unlocked_message(
                                        bonus[0],
                                        bonus[1],
                                        referrer_actualizado
                                    ),
                                    parse_mode="Markdown"
                                )
                                
                                # Notificar al admin del bono
                                try:
                                    await bot.send_message(
                                        chat_id=ADMIN_ID,
                                        text=f"""
🎁 *BONO OTORGADO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 @{referrer['username'] or referrer['first_name']}
🆔 ID: `{referrer['id']}`
🎁 Bono: ${bonus[1]:.2f}
💎 Premium alcanzados: {bonus[0]}
""",
                                        parse_mode="Markdown"
                                    )
                                except Exception as e:
                                    print(f"Error notificando admin: {e}")
                        
                        except Exception as e:
                            print(f"Error notificando referidor: {e}")
                
                print(f"✅ Premium activado: {user['id']}")
        
        except Exception as e:
            print(f"❌ Error monitor: {e}")
        
        # Esperar 30 segundos
        await asyncio.sleep(30)
