# How to Check Supabase Network Settings

## Quick Access Links

- **Supabase Dashboard**: https://supabase.com/dashboard
- **Your Project**: `ssdcbhxctakgysnayzeq`
- **Direct Project Link**: https://supabase.com/dashboard/project/ssdcbhxctakgysnayzeq

---

## Step-by-Step Instructions

### Step 1: Access Your Supabase Project

1. Go to https://supabase.com/dashboard
2. Log in to your Supabase account
3. Find and click on your project: **`ssdcbhxctakgysnayzeq`**

### Step 2: Navigate to Database Settings

1. In the left sidebar, click **"Settings"** (gear icon)
2. Click **"Database"** in the settings menu
3. You should now see database configuration options

### Step 3: Check IP Allowlist (Network Restrictions)

1. In the Database settings page, look for:
   - **"Network Restrictions"** section
   - **"IP Allowlist"** or **"Connection Pooling"** section
   - **"Database Access"** section

2. **What to look for:**
   - **IP Allowlist**: A list of allowed IP addresses
   - **"Restrict connections to specific IPs"**: A toggle/checkbox
   - **"Allow all IPs"** or **"No restrictions"**: Should be enabled for development

3. **If IP Allowlist is enabled:**
   - Check if your current IP is in the list
   - If not, you can:
     - Add your IP address to the allowlist
     - Or disable IP restrictions (for development)

4. **To find your current IP:**
   - Visit: https://whatismyipaddress.com/
   - Copy your IPv4 address
   - Add it to the Supabase allowlist

### Step 4: Check Connection Pooling Settings

1. In the Database settings, look for **"Connection Pooling"** section

2. **Connection Pooler Options:**
   - **Direct Connection**: Uses port `5432` (what we're trying to use)
   - **Connection Pooler**: Uses port `6543` (transaction mode) or `5432` (session mode)

3. **Check if Pooling is Enabled:**
   - If enabled, you might see a different connection string
   - Format: `postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres`

4. **Try Using Connection Pooler:**
   - Connection pooler might have better IPv4 support
   - Copy the pooler connection string if available
   - Update your `DATABASE_URL` to use the pooler

### Step 5: Check Database Access Settings

1. Look for **"Database Access"** or **"Security"** section

2. **Check these settings:**
   - **"Require SSL"**: Should be enabled (we're using `sslmode=require`)
   - **"Database Password"**: Make sure you have the correct password
   - **"Connection String"**: Verify the format matches what we're using

### Step 6: Verify Connection String Format

In the Database settings, you should see a **"Connection string"** section with tabs:
- **URI**: Full connection string
- **JDBC**: Java format
- **Golang**: Go format
- **etc.**

**What to check:**
- The hostname should be: `db.ssdcbhxctakgysnayzeq.supabase.co`
- Port should be: `5432`
- Format: `postgresql://postgres:[PASSWORD]@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres`

---

## Common Issues and Solutions

### Issue 1: "Connection Refused" Error

**Possible Causes:**
- IP address not in allowlist
- Firewall blocking port 5432
- IPv6-only resolution (your network doesn't support IPv6)

**Solutions:**
1. **Disable IP restrictions** (for development):
   - Go to Database settings
   - Find "Network Restrictions"
   - Disable IP allowlist or add your IP

2. **Use Connection Pooler** (if available):
   - Connection pooler might have better network support
   - Use the pooler connection string instead

3. **Check your network:**
   - Try from a different network (mobile hotspot, etc.)
   - Check if your VPN is blocking connections

### Issue 2: IPv6 Connection Issues

**Symptom:** Hostname only resolves to IPv6, connection fails

**Solutions:**
1. **Use Connection Pooler** (often has IPv4 support)
2. **Check Supabase project region** (some regions have better IPv4 support)
3. **Contact Supabase support** if IPv4 is required

### Issue 3: Can't Find Network Settings

**If you don't see "Network Restrictions" or "IP Allowlist":**
- These features might be in a different location
- Try: **Settings → Database → Connection Pooling**
- Or: **Settings → Database → Security**
- Or: **Project Settings → Network**

---

## What to Do After Checking Settings

### If IP Allowlist Was the Issue:

1. **Add your IP** or **disable restrictions**
2. **Wait a few minutes** for changes to propagate
3. **Test the connection again** using the MCP tool

### If Connection Pooling is Available:

1. **Copy the pooler connection string**
2. **Update `~/.cursor/mcp.json`** with the pooler URL:
   ```json
   "DATABASE_URL": "postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres"
   ```
3. **Restart Cursor**
4. **Test the connection**

### If Settings Look Correct:

1. **Check your local network/firewall**
2. **Try from a different network** (mobile hotspot)
3. **Contact Supabase support** if the issue persists

---

## Quick Checklist

- [ ] Accessed Supabase Dashboard
- [ ] Navigated to Settings → Database
- [ ] Checked IP Allowlist settings
- [ ] Verified Connection Pooling options
- [ ] Confirmed connection string format
- [ ] Added IP to allowlist (if needed)
- [ ] Tried connection pooler (if available)
- [ ] Tested connection after changes

---

## Need Help?

If you can't find these settings or need assistance:
1. **Supabase Documentation**: https://supabase.com/docs/guides/database/connecting-to-postgres
2. **Supabase Support**: https://supabase.com/support
3. **Check Supabase Status**: https://status.supabase.com/




