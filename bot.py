import discord
from discord.ext import commands
import asyncio
import logging
import os
from dotenv import load_dotenv
from views import MessageButtonView
from config import Config
from keep_alive import start_web_server

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('discord_bot')

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(
            command_prefix=Config.COMMAND_PREFIX,
            intents=intents,
            help_command=None
        )
    
    async def setup_hook(self):
        """Called when the bot is starting up"""
        logger.info("Bot is starting up...")
        
        # Add the persistent view for button interactions
        self.add_view(MessageButtonView())
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is in {len(self.guilds)} guilds')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="les alertes et notifications"
            ),
            status=discord.Status.online
        )
    
    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Commande non trouvée. Utilisez `/help` pour voir les commandes disponibles.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Vous n'avez pas les permissions nécessaires pour cette commande.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ Le bot n'a pas les permissions nécessaires pour exécuter cette commande.")
        else:
            logger.error(f"Unexpected error: {error}")
            await ctx.send("❌ Une erreur inattendue s'est produite.")

# Create bot instance
bot = DiscordBot()

# Traditional prefix commands
@bot.command(name='ping')
async def ping_command(ctx):
    """Commande ping pour tester la latence du bot"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latence: {latency}ms",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name='hello')
async def hello_command(ctx):
    """Commande pour saluer l'utilisateur"""
    embed = discord.Embed(
        title="👋 Salut!",
        description=f"Bonjour {ctx.author.mention}! Comment allez-vous?",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# Slash commands
@bot.tree.command(name="ping", description="Teste la latence du bot")
async def ping_slash(interaction: discord.Interaction):
    """Slash command pour ping"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latence: {latency}ms",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="hello", description="Salue l'utilisateur")
async def hello_slash(interaction: discord.Interaction):
    """Slash command pour hello"""
    embed = discord.Embed(
        title="👋 Salut!",
        description=f"Bonjour {interaction.user.mention}! Comment allez-vous?",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Affiche l'aide du bot")
async def help_slash(interaction: discord.Interaction):
    """Slash command pour l'aide"""
    embed = discord.Embed(
        title="📚 Aide - Alerte Percepteur",
        description="Voici les commandes disponibles:",
        color=discord.Color.purple()
    )
    
    embed.add_field(
        name="Commandes Slash",
        value="`/ping` - Teste la latence\n"
              "`/hello` - Salue l'utilisateur\n"
              "`/buttons` - Affiche les boutons interactifs\n"
              "`/help` - Affiche cette aide",
        inline=False
    )
    
    embed.add_field(
        name="Commandes Préfixe",
        value=f"`{Config.COMMAND_PREFIX}ping` - Teste la latence\n"
              f"`{Config.COMMAND_PREFIX}hello` - Salue l'utilisateur",
        inline=False
    )
    
    embed.set_footer(text="Alerte Percepteur - Bot créé avec discord.py")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="buttons", description="Affiche les boutons interactifs")
async def buttons_slash(interaction: discord.Interaction):
    """Slash command pour afficher les boutons"""
    embed = discord.Embed(
        title="🚨 Alerte Percepteur🚨",
        description="😎 Ce Bot codé par Viti vous permet de ping rapidement les niveaux 200 en cas d'attaque ! 😎",
        color=discord.Color.orange()
    )
    
    view = MessageButtonView()
    await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    """Log all interactions for debugging"""
    if interaction.type == discord.InteractionType.component:
        logger.info(f"Button interaction from {interaction.user}: {interaction.data}")


# Main function to run the bot
async def main():
    """Main function to start the bot"""
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        return
    
    try:
        # Start web server for UptimeRobot
        start_web_server()
        
        # Start keep alive task
        asyncio.create_task(keep_alive_task())
        
        # Start the bot
        await bot.start(token)
    except discord.LoginFailure:
        logger.error("Invalid Discord token!")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")

# Rename the existing keep_alive function to avoid conflict
async def keep_alive_task():
    """Keep the bot alive on hosting services"""
    while True:
        await asyncio.sleep(300)  # 5 minutes
        logger.info("Keep alive ping")

if __name__ == "__main__":
    # Run the bot
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
