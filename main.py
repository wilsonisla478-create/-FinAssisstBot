import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# --- Configuration ---
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN set in environment variables")

# For admin-only features (optional)
ADMIN_ID = os.environ.get("BOT_ADMIN_ID")

# --- Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple in-memory user data. For production, use a database like PostgreSQL or MongoDB.
user_data = {}

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message and show the main menu."""
    user_id = update.effective_user.id
    user_data[user_id] = {"balance": 0, "name": update.effective_user.first_name}

    keyboard = [
        [InlineKeyboardButton("💰 Check Balance", callback_data="balance")],
        [InlineKeyboardButton("📈 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("📉 Withdraw", callback_data="withdraw")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        f"Welcome, {update.effective_user.first_name}! 👋\n\n"
        f"I'm your virtual banking assistant.\n"
        f"Use the buttons below to manage your account.\n\n"
        f"⚠️ **This is a simulation. Do not use for real money.**"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the user's current balance."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    bal = user_data.get(user_id, {}).get("balance", 0)
    await query.edit_message_text(f"💰 Your current balance is: ${bal:.2f}")

async def handle_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user for a deposit amount."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📈 Please enter the amount you'd like to deposit.\n(Enter a number, or /cancel)")

    # Set a state to capture the next text message as an amount
    context.user_data['awaiting_amount'] = 'deposit'

async def handle_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user for a withdrawal amount."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📉 Please enter the amount you'd like to withdraw.\n(Enter a number, or /cancel)")

    context.user_data['awaiting_amount'] = 'withdraw'

async def handle_amount_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the amount the user entered after a deposit or withdraw request."""
    user_id = update.effective_user.id
    text = update.message.text.strip()

    try:
        amount = float(text)
        if amount <= 0:
            await update.message.reply_text("❌ Please enter a positive number.")
            return
    except ValueError:
        await update.message.reply_text("❌ Invalid amount. Please enter a number.")
        return

    action = context.user_data.pop('awaiting_amount', None)
    if action == 'deposit':
        user_data[user_id]["balance"] = user_data[user_id].get("balance", 0) + amount
        await update.message.reply_text(f"✅ Successfully deposited ${amount:.2f}. Your new balance is ${user_data[user_id]['balance']:.2f}.")
    elif action == 'withdraw':
        if user_data[user_id].get("balance", 0) >= amount:
            user_data[user_id]["balance"] -= amount
            await update.message.reply_text(f"✅ Withdrew ${amount:.2f}. Your new balance is ${user_data[user_id]['balance']:.2f}.")
        else:
            await update.message.reply_text(f"❌ Insufficient funds. You have ${user_data[user_id]['balance']:.2f}.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current operation."""
    context.user_data.pop('awaiting_amount', None)
    await update.message.reply_text("Cancelled. Send /start to return to the main menu.")

# --- Main Application ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel))

    # Callback query handlers for buttons
    app.add_handler(CallbackQueryHandler(handle_balance, pattern="balance"))
    app.add_handler(CallbackQueryHandler(handle_deposit, pattern="deposit"))
    app.add_handler(CallbackQueryHandler(handle_withdraw, pattern="withdraw"))

    # Message handler to capture numeric input for deposit/withdraw
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount_input))

    logger.info("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
