# Contributing to syslogng-dynamic

Thank you for your interest in contributing to syslogng-dynamic! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use the appropriate issue template**:
   - Bug reports for problems or errors
   - Feature requests for new functionality
   - Configuration help for setup questions
3. **Provide detailed information** including:
   - Environment details (OS, Docker version, etc.)
   - Configuration files
   - Log output
   - Steps to reproduce

### Submitting Changes

#### 1. Fork and Clone

```bash
git clone https://github.com/yourusername/syslogng-dynamic.git
cd syslogng-dynamic
```

#### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

#### 3. Make Changes

Follow these guidelines:
- **Configuration files**: Use proper syslog-ng syntax and formatting
- **Shell scripts**: Follow bash best practices and include error handling
- **Docker files**: Optimize for size and security
- **Documentation**: Update relevant docs for any changes

#### 4. Test Your Changes

**Required Testing:**
```bash
# Test syslog-ng configuration syntax
docker run --rm -v $(pwd)/syslog-ng:/etc/syslog-ng:ro \
  balabit/syslog-ng:latest \
  syslog-ng --syntax-only -f /etc/syslog-ng/syslog-ng.conf

# Build and test Docker image
docker build -t syslogng-test ./syslogng-reloader

# Test with docker-compose
docker compose config
docker compose up -d
# Test log reception
python3 send_syslog.py localhost 5514
# Check logs
tail -f logs/*.log
docker compose down
```

**Additional Testing:**
- Test configuration reloading by modifying files
- Test with multiple log sources
- Verify health checks work
- Test on different platforms if possible

#### 5. Commit Changes

Use clear, descriptive commit messages:
```bash
git add .
git commit -m "feat: add support for TCP log sources"
# or
git commit -m "fix: resolve configuration reload timing issue"
```

**Commit Message Format:**
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `config:` for configuration changes
- `docker:` for Docker-related changes
- `test:` for testing improvements

#### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Create a pull request using the provided template and fill in all relevant sections.

## Development Guidelines

### Configuration Management

1. **Modular Structure**: Keep configurations modular and organized
   - Options in `conf.d/options/`
   - Location-specific configs in `conf.d/locations/`
   - Use priority prefixes (e.g., `10-`, `20-`)

2. **Naming Conventions**:
   - Configuration files: `[priority]-[descriptive-name].conf`
   - Sources: `s_[location/purpose]`
   - Destinations: `d_[location/purpose]`
   - Log paths: descriptive names

3. **Best Practices**:
   - Always include `create-dirs(yes)` for file destinations
   - Use appropriate templates for log formatting
   - Consider flow-control for high-volume sources
   - Test syntax before committing

### Docker Development

1. **Image Building**:
   - Keep images minimal and secure
   - Use multi-stage builds when appropriate
   - Pin base image versions
   - Include health checks

2. **Script Development**:
   - Use `set -Eeuo pipefail` for bash scripts
   - Include proper error handling
   - Make scripts portable across distributions
   - Add meaningful log output

### Documentation

1. **Update README.md** for:
   - New features or configuration options
   - Changed behavior
   - New requirements

2. **Inline Documentation**:
   - Comment complex configurations
   - Explain non-obvious script logic
   - Include examples where helpful

3. **Configuration Examples**:
   - Provide working examples for new features
   - Include common use cases
   - Document any prerequisites

## Testing Requirements

### Automated Tests

The CI pipeline runs:
- Configuration syntax validation
- Docker image building
- Basic container functionality
- Security scanning

### Manual Testing Checklist

Before submitting a PR, verify:
- [ ] Configuration syntax is valid
- [ ] Docker image builds successfully  
- [ ] Container starts and runs healthily
- [ ] Configuration reloading works
- [ ] Log messages are received and written correctly
- [ ] No regression in existing functionality
- [ ] Documentation is updated

### Testing Environments

Test in multiple environments when possible:
- **Linux**: Native Docker or VM
- **macOS**: Docker Desktop or Multipass
- **Windows**: Docker Desktop or WSL2

## Release Process

### Versioning

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version numbers
2. Update CHANGELOG.md
3. Test thoroughly
4. Create release tag
5. Update Docker images
6. Update documentation

## Getting Help

- **Questions**: Open a discussion or configuration help issue
- **Problems**: Search existing issues or create a bug report
- **Ideas**: Create a feature request

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for helping make syslogng-dynamic better!
