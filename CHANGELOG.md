# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup with Docker-based syslog-ng
- Dynamic configuration reloading with inotify and polling fallback
- Modular configuration structure for multiple sites
- Docker Compose setup with host networking
- Python test script for generating syslog messages
- Comprehensive documentation and README
- GitHub Actions CI/CD workflows
- Issue templates and pull request template
- Contributing guidelines

### Features
- **Dynamic Reloading**: Automatic configuration reload without service interruption
- **Multi-site Support**: Modular configuration for different locations
- **Health Monitoring**: Built-in health checks and monitoring
- **Cross-platform**: Works on Linux, macOS, and Windows with Docker
- **Testing Utilities**: Python script for generating test messages

### Configuration
- Global syslog-ng options in `conf.d/options/`
- Site-specific configurations in `conf.d/locations/`
- Support for UDP log sources on different ports
- File-based log destinations with automatic directory creation

### Docker
- Custom Docker image based on `balabit/syslog-ng:latest`
- Intelligent entrypoint script with configuration monitoring
- Health checks using `syslog-ng-ctl`
- Volume mounts for configuration and logs
- Host networking mode for proper port binding

### Documentation
- Comprehensive README with quick start guide
- Configuration examples and best practices
- Troubleshooting guide
- Development guidelines
- Contributing instructions

## [0.1.0] - Initial Release

### Added
- Basic syslog-ng Docker setup
- Configuration structure
- Docker Compose configuration
- Test utilities
