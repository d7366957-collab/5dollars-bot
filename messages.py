"""
Textos del bot 5DOLLARS
"""
from config import (
    BOT_NAME, ENTRY_PRICE, REFERRAL_COMMISSION,
    REFERRAL_REGISTRATION_FEE, MIN_WITHDRAWAL,
    MIN_WITHDRAWAL_FREE, DEPOSIT_WALLET, BONUSES
)


# ============ BIENVENIDA ============

def welcome_message():
    return f"""
✨ *{BOT_NAME}* ✨

*Deposita ${ENTRY_PRICE:.0f} una vez.*
*Gana para siempre.*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 *PLAN GRATIS*
→ Gana *${REFERRAL_REGISTRATION_FEE:.2f}* por cada amigo
→ Retira desde *${MIN_WITHDRAWAL_FREE:.0f}*

💎 *PLAN PREMIUM* — ${ENTRY_PRICE:.0f} único
→ Gana *${REFERRAL_REGISTRATION_FEE:.2f}* por cada amigo
→ + *${REFERRAL_COMMISSION:.2f}* por referido premium
→ Retira desde *${MIN_WITHDRAWAL:.0f}*
→ Bonos hasta *$190*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 *Tu link. Tu red. Tus ganancias.*

*El momento es ahora.*
"""


# ============ CÓMO FUNCIONA ============

def how_it_works_message():
    return f"""
📖 *ASÍ FUNCIONA*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 *PLAN GRATIS*

1️⃣ Entras sin pagar nada
2️⃣ Recibes tu link único
3️⃣ Cada amigo que entra → *+${REFERRAL_REGISTRATION_FEE:.2f}*
4️⃣ Retiras desde *${MIN_WITHDRAWAL_FREE:.0f}*

💎 *PLAN PREMIUM* — ${ENTRY_PRICE:.0f} único

1️⃣ Depositas ${ENTRY_PRICE:.0f} USDT (BEP20)
2️⃣ Acceso premium de por vida
3️⃣ Cada amigo que entra → *+${REFERRAL_REGISTRATION_FEE:.2f}*
4️⃣ Cada referido premium → *+${REFERRAL_COMMISSION:.2f}*
5️⃣ Bonos hasta *$190*
6️⃣ Retiras desde *${MIN_WITHDRAWAL:.0f}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 *Ejemplo Premium:*

Si 10 amigos entran:
→ 10 × ${REFERRAL_REGISTRATION_FEE:.2f} = *${10 * REFERRAL_REGISTRATION_FEE:.2f}*

Si 5 adquieren premium:
→ 5 × ${REFERRAL_COMMISSION:.2f} = *${5 * REFERRAL_COMMISSION:.2f}*

*TOTAL: ${10 * REFERRAL_REGISTRATION_FEE + 5 * REFERRAL_COMMISSION:.2f}* 🔥

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Comparte. Crece. Gana.*
"""


# ============ DEPÓSITO ============

def deposit_message():
    return f"""
🚀 *ACTIVA TU PREMIUM*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💎 *${ENTRY_PRICE:.0f} USDT = Acceso de por vida*

✅ *${REFERRAL_REGISTRATION_FEE:.2f}* por cada amigo que entra
✅ *${REFERRAL_COMMISSION:.2f}* por cada referido premium
✅ Bonos hasta *$190*
✅ Retiros desde *${MIN_WITHDRAWAL:.0f}*
✅ Soporte prioritario

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🪙 *Red:* BEP20
💵 *Monto:* ${ENTRY_PRICE:.0f} USDT

📋 *Dirección:*
`{DEPOSIT_WALLET}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ *Pasos:*
1️⃣ Vincula tu wallet
2️⃣ Envía ${ENTRY_PRICE:.0f} USDT
3️⃣ Espera 30 segundos

*Envía exactamente ${ENTRY_PRICE:.0f}*
*Solo USDT en red BEP20*
"""


# ============ VINCULAR WALLET ============

