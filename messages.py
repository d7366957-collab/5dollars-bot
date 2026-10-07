"""
Textos del bot 5DOLLARS
"""
from config import (
    BOT_NAME, ENTRY_PRICE, REFERRAL_COMMISSION,
    REFERRAL_REGISTRATION_FEE, MIN_WITHDRAWAL,
    MIN_WITHDRAWAL_FREE, DEPOSIT_WALLET, BONUSES
)


def welcome_message():
    return f"""
✨ *{BOT_NAME}* ✨

*Deposita ${ENTRY_PRICE:.0f} una vez.*
*Gana para siempre.*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 *PLAN GRATIS*
→ Gana *${REFERRAL_REGISTRATION_FEE:.2f}* por cada amigo
→ Retira desde *${MIN_WITHDRAWAL_FREE:.0f}*
→ Sin invertir nada

💎 *PLAN PREMIUM* — ${ENTRY_PRICE:.0f} único
→ Gana *${REFERRAL_REGISTRATION_FEE:.2f}* por cada amigo
→ + *${REFERRAL_COMMISSION:.2f}* cuando depositan
→ Total: *${REFERRAL_REGISTRATION_FEE + REFERRAL_COMMISSION:.2f}* por activo
→ Retira desde *${MIN_WITHDRAWAL:.0f}*
→ Bonos hasta *$500*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 *Tu link. Tu red. Tus ganancias.*

*El momento es ahora.*
"""


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

1️⃣ Depositas ${ENTRY_PRICE:.0f} USDT
2️⃣ Acceso premium de por vida
3️⃣ Cada amigo que entra → *+${REFERRAL_REGISTRATION_FEE:.2f}*
4️⃣ Si ese amigo deposita → *+${REFERRAL_COMMISSION:.2f}*
5️⃣ Total por activo: *${REFERRAL_REGISTRATION_FEE + REFERRAL_COMMISSION:.2f}*
6️⃣ Bonos hasta $500
7️⃣ Retiras desde *${MIN_WITHDRAWAL:.0f}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 *Ejemplo Premium:*

Si 10 amigos entran:
→ 10 × ${REFERRAL_REGISTRATION_FEE:.2f} = *${10 * REFERRAL_REGISTRATION_FEE:.2f}*

Si 5 de ellos depositan:
→ 5 × ${REFERRAL_COMMISSION:.2f} = *${5 * REFERRAL_COMMISSION:.2f}*

*TOTAL: ${10 * REFERRAL_REGISTRATION_FEE + 5 * REFERRAL_COMMISSION:.2f}* 🔥

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Comparte. Crece. Gana.*
"""


def deposit_message():
    return f"""
🚀 *ACTIVA TU PREMIUM*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💎 *${ENTRY_PRICE:.0f} USDT = Acceso de por vida*

✅ *${REFERRAL_REGISTRATION_FEE:.2f}* por cada amigo que entra
✅ *${REFERRAL_COMMISSION:.2f}* por cada amigo que deposita
✅ Total: *${REFERRAL_REGISTRATION_FEE + REFERRAL_COMMISSION:.2f}* por activo
✅ Bonos hasta *$500*
✅ Retiros desde *${MIN_WITHDRAWAL:.0f}*
✅ Soporte prioritario

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🪙 *Red:* BEP20
💵 *Monto:* ${ENTRY_PRICE:.0f} USDT

📋 *Dirección:*
`{DEPOSIT_WALLET}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ *Envía exactamente ${ENTRY_PRICE:.0f}*
*Solo USDT en red BEP20*

*Después envía la captura.*
"""


def send_proof_message():
    return f"""
📸 *ENVÍA TU CAPTURA*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Que muestre:
✅ Monto: ${ENTRY_PRICE:.0f} USDT
✅ Red: BEP20
✅ Fecha reciente

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Tu futuro empieza aquí.*
"""


def proof_received_message(ticket):
    return f"""
✅ *RECIBIDO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 `{ticket}`
⏱️ En revisión
⏰ Menos de 24h

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Estás a un paso.*
"""


def deposit_approved_message(user, referral_code):
    return f"""
✨ *BIENVENIDO AL PREMIUM*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Acceso premium activado
🎯 Listo para crecer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 *TU LINK ÚNICO:*

`t.me/TuBot?start={referral_code}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💸 *TUS COMISIONES:*

👥 Si entra con tu link → *+${REFERRAL_REGISTRATION_FEE:.2f}*
💰 Si deposita ${ENTRY_PRICE:.0f} → *+${REFERRAL_COMMISSION:.2f}*

