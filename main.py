"""
5DOLLARS BOT - Punto de entrada
"""
import asyncio
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters
)
from config import BOT_TOKEN
from database import init_db
from handlers import (
    start, menu_command, admin_command,
    button_handler, handle_text
)
from admin import (
    broadcast_command, ban_command, unban_command,
    user_info_command, export_db_command,
    give_premium_command, remove_premium_command,
    add_balance_command, stats_command
)
from monitor import monitor_deposits


async def post_init(app):
    """Inicia el monitor después del arranque"""
    asyncio.create_task(monitor_deposits(app.bot))
    print("👁️ Monitor de depósitos ACTIVADO")


def main():
    """Función principal"""
    print("🚀 Iniciando 5DOLLARS BOT...")
    
    # Inicializar base de datos
    init_db()
    
    # Crear aplicación
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    # ============ COMANDOS ============
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("ban", ban_command))
    app.add_handler(CommandHandler("unban", unban_command))
    app.add_handler(CommandHandler("userinfo", user_info_command))
    app.add_handler(CommandHandler("exportdb", export_db_command))
    app.add_handler(CommandHandler("givepremium", give_premium_command))
    app.add_handler(CommandHandler("removepremium", remove_premium_command))
    app.add_handler(CommandHandler("addbalance", add_balance_command))
    
    # ============ CALLBACKS ============
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # ============ MENSAJES ============
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("✅ Bot iniciado correctamente")
    print("💎 5DOLLARS está en línea")
    
    # Iniciar polling
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
