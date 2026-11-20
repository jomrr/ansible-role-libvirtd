# Ansible Role: libvirtd

![GitHub](https://img.shields.io/github/license/jomrr/ansible-role-libvirtd)
![GitHub last commit](https://img.shields.io/github/last-commit/jomrr/ansible-role-libvirtd)
![GitHub issues](https://img.shields.io/github/issues-raw/jomrr/ansible-role-libvirtd)
[![dev](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-libvirtd/dev.yml?branch=dev&label=dev)](https://github.com/jomrr/ansible-role-libvirtd/actions/workflows/dev.yml?query=branch%3Adev)
[![main](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-libvirtd/main.yml?branch=main&label=main)](https://github.com/jomrr/ansible-role-libvirtd/actions/workflows/main.yml?query=branch%3Amain)

Ansible role for a QEMU/KVM host with libvirt management and GuestFS tools.

## Purpose

Install and configure a functional libvirt QEMU/KVM host with running system
services,
virsh, virt-install, UEFI firmware and GuestFS image maintenance tools.
Provide the drivers for virtual machines, local storage pools and volumes,
virtual networks, network filters, secrets and host devices.

## Scope

### Managed

- Distribution-specific virtualization packages, optional extra packages and
  service activation.
- Supplementary libvirt group membership for selected local users.
- Optional QEMU driver and guest lifecycle configuration.
- Activation of libvirt-guests and removal of monolithic service activation on
  modular platforms.
- System libvirt access for virsh and API clients such as the OpenTofu libvirt
  provider.
- GuestFS tools for offline image customization, inspection, resizing and
  template preparation.

### Not Managed

- Virtual machine, storage pool and custom network definitions.
- SSH accounts, remote access credentials and TCP or TLS listeners.
- Hardware virtualization settings and guest operating system configuration.

## Requirements

- An x86_64 host with systemd and hardware virtualization enabled for KVM
  guests.

## Dependencies

```yaml
collections:
  - name: community.general
    version: '>=12.0.0'
  - name: ansible.posix
    version: '>=2.0.0'
```

## Role Variables

### `libvirtd_extra_packages`

Type: `list`. Required: `false`.

Additional distribution packages installed alongside the virtualization tools,
such as storage backend drivers.

Default:

```yaml
libvirtd_extra_packages: []
```

### `libvirtd_users`

Type: `list`. Required: `false`.

Local users added to the libvirt group without removing other supplementary
memberships. Missing users are created.

Default:

```yaml
libvirtd_users: []
```

### `libvirtd_qemu_config`

Type: `dict`. Required: `false`.

Settings for /etc/libvirt/qemu.conf, using native YAML integers, strings or
lists of strings.
A nonempty mapping replaces the complete file and restarts the platform QEMU
daemon when changed.
An empty mapping leaves the file unchanged, including any previously managed
configuration.

Default:

```yaml
libvirtd_qemu_config: {}
```

### `libvirtd_guests_config`

Type: `dict`. Required: `false`.

Uppercase libvirt-guests settings with string or integer values, quoted as shell
assignments.
Uses /etc/default/libvirt-guests on Debian families and
/etc/sysconfig/libvirt-guests on RPM families.
A nonempty mapping replaces the complete file; an empty mapping leaves the file
unchanged.
Changes apply to the next service action without restarting the service or
interrupting running guests.

Default:

```yaml
libvirtd_guests_config: {}
```

### `libvirtd_guests_enabled`

Type: `bool`. Required: `false`.

Enable and start libvirt-guests for guest lifecycle handling at host boot and
shutdown.
False disables boot activation without stopping an already active service or its
guests.

Default:

```yaml
libvirtd_guests_enabled: true
```

## Managed Files

- `/etc/libvirt/qemu.conf` Managed when libvirtd_qemu_config is nonempty;
  root-owned with mode 0600.
- `/etc/default/libvirt-guests` Debian families, managed when
  libvirtd_guests_config is nonempty.
- `/etc/sysconfig/libvirt-guests` RPM families, managed when
  libvirtd_guests_config is nonempty.

## Check Mode

Package, user, configuration and service tasks support check mode.

- User, configuration and service operations are deferred when check mode
  predicts package changes because their prerequisites may not exist.

## Service Behavior

Enable the platform's libvirt services and local sockets, including VM autostart
support.
Modular deployments provide the traditional libvirt management socket through
virtproxyd.
Installed libvirtd services and sockets are stopped and disabled before modular
services start;
absent monolithic units require no action.
libvirt-guests is enabled and started by default. Setting
libvirtd_guests_enabled to false
disables boot activation without invoking the stop action on running guests.

### Handlers

- QEMU configuration changes restart virtqemud.service on modular platforms or
  libvirtd.service on Debian families.
- Guest lifecycle configuration is read on the next service action without a
  service restart.

## Security Notes

- Membership in the libvirt group grants privileged access to host
  virtualization.

## Operational Notes

- The role is idempotent.
- RPM platforms select individual drivers and QEMU components instead of the
  libvirt-daemon-kvm metapackage.
- GuestFS tools operate on image contents; shut down a VM before modifying its
  disk images.
- OpenTofu can manage domains, networks, pools and volumes through the supplied
  libvirt API; remote authentication is configured separately.
- Molecule verifies services, the system API, networking and storage in isolated
  containers; VM and GuestFS execution use KVM when available and QEMU software
  emulation otherwise.

## Supported Platforms

| OS Family | Distribution | Version | Container Image |
| --------- | ------------ | ------- | --------------- |
| RedHat | AlmaLinux | latest | [jomrr/molecule-almalinux:latest](https://hub.docker.com/r/jomrr/molecule-almalinux) |
| Debian | Debian | latest | [jomrr/molecule-debian:latest](https://hub.docker.com/r/jomrr/molecule-debian) |
| RedHat | Fedora | latest | [jomrr/molecule-fedora:latest](https://hub.docker.com/r/jomrr/molecule-fedora) |
| Suse | OpenSuse Leap | latest | [jomrr/molecule-opensuse-leap:latest](https://hub.docker.com/r/jomrr/molecule-opensuse-leap) |
| Suse | OpenSuse Tumbleweed | latest | [jomrr/molecule-opensuse-tumbleweed:latest](https://hub.docker.com/r/jomrr/molecule-opensuse-tumbleweed) |
| Debian | Ubuntu | latest | [jomrr/molecule-ubuntu:latest](https://hub.docker.com/r/jomrr/molecule-ubuntu) |

## Example Playbook

### Configure a virtualization host

Select extra packages using distribution package names. Nonempty
configuration mappings own the complete corresponding file; include all
desired settings. Empty mappings leave files unchanged.
QEMU strings and lists are quoted automatically. auto_start_delay is
measured in milliseconds; libvirt-guests START_DELAY and
SHUTDOWN_TIMEOUT are measured in seconds.

```yaml
---
- name: Configure virtualization hosts
  hosts: hypervisors
  gather_facts: true
  roles:
    - role: jomrr.libvirtd
      libvirtd_extra_packages:
        - libvirt-daemon-driver-storage-logical
      libvirtd_users:
        - operator
      libvirtd_qemu_config:
        auto_start_delay: 1000
      libvirtd_guests_config:
        URIS: qemu:///system
        ON_BOOT: start
        ON_SHUTDOWN: shutdown
        SHUTDOWN_TIMEOUT: 300
      libvirtd_guests_enabled: true
```

## References

- [Debian Wiki](https://wiki.debian.org/KVM)
- [Fedora Documentation](https://docs.fedoraproject.org/en-US/quick-docs/virtualization-getting-started/)
- [Libvirt RPM deployment](https://libvirt.org/kbase/rpm-deployment.html)
- [Libvirt daemons](https://libvirt.org/daemons.html)
- [Libguestfs tools](https://libguestfs.org/)
- [Ubuntu Documentation](https://help.ubuntu.com/community/KVM/Installation)

## Author

[Jonas Mauer](https://github.com/jomrr)

## License

This project is licensed under the MIT License.
See [LICENSE](LICENSE) for the full license text.

Copyright (c) 2024 Jonas Mauer.
