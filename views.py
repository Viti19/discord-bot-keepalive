import discord
from discord.ext import commands
import logging
from config import Config

logger = logging.getLogger('discord_bot')

class MessageButtonView(discord.ui.View):
    """Vue contenant les boutons interactifs pour envoyer des messages"""
    
    def __init__(self):
        super().__init__(timeout=None)  # Persistent view
    
    @discord.ui.button(
        label="🚨 Attaque Percepteur🚨",
        style=discord.ButtonStyle.danger,
        custom_id="alert_button"
    )
    async def alert_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Bouton pour envoyer une attaque percepteur"""
        await self.send_message_to_channel(
            interaction,
            Config.ALERT_CHANNEL_ID,
            f"🚨 **ATTAQUE PERCEPTEUR**\n\n{interaction.user.mention} a déclencher l'alerte ! <@&1342890492463022121> si vous le pouvez venez défendre !",
            "Attaque Percepteur signalée!"
        )
    
    async def send_message_to_channel(self, interaction: discord.Interaction, channel_id: int, message_content: str, success_message: str):
        """
        Envoie un message dans un channel spécifique
        
        Args:
            interaction: L'interaction Discord
            channel_id: L'ID du channel de destination
            message_content: Le contenu du message à envoyer
            success_message: Le message de confirmation à afficher
        """
        try:
            # Vérifier si l'utilisateur a les permissions
            if not await self.check_user_permissions(interaction):
                return
            
            # Obtenir le channel
            channel = interaction.client.get_channel(channel_id)
            
            if not channel:
                await interaction.response.send_message(
                    "❌ Channel non trouvé! Vérifiez la configuration.",
                    ephemeral=True
                )
                logger.error(f"Channel {channel_id} not found")
                return
            
            # Vérifier que c'est un channel de texte
            if not isinstance(channel, discord.TextChannel):
                await interaction.response.send_message(
                    "❌ Le channel configuré n'est pas un channel de texte!",
                    ephemeral=True
                )
                return
            
            # Vérifier les permissions du bot
            if interaction.guild and interaction.guild.me:
                if not channel.permissions_for(interaction.guild.me).send_messages:
                    await interaction.response.send_message(
                        f"❌ Le bot n'a pas la permission d'envoyer des messages dans {channel.mention}",
                        ephemeral=True
                    )
                    return
            
            # Créer l'embed pour le message
            embed = discord.Embed(
                description=message_content,
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow()
            )
            embed.set_footer(
                text=f"Envoyé par {interaction.user.display_name}",
                icon_url=interaction.user.display_avatar.url
            )
            
            # Envoyer le message
            sent_message = await channel.send(embed=embed)
            
            # Confirmer l'envoi
            success_embed = discord.Embed(
                title="✅ Succès",
                description=f"{success_message}\n"
                           f"**Channel:** {channel.mention}\n"
                           f"**Message:** [Voir le message]({sent_message.jump_url})",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=success_embed, ephemeral=True)
            
            # Log l'action
            logger.info(f"Message sent by {interaction.user} to channel {channel.name} ({channel_id})")
            
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Permission refusée. Le bot n'a pas les droits nécessaires.",
                ephemeral=True
            )
            logger.error(f"Forbidden: Cannot send message to channel {channel_id}")
            
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"❌ Erreur lors de l'envoi du message: {str(e)}",
                ephemeral=True
            )
            logger.error(f"HTTP error sending message: {e}")
            
        except Exception as e:
            await interaction.response.send_message(
                "❌ Une erreur inattendue s'est produite.",
                ephemeral=True
            )
            logger.error(f"Unexpected error in send_message_to_channel: {e}")
    
    async def check_user_permissions(self, interaction: discord.Interaction) -> bool:
        """
        Vérifie si l'utilisateur a les permissions pour utiliser les boutons
        
        Args:
            interaction: L'interaction Discord
            
        Returns:
            bool: True si l'utilisateur a les permissions, False sinon
        """
        # Vérifier si l'utilisateur a des rôles autorisés (si configurés)
        if Config.ALLOWED_ROLE_IDS and isinstance(interaction.user, discord.Member):
            user_role_ids = [role.id for role in interaction.user.roles]
            if not any(role_id in Config.ALLOWED_ROLE_IDS for role_id in user_role_ids):
                await interaction.response.send_message(
                    "❌ Vous n'avez pas les permissions nécessaires pour utiliser ce bouton.",
                    ephemeral=True
                )
                logger.warning(f"User {interaction.user} attempted to use button without permission")
                return False
        
        # Vérifier les permissions de gestion des messages pour les membres du serveur
        if isinstance(interaction.user, discord.Member) and interaction.user.guild_permissions:
            if not interaction.user.guild_permissions.manage_messages:
                # Si pas de rôles spécifiques configurés, vérifier les permissions Discord
                if not Config.ALLOWED_ROLE_IDS:
                    await interaction.response.send_message(
                        "❌ Vous devez avoir la permission 'Gérer les messages' pour utiliser ce bouton.",
                        ephemeral=True
                    )
                    return False
        
        return True

class ConfirmationView(discord.ui.View):
    """Vue de confirmation pour les actions importantes"""
    
    def __init__(self, action_callback, *args, **kwargs):
        super().__init__(timeout=60.0)
        self.action_callback = action_callback
        self.args = args
        self.kwargs = kwargs
        self.confirmed = False
    
    @discord.ui.button(label="✅ Confirmer", style=discord.ButtonStyle.success)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Bouton de confirmation"""
        self.confirmed = True
        await self.action_callback(interaction, *self.args, **self.kwargs)
        self.stop()
    
    @discord.ui.button(label="❌ Annuler", style=discord.ButtonStyle.danger)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Bouton d'annulation"""
        await interaction.response.send_message("❌ Action annulée.", ephemeral=True)
        self.stop()
    
    async def on_timeout(self):
        """Called when the view times out"""
        self.clear_items()
