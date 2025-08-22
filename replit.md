# Discord Bot with Interactive Buttons

## Overview

This is a modern Discord bot built with Python using discord.py 2.0+ that features interactive buttons for sending automated messages to specific channels. The bot supports both slash commands and traditional prefix commands, with a robust permission system and comprehensive logging. It's designed to streamline server communication by allowing authorized users to quickly send predefined messages to various channels through an intuitive button interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Discord.py 2.0+**: Modern Discord bot framework with support for slash commands and UI components
- **Command System**: Dual command support with both slash commands (/ping, /hello, /help, /buttons) and prefix commands (!ping, !hello)
- **Persistent Views**: Button interactions persist across bot restarts using custom_id system

### Configuration Management
- **Environment Variables**: Configuration through .env files for sensitive data like tokens and channel IDs
- **Config Class**: Centralized configuration management with validation and error handling
- **Flexible Setup**: Supports optional role-based permissions and customizable command prefixes

### Interactive UI Components
- **Button Views**: Custom Discord UI View class with multiple themed buttons (announcements, general messages, events, alerts)
- **Message Automation**: Each button sends predefined messages to configured channels with appropriate formatting and emojis
- **User Feedback**: Immediate response to button interactions with success/error messages

### Permission System
- **Role-based Access**: Optional role ID configuration to restrict button usage to specific server roles
- **Permission Validation**: Built-in checks to ensure users have appropriate permissions before executing commands

### Logging & Error Handling
- **Comprehensive Logging**: Multi-level logging system with both file and console output
- **Error Recovery**: Robust error handling for API failures, configuration issues, and user permission problems
- **Bot Lifecycle Management**: Proper startup procedures including command synchronization and view registration

### Channel Management
- **Multi-Channel Support**: Configurable target channels for different message types (announcements, general, events, alerts)
- **Message Formatting**: Consistent message formatting with emojis and mentions for better user experience

## External Dependencies

### Core Dependencies
- **discord.py**: Primary Discord API wrapper for Python
- **python-dotenv**: Environment variable management for configuration

### Discord Platform
- **Discord Developer Portal**: Bot registration and token management
- **Discord Guild Permissions**: Server-level permissions for bot functionality
- **Discord API**: Real-time communication and message sending capabilities

### Infrastructure Requirements
- **Environment Variables**: DISCORD_TOKEN, channel IDs, role IDs, and command prefix configuration
- **File System**: Local logging to 'bot.log' file for debugging and monitoring
- **Network Access**: Stable internet connection for Discord API communication