def wallet_setup_message():
    return f"""
🔗 *VINCULA TU WALLET*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Envía tu dirección USDT BEP20:

⚠️ Debe empezar con `0x`
⚠️ Es la wallet desde donde
   enviarás los ${ENTRY_PRICE:.0f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *Los depósitos se detectarán*
*automáticamente.*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 *Ejemplo:*
`0x742d35Cc6634C0532925a3b8...`
"""


def wallet_linked_message(wallet):
    wallet_short = f"{wallet[:10]}...{wallet[-6:]}"
    return f"""
✅ *WALLET VINCULADA*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 *Tu wallet:*
`{wallet_short}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 *AHORA ENVÍA ${ENTRY_PRICE:.0f} USDT*

📋 A esta dirección:
`{DEPOSIT_WALLET}`

🪙 Red: BEP20
💵 Monto: ${ENTRY_PRICE:.0f} USDT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️ El sistema detectará el depósito
automáticamente en 30 segundos.

🔔 Recibirás una notificación
cuando se active tu premium.
"""


# ============ PREMIUM ACTIVADO ============

def premium_activated_message(referral_code):
    return f"""
✨ *PLAN PREMIUM ACTIVADO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 *Bienvenido al plan premium*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💎 *TUS BENEFICIOS:*

→ ${REFERRAL_REGISTRATION_FEE:.2f} por cada amigo que entra
→ ${REFERRAL_COMMISSION:.2f} por cada referido premium
→ Bonos hasta $190
→ Retira desde ${MIN_WITHDRAWAL:.0f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 *TU LINK ÚNICO:*

`t.me/TuBot?start={referral_code}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💸 *Comparte y empieza a ganar*

*El momento es ahora.*
"""


# ============ MENÚ PRINCIPAL ============

def main_menu_message(user):
    plan = "💎 PREMIUM" if user['has_deposited'] else "🎁 GRATIS"
    
    if user['has_deposited']:
        comision_texto = f"${REFERRAL_COMMISSION:.2f} por ref. premium"
    else:
        comision_texto = f"${REFERRAL_REGISTRATION_FEE:.2f} por referido"
    
    # Barra de progreso para bono de 10
    progress = int((user['total_premium'] / 10) * 100) if user['total_premium'] < 10 else 100
    filled = int((progress / 100) * 10)
    bar = "▓" * filled + "░" * (10 - filled)
    
    return f"""
💰 *{BOT_NAME}*

👤 @{user['username'] or 'usuario'}
{plan}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💵 *Saldo:* ${user['balance']:.2f}
📈 *Ganado:* ${user['total_earned']:.2f}
💸 *Comisión:* {comision_texto}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 Referidos: *{user['total_registered']}*
✅ Premium: *{user['total_premium']}*
⏳ Pendientes: *{user['total_pending']}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 *BONO $10* ({user['total_premium']}/10)
{bar} {progress}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 *Tu red crece. Tú creces.*
"""


# ============ MI LINK ============

def my_link_message(user, bot_username):
    link = f"https://t.me/{bot_username}?start={user['referral_code']}"
    plan = "💎 PREMIUM" if user['has_deposited'] else "🎁 GRATIS"
    
    return f"""
🔗 *TU LINK*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

`{link}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{plan}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 Registrados: *{user['total_registered']}*
✅ Premium: *{user['total_premium']}*
⏳ Pendientes: *{user['total_pending']}*

💰 Ganado: *${user['total_earned']:.2f}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 *Comparte en grupos.*
*Cada persona es una oportunidad.*
"""


# ============ MIS REFERIDOS ============

