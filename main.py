"""
5DOLLARS BOT - Punto de entrada
"""
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters
)
from config import BOT_TOKEN
from database import init_db
from handlers import (
    start, menu_command, admin_command,
    button_handler, handle_photo, handle_text
)
from admin import (
    broadcast_command, ban_command, user_info_command,
    export_db_command
)


def main():
    print("🚀 Iniciando 5DOLLARS BOT...")
    
    init_db()
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("ban", ban_command))
    app.add_handler(CommandHandler("userinfo", user_info_command))
    app.add_handler(CommandHandler("exportdb", export_db_command))
    
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("✅ Bot iniciado correctamente")
    print("💎 5DOLLARS está en línea")
    
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
