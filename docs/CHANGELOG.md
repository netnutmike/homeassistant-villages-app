# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2024-12-06

### Added
- Easy-access `performers` attribute for sensor entities (list of performer names)
- Easy-access `venues` attribute for favorite performer binary sensors
- Comprehensive documentation structure in `docs/` folder
- Documentation index at `docs/README.md`
- Documentation structure guide

### Fixed
- **Config flow options error** - Fixed "AttributeError: property 'config_entry' has no setter"
- Options flow now works correctly when clicking gear icon to edit settings
- Changed from `self.config_entry` to `self._config_entry` to avoid property conflict

### Changed
- Reorganized documentation into `docs/` folder for cleaner root directory
- Updated all documentation links to point to new location
- Improved error handling in config flow with better logging

### Documentation
- Created comprehensive documentation index
- Added troubleshooting guides for common issues
- Added log viewing guide
- Added cache clearing guide
- Added icon troubleshooting guides

## [0.1.0] - 2024-12-06

### Added
- Initial release of The Villages Events integration
- Per-venue event sensors for today and tomorrow
- Binary sensors for favorite performer tracking
- UI-based configuration flow with options flow support
- Configurable update intervals (15-1440 minutes)
- Favorite performer matching with case-insensitive search
- Automatic retry with exponential backoff on failures
- Rich event attributes (performer, times, event type, venue)
- Easy-access `performers` attribute for simple performer name lists
- Easy-access `venues` attribute for favorite performer binary sensors
- Home Assistant events for automations:
  - `villages_events_favorite_performer` - Fired when favorites are detected
  - `villages_events_new_events` - Fired when new events are added
- Manual refresh service: `villages_events.refresh`
- Live data fetching from The Villages API
- Embedded Villages Events library (no external dependencies)
- Custom integration icons for HACS
- HACS compatibility
- Comprehensive documentation:
  - Developer guide (DEVELOPER.md)
  - Events documentation (EVENTS.md)
  - Services documentation (SERVICES.md)
  - Troubleshooting guide (TROUBLESHOOTING.md)
  - Getting live data guide (GETTING_LIVE_DATA.md)
- Inline code documentation with Google-style docstrings

### Features
- Dynamic entity creation based on available venues
- Coordinator-based data fetching for efficiency
- Graceful error handling and recovery
- Entity availability tracking
- Last updated timestamps
- Event count and detailed event information
- Performer names easily accessible in attributes
- Mock data fallback for testing and development

[Unreleased]: https://github.com/yourusername/villages-events-integration/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/yourusername/villages-events-integration/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/yourusername/villages-events-integration/releases/tag/v0.1.0
