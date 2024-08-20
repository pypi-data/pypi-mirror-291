import glob
from pathlib import Path

from .pcidevice import PCIDevice
from .amdgpu import AmdGpuDeviceDB
from .devicetree import DeviceTreeGPU
from .intel import IntelI915GpuDeviceDB, IntelXeGpuDeviceDB
from .nvidia import NvidiaGpuDeviceDB
from .virt import VirtIOGpuDeviceDB
from .radeon import RadeonGpuDeviceDB
from .gfxinfo_vulkan import VulkanInfo


SUPPORTED_GPU_DBS = [AmdGpuDeviceDB(), IntelXeGpuDeviceDB(), IntelI915GpuDeviceDB(),
                     NvidiaGpuDeviceDB(), VirtIOGpuDeviceDB(), RadeonGpuDeviceDB()]


def pci_devices():
    def readfile(path, default=None):
        try:
            with open(path) as f:
                return f.read().strip()
        except Exception:
            return default

    pciids = []
    pci_dev_root = Path("/sys/bus/pci/devices/")
    for pci_dev_path in pci_dev_root.iterdir():
        vendor = readfile(pci_dev_path / "vendor")
        device = readfile(pci_dev_path / "device")
        revision = readfile(pci_dev_path / "revision")
        subsystem_vendor = readfile(pci_dev_path / "subsystem_vendor", "0x0")
        subsystem_device = readfile(pci_dev_path / "subsystem_device", "0x0")

        if vendor and device and revision:
            pci_dev = PCIDevice(vendor_id=int(vendor, 16),
                                product_id=int(device, 16),
                                revision=int(revision, 16),
                                subsys_vendor_id=int(subsystem_vendor, 16),
                                subsys_product_id=int(subsystem_device, 16))
            pciids.append(pci_dev)

    return pciids


def find_gpu(allow_db_updates=True):
    def find_devicetree_gpu():
        for path in glob.glob("/proc/device-tree/gpu*/compatible") + \
                glob.glob("/sys/bus/platform/devices/*gpu/of_node/compatible"):
            try:
                with open(path) as f:
                    return DeviceTreeGPU.from_compatible_str(f.read())
            except OSError:
                pass

    def find_pci_gpu():
        devices = pci_devices()

        for pci_device in devices:
            for gpu_db in SUPPORTED_GPU_DBS:
                if gpu := gpu_db.from_pciid(pci_device):
                    return gpu

        # We could not find the GPU in our databases, update them
        if allow_db_updates:
            for gpu_db in SUPPORTED_GPU_DBS:
                gpu_db.update()

            # Retry, now that we have updated our DBs
            for pci_device in devices:
                for gpu_db in SUPPORTED_GPU_DBS:
                    if gpu := gpu_db.from_pciid(pci_device):
                        return gpu

    """For now we only support single-gpu DUTs"""
    if gpu := find_devicetree_gpu():
        return gpu
    elif gpu := find_pci_gpu():
        return gpu
    else:
        return None


def cache_db():
    for gpu_db in SUPPORTED_GPU_DBS:
        gpu_db.cache_db()


def check_db():
    result = True
    for gpu_db in SUPPORTED_GPU_DBS:
        if not gpu_db.check_db():
            result = False
    return result


def find_gpu_from_pciid(pciid):
    for gpu_db in SUPPORTED_GPU_DBS:
        if gpu := gpu_db.from_pciid(pciid):
            return gpu

    # We could not find the GPU, retry with updated DBs
    for gpu_db in SUPPORTED_GPU_DBS:
        gpu_db.update()
        if gpu := gpu_db.from_pciid(pciid):
            return gpu


__all__ = ['pci_devices', 'find_gpu', 'cache_db', 'VulkanInfo']
