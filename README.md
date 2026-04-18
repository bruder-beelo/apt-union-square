# Union 346 Apartment Availability Checker

Automatically checks for 1 bedroom and 1 bedroom + den apartment availability at Union 346 every hour and creates GitHub Issues to notify you.

## Features

- ✅ Checks SightMap API for 1 bedroom and 1 bedroom + den availability
- ⏰ Runs automatically every hour via GitHub Actions
- 🔔 Creates a GitHub Issue when 1 bedroom becomes available
- 🔒 No secrets needed - uses GitHub's built-in notifications
- 🚫 Prevents duplicate issues

## Setup Instructions

### 1. Test the Script Locally

```bash
python3 check_availability.py
```

Exit codes:
- `0` - 1 bedroom apartment available
- `1` - No 1 bedroom apartments available
- `2` - Error occurred

### 2. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: apartment availability checker"
git branch -M main
git remote add origin YOUR_REPO_URL
git push -u origin main
```

### 3. Enable GitHub Actions

- Go to **Actions** tab in your repository
- Enable workflows if prompted
- The job will run automatically every hour

### 4. Enable GitHub Notifications

To get notified when an apartment is available:

1. Go to your repository on GitHub
2. Click **Watch** (top right) → **Custom** → Check **Issues**
3. You'll get notifications via:
   - GitHub notifications bell icon
   - Email (if enabled in your GitHub settings)
   - Mobile app (if you have GitHub mobile)

## How It Works

1. **Every hour**, the GitHub Action runs the Python script
2. **If a 1 bedroom or 1 bed + den is available**, it creates a GitHub Issue with:
   - 🏠 Alert title
   - 📋 Unit details
   - 🔗 Links to the building website
   - 📝 Next steps to apply
3. **You get notified** via GitHub (no email setup needed!)
4. **Prevents duplicates** - won't create multiple issues

## Manual Testing

Run manually via GitHub Actions:
1. Go to **Actions** tab
2. Select "Check 1 Bedroom Availability"
3. Click **Run workflow**

## API Details

The script uses the SightMap API:
```
https://sightmap.com/app/api/v1/rkwnqjo8wd2/sightmaps/45000
```

It filters for units where `bedroom_count == 1` or filter_label contains "den" and creates issues when available.

## Customization

### Change check frequency

Edit `.github/workflows/check-apartment-availability.yml`:

```yaml
schedule:
  - cron: '0 */2 * * *'  # Every 2 hours
  - cron: '*/30 * * * *'  # Every 30 minutes
```

### Check for different bedroom counts

Edit `check_availability.py` and modify the matching logic in the script.

### Close the issue when done

When you've checked the apartment or it's no longer relevant:
1. Go to **Issues** tab
2. Find the "apartment-available" issue
3. Close it manually

## Troubleshooting

**No notifications:**
- Make sure you're **watching** the repository for Issues
- Check your GitHub notification settings

**Script failing:**
- Check the Actions logs for errors
- API might be down or changed

**Want email instead?**
- Check git history for the email version
- Requires Gmail app password setup

## License

MIT
