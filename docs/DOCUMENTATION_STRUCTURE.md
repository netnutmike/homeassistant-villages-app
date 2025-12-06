# Documentation Structure

This document explains the organization of documentation for The Villages Events integration.

## Directory Structure

```
/
├── README.md                    # Main project README (stays in root)
├── LICENSE                      # License file (stays in root)
├── hacs.json                    # HACS configuration (stays in root)
├── info.md                      # HACS info (stays in root)
├── icon.png / icon@2x.png      # Integration icons (stay in root)
├── logo.png / logo@2x.png      # Integration logos (stay in root)
│
├── docs/                        # 📁 All documentation moved here
│   ├── README.md               # Documentation index
│   │
│   ├── CHANGELOG.md            # Version history
│   ├── SERVICES.md             # Services documentation
│   ├── EVENTS.md               # Events documentation
│   ├── TROUBLESHOOTING.md      # Troubleshooting guide
│   │
│   ├── DEVELOPER.md            # Developer guide
│   ├── GETTING_LIVE_DATA.md    # API integration details
│   ├── EMBEDDED_LIBRARY.md     # Library documentation
│   ├── VERSION_MANAGEMENT.md   # Version management
│   ├── DEBUG.md                # Debug guide
│   │
│   ├── CONFIG_FLOW_FIX.md      # Config flow fixes
│   ├── CONFIG_FLOW_FIXED.md    # Config flow solution
│   ├── FIX_CONFIG_FLOW.md      # Config flow troubleshooting
│   ├── CLEAR_CACHE.md          # Cache clearing guide
│   ├── VIEW_LOGS.md            # Log viewing guide
│   │
│   ├── HACS_ICON_TROUBLESHOOTING.md  # HACS icon issues
│   ├── ICON_INFO.md            # Icon information
│   ├── WHY_ICONS_DONT_SHOW.md  # Icon explanation
│   │
│   ├── install_icons.sh        # Icon installation script
│   └── DOCUMENTATION_STRUCTURE.md  # This file
│
└── custom_components/
    └── villages_events/         # Integration code
```

## Documentation Categories

### Root Files (Not Moved)
These files stay in the root for functional reasons:
- `README.md` - Main entry point, must be in root for GitHub
- `LICENSE` - License file, standard location
- `hacs.json` - HACS configuration, must be in root
- `info.md` - HACS info, must be in root
- `icon.png`, `icon@2x.png` - HACS icons, must be in root
- `logo.png`, `logo@2x.png` - Integration logos, must be in root

### User Documentation
Files for end users:
- `SERVICES.md` - How to use services
- `EVENTS.md` - Home Assistant events
- `TROUBLESHOOTING.md` - Common issues

### Developer Documentation
Files for developers and contributors:
- `DEVELOPER.md` - Architecture and development
- `GETTING_LIVE_DATA.md` - API integration
- `EMBEDDED_LIBRARY.md` - Library details
- `VERSION_MANAGEMENT.md` - Release process
- `DEBUG.md` - Debugging tips

### Troubleshooting Documentation
Specific fixes and solutions:
- `CONFIG_FLOW_FIX.md` - Config flow error fix
- `CONFIG_FLOW_FIXED.md` - Config flow solution
- `FIX_CONFIG_FLOW.md` - Config flow troubleshooting
- `CLEAR_CACHE.md` - Cache issues
- `VIEW_LOGS.md` - Log viewing

### Icon Documentation
Everything about icons:
- `HACS_ICON_TROUBLESHOOTING.md` - HACS icon issues
- `ICON_INFO.md` - How icons work
- `WHY_ICONS_DONT_SHOW.md` - Icon explanation
- `install_icons.sh` - Icon installation script

### Reference Documentation
- `CHANGELOG.md` - Version history
- `DOCUMENTATION_STRUCTURE.md` - This file

## Accessing Documentation

### From GitHub
- Main README: `https://github.com/yourusername/repo/`
- Documentation index: `https://github.com/yourusername/repo/blob/main/docs/README.md`
- Specific doc: `https://github.com/yourusername/repo/blob/main/docs/SERVICES.md`

### From Local Installation
- Documentation is in `/config/custom_components/villages_events/../../docs/`
- Or view on GitHub (recommended)

### From Main README
The main README.md has links to all important documentation in the docs folder.

## Link Updates

All internal documentation links have been updated to reflect the new structure:
- Main README links to `docs/FILENAME.md`
- Docs index links to `FILENAME.md` (relative)
- Cross-references between docs use relative paths

## Benefits of This Structure

### Cleaner Root Directory
- Only essential files in root
- Easier to navigate
- Professional appearance

### Organized Documentation
- All docs in one place
- Easy to find
- Clear categorization

### Better Maintenance
- Easier to update docs
- Clear structure for contributors
- Logical organization

### GitHub Friendly
- Main README still in root (GitHub requirement)
- Documentation accessible via docs folder
- Clean repository view

## Adding New Documentation

When adding new documentation:

1. **Create file in docs folder**
   ```bash
   touch docs/NEW_DOCUMENT.md
   ```

2. **Add to docs/README.md index**
   - Choose appropriate category
   - Add link and description

3. **Update main README.md if needed**
   - Add to Quick Links if important

4. **Use relative links**
   - From main README: `docs/FILENAME.md`
   - From docs: `FILENAME.md`
   - Cross-references: `OTHER_DOC.md`

## Migration Notes

### What Was Moved
All `.md` files except:
- `README.md` (must stay in root)
- `info.md` (HACS requirement)

All documentation scripts:
- `install_icons.sh`

### What Stayed
- `README.md` - Main README
- `LICENSE` - License file
- `hacs.json` - HACS config
- `info.md` - HACS info
- Icon files - HACS requirements

### Links Updated
- Main README.md → Updated to point to docs/
- docs/README.md → Created as index
- All internal links verified

## Maintenance

### Regular Updates
- Keep docs/README.md index current
- Update CHANGELOG.md for each release
- Review and update troubleshooting docs

### Link Checking
Periodically verify all links work:
```bash
# Check for broken links
grep -r "](.*\.md)" docs/ README.md
```

### Documentation Review
- Review docs quarterly
- Update for new features
- Remove outdated information
- Improve clarity

## Questions?

If you have questions about the documentation structure:
1. Check this file
2. Check docs/README.md
3. Open an issue on GitHub
