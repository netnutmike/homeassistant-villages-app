# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-XX

### Added
- Initial release of The Villages Events integration
- Per-venue event sensors for today and tomorrow
- Binary sensors for favorite performer tracking
- UI-based configuration flow
- Configurable update intervals (15-1440 minutes)
- Favorite performer matching with case-insensitive search
- Automatic retry with exponential backoff on failures
- Rich event attributes (performer, times, event type, venue)
- HACS compatibility
- Comprehensive developer documentation
- Inline code documentation with Google-style docstrings

### Features
- Dynamic entity creation based on available venues
- Coordinator-based data fetching for efficiency
- Graceful error handling and recovery
- Entity availability tracking
- Last updated timestamps
- Event count and detailed event information

[Unreleased]: https://github.com/yourusername/villages-events-integration/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/villages-events-integration/releases/tag/v0.1.0
