"""Exercise the installed libvirt system API and GuestFS image tools."""

from collections.abc import Mapping
import json
import os
from pathlib import Path
import subprocess
import tempfile
import uuid
from xml.etree import ElementTree


URI = "qemu+unix:///system?socket=/run/libvirt/libvirt-sock"


def run(*args: str, env: Mapping[str, str] | None = None) -> str:
    """Run a fixture operation and retain its output for behavioral assertions."""
    result = subprocess.run(
        args,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        timeout=300,
        env=env,
    )
    return result.stdout.strip()


def virsh(*args: str) -> str:
    """Use the shared management socket consumed by external API clients."""
    return run("virsh", "--connect", URI, *args)


def verify_management(root: Path, name: str) -> None:
    """Create and remove a KVM domain with a network and storage volume."""
    virsh("list", "--all")
    capabilities = ElementTree.fromstring(virsh("capabilities"))
    assert capabilities.find(".//domain[@type='kvm']") is not None
    pool = root / "pool"
    pool.mkdir()
    virsh("pool-define-as", name, "dir", "--target", str(pool))
    virsh("pool-start", name)
    virsh("vol-create-as", name, "disk.qcow2", "32M", "--format", "qcow2")
    disk = virsh("vol-path", "disk.qcow2", "--pool", name)
    info = json.loads(run("qemu-img", "info", "--output=json", disk))
    assert info["format"] == "qcow2"
    network = root / "network.xml"
    network.write_text(
        f"<network><name>{name}</name>"
        "<bridge name='virbr-test'/>"
        "<ip address='192.0.2.1' netmask='255.255.255.0'>"
        "<dhcp><range start='192.0.2.10' end='192.0.2.20'/></dhcp>"
        "</ip></network>",
        encoding="utf-8",
    )
    virsh("net-define", str(network))
    virsh("net-start", name)
    domain = root / "domain.xml"
    domain.write_text(
        run(
            "virt-install",
            "--connect",
            URI,
            "--name",
            name,
            "--memory",
            "128",
            "--vcpus",
            "1",
            "--import",
            "--osinfo",
            "detect=off,name=generic",
            "--boot",
            "hd",
            "--disk",
            f"path={disk},format=qcow2,bus=virtio",
            "--network",
            f"network={name}",
            "--graphics",
            "none",
            "--print-xml",
        ),
        encoding="utf-8",
    )
    virsh("create", str(domain), "--paused")
    assert virsh("domstate", name) == "paused"
    virsh("destroy", name)
    virsh("net-destroy", name)
    virsh("net-undefine", name)
    virsh("vol-delete", "disk.qcow2", "--pool", name)
    virsh("pool-destroy", name)
    virsh("pool-undefine", name)


def verify_guestfs(root: Path, name: str) -> None:
    """Build a filesystem image and read a file through the GuestFS appliance."""
    source = root / "source"
    source.mkdir()
    (source / "marker").write_text(name, encoding="utf-8")
    image = root / "guestfs.img"
    environment = dict(os.environ, LIBGUESTFS_BACKEND="direct")
    run(
        "virt-make-fs",
        "--type=ext4",
        "--size=64M",
        str(source),
        str(image),
        env=environment,
    )
    content = run(
        "virt-cat",
        "-a",
        str(image),
        "-m",
        "/dev/sda",
        "/marker",
        env=environment,
    )
    assert content == name, content


def main() -> None:
    """Run isolated fixtures inside a disposable Molecule container."""
    name = "molecule-libvirtd-" + uuid.uuid4().hex[:8]
    with tempfile.TemporaryDirectory(prefix=name) as directory:
        root = Path(directory)
        verify_management(root, name)
        verify_guestfs(root, name)
    print("Verified KVM domain, network, volume, pool and GuestFS image access")


if __name__ == "__main__":
    main()
