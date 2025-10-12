#!/usr/bin/env python3
"""
Apply database schema to Supabase.
"""
import os
import sys
import asyncio
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from fastapi_app.utils.database import db_manager

async def apply_schema():
    """Apply the database schema to Supabase."""
    print("🗄️  Applying Database Schema to Supabase")
    print("=" * 50)
    
    try:
        # Test connection first
        print("🔌 Testing database connection...")
        is_connected = await db_manager.test_connection()
        if not is_connected:
            print("❌ Database connection failed")
            return False
        
        print("✅ Database connection successful")
        
        # Read the schema file
        schema_file = Path(__file__).parent.parent.parent / "infra" / "database" / "schema.sql"
        if not schema_file.exists():
            print(f"❌ Schema file not found: {schema_file}")
            return False
        
        print(f"📄 Reading schema file: {schema_file}")
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        # Split the schema into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        print(f"📝 Found {len(statements)} SQL statements to execute")
        
        # Execute each statement
        for i, statement in enumerate(statements, 1):
            if statement:
                try:
                    print(f"⚡ Executing statement {i}/{len(statements)}...")
                    # Use the Supabase client to execute the statement
                    result = db_manager.client.rpc('exec_sql', {'sql': statement}).execute()
                    print(f"✅ Statement {i} executed successfully")
                except Exception as e:
                    print(f"⚠️  Statement {i} failed (might already exist): {e}")
                    continue
        
        print("🎉 Schema application completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error applying schema: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(apply_schema())
    sys.exit(0 if success else 1)
