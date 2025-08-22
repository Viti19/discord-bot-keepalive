from flask import Flask, request
import threading
import logging
from datetime import datetime

# Configure logging for Flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

# Configure custom logger
logger = logging.getLogger('keep_alive')

app = Flask(__name__)

@app.route('/')
def home():
    logger.info(f"🏠 Page d'accueil visitée depuis {request.remote_addr}")
    return "🚨 Alerte Percepteur Bot is running! 🚨"

@app.route('/status')
def status():
    logger.info(f"📊 Status vérifié depuis {request.remote_addr}")
    return {
        "status": "online",
        "bot": "Alerte Percepteur",
        "message": "Bot Discord opérationnel"
    }

@app.route('/ping')
def ping():
    current_time = datetime.now().strftime("%H:%M:%S")
    user_agent = request.headers.get('User-Agent', 'Unknown')
    remote_addr = request.remote_addr or 'Unknown'
    
    # Identifier le type de requête
    if 'cron-job.org' in user_agent.lower():
        source_type = "🕒 CRON-JOB"
    elif 'github-actions' in user_agent.lower():
        source_type = "🐙 GITHUB-ACTIONS"
    elif remote_addr.startswith('172.31.') if remote_addr != 'Unknown' else False:
        source_type = "🏠 REPLIT-INTERNE"
    else:
        source_type = "🌐 EXTERNE"
    
    logger.info(f"🔄 PING {source_type} depuis {remote_addr} à {current_time}")
    logger.info(f"   User-Agent: {user_agent}")
    
    return "pong"

def run():
    """Lance le serveur Flask sur le port 5000"""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def start_web_server():
    """Lance le serveur web dans un thread séparé"""
    print("🌐 Démarrage du serveur web pour UptimeRobot...")
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    print("✅ Serveur web démarré sur le port 5000")