import os
from typing import List, Optional

class Config:
    """Configuration du bot Discord"""
    
    # Token du bot Discord
    DISCORD_TOKEN: str = os.getenv('DISCORD_TOKEN', '')
    
    # Préfixe des commandes
    COMMAND_PREFIX: str = os.getenv('COMMAND_PREFIX', '!')
    
    # IDs des channels pour les boutons
    ANNOUNCEMENT_CHANNEL_ID: int = int(os.getenv('ANNOUNCEMENT_CHANNEL_ID', '1340822272956567572'))
    GENERAL_CHANNEL_ID: int = int(os.getenv('GENERAL_CHANNEL_ID', '1340822272956567572'))
    EVENT_CHANNEL_ID: int = int(os.getenv('EVENT_CHANNEL_ID', '1340822272956567572'))
    ALERT_CHANNEL_ID: int = int(os.getenv('ALERT_CHANNEL_ID', '1408473953277841570'))
    
    # IDs des rôles autorisés à utiliser les boutons (optionnel)
    ALLOWED_ROLE_IDS: List[int] = []
    
    @classmethod
    def load_allowed_roles(cls):
        """Charge les IDs des rôles autorisés depuis les variables d'environnement"""
        roles_str = os.getenv('ALLOWED_ROLE_IDS', '')
        if roles_str:
            try:
                cls.ALLOWED_ROLE_IDS = [int(role_id.strip()) for role_id in roles_str.split(',') if role_id.strip()]
            except ValueError:
                print("Erreur: ALLOWED_ROLE_IDS doit contenir des IDs numériques séparés par des virgules")
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """
        Valide la configuration et retourne une liste d'erreurs
        
        Returns:
            List[str]: Liste des erreurs de configuration
        """
        errors = []
        
        if not cls.DISCORD_TOKEN:
            errors.append("DISCORD_TOKEN est requis")
        
        if cls.ANNOUNCEMENT_CHANNEL_ID == 0:
            errors.append("ANNOUNCEMENT_CHANNEL_ID doit être configuré")
        
        if cls.GENERAL_CHANNEL_ID == 0:
            errors.append("GENERAL_CHANNEL_ID doit être configuré")
        
        if cls.EVENT_CHANNEL_ID == 0:
            errors.append("EVENT_CHANNEL_ID doit être configuré")
        
        if cls.ALERT_CHANNEL_ID == 0:
            errors.append("ALERT_CHANNEL_ID doit être configuré")
        
        return errors
    
    @classmethod
    def print_config_status(cls):
        """Affiche le statut de la configuration"""
        print("=== Configuration du Bot Discord ===")
        print(f"Token configuré: {'✅' if cls.DISCORD_TOKEN else '❌'}")
        print(f"Préfixe: {cls.COMMAND_PREFIX}")
        print(f"Channel Annonces: {cls.ANNOUNCEMENT_CHANNEL_ID if cls.ANNOUNCEMENT_CHANNEL_ID != 0 else '❌ Non configuré'}")
        print(f"Channel Général: {cls.GENERAL_CHANNEL_ID if cls.GENERAL_CHANNEL_ID != 0 else '❌ Non configuré'}")
        print(f"Channel Événements: {cls.EVENT_CHANNEL_ID if cls.EVENT_CHANNEL_ID != 0 else '❌ Non configuré'}")
        print(f"Channel Alertes: {cls.ALERT_CHANNEL_ID if cls.ALERT_CHANNEL_ID != 0 else '❌ Non configuré'}")
        print(f"Rôles autorisés: {len(cls.ALLOWED_ROLE_IDS)} rôle(s)")
        
        errors = cls.validate_config()
        if errors:
            print("\n❌ Erreurs de configuration:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("\n✅ Configuration valide!")
        print("=" * 37)

# Charger les rôles autorisés au démarrage
Config.load_allowed_roles()

# Variables d'environnement requises
REQUIRED_ENV_VARS = [
    'DISCORD_TOKEN',
    'ANNOUNCEMENT_CHANNEL_ID',
    'GENERAL_CHANNEL_ID',
    'EVENT_CHANNEL_ID',
    'ALERT_CHANNEL_ID'
]

# Variables d'environnement optionnelles
OPTIONAL_ENV_VARS = [
    'COMMAND_PREFIX',
    'ALLOWED_ROLE_IDS'
]
