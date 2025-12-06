# HACS Icon Troubleshooting

Your icons are correctly set up in the repository. If they're not showing in HACS, follow these steps:

## Current Setup ✅

Your repository has icons in the correct locations:

```
Repository Root (for HACS):
├── icon.png       ✅ Committed
├── icon@2x.png    ✅ Committed
├── logo.png       ✅ Committed
└── logo@2x.png    ✅ Committed

Integration Folder:
custom_components/villages_events/
├── icon.png       ✅ Committed
├── icon@2x.png    ✅ Committed
├── logo.png       ✅ Committed
└── logo@2x.png    ✅ Committed
```

## Why Icons Don't Show

HACS caches repository information and icons. Even after pushing icons to GitHub, HACS may show the old cached version.

## Solution Steps

### Step 1: Verify Icons on GitHub

1. Go to your GitHub repository
2. Check that these files are visible in the root:
   - `icon.png`
   - `icon@2x.png`
   - `logo.png`
   - `logo@2x.png`

If they're not there, you need to push them:
```bash
git add icon.png icon@2x.png logo.png logo@2x.png
git commit -m "Add custom icons for HACS"
git push origin main
```

### Step 2: Clear HACS Cache

HACS caches repository data. To force a refresh:

**Option A: Remove and Re-add Repository**
1. In Home Assistant, go to **HACS** → **Integrations**
2. Click the three dots on "The Villages Events"
3. Select **Remove**
4. Go to **HACS** → **Integrations** → **⋮** (three dots) → **Custom repositories**
5. Re-add your repository URL
6. Category: **Integration**
7. Click **Add**
8. Find "The Villages Events" and install it

**Option B: Restart Home Assistant**
1. Go to **Settings** → **System** → **Restart**
2. Wait for restart to complete
3. Go back to HACS and check

### Step 3: Clear Browser Cache

Browsers aggressively cache images:

**Hard Refresh:**
- Windows/Linux: `Ctrl + Shift + R`
- Mac: `Cmd + Shift + R`

**Or use Incognito/Private mode:**
- This bypasses all caches

### Step 4: Wait for HACS to Update

HACS may take time to refresh repository data:
- Wait 5-10 minutes
- HACS checks repositories periodically
- Icons may appear after the next check

### Step 5: Check HACS Logs

If icons still don't show:

1. Go to **Settings** → **System** → **Logs**
2. Search for "HACS" or your repository name
3. Look for errors related to downloading or parsing repository data

## Common Issues

### Issue 1: Icons Not on GitHub

**Problem:** Icons are on your local machine but not pushed to GitHub

**Solution:**
```bash
git status  # Check if icons are tracked
git add icon*.png logo*.png
git commit -m "Add icons"
git push
```

### Issue 2: Wrong Icon Location

**Problem:** Icons are in the wrong folder

**Solution:** Icons must be in the **repository root** for HACS:
```
✅ Correct: /icon.png
❌ Wrong: /custom_components/villages_events/icon.png (this is for HA, not HACS)
```

### Issue 3: HACS Cache

**Problem:** HACS is showing old cached data

**Solution:** Remove and re-add the repository in HACS

### Issue 4: Browser Cache

**Problem:** Browser is showing cached icon

**Solution:** Hard refresh (`Ctrl+Shift+R`) or use incognito mode

### Issue 5: Icon File Format

**Problem:** Icon file is corrupted or wrong format

**Verify:**
```bash
file icon.png
# Should show: PNG image data, 256 x 256, 8-bit/color RGBA
```

## Verification Checklist

- [ ] Icons are in repository root (not just integration folder)
- [ ] Icons are committed to git
- [ ] Icons are pushed to GitHub
- [ ] Icons are visible on GitHub web interface
- [ ] Removed and re-added repository in HACS
- [ ] Cleared browser cache (hard refresh)
- [ ] Waited 5-10 minutes for HACS to update
- [ ] Restarted Home Assistant

## Expected Result

After following these steps, you should see your custom icon:

1. **In HACS Store:**
   - Go to HACS → Integrations
   - Search for "The Villages Events"
   - Your custom icon should appear in the card

2. **In Installed Integrations:**
   - HACS → Integrations (installed)
   - "The Villages Events" should show your icon

## Still Not Working?

If icons still don't show after all steps:

### Check Icon Files on GitHub

Visit your repository on GitHub and verify:
```
https://github.com/yourusername/yourrepo/blob/main/icon.png
```

The icon should be viewable directly.

### Check HACS Repository Info

HACS stores repository info in:
```
/config/.storage/hacs.repositories
```

You can check if HACS has downloaded your repository data correctly.

### Alternative: Use Default Icons

If custom icons continue to cause issues, you can:
1. Remove the icon files
2. HACS will use default icons
3. Focus on functionality over appearance

## For Home Assistant Integration Page

Note: Custom icons in HACS don't automatically show in the Home Assistant Integrations page. For that, you need to:

1. Add icons to Home Assistant brands repository
2. Submit a pull request
3. Wait for approval

See [ICON_INFO.md](ICON_INFO.md) for details.

## Summary

Your icons are correctly set up in the repository. The issue is likely:
1. **HACS cache** - Remove and re-add repository
2. **Browser cache** - Hard refresh
3. **Time delay** - Wait for HACS to update

Most commonly, removing and re-adding the repository in HACS solves the issue!
