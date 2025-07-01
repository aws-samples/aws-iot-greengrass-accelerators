# AWS IoT Greengrass V2 Docker Stack Upgrade Plan

## Current State Analysis

### Current Configuration
- **Base OS**: Amazon Linux 2
- **Greengrass Version**: 2.10.3 (Released ~2023)
- **Python Versions**: 3.7 + 3.8 (via amazon-linux-extras)
- **Java Version**: Java 11 (Amazon Corretto)
- **Docker Image**: `x86_64/aws-iot-greengrass-v2:2.10.3`

### Issues Identified
1. **Outdated Greengrass**: v2.10.3 vs latest v2.14.3 (missing 4 major releases)
2. **Legacy Python**: Python 3.7/3.8 vs recommended 3.11/3.12
3. **Amazon Linux 2**: In maintenance mode, AL2023 available
4. **Java 11**: Java 17/21 LTS available with better performance
5. **Single-stage build**: Inefficient, large image size
6. **Security concerns**: Running as root, unnecessary packages

## Upgrade Strategy

### Phase 1: Base Infrastructure (Priority: High)
**Timeline: 2-3 hours**

#### 1.1 Amazon Linux 2023 Migration
```dockerfile
# Current
FROM amazonlinux:2

# Target
FROM amazonlinux:2023
```

**Benefits:**
- Modern package manager (dnf vs yum)
- Better security updates
- Native Python 3.11+ support
- Optimized for containers

#### 1.2 Python Stack Modernization
```dockerfile
# Current
RUN amazon-linux-extras enable python3.8 && yum install -y python3.8

# Target
RUN dnf install -y python3.11 python3.11-pip
```

**Benefits:**
- 10-60% performance improvement
- Better typing and async support
- Modern library compatibility
- Security patches

#### 1.3 Java Runtime Upgrade
```dockerfile
# Current
RUN yum install -y java-11-amazon-corretto-headless

# Target
RUN dnf install -y java-17-amazon-corretto-headless
```

**Benefits:**
- Performance improvements (15-20%)
- Better memory management
- Extended LTS support until 2029

### Phase 2: Greengrass Core Update (Priority: High)
**Timeline: 1-2 hours**

#### 2.1 Version Bump
```dockerfile
# Current
ARG GREENGRASS_RELEASE_VERSION=2.10.3

# Target
ARG GREENGRASS_RELEASE_VERSION=2.14.3
```

#### 2.2 Configuration Updates
- Review breaking changes in 2.11.x - 2.14.x
- Update component versions in config.yaml.template
- Validate Lambda runtime compatibility

### Phase 3: Container Optimization (Priority: Medium)
**Timeline: 3-4 hours**

#### 3.1 Multi-stage Build Implementation
```dockerfile
# Build stage
FROM amazonlinux:2023 AS builder
RUN dnf install -y wget unzip
# Download and prepare Greengrass

# Runtime stage
FROM amazonlinux:2023 AS runtime
COPY --from=builder /opt/greengrassv2 /opt/greengrassv2
# Minimal runtime dependencies only
```

#### 3.2 Security Hardening
```dockerfile
# Create non-root user
RUN groupadd -r greengrass && useradd -r -g greengrass greengrass
USER greengrass

# Minimal package installation
RUN dnf install -y --setopt=install_weak_deps=False \
    python3.11 java-17-amazon-corretto-headless && \
    dnf clean all
```

### Phase 4: Development Experience (Priority: Low)
**Timeline: 2-3 hours**

#### 4.1 Build System Enhancements
- Docker Buildx for multi-arch builds
- Build caching optimization
- Health checks and monitoring

#### 4.2 Configuration Management
- Environment-based configuration
- Secrets management integration
- Improved logging and debugging

## Implementation Checklist

### Pre-Implementation
- [ ] Backup current working configuration
- [ ] Review Greengrass 2.11-2.14 release notes
- [ ] Test current setup functionality
- [ ] Document current component versions

### Phase 1: Base Infrastructure
- [ ] Update Dockerfile to Amazon Linux 2023
- [ ] Migrate from yum to dnf package manager
- [ ] Update Python to 3.11/3.12
- [ ] Update Java to 17 or 21
- [ ] Test basic container build
- [ ] Validate package installations

### Phase 2: Greengrass Update
- [ ] Update Greengrass version to 2.14.3
- [ ] Update config.yaml.template
- [ ] Review component compatibility
- [ ] Test Greengrass installation
- [ ] Validate core functionality

### Phase 3: Container Optimization
- [ ] Implement multi-stage build
- [ ] Add security hardening
- [ ] Optimize image size
- [ ] Add health checks
- [ ] Performance testing

### Phase 4: Testing & Validation
- [ ] Build new Docker image
- [ ] Test container startup
- [ ] Validate Greengrass core functionality
- [ ] Test component deployment
- [ ] Performance benchmarking
- [ ] Security scanning

## Risk Assessment

### High Risk
- **Breaking changes** in Greengrass 2.11-2.14
- **Python compatibility** issues with existing components
- **Java runtime** compatibility with Lambda functions

### Medium Risk
- **Amazon Linux 2023** package differences
- **Container size** increase during transition
- **Build time** increase with multi-stage builds

### Low Risk
- **Configuration** template updates
- **Environment variable** changes
- **Documentation** updates

## Rollback Plan

1. **Git tags** for each phase
2. **Docker image versioning** strategy
3. **Configuration backups**
4. **Component version pinning**
5. **Automated testing** for validation

## Success Metrics

### Performance
- [ ] Container startup time < 30 seconds
- [ ] Image size reduction by 20%+
- [ ] Memory usage optimization
- [ ] CPU performance improvement

### Security
- [ ] Zero critical vulnerabilities
- [ ] Non-root execution
- [ ] Minimal attack surface
- [ ] Updated security patches

### Maintainability
- [ ] Modern toolchain
- [ ] Clear documentation
- [ ] Automated testing
- [ ] CI/CD integration

## Timeline Summary

| Phase | Duration | Priority | Dependencies |
|-------|----------|----------|--------------|
| Phase 1: Base Infrastructure | 2-3 hours | High | None |
| Phase 2: Greengrass Update | 1-2 hours | High | Phase 1 |
| Phase 3: Container Optimization | 3-4 hours | Medium | Phase 2 |
| Phase 4: Development Experience | 2-3 hours | Low | Phase 3 |
| **Total** | **8-12 hours** | | |

## Next Steps

1. **Immediate**: Begin Phase 1 implementation
2. **Research**: Review Greengrass 2.11-2.14 changelogs
3. **Testing**: Set up validation environment
4. **Documentation**: Update README and deployment guides

---

**Note**: This plan prioritizes stability and security while modernizing the stack. Each phase can be implemented and tested independently, allowing for incremental rollout and validation.
