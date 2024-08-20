from dataclasses import dataclass


@dataclass
class PCIDevice:
    vendor_id: int
    product_id: int
    revision: int

    subsys_vendor_id: int = 0
    subsys_product_id: int = 0

    def __hash__(self):
        return hash((self.vendor_id, self.product_id, self.revision, self.subsys_vendor_id, self.subsys_product_id))

    def __str__(self):
        s = f"{hex(self.vendor_id)}:{hex(self.product_id)}:{hex(self.revision)}"
        if self.subsys_vendor_id > 0 or self.subsys_product_id > 0:
            s += f":{hex(self.subsys_vendor_id)}:{hex(self.subsys_product_id)}"
        return s

    @classmethod
    def from_str(cls, pciid):
        fields = pciid.split(":")
        if len(fields) not in [2, 3, 5]:
            raise ValueError("The pciid '{pciid}' is invalid. Format: xxxx:xxxx[:xx] or xxxx:xxxx:xx:xxxx:xxxx]")

        revision = 0 if len(fields) < 3 else int(fields[2], 16)
        subsys_vendor_id = 0 if len(fields) < 5 else int(fields[3], 16)
        subsys_product_id = 0 if len(fields) < 5 else int(fields[4], 16)

        return cls(vendor_id=int(fields[0], 16),
                   product_id=int(fields[1], 16),
                   revision=revision,
                   subsys_vendor_id=subsys_vendor_id,
                   subsys_product_id=subsys_product_id)
