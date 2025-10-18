#!/usr/bin/env python3
"""
Secure Configuration Manager for AI Agent Factory
This script provides secure handling of API keys and sensitive configuration
"""

import os
import sys
import json
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecureConfigManager:
    def __init__(self, config_dir=None):
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent
        self.encrypted_file = self.config_dir / "secrets.enc"
        self.key_file = self.config_dir / ".config_key"
        
    def _get_encryption_key(self, password=None):
        """Generate or retrieve encryption key"""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                return f.read()
        
        # Generate new key
        if password:
            # Use password-based key derivation
            password_bytes = password.encode()
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        else:
            # Generate random key
            key = Fernet.generate_key()
        
        # Save key
        with open(self.key_file, 'wb') as f:
            f.write(key)
        
        # Set restrictive permissions
        os.chmod(self.key_file, 0o600)
        
        return key
    
    def encrypt_secrets(self, secrets_dict, password=None):
        """Encrypt and store secrets"""
        key = self._get_encryption_key(password)
        fernet = Fernet(key)
        
        # Convert to JSON and encrypt
        secrets_json = json.dumps(secrets_dict)
        encrypted_data = fernet.encrypt(secrets_json.encode())
        
        # Save encrypted file
        with open(self.encrypted_file, 'wb') as f:
            f.write(encrypted_data)
        
        # Set restrictive permissions
        os.chmod(self.encrypted_file, 0o600)
        
        print(f"✅ Secrets encrypted and saved to: {self.encrypted_file}")
    
    def decrypt_secrets(self, password=None):
        """Decrypt and retrieve secrets"""
        if not self.encrypted_file.exists():
            return {}
        
        key = self._get_encryption_key(password)
        fernet = Fernet(key)
        
        with open(self.encrypted_file, 'rb') as f:
            encrypted_data = f.read()
        
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"❌ Failed to decrypt secrets: {e}")
            return {}
    
    def load_secure_config(self, password=None):
        """Load configuration with encrypted secrets"""
        # Load base configuration
        base_config = self._load_base_config()
        
        # Load encrypted secrets
        secrets = self.decrypt_secrets(password)
        
        # Merge configurations
        config = {**base_config, **secrets}
        
        return config
    
    def _load_base_config(self):
        """Load non-sensitive configuration"""
        base_config = {
            # Google Cloud (non-sensitive)
            'GOOGLE_CLOUD_PROJECT_ID': 'agent-factory-474201',
            'GOOGLE_CLOUD_REGION': 'us-central1',
            'GOOGLE_CLOUD_SERVICE_ACCOUNT_KEY': 'config/google-cloud-service-account.json',
            'REDIS_HOST': '10.1.93.195',
            'REDIS_PORT': '6379',
            'REDIS_URL': 'redis://10.1.93.195:6379',
            'CLOUD_RUN_REGION': 'us-central1',
            'CLOUD_RUN_PROJECT_ID': 'agent-factory-474201',
            'CLOUD_RUN_SERVICE_URL': 'https://test-agent-service-952475323593.us-central1.run.app',
            'GCR_REGISTRY': 'gcr.io/agent-factory-474201',
            'DEPLOYMENT_PLATFORM': 'google-cloud-run',
            'DEPLOYMENT_REGION': 'us-central1',
            'DEPLOYMENT_PROJECT': 'agent-factory-474201',
            
            # Application settings
            'ENVIRONMENT': 'development',
            'DEBUG': 'true',
            'LOG_LEVEL': 'INFO',
        }
        
        return base_config

def main():
    """Main function for secure configuration management"""
    manager = SecureConfigManager()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 secure-config.py encrypt [password]  - Encrypt secrets")
        print("  python3 secure-config.py decrypt [password]  - Decrypt secrets")
        print("  python3 secure-config.py load [password]     - Load secure config")
        return
    
    command = sys.argv[1]
    password = sys.argv[2] if len(sys.argv) > 2 else None
    
    if command == "encrypt":
        # Load current secrets from .env.local
        env_file = manager.config_dir / "env" / ".env.local"
        if not env_file.exists():
            print("❌ No .env.local file found to encrypt")
            return
        
        secrets = {}
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Only encrypt sensitive keys
                    if any(sensitive in key.upper() for sensitive in ['KEY', 'TOKEN', 'SECRET', 'PASSWORD']):
                        secrets[key.strip()] = value.strip()
        
        manager.encrypt_secrets(secrets, password)
        
    elif command == "decrypt":
        secrets = manager.decrypt_secrets(password)
        print("Decrypted secrets:")
        for key, value in secrets.items():
            print(f"  {key}: {value[:20]}..." if len(value) > 20 else f"  {key}: {value}")
            
    elif command == "load":
        config = manager.load_secure_config(password)
        print(f"Loaded {len(config)} configuration variables")
        
        # Create .env file
        env_file = Path(__file__).parent.parent / ".env"
        with open(env_file, 'w') as f:
            f.write("# AI Agent Factory Configuration (Secure)\n")
            f.write("# Generated by secure-config.py\n\n")
            
            for key, value in config.items():
                f.write(f"{key}={value}\n")
        
        print(f"✅ Configuration written to: {env_file}")
        
    else:
        print("❌ Unknown command. Use 'encrypt', 'decrypt', or 'load'")

if __name__ == "__main__":
    main()