*TOTAL por activo: ${REFERRAL_REGISTRATION_FEE + REFERRAL_COMMISSION:.2f}* 🔥

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 *Bonos:*
10 activos → $10
50 activos → $25
100 activos → $50

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Comparte. Crece. Gana.*
"""


def main_menu_message(user):
    plan = "💎 PREMIUM" if user['has_deposited'] else "🎁 GRATIS"
    
    if user['has_deposited']:
        comision_texto = f"${REFERRAL_REGISTRATION_FEE + REFERRAL_COMMISSION:.2f} por activo"
        min_w = MIN_WITHDRAWAL
    else:
        comision_texto = f"${REFERRAL_REGISTRATION_FEE:.2f} por referido"
        min_w = MIN_WITHDRAWAL_FREE
    
    progress = int((user['total_active'] / 10) * 100) if user['total_active'] < 10 else 100
    bar_length = 10
    filled = int((progress / 100) * bar_length)
    bar = "▓" * filled + "░" * (bar_length - filled)
    
    return f"""
💰 *{BOT_NAME}*

👤 @{user['username'] or 'usuario'}
{plan}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💵 *Saldo:* ${user['balance']:.2f}
📈 *Ganado:* ${user['total_earned']:.2f}
💸 *Comisión:* {comision_texto}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 Registrados: *{user['total_registered']}*
✅ Activos: *{user['total_active']}*
⏳ Pendientes: *{user['total_pending']}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 *BONO $10* ({user['total_active']}/10)
{bar} {progress}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 *Tu red crece. Tú creces.*
"""


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
✅ Activos: *{user['total_active']}*
⏳ Pendientes: *{user['total_pending']}*

💰 Ganado: *${user['total_earned']:.2f}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 *Comparte en grupos.*
*Cada persona es una oportunidad.*
"""


def my_referrals_message(user, referrals):
    active = [r for r in referrals if r['has_deposited']]
    pending = [r for r in referrals if not r['has_deposited']]
    
    text = f"""
👥 *TUS REFERIDOS*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 Registrados: *{len(referrals)}*
✅ Activos: *{len(active)}*
⏳ Pendientes: *{len(pending)}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    if active:
        text += "\n✅ *ACTIVOS*\n\n"
        for i, ref in enumerate(active[:10], 1):
            comision = REFERRAL_COMMISSION if user['has_deposited'] else 0
            text += f"{i}. @{ref['username'] or 'usuario'}  *+${comision:.2f}*\n"
        
        if len(active) > 10:
            text += f"\n_...y {len(active) - 10} más_\n"
    
    if pending:
        text += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        text += "\n⏳ *PENDIENTES*\n\n"
        for i, ref in enumerate(pending[:10], len(active) + 1):
            text += f"{i}. @{ref['username'] or 'usuario'}  *+${REFERRAL_REGISTRATION_FEE:.2f}*\n"
        
        if len(pending) > 10:
            text += f"\n_...y {len(pending) - 10} más_\n"
    
    text += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 *Recuérdales que depositen.*
*Cada activo es ganancia.*
"""
    return text


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
⏳ *AÚN NO PUEDES RETIRAR*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{plan}

