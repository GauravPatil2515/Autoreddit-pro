# Reddit Authentication Troubleshooting Guide

## Current Issue: `invalid_grant` Error

The `invalid_grant` error when authenticating with Reddit API typically occurs due to one of these reasons:

### 1. Two-Factor Authentication (2FA) - Most Common Issue

If you have 2FA enabled on your Reddit account, you **cannot** use your regular password. You need to create an **app password**.

#### Steps to create an app password:
1. Go to Reddit.com and log in
2. Go to https://www.reddit.com/prefs/apps/
3. Click "User Settings" → "Safety & Privacy" → "Use two-factor authentication"
4. Generate an app password specifically for this application
5. Use this app password in your `.env` file instead of your regular Reddit password

### 2. Account Verification

Your Reddit account might need email verification:
1. Check your email for verification messages from Reddit
2. Verify your email address if needed
3. Make sure your account is in good standing (not suspended)

### 3. Credential Issues

Double-check your credentials:
- Username should be exactly as it appears on Reddit (case-sensitive)
- Password should be your current Reddit password (or app password if 2FA is enabled)
- Make sure there are no extra spaces in the `.env` file

### 4. Rate Limiting / Account Lockout

If you've made too many failed authentication attempts:
- Wait 15-30 minutes before trying again
- Try logging into Reddit manually first to ensure your account is accessible

## Next Steps

### Option 1: Check for 2FA (Recommended)
1. Log into Reddit manually at reddit.com
2. Go to User Settings → Safety & Privacy
3. Check if "Use two-factor authentication" is enabled
4. If yes, generate an app password and update your `.env` file

### Option 2: Verify Account Status
1. Try logging into Reddit manually
2. Check for any verification emails
3. Ensure your account is active and verified

### Option 3: Create a New Reddit App (if needed)
1. Go to https://www.reddit.com/prefs/apps/
2. Click "Create App"
3. Choose "script" as the app type
4. Use the new client ID and secret

## Testing

After making changes to your `.env` file, test with:
```
python test_reddit_auth_fixed.py
```

## Common `.env` Format Issues

Make sure your `.env` file looks like this (no quotes, no spaces around =):
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password_or_app_password
REDDIT_USER_AGENT=reddit_automation_bot_1.0
```

## Still Having Issues?

If you continue to have problems:
1. Try creating a new Reddit account for testing
2. Make sure the Reddit app type is set to "script"
3. Double-check all credentials are correct
4. Contact Reddit support if the account seems locked
