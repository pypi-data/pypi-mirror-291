from dataclasses import dataclass

from .gpudb import GpuDevice

import sys


@dataclass
class DeviceTreeGPU(GpuDevice):
    vendor: str
    model: str

    @property
    def codename(self):
        codenames = {
            ("qcom", "adreno-43050a01"): "a740",
            ("qcom", "adreno-43051401"): "a750",
        }

        return codenames.get((self.vendor, self.model))

    @property
    def base_name(self):
        return f'{self.vendor}-{self.codename or self.model}'

    @property
    def pci_device(self):
        return None

    @property
    def tags(self):
        tags = {
            f"dt_gpu:vendor:{self.vendor}",
            f"dt_gpu:model:{self.model}",
        }

        if self.codename:
            tags.add(f"dt_gpu:codename:{self.codename}")

        return tags

    @property
    def structured_tags(self):
        tags = {
            "type": "devicetree",
            "vendor": self.vendor,
            "model": self.model
        }

        if self.codename:
            tags["codename"] = self.codename

        return tags

    def __str__(self):
        return f"<DeviceTreeGPU: {self.vendor}/{self.codename or self.model}>"

    @classmethod
    def from_compatible_str(cls, compatible):
        main_compatible = compatible.split('\0')[0]

        fields = main_compatible.split(',')
        if len(fields) == 2:
            return cls(vendor=fields[0], model=fields[1])
        else:
            print(f"ERROR: The compatible '{main_compatible}' is not following the expected format 'vendor,model'",
                  file=sys.stderr)
            return None
