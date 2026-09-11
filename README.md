# Ansible Role: libvirtd

![GitHub](https://img.shields.io/github/license/jomrr/ansible-role-libvirtd)
![GitHub last commit](https://img.shields.io/github/last-commit/jomrr/ansible-role-libvirtd)
![GitHub issues](https://img.shields.io/github/issues-raw/jomrr/ansible-role-libvirtd)
[![dev](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-libvirtd/dev.yml?branch=dev&event=push&label=dev)](https://github.com/jomrr/ansible-role-libvirtd/actions/workflows/dev.yml?query=branch%3Adev)
[![main](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-libvirtd/main.yml?branch=main&event=push&label=main)](https://github.com/jomrr/ansible-role-libvirtd/actions/workflows/main.yml?query=branch%3Amain)

Ansible role for a QEMU/KVM host with libvirt management and GuestFS tools.

## Purpose

Install and configure a functional libvirt QEMU/KVM host with running system
services,
virsh, virt-install, UEFI firmware and GuestFS image maintenance tools.
Provide the drivers for virtual machines, local storage pools and volumes,
virtual networks, network filters, secrets and host devices.

## Scope

### Managed

- Distribution-specific virtualization packages and service activation.
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
- Distribution repositories containing the virtualization and GuestFS packages.
- Root access for package installation and service management.

## Dependencies

```yaml
collections:
  - name: community.general
    version: '>=12.0.0'
```

## Role Variables

No public role variable interface is declared in `meta/argument_specs.yml`.

## Check Mode

Package and service tasks support check mode.

- On a fresh host, service operations are deferred when check mode predicts
  package changes because the units do not yet exist.

## Service Behavior

Enable the platform's libvirt services and local sockets, including VM autostart
support.
Modular deployments provide the traditional libvirt management socket through
virtproxyd.

## Operational Notes

- The role is idempotent.
- The supported distributions and test matrix follow the generator's default
  platforms.
- RPM platforms select individual drivers and QEMU components instead of the
  libvirt-daemon-kvm metapackage.
- GuestFS tools operate on image contents; shut down a VM before modifying its
  disk images.
- OpenTofu can manage domains, networks, pools and volumes through the supplied
  libvirt API; remote authentication is configured separately.
- Molecule uses isolated containers with KVM and TUN access; container-specific
  QEMU settings belong to test fixtures only.

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

### Simple example playbook

Minimal example for applying this role.

```yaml
---
- name: "Configure libvirtd"
  hosts: "libvirtd"
  gather_facts: true
  roles:
    - role: "jomrr.libvirtd"
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
