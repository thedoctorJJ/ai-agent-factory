#!/bin/bash

# Check Network Configuration for Supabase Connection
# This script helps diagnose network issues with Supabase

echo "🔍 Supabase Network Configuration Checker"
echo "=========================================="
echo ""

# Get current IP address
echo "📡 Your Current Network Information:"
echo "-----------------------------------"
echo -n "IPv4 Address: "
CURRENT_IP=$(curl -s https://api.ipify.org 2>/dev/null || echo "Unable to determine")
echo "$CURRENT_IP"

echo -n "IPv6 Address: "
CURRENT_IPV6=$(curl -s https://api64.ipify.org 2>/dev/null || echo "Not available")
echo "$CURRENT_IPV6"

echo ""
echo "🌐 Supabase Project Information:"
echo "--------------------------------"
echo "Project Reference: ssdcbhxctakgysnayzeq"
echo "Database Hostname: db.ssdcbhxctakgysnayzeq.supabase.co"
echo "Port: 5432"
echo ""

# Test DNS resolution
echo "🔍 DNS Resolution Test:"
echo "----------------------"
if command -v nslookup &> /dev/null; then
    echo "IPv4 addresses:"
    nslookup db.ssdcbhxctakgysnayzeq.supabase.co | grep -A 2 "Name:" || echo "  Unable to resolve"
    echo ""
    echo "IPv6 addresses:"
    nslookup -type=AAAA db.ssdcbhxctakgysnayzeq.supabase.co 2>/dev/null | grep -A 2 "Name:" || echo "  Unable to resolve"
else
    echo "  nslookup not available, skipping DNS test"
fi

echo ""
echo "📋 What to Check in Supabase Dashboard:"
echo "======================================="
echo ""
echo "1. Go to: https://supabase.com/dashboard/project/ssdcbhxctakgysnayzeq/settings/database"
echo ""
echo "2. Look for these sections:"
echo "   - Network Restrictions / IP Allowlist"
echo "   - Connection Pooling"
echo "   - Database Access / Security"
echo ""
echo "3. If IP Allowlist is enabled:"
if [ "$CURRENT_IP" != "Unable to determine" ]; then
    echo "   ✅ Add this IP to allowlist: $CURRENT_IP"
else
    echo "   ⚠️  Could not determine your IP - visit https://whatismyipaddress.com/"
fi
echo ""
echo "4. Check Connection Pooling:"
echo "   - If available, try using the connection pooler"
echo "   - Pooler might have better IPv4 support"
echo ""
echo "5. Verify Connection String:"
echo "   - Should be: postgresql://postgres:[PASSWORD]@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres"
echo "   - Or pooler: postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres"
echo ""
echo "📖 Full Guide: .cursor/CHECK_SUPABASE_NETWORK_SETTINGS.md"
echo ""




