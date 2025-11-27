# Finding Database Password in Supabase Dashboard

## Alternative Locations

If you don't see "Connection string" in Settings → Database, try these locations:

### Option 1: Project Settings → Database → Connection Pooling
1. Go to: https://supabase.com/dashboard/project/ssdcbhxctakgysnayzeq/settings/database
2. Look for **"Connection Pooling"** section
3. Check **"Connection string"** or **"Session mode"** tabs
4. The connection string should be there

### Option 2: Project Settings → Database → Connection Info
1. Go to: Settings → Database
2. Look for **"Connection info"** or **"Database"** section
3. You might see:
   - Host
   - Port
   - Database name
   - User
   - **Password** (might be hidden, click "Show" or "Reveal")

### Option 3: Reset Database Password
If you can't find the password, you can reset it:

1. Go to: Settings → Database
2. Look for **"Database password"** or **"Reset database password"**
3. Click **"Reset database password"** or **"Generate new password"**
4. Copy the new password immediately (it won't be shown again)
5. Use it in the connection string:
   ```
   postgresql://postgres:NEW_PASSWORD@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres
   ```

### Option 4: Use Connection Pooler (Recommended)
Supabase provides a connection pooler that might be easier:

1. Go to: Settings → Database → Connection Pooling
2. Look for **"Connection string"** under **"Session mode"**
3. Format: `postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres`
4. This uses the pooler which might have different credentials

### Option 5: Check API Settings
Sometimes the connection info is in API settings:

1. Go to: Settings → API
2. Look for **"Database"** or **"Connection"** section
3. Check for connection strings or database credentials

## What You're Looking For

The connection string format should be one of these:

**Direct connection:**
```
postgresql://postgres:[PASSWORD]@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres
```

**Pooled connection (Session mode):**
```
postgresql://postgres.ssdcbhxctakgysnayzeq:[PASSWORD]@aws-0-us-central1.pooler.supabase.com:5432/postgres
```

**Pooled connection (Transaction mode):**
```
postgresql://postgres.ssdcbhxctakgysnayzeq:[PASSWORD]@aws-0-us-central1.pooler.supabase.com:6543/postgres
```

## If You Still Can't Find It

1. **Reset the password** (Option 3 above) - this is the most reliable way
2. **Check your project's initial setup** - the password might have been set during project creation
3. **Contact Supabase support** - they can help you retrieve or reset it

## Quick Test

Once you have the password, you can test it:
```bash
psql "postgresql://postgres:YOUR_PASSWORD@db.ssdcbhxctakgysnayzeq.supabase.co:5432/postgres" -c "SELECT 1;"
```

If this works, the password is correct!







