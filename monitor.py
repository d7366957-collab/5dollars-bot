"""
Monitor de depósitos automáticos
"""
import asyncio
from blockchain import check_new_deposits
from database import (
    get_user_by_wallet, create_auto_deposit,
    approve_deposit, get_user, process_referral_commission,
    check_bonuses
)
from config import ADMIN_ID, ENTRY_PRICE, REFERRAL_COMMISSION


async def monitor_deposits(bot):
    """Monitorea la blockchain cada 30 segundos"""
    print("👁️ Monitor de depósitos iniciado")
    
    while True:
        try:
            new_deposits = check_new_deposits()
            
            for deposit in new_deposits:
                tx_hash = deposit['tx_hash']
                wallet = deposit['from']
                amount = deposit['amount']
                
                print(f"💰 Nuevo depósito: ${amount} de {wallet}")
                
                # Buscar usuario por wallet
                user = get_user_by_wallet(wallet)
                
                if not user:
                    print(f"⚠️ Wallet no vinculada: {wallet}")
                    continue
                
                # Crear depósito
                ticket = create_auto_deposit(user['id'], amount, tx_hash)
                
                if not ticket:
                    print(f"⚠️ Ya procesado: {tx_hash}")
                    continue
                
                # Aprobar automáticamente
                approve_deposit(ticket, ADMIN_ID)
                
                # Notificar al usuario
                try:
                    await bot.send_message(
                        chat_id=user['id'],
                        text=f"""
✨ *DEPÓSITO DETECTADO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 Monto: ${amount:.2f}
🔗 TX: `{tx_hash[:20]}...`
✅ Estado: *APROBADO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 *Acceso premium activado*

🔗 Comparte tu link y empieza a ganar.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    print(f"Error notificando: {e}")
                
                # Procesar referidor
                referrer = process_referral_commission(user['id'])
                
                # Notificar al referidor
                if referrer and referrer['has_deposited']:
                    try:
                        referrer_actual = get_user(referrer['id'])
                        bonus = check_bonuses(referrer['id'])
                        
                        await bot.send_message(
                            chat_id=referrer['id'],
                            text=f"""
💰 *+${REFERRAL_COMMISSION:.2f}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ @{user['username'] or user['first_name']} depositó

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💵 Saldo: *${referrer_actual['balance']:.2f}*
✅ Activos: *{referrer_actual['total_active']}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Tu red crece.*
*Sigue así.*
""",
                            parse_mode="Markdown"
                        )
                        
                        # Notificar bono si desbloqueó
                        if bonus:
                            referrer_bonus = get_user(referrer['id'])
                            await bot.send_message(
                                chat_id=referrer['id'],
                                text=f"""
🎉 *BONO DESBLOQUEADO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 *+${bonus[1]:.2f}*

✅ Llegaste a *{bonus[0]} activos*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💵 Nuevo saldo: *${referrer_bonus['balance']:.2f}*
👥 Activos: *{referrer_bonus['total_active']}*
🎁 Bonos: *${referrer_bonus['total_bonuses']:.2f}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 *Esto es solo el comienzo.*
""",
                                parse_mode="Markdown"
                            )
                    except Exception as e:
                        print(f"Error notificando referidor: {e}")
                
                # Notificar al admin
                try:
                    await bot.send_message(
                        chat_id=ADMIN_ID,
                        text=f"""
💰 *DEPÓSITO AUTOMÁTICO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 @{user['username'] or user['first_name']}
🆔 ID: `{user['id']}`
💰 Monto: ${amount:.2f}
🔗 TX: `{tx_hash[:20]}...`
✅ Estado: Aprobado
""",
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    print(f"Error notificando admin: {e}")
                
                print(f"✅ Depósito procesado: {ticket}")
        
        except Exception as e:
            print(f"❌ Error monitor: {e}")
        
        # Esperar 30 segundos
        await asyncio.sleep(30)
