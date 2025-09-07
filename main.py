import os
import sys
import argparse
import logging
from datetime import datetime
from dotenv import load_dotenv
import discord
from discord.ext import commands

from bot import ChatBot

# Setup logging
def setup_logging(log_level="INFO", log_file="logs/bot.log"):
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/bot.log")

# Setup logging
logger = setup_logging(LOG_LEVEL, LOG_FILE)

def run_cli():
    """Run chatbot in CLI mode"""
    chatbot = ChatBot()
    print("FestPal Bot CLI - Ketik 'quit' untuk keluar\n")
    logger.info("FestPal Bot CLI started")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Bot: Sampai jumpa! 🎶")
                logger.info("CLI session ended by user")
                break
            
            if not user_input:
                continue
                
            logger.info(f"CLI user query: '{user_input}'")
            response = chatbot.reply(user_input)
            print(f"Bot: {response}\n")
            logger.info(f"CLI bot response provided")
            
        except KeyboardInterrupt:
            print("\n\nBot: Sampai jumpa! 🎶")
            logger.info("CLI session ended by keyboard interrupt")
            break
        except Exception as e:
            print(f"Error: {e}")
            logger.error(f"CLI error: {e}")

def run_discord_bot():
    """Run Discord bot"""
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN not found in environment variables")
        print("Error: DISCORD_TOKEN tidak ditemukan di file .env")
        print("Buat file .env dan isi dengan token Discord bot Anda.")
        return
    
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
    chatbot = ChatBot()
    
    @bot.event
    async def on_ready():
        logger.info(f"Discord bot logged in as {bot.user} (id: {bot.user.id})")
        print(f"Logged in as {bot.user} (id: {bot.user.id})")
    
    @bot.event
    async def on_message(message: discord.Message):
        if message.author == bot.user:
            return
        
        await bot.process_commands(message)
        if message.content.startswith("!"):
            return
        
        logger.info(f"Discord message from {message.author}: '{message.content}'")
        reply = chatbot.reply(message.content)
        await message.channel.send(reply)
        logger.info("Discord response sent")
    
    @bot.event
    async def on_error(event, *args, **kwargs):
        logger.error(f"Discord bot error in {event}: {args}")
    
    try:
        logger.info("Starting Discord bot...")
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        logger.error("Invalid Discord token")
        print("Error: Token Discord tidak valid")
    except Exception as e:
        logger.error(f"Discord bot error: {e}")
        print(f"Error starting Discord bot: {e}")

def main():
    parser = argparse.ArgumentParser(description="FestPal Bot - Festival chatbot")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--discord", action="store_true", help="Run Discord bot (default)")
    parser.add_argument("--log-level", default=LOG_LEVEL, 
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       help="Set logging level")
    
    args = parser.parse_args()
    
    if args.log_level != LOG_LEVEL:
        logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))
    
    logger.info(f"FestPal Bot starting - Mode: {'CLI' if args.cli else 'Discord'}")
    
    if args.cli:
        run_cli()
    else:
        run_discord_bot()

if __name__ == "__main__":
    main()