💵 Saldo: *${user['balance']:.2f}* / ${min_withdrawal:.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Te falta *${falta:.2f}*
"""
        
        if not user['has_deposited']:
            text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 *¿QUIERES RETIRAR DESDE ${MIN_WITHDRAWAL:.0f}?*

Activa PREMIUM por ${ENTRY_PRICE:.0f}:

✅ ${REFERRAL_COMMISSION:.2f} por referido activo
✅ Mínimo retiro: ${MIN_WITHDRAWAL:.0f}
✅ Bonos hasta $500
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

✅ *Listo para retirar*

*Tu esfuerzo, recompensado.*
"""


def wallet_request_message(amount):
    return f"""
📝 *TU WALLET BEP20*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 Monto: *${amount:.2f}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Envía tu dirección USDT BEP20:

⚠️ Debe empezar con `0x`
⚠️ Verifica que sea BEP20

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Un paso más.*
"""


def withdrawal_created_message(ticket, amount, wallet):
    return f"""
✅ *SOLICITUD ENVIADA*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 `{ticket}`
💰 *${amount:.2f}*
📍 `{wallet[:10]}...{wallet[-6:]}`
⏱️ Pendiente
⏰ Menos de 24h

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Tu dinero está en camino.*
"""


def bonuses_message(user):
    if not user['has_deposited']:
        return f"""
🔒 *BONOS BLOQUEADOS*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Los bonos son exclusivos del *PLAN PREMIUM*.

🚀 *Activa PREMIUM por ${ENTRY_PRICE:.0f}* y desbloquea:

🎁 $10 al llegar a 10 activos
🎁 $25 al llegar a 50 activos
🎁 $50 al llegar a 100 activos
🎁 $250 al llegar a 500 activos
🎁 $500 al llegar a 1,000 activos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Total en bonos: $835*
"""
    
    text = f"""
🎁 *TUS BONOS*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    for required, amount in sorted(BONUSES.items()):
        active = user['total_active']
        unlocked = active >= required
        progress = min(100, int((active / required) * 100))
        
        status = "✅" if unlocked else "🔒"
        filled = progress // 10
        bar = "▓" * filled + "░" * (10 - filled)
        
        text += f"{status} *${amount:.0f}* — {required} activos\n"
        text += f"   {bar} {active}/{required}\n\n"
    
    text += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 *Ganado en bonos:* ${user['total_bonuses']:.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Cada referido te acerca.*
"""
    return text


def bonus_unlocked_message(required, amount, user):
    return f"""
🎉 *BONO DESBLOQUEADO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 *+${amount:.2f}*

✅ Llegaste a *{required} activos*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💵 Nuevo saldo: *${user['balance']:.2f}*
👥 Activos: *{user['total_active']}*
🎁 Bonos: *${user['total_bonuses']:.2f}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 *Esto es solo el comienzo.*
"""


def ranking_message(ranking, user_id):
    text = """
🏆 *RANKING PREMIUM*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    medals = ["🥇", "🥈", "🥉"]
    
    for i, user in enumerate(ranking[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        username = user['username'] or f"user{user['id']}"
        marker = " ← *tú*" if user['id'] == user_id else ""
        text += f"{medal} @{username}  *${user['total_earned']:.2f}*{marker}\n"
    
    text += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 *Premios semanales:*
🥇 $50  |  🥈 $25  |  🥉 $10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*¿Quieres estar arriba?*
*Comparte más.*
"""
    return text


def help_message():
    return f"""
📞 *AYUDA*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎁 *PLAN GRATIS*
→ ${REFERRAL_REGISTRATION_FEE:.2f} por amigo
→ Retira desde ${MIN_WITHDRAWAL_FREE:.0f}

💎 *PLAN PREMIUM*
→ ${REFERRAL_REGISTRATION_FEE:.2f} por amigo
→ +${REFERRAL_COMMISSION:.2f} si deposita
→ Retira desde ${MIN_WITHDRAWAL:.0f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ *Preguntas frecuentes*

💵 *¿Cuándo pagan?*
→ Menos de 24h

🪙 *¿Qué red?*
→ BEP20 (BSC)

⏳ *¿Por qué no gano $3.75?*
→ Solo premium gana esa comisión

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 *Soporte:* @TuSoporte

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Estamos para ayudarte.*
"""


def new_referral_notification(username, referrer_has_deposit=False):
    if referrer_has_deposit:
        return f"""
👥 *NUEVO REGISTRADO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@{username} entró con tu link.

✅ *+${REFERRAL_REGISTRATION_FEE:.2f}* acreditados
⏳ *Pendiente de depósito*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 *Si deposita ${ENTRY_PRICE:.0f}:*
*Ganas +${REFERRAL_COMMISSION:.2f}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Cada pendiente es una oportunidad.*
"""
    else:
        return f"""
👥 *NUEVO REGISTRADO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@{username} entró con tu link.

✅ *+${REFERRAL_REGISTRATION_FEE:.2f}* acreditados

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 *Activa PREMIUM y gana*
*${REFERRAL_COMMISSION:.2f} por cada depósito.*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Cada pendiente es una oportunidad.*
"""


def referral_deposited_notification(username, amount, balance, active):
    return f"""
💰 *+${amount:.2f}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ @{username} depositó

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💵 Saldo: *${balance:.2f}*
✅ Activos: *{active}*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Tu red crece.*
*Sigue así.*
"""


def withdrawal_paid_notification(ticket, amount, wallet):
    return f"""
✨ *PAGADO*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆔 `{ticket}`
💰 *${amount:.2f}*
📍 `{wallet[:10]}...{wallet[-6:]}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*Tu dinero está en tu wallet.*

*Comparte y sigue creciendo.*
"""
