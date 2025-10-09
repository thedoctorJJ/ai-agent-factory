#!/bin/bash

# Script to update Supabase configuration in .env file

echo "🗄️  Updating Supabase configuration in .env file..."

# Backup the current .env file
cp .env .env.backup.supabase
echo "✅ Created backup: .env.backup.supabase"

# Update Supabase configuration (user needs to provide their own credentials)
echo "⚠️  Please manually update Supabase credentials in your .env file:"
echo "   - SUPABASE_URL: Your Supabase project URL"
echo "   - SUPABASE_KEY: Your Supabase anon key"
echo "   - SUPABASE_SERVICE_ROLE_KEY: Your Supabase service role key"
echo "   - NEXT_PUBLIC_SUPABASE_URL: Your Supabase project URL"
echo "   - NEXT_PUBLIC_SUPABASE_ANON_KEY: Your Supabase anon key"
echo "   - DATABASE_URL: Your Supabase database URL"

echo "✅ Supabase configuration template ready!"
echo ""
echo "📋 Next steps:"
echo "  1. Get your credentials from Supabase dashboard"
echo "  2. Update the .env file with your actual values"
echo "  3. Run 'python3 scripts/validate-config.py' to test"