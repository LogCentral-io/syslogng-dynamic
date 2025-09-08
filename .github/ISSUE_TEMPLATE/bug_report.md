---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment (please complete the following information):**
- OS: [e.g. Ubuntu 22.04, macOS 13.0, Windows 11]
- Docker version: [e.g. 24.0.0]
- Docker Compose version: [e.g. 2.20.0]
- Container runtime: [e.g. Docker Desktop, Multipass, native Docker]

**Configuration**
Please provide relevant configuration files:
- syslog-ng configuration snippets
- docker-compose.yml modifications
- Environment variables

**Logs**
Please include relevant log output:
```
# Container logs
docker compose logs syslog-ng

# Syslog-ng logs
tail -f logs/*.log
```

**Additional context**
Add any other context about the problem here.

**Checklist**
- [ ] I have searched existing issues
- [ ] I have tested with the latest version
- [ ] I have included all relevant configuration
- [ ] I have included log output
