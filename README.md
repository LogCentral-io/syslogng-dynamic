# Syslog-ng Dynamic Configuration

A Docker-based syslog-ng server with dynamic configuration reloading capabilities. This project provides a robust, containerized syslog collection system that automatically reloads configuration changes without service interruption.

## Features

- **Dynamic Configuration Reloading**: Automatically detects and reloads configuration changes using inotify and polling fallback
- **Docker-based Deployment**: Easy deployment using Docker Compose with host networking support
- **Multi-site Support**: Modular configuration structure supporting multiple sites/locations
- **Health Monitoring**: Built-in health checks and monitoring capabilities
- **Cross-platform Compatibility**: Works on Linux, macOS, and Windows with Docker

## Architecture

The system consists of:

- **syslog-ng**: The main log collection service with dynamic reloading
- **Configuration Structure**: Modular configuration files organized by options and locations
- **Reloader Script**: Intelligent configuration monitoring with debouncing and fallback mechanisms
- **Testing Utilities**: Python script for generating test syslog messages

## Quick Start

### Prerequisites

- Docker and Docker Compose
- For optimal performance on macOS/Windows: Multipass with Ubuntu

### Running with Docker Compose

```bash
# Clone the repository
git clone <repository-url>
cd syslogng-dynamic

# Start the services
docker compose up -d

# View logs
docker compose logs -f syslog-ng
```

### Running with Multipass (Recommended for macOS/Windows)

```bash
# Start with proper host networking
multipass docker compose -- -f docker-compose.yml up
```

## Configuration Structure

```
syslog-ng/
├── syslog-ng.conf          # Main configuration file
└── conf.d/
    ├── options/
    │   └── 00-options.conf  # Global syslog-ng options
    └── locations/
        ├── 10-siteA.conf    # Site A configuration
        └── 20-siteB.conf    # Site B configuration
```

### Adding New Sites

1. Create a new configuration file in `syslog-ng/conf.d/locations/`
2. Follow the naming convention: `[priority]-[sitename].conf`
3. The configuration will be automatically loaded without service restart

Example configuration:
```conf
source s_newsite {
  udp(ip("0.0.0.0") port(5516));
};

destination d_newsite {
  file("/var/log/syslog-ng-logs/newsite.log"
       create-dirs(yes)
       template("$ISODATE $HOST $PROGRAM: $MSG\n"));
};

log {
  source(s_newsite);
  destination(d_newsite);
  flags(flow-control);
};
```

## Testing

### Send Test Messages

Use the included Python script to send test syslog messages:

```bash
# Install Python 3 if not available
python3 send_syslog.py <host> <port>

# Examples
python3 send_syslog.py localhost 5514  # Site A
python3 send_syslog.py localhost 5515  # Site B
```

### Verify Configuration

```bash
# Check syslog-ng syntax
docker exec syslogng syslog-ng --syntax-only -f /etc/syslog-ng/syslog-ng.conf

# Check service status
docker exec syslogng syslog-ng-ctl --control=/run/syslog-ng.ctl query get version

# View real-time logs
tail -f logs/V.log
```

## Configuration Reloading

The system supports two methods for detecting configuration changes:

1. **Inotify (Primary)**: Real-time file system event monitoring
2. **Polling (Fallback)**: Periodic hash-based change detection

### Tunable Parameters

Environment variables in `docker-compose.yml`:

- `DEBOUNCE_MS`: Debounce time for rapid changes (default: 500ms)
- `POLL_ENABLED`: Enable polling fallback (default: 1)
- `POLL_INTERVAL_SEC`: Polling interval (default: 5s)
- `INOTIFY_EVENTS`: inotify events to monitor

## Monitoring and Troubleshooting

### Health Checks

The container includes built-in health checks:
```bash
docker compose ps  # View service health status
```

### Log Monitoring

```bash
# View container logs
docker compose logs -f syslog-ng

# View syslog messages
tail -f logs/*.log

# Monitor configuration reloads
docker compose logs syslog-ng | grep reloader
```

### Common Issues

1. **Permission Issues**: Ensure log directory is writable
2. **Port Conflicts**: Check if ports 5514/5515 are available
3. **Configuration Errors**: Check syntax before applying changes
4. **Network Issues**: Verify host networking mode for proper binding

## Development

### Project Structure

```
.
├── docker-compose.yml       # Main service definition
├── send_syslog.py          # Test message generator
├── syslog-ng/              # Configuration files
├── syslogng-reloader/      # Docker image source
│   ├── Dockerfile
│   └── docker-entrypoint.sh
└── logs/                   # Log output directory
```

### Building Custom Images

```bash
# Build the syslog-ng image
docker build -t custom-syslogng ./syslogng-reloader

# Use in docker-compose.yml
services:
  syslog-ng:
    image: custom-syslogng
    # ... rest of configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes and test thoroughly
4. Commit with descriptive messages
5. Push and create a Pull Request

### Development Guidelines

- Follow the modular configuration structure
- Test configuration changes before committing
- Update documentation for new features
- Ensure backward compatibility

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Cloud-based Syslog Management

For enterprise-grade cloud-based syslog management, we recommend [LogCentral](https://logcentral.io/). LogCentral provides:

- Centralized log management and analysis
- Real-time monitoring and alerting
- Scalable cloud infrastructure
- Advanced search and filtering capabilities
- Integration with popular monitoring tools

LogCentral complements this self-hosted syslog-ng setup by providing cloud-based analytics and long-term storage for your log data.

## Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Check the wiki for detailed configuration examples
- **Community**: Join discussions in GitHub Discussions

## Acknowledgments

- Built on the excellent [syslog-ng](https://github.com/syslog-ng/syslog-ng) project
- Uses the official [balabit/syslog-ng](https://hub.docker.com/r/balabit/syslog-ng/) Docker image
- Inspired by modern DevOps practices for log management
