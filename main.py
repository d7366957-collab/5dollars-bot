"""
5DOLLARS BOT - Punto de entrada
"""
import asyncio
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters
)
from config import BOT_TOKEN, BSCSCAN_API_KEY
from database import init_db
from handlers import (
    start, menu_command, admin_command,
    button_handler, handle_photo, handle_text
)
from admin import (
    broadcast_command, ban_command, user_info_command,
    export_db_command
)
from monitor import monitor_deposits


async def post_init(app):
    """Inicia el monitor después del arranque"""
    if BSCSCAN_API_KEY:
        asyncio.create_task(monitor_deposits(app.bot))
        print("👁️ Monitor de depósitos automáticos ACTIVADO")
    else:
        print("⚠️ Monitor de depósitos DESACTIVADO (falta BSCSCAN_API_KEY)")


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
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("ban", ban_command))
    app.add_handler(CommandHandler("userinfo", user_info_command))
    app.add_handler(CommandHandler("exportdb", export_db_command))
    
    # ============ CALLBACKS ============
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # ============ MENSAJES ============
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("✅ Bot iniciado correctamente")
    print("💎 5DOLLARS está en línea")
    
    # Iniciar polling
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