def my_referrals_message(user, referrals):
    premium = [r for r in referrals if r['has_deposited']]
    gratis = [r for r in referrals if not r['has_deposited']]
    
    text = f"""
👥 *TUS REFERIDOS*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 *RESUMEN:*
👥 Registrados: *{len(referrals)}*
✅ Premium: *{len(premium)}*
⏳ Gratis: *{len(gratis)}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    if premium:
        text += "\n💎 *REFERIDOS PREMIUM*\n\n"
        for i, ref in enumerate(premium[:10], 1):
            text += f"{i}. @{ref['username'] or 'usuario'}  *+${REFERRAL_COMMISSION:.2f}*\n"
        
        if len(premium) > 10:
            text += f"\n_...y {len(premium) - 10} más_\n"
    
    if gratis:
        text += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        text += "\n🎁 *REFERIDOS GRATIS*\n\n"
        for i, ref in enumerate(gratis[:10], len(premium) + 1):
            text += f"{i}. @{ref['username'] or 'usuario'}\n"
        
        if len(gratis) > 10:
            text += f"\n_...y {len(gratis) - 10} más_\n"
    
    if not referrals:
        text += "\n_(ninguno aún)_\n"
    
    text += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 *Comparte tu link para crecer.*
"""
    return text


# ============ RETIRO ============

def withdraw_message(user):
    if user['has_deposited']:
        min_withdrawal = MIN_WITHDRAWAL
        plan = "💎 PREMIUM"
    else:
        min_withdrawal = MIN_WITHDRAWAL_FREE
        plan = "🎁 GRATIS"
    
    can_withdraw = user['balance'] >= min_withdrawal
    
    if not can_withdraw:
        falta = max(0, min_withdrawal - user['balance'])
        
        text = f"""
💸 *RETIRAR*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{plan}

💵 Disponible: *${user['balance']:.2f}*
📉 Mínimo: *${min_withdrawal:.2f}*
⚡ Menos de 24h
🪙 BEP20

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏳ *AÚN NO PUEDES RETIRAR*

💡 Te falta *${falta:.2f}*
"""
        
        if not user['has_deposited']:
            text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 *¿QUIERES RETIRAR DESDE ${MIN_WITHDRAWAL:.0f}?*

Activa PREMIUM por ${ENTRY_PRICE:.0f}:

✅ ${REFERRAL_COMMISSION:.2f} por referido premium
✅ Mínimo retiro: ${MIN_WITHDRAWAL:.0f}
✅ Bonos hasta $190
"""
        
        text += "\n*Sigue compartiendo.*\n*Estás cerca.*\n"
        return text
    
    return f"""
💸 *RETIRAR*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{plan}

💵 Disponible: *${user['balance']:.2f}*
📉 Mínimo: *${min_withdrawal:.2f}*
⚡ Menos de 24h
🪙 BEP20

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 *¿Cuánto quieres retirar?*
"""


def wallet_request_message(amount):
    return f"""
📝 *DIRECCIÓN DE RETIRO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 Monto: *${amount:.2f}*
🪙 Red: BEP20

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Envía tu dirección BEP20:

⚠️ Debe empezar con `0x`
⚠️ Verifica que sea BEP20

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Un paso más.*
"""


def withdrawal_created_message(ticket, amount, wallet):
    wallet_short = f"{wallet[:10]}...{wallet[-6:]}"
    return f"""
✅ *SOLICITUD ENVIADA*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 Ticket: `{ticket}`
💰 Monto: *${amount:.2f}*
📍 Wallet: `{wallet_short}`
⏱️ Estado: Pendiente
⏰ Menos de 24h

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Tu dinero está en camino.*
"""


# ============ BONOS ============

def bonuses_message(user):
    if not user['has_deposited']:
        return f"""
🔒 *BONOS BLOQUEADOS*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Los bonos son exclusivos del *PLAN PREMIUM*.

🚀 *Activa PREMIUM por ${ENTRY_PRICE:.0f}* y desbloquea:

🎁 $10 al llegar a 10 premium
🎁 $30 al llegar a 30 premium
🎁 $50 al llegar a 50 premium
🎁 $100 al llegar a 100 premium

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Total en bonos: $190*
"""
    
    text = f"""
