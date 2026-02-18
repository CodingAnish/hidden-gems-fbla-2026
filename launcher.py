#!/usr/bin/env python3
"""
Hidden Gems Desktop Launcher
Starts Flask backend and handles app lifecycle
"""

import os
import sys
import time
import subprocess
import signal
import atexit
import tempfile
from pathlib import Path
import json
import socket

# Get app directory
APP_DIR = Path(__file__).parent
VENV_DIR = APP_DIR / ".venv"
WEB_DIR = APP_DIR / "web"
DB_FILE = APP_DIR / "hidden_gems.db"
ENV_FILE = APP_DIR / ".env"

# Config directories for user secrets
if sys.platform == "darwin":  # macOS
    CONFIG_DIR = Path.home() / "Library" / "Application Support" / "Hidden Gems"
elif sys.platform == "win32":  # Windows
    CONFIG_DIR = Path.home() / "AppData" / "Roaming" / "Hidden Gems"
else:  # Linux
    CONFIG_DIR = Path.home() / ".config" / "hidden-gems"

CONFIG_DIR.mkdir(parents=True, exist_ok=True)
USER_ENV_FILE = CONFIG_DIR / ".env"

flask_process = None


def log(msg: str, level: str = "INFO"):
    """Log messages with timestamp"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}", flush=True)


def is_port_available(port: int = 5001) -> bool:
    """Check if port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            return sock.connect_ex(("localhost", port)) != 0
    except Exception:
        return True


def get_python_executable() -> str:
    """Get Python executable path"""
    if VENV_DIR.exists():
        if sys.platform == "win32":
            return str(VENV_DIR / "Scripts" / "python.exe")
        else:
            return str(VENV_DIR / "bin" / "python")
    return sys.executable


def setup_environment():
    """Load environment variables from .env files"""
    # Load app .env if exists
    if ENV_FILE.exists():
        from dotenv import load_dotenv
        load_dotenv(ENV_FILE)
    
    # Load user config .env (secrets)
    if USER_ENV_FILE.exists():
        from dotenv import load_dotenv
        load_dotenv(USER_ENV_FILE)
    
    # Ensure critical vars are set
    if not os.getenv("GROQ_API_KEY"):
        log("⚠️  GROQ_API_KEY not configured", "WARN")
    
    log("✓ Environment loaded", "INFO")


def start_flask():
    """Start Flask development server"""
    global flask_process
    
    port = 5001
    
    if not is_port_available(port):
        log(f"❌ Port {port} is already in use", "ERROR")
        sys.exit(1)
    
    python_exec = get_python_executable()
    
    if not Path(python_exec).exists():
        log(f"❌ Python not found: {python_exec}", "ERROR")
        sys.exit(1)
    
    log(f"🚀 Starting Flask backend with {python_exec}...", "INFO")
    
    try:
        flask_process = subprocess.Popen(
            [python_exec, "-m", "web.app"],
            cwd=APP_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=os.environ.copy(),
        )
        
        log(f"✓ Flask process started (PID: {flask_process.pid})", "INFO")
        
        # Wait for Flask to be ready
        for attempt in range(30):
            if not is_port_available(port):
                log(f"✓ Flask is ready on port {port}", "INFO")
                return True
            
            if flask_process.poll() is not None:
                # Process exited already
                _, stderr = flask_process.communicate()
                log(f"❌ Flask failed to start: {stderr.decode()}", "ERROR")
                return False
            
            time.sleep(0.5)
        
        log("❌ Flask startup timeout", "ERROR")
        return False
    
    except Exception as e:
        log(f"❌ Failed to start Flask: {e}", "ERROR")
        return False


def stop_flask():
    """Stop Flask background process"""
    global flask_process
    
    if flask_process and flask_process.poll() is None:
        log("🛑 Stopping Flask backend...", "INFO")
        try:
            flask_process.terminate()
            flask_process.wait(timeout=5)
            log("✓ Flask stopped", "INFO")
        except subprocess.TimeoutExpired:
            flask_process.kill()
            log("✓ Flask force-killed", "INFO")
        except Exception as e:
            log(f"⚠️  Error stopping Flask: {e}", "WARN")


def handle_interrupt(signum, frame):
    """Handle Ctrl+C"""
    log("\n🛑 Shutting down...", "INFO")
    stop_flask()
    sys.exit(0)


def show_launch_info():
    """Show launch information"""
    print("\n" + "=" * 60)
    print("🎯 Hidden Gems Desktop Application")
    print("=" * 60)
    print(f"🌐 Web Interface: http://localhost:5001")
    print(f"📁 App Directory: {APP_DIR}")
    print(f"🗄️  Database: {DB_FILE}")
    print(f"⚙️  Config: {CONFIG_DIR}")
    print("=" * 60 + "\n")


def main():
    """Main launcher function"""
    log("🎯 Hidden Gems Desktop Launcher", "INFO")
    
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)
    
    # Register cleanup on exit
    atexit.register(stop_flask)
    
    # Setup environment
    setup_environment()
    
    # Change to app directory
    os.chdir(APP_DIR)
    
    # Start Flask
    if not start_flask():
        log("❌ Failed to start Flask backend", "ERROR")
        sys.exit(1)
    
    show_launch_info()
    log("✅ Ready! The app will open shortly...", "INFO")
    
    # Keep process alive
    try:
        while True:
            time.sleep(1)
            
            # Check if Flask process is still alive
            if flask_process and flask_process.poll() is not None:
                log("❌ Flask process exited unexpectedly", "ERROR")
                sys.exit(1)
    
    except KeyboardInterrupt:
        handle_interrupt(None, None)


if __name__ == "__main__":
    main()
