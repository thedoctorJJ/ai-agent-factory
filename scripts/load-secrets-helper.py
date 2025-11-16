#!/usr/bin/env python3
"""Helper script to load secrets from encrypted storage"""
import sys
import os
import importlib.util

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import secure-api-manager (has hyphens, need special handling)
secure_api_path = os.path.join(project_root, 'config', 'secure-api-manager.py')
spec = importlib.util.spec_from_file_location("secure_api_manager", secure_api_path)
secure_api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(secure_api)
SecureAPIManager = secure_api.SecureAPIManager

manager = SecureAPIManager()
secrets = manager.load_api_keys()

# Print secrets in format: SECRET_NAME|value
for key, value in secrets.items():
    if value and not key.startswith('_'):
        # Escape pipe characters in value
        value_escaped = value.replace('|', '\\|')
        print(f"{key}|{value_escaped}")

