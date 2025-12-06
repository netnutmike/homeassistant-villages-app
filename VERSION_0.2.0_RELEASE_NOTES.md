# Version 0.2.0 Release Notes

## 🎉 What's New in v0.2.0

### Major Improvements

#### 🐛 Fixed Config Flow Options Error
- **Fixed the "500 Internal Server Error"** when clicking the gear icon to edit integration settings
- Root cause: `config_entry` property conflict in OptionsFlow
- Solution: Changed to use `_config_entry` private variable
- Options flow now works correctly for editing update interval and favorite performers

#### 📊 Easy-Access Attributes
- **New `performers` attribute** on sensor entities - simple list of performer names
- **New `venues` attribute** on favorite performer binary sensors
- Makes it much easier to use performer names in automations and templates
- No need to parse the complex `events` list anymore

#### 📚 Documentation Reorganization
- **All documentation moved to `docs/` folder** for cleaner root directory
- **New documentation index** at `docs/README.md` with complete navigation
- **Better organization** by category (User, Developer, Troubleshooting)
- **Comprehensive guides** for common issues and solutions

### New Documentation

#### User Guides
- Complete troubleshooting guide
- Log viewing guide (how to see real errors)
- Cache clearing guide
- Icon troubleshooting guides

#### Developer Guides
- Documentation structure guide
- Version management guide
- Debug guide improvements

### Bug Fixes

- ✅ Fixed AttributeError in options flow initialization
- ✅ Fixed config flow error handling
- ✅ Improved error logging throughout

### Improvements

- Better error handling in config flow
- More comprehensive logging for debugging
- Cleaner project structure
- Professional documentation organization

## 📦 Upgrade Instructions

### Via HACS (Recommended)

1. Go to **HACS** → **Integrations**
2. Find "The Villages Events"
3. Click **⋮** (three dots) → **Redownload**
4. Go to **Settings** → **System** → **Restart**
5. Restart Home Assistant

### Manual Update

1. Download the latest release
2. Replace `/config/custom_components/villages_events/` with new files
3. Restart Home Assistant

## 🔄 Breaking Changes

**None!** This is a backwards-compatible release.

All existing configurations, automations, and dashboards will continue to work without changes.

## ✨ New Features You Can Use

### Easy Performer Names in Automations

**Before (v0.1.0):**
```yaml
# Had to loop through events list
{% for event in state_attr('sensor.villages_events_spanish_springs_today', 'events') %}
  {{ event.performer }}
{% endfor %}
```

**Now (v0.2.0):**
```yaml
# Simple list access
{{ state_attr('sensor.villages_events_spanish_springs_today', 'performers') }}

# Join into string
{{ state_attr('sensor.villages_events_spanish_springs_today', 'performers') | join(', ') }}

# Check if specific performer
{{ 'The Beatles' in state_attr('sensor.villages_events_spanish_springs_today', 'performers') }}
```

### Edit Settings Without Errors

You can now click the gear icon on the integration to edit:
- Update interval
- Favorite performers

No more 500 errors!

## 📖 Documentation

All documentation is now organized in the `docs/` folder:

- [Documentation Index](docs/README.md)
- [Services Guide](docs/SERVICES.md)
- [Events Guide](docs/EVENTS.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Developer Guide](docs/DEVELOPER.md)
- [Changelog](docs/CHANGELOG.md)

## 🙏 Thank You

Thank you for using The Villages Events integration!

If you encounter any issues, please:
1. Check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
2. Review the [Log Viewing Guide](docs/VIEW_LOGS.md)
3. Open an issue on GitHub with logs

## 📅 Release Date

December 6, 2024

## 🔗 Links

- [Full Changelog](docs/CHANGELOG.md)
- [Documentation](docs/README.md)
- [GitHub Repository](https://github.com/yourusername/villages-events-integration)

---

**Upgrading from v0.1.0?** No configuration changes needed - just update and restart!
