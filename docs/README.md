# The Villages Events - Documentation

Complete documentation for The Villages Events Home Assistant integration.

## 📚 Table of Contents

### Getting Started
- [Main README](../README.md) - Overview, installation, and quick start
- [Installation Guide](../README.md#installation) - HACS and manual installation
- [Configuration Guide](../README.md#configuration) - Initial setup

### User Guides
- [**Services**](SERVICES.md) - Manual refresh service documentation
- [**Events**](EVENTS.md) - Home Assistant events for automations
- [**Troubleshooting**](TROUBLESHOOTING.md) - Common issues and solutions

### Technical Documentation
- [**Developer Guide**](DEVELOPER.md) - Architecture, code structure, and development
- [**Getting Live Data**](GETTING_LIVE_DATA.md) - How the API integration works
- [**Embedded Library**](EMBEDDED_LIBRARY.md) - Villages Events library details
- [**Version Management**](VERSION_MANAGEMENT.md) - How to update versions

### Troubleshooting & Fixes
- [**Troubleshooting Guide**](TROUBLESHOOTING.md) - General troubleshooting
- [**Clear Cache**](CLEAR_CACHE.md) - How to clear Python cache
- [**View Logs**](VIEW_LOGS.md) - How to properly view Home Assistant logs
- [**Config Flow Fix**](CONFIG_FLOW_FIXED.md) - Fix for options flow error
- [**Icon Troubleshooting**](HACS_ICON_TROUBLESHOOTING.md) - HACS icon issues
- [**Icon Information**](ICON_INFO.md) - How integration icons work
- [**Why Icons Don't Show**](WHY_ICONS_DONT_SHOW.md) - Icon display explanation

### Reference
- [**Changelog**](CHANGELOG.md) - Version history and changes
- [**Debug Guide**](DEBUG.md) - Debugging tips and techniques

## 📖 Quick Links

### For Users
- **First time setup?** → [Main README](../README.md)
- **Integration not working?** → [Troubleshooting](TROUBLESHOOTING.md)
- **Want to create automations?** → [Events](EVENTS.md) & [Services](SERVICES.md)
- **Icons not showing?** → [Icon Troubleshooting](HACS_ICON_TROUBLESHOOTING.md)

### For Developers
- **Want to contribute?** → [Developer Guide](DEVELOPER.md)
- **Understanding the code?** → [Developer Guide](DEVELOPER.md)
- **API integration details?** → [Getting Live Data](GETTING_LIVE_DATA.md)
- **Release new version?** → [Version Management](VERSION_MANAGEMENT.md)

### For Troubleshooting
- **Config flow errors?** → [Config Flow Fix](CONFIG_FLOW_FIXED.md)
- **No logs showing?** → [View Logs](VIEW_LOGS.md)
- **Integration won't load?** → [Clear Cache](CLEAR_CACHE.md)
- **General issues?** → [Troubleshooting](TROUBLESHOOTING.md)

## 📋 Document Descriptions

### User Documentation

#### [Services](SERVICES.md)
Learn how to use the `villages_events.refresh` service to manually update event data. Includes examples for automations and scripts.

#### [Events](EVENTS.md)
Complete guide to Home Assistant events fired by this integration:
- `villages_events_favorite_performer` - When favorites are detected
- `villages_events_new_events` - When new events are added

Includes automation examples and event data structures.

#### [Troubleshooting](TROUBLESHOOTING.md)
Solutions for common issues:
- Config flow errors
- No events showing
- Entities unavailable
- Update interval not working
- Favorite performers not detected

### Developer Documentation

#### [Developer Guide](DEVELOPER.md)
Comprehensive guide for developers:
- Architecture overview with diagrams
- Component interaction
- Data flow
- Code structure
- Development setup
- Testing procedures
- Adding new features

#### [Getting Live Data](GETTING_LIVE_DATA.md)
How the integration fetches live data from The Villages API:
- API details and endpoints
- Authentication token extraction
- Data processing
- Error handling
- Mock data fallback

#### [Embedded Library](EMBEDDED_LIBRARY.md)
Details about the embedded Villages Events library:
- Why it's embedded
- Library structure
- API client implementation
- Configuration

#### [Version Management](VERSION_MANAGEMENT.md)
How to manage versions:
- Semantic versioning
- Where versions are stored
- How to update versions
- Creating releases
- HACS version display

### Troubleshooting Documentation

#### [Config Flow Fix](CONFIG_FLOW_FIXED.md)
Fix for the "500 Internal Server Error" when clicking the gear icon to edit settings. Explains the root cause and solution.

#### [Clear Cache](CLEAR_CACHE.md)
How to clear Python bytecode cache when Home Assistant uses old code:
- Methods for different installation types
- Docker/Container instructions
- Home Assistant OS instructions

#### [View Logs](VIEW_LOGS.md)
How to properly view Home Assistant logs:
- Why web interface is limited
- Using SSH/Terminal
- Real-time log monitoring
- Searching logs
- Docker logs

#### [HACS Icon Troubleshooting](HACS_ICON_TROUBLESHOOTING.md)
Why custom icons don't show and how to fix it:
- Icon file locations
- HACS cache issues
- Browser cache
- GitHub repository setup

#### [Icon Information](ICON_INFO.md)
Complete guide to integration icons:
- Where icons are used
- Why custom integrations don't show icons in HA
- How to add to brands repository
- Icon file requirements

### Reference Documentation

#### [Changelog](CHANGELOG.md)
Version history following Keep a Changelog format:
- All releases
- Added features
- Bug fixes
- Breaking changes

#### [Debug Guide](DEBUG.md)
Tips for debugging the integration:
- Enabling debug logging
- Common error messages
- Diagnostic tools

## 🔍 Finding What You Need

### By Topic

**Installation & Setup**
- [Main README](../README.md) → Installation
- [Main README](../README.md) → Configuration

**Using the Integration**
- [Services](SERVICES.md) → Manual refresh
- [Events](EVENTS.md) → Automations
- [Main README](../README.md) → Dashboard examples

**Troubleshooting**
- [Troubleshooting](TROUBLESHOOTING.md) → General issues
- [Config Flow Fix](CONFIG_FLOW_FIXED.md) → Options error
- [Clear Cache](CLEAR_CACHE.md) → Cache issues
- [View Logs](VIEW_LOGS.md) → Finding errors

**Development**
- [Developer Guide](DEVELOPER.md) → Architecture & code
- [Getting Live Data](GETTING_LIVE_DATA.md) → API details
- [Version Management](VERSION_MANAGEMENT.md) → Releases

**Icons**
- [Icon Information](ICON_INFO.md) → How icons work
- [HACS Icon Troubleshooting](HACS_ICON_TROUBLESHOOTING.md) → Icon issues

### By User Type

**End Users**
1. [Main README](../README.md) - Start here
2. [Services](SERVICES.md) - Manual refresh
3. [Events](EVENTS.md) - Automations
4. [Troubleshooting](TROUBLESHOOTING.md) - Problems

**Developers**
1. [Developer Guide](DEVELOPER.md) - Architecture
2. [Getting Live Data](GETTING_LIVE_DATA.md) - API
3. [Version Management](VERSION_MANAGEMENT.md) - Releases
4. [Changelog](CHANGELOG.md) - History

**Troubleshooters**
1. [Troubleshooting](TROUBLESHOOTING.md) - Start here
2. [View Logs](VIEW_LOGS.md) - Find errors
3. [Clear Cache](CLEAR_CACHE.md) - Cache issues
4. [Config Flow Fix](CONFIG_FLOW_FIXED.md) - Options error

## 📝 Contributing to Documentation

Found an error or want to improve the docs? Contributions are welcome!

1. Fork the repository
2. Edit the relevant markdown file
3. Submit a pull request

## 📄 License

This documentation is part of The Villages Events integration and is licensed under GPL v3.

---

**Need help?** Check the [Troubleshooting Guide](TROUBLESHOOTING.md) or open an issue on GitHub.