🎁 *TUS BONOS*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    for required, amount in sorted(BONUSES.items()):
        premium = user['total_premium']
        unlocked = premium >= required
        progress = min(100, int((premium / required) * 100))
        
        status = "✅" if unlocked else "🔒"
        filled = progress // 10
        bar = "▓" * filled + "░" * (10 - filled)
        
        text += f"{status} *${amount:.0f}* — {required} premium\n"
        text += f"   {bar} {premium}/{required}\n\n"
    
    text += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 *Ganado en bonos:* ${user['total_bonuses']:.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Cada referido premium te acerca.*
"""
    return text


def bonus_unlocked_message(required, amount, user):
    siguiente = None
    for req, amt in sorted(BONUSES.items()):
        if req > required:
            siguiente = (req, amt)
            break
    
    text = f"""
🎉 *BONO DESBLOQUEADO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 *+${amount:.2f}*

✅ Llegaste a *{required} referidos premium*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💵 Nuevo saldo: *${user['balance']:.2f}*
✅ Premium: *{user['total_premium']}*
🎁 Bonos: *${user['total_bonuses']:.2f}*
"""
    
    if siguiente:
        text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 *Siguiente bono:*
${siguiente[1]:.0f} al llegar a {siguiente[0]} premium
"""
    
    text += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 *Esto es solo el comienzo.*
"""
    return text


# ============ RANKING ============

def ranking_message(ranking, user_id):
    text = """
🏆 *RANKING*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    medals = ["🥇", "🥈", "🥉"]
    
    for i, user in enumerate(ranking[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        username = user['username'] or f"user{user['id']}"
        marker = " ← *tú*" if user['id'] == user_id else ""
        text += f"{medal} @{username}  *{user['total_registered']} refs*{marker}\n"
    
    if not ranking:
        text += "_(ninguno aún)_\n"
    
    text += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 *¿Quieres estar arriba?*
*Comparte más.*
"""
    return text


# ============ AYUDA ============

def help_message():
    return f"""
📞 *AYUDA*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 *PLAN GRATIS*
→ ${REFERRAL_REGISTRATION_FEE:.2f} por amigo
→ Retira desde ${MIN_WITHDRAWAL_FREE:.0f}

💎 *PLAN PREMIUM*
→ ${REFERRAL_REGISTRATION_FEE:.2f} por amigo
→ +${REFERRAL_COMMISSION:.2f} por referido premium
→ Retira desde ${MIN_WITHDRAWAL:.0f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ *Preguntas frecuentes*

💵 *¿Cuándo pagan?*
→ Menos de 24h

🪙 *¿Qué red?*
→ BEP20 (BSC)

💰 *¿Cuánto por referido?*
→ ${REFERRAL_REGISTRATION_FEE:.2f} por registro
→ +${REFERRAL_COMMISSION:.2f} si adquiere premium

⏳ *¿Por qué no gano ${REFERRAL_COMMISSION:.2f}?*
→ Solo premium gana esa comisión

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 *Soporte:* @YordanSoporte
⏰ Respuesta en menos de 6h

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Estamos para ayudarte.*
"""


# ============ SOPORTE ============

def support_message():
    return f"""
📞 *SOPORTE*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 *¿Tienes algún problema?*

Si tu depósito no se acreditó:
→ Contacta al soporte
→ Envía tu TX hash
→ Te ayudaremos en menos de 6h

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📩 *Contacto:*
@YordanSoporte

⏰ Respuesta en menos de 6h
"""


# ============ NOTIFICACIONES ============

def new_referral_notification(username):
    return f"""
👥 *+${REFERRAL_REGISTRATION_FEE:.2f}*

@{username} entró con tu link.
"""


def referral_premium_notification(username, amount, balance, premium):
    return f"""
💰 *¡¡¡+${amount:.2f}!!!*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ @{username} adquirió premium

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💵 Saldo: *${balance:.2f}*
💎 Premium: *{premium}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 *Tu red crece.*
"""


def withdrawal_paid_notification(ticket, amount, wallet):
    wallet_short = f"{wallet[:10]}...{wallet[-6:]}"
    return f"""
✨ *PAGADO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 `{ticket}`
💰 *${amount:.2f}*
📍 `{wallet_short}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Tu dinero está en tu wallet.*

*Comparte y sigue creciendo.*
"""
