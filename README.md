# Ansible role libvirtd

![GitHub](https://img.shields.io/github/license/jomrr/ansible-role-libvirtd) ![GitHub last commit](https://img.shields.io/github/last-commit/jomrr/ansible-role-libvirtd) ![GitHub issues](https://img.shields.io/github/issues-raw/jomrr/ansible-role-libvirtd)

**Ansible role for installing libvirt-daemon and tools.**

## Description

Install libvirtd, client tools and qemu-kvm packags on supported systems.


## Prerequisites

This role has no special prerequisites.

### System packages (Fedora)

- `python3` (Python 3.6 or later)

### Python (requirements.txt)

- ansible >= 2.15

## Dependencies (requirements.yml)

This role has no dependencies.

## Supported Platforms

| OS Family | Distribution | Version | Container Image |
|-----------|--------------|---------|-----------------|
| Alpine | Alpine | 3.18 | [jomrr/molecule-alpine:3.18]( https://hub.docker.com/r/jomrr/molecule-alpine ) |
| | | 3.19 | [jomrr/molecule-alpine:3.19]( https://hub.docker.com/r/jomrr/molecule-alpine ) |
| Archlinux | ArchLinux | latest | [jomrr/molecule-archlinux:latest]( https://hub.docker.com/r/jomrr/molecule-archlinux ) |
| Debian | Debian | 11 | [jomrr/molecule-debian:11]( https://hub.docker.com/r/jomrr/molecule-debian ) |
| | | 12 | [jomrr/molecule-debian:12]( https://hub.docker.com/r/jomrr/molecule-debian ) |
| Debian | Ubuntu | 20.04 | [jomrr/molecule-ubuntu:20.04]( https://hub.docker.com/r/jomrr/molecule-ubuntu ) |
| | | 22.04 | [jomrr/molecule-ubuntu:22.04]( https://hub.docker.com/r/jomrr/molecule-ubuntu ) |
| RedHat | AlmaLinux | 8 | [jomrr/molecule-almalinux:8]( https://hub.docker.com/r/jomrr/molecule-almalinux ) |
| | | 9 | [jomrr/molecule-almalinux:9]( https://hub.docker.com/r/jomrr/molecule-almalinux ) |
| RedHat | Fedora | 39 | [jomrr/molecule-fedora:39]( https://hub.docker.com/r/jomrr/molecule-fedora ) |
| | | 40 | [jomrr/molecule-fedora:40]( https://hub.docker.com/r/jomrr/molecule-fedora ) |
| | | rawhide | [jomrr/molecule-fedora:rawhide]( https://hub.docker.com/r/jomrr/molecule-fedora ) |
| RedHat | OracleLinux | 8 | [jomrr/molecule-oraclelinux:8]( https://hub.docker.com/r/jomrr/molecule-oraclelinux ) |
| | | 9 | [jomrr/molecule-oraclelinux:9]( https://hub.docker.com/r/jomrr/molecule-oraclelinux ) |

## Role Variables

No role default variables specified, see [defaults/main.yml](defaults/main.yml).

## Example Playbook

Example(s) of how to use this role:

## The default example playbook

The default example playbook for the role.

```yaml
---
# name: "jomrr.libvirtd"
# file: "libvirtd.yml"
- hosts: libvirtd
  gather_facts: true
  roles:
    - role: "jomrr.libvirtd"

```

## License

This role is published under the [MIT License](LICENSE).

## Author Information

This role was created in 2024 by Jonas Mauer (@jomrr).

## Contributing

Contributions to this role are welcome.
Please follow the steps described in [CONTRIBUTING.md](CONTRIBUTING.md).

## References

The following are the default variables that should be adjusted:

- [ArchWiki](https://wiki.archlinux.org/index.php/Libvirt)
- [Fedora Documentation](https://docs.fedoraproject.org/en-US/quick-docs/virtualization-getting-started/)

---
