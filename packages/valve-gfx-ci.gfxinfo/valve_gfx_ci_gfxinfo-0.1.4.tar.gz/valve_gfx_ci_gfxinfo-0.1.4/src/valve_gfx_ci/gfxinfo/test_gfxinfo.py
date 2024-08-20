from unittest.mock import patch, MagicMock
from urllib.parse import urlparse

import contextlib
import io
import unittest
import os

from gfxinfo import SUPPORTED_GPU_DBS, PCIDevice, DeviceTreeGPU

from .amdgpu import AMDGPU, AmdGpuDeviceDB
from .radeon import RadeonGPU, RadeonGpuDeviceDB
from .intel import IntelGPU, IntelI915GpuDeviceDB
from .nvidia import NvidiaGPU, NvidiaGpuDeviceDB
from .virt import VirtGPU


class DatabaseTests(unittest.TestCase):
    def test_check_db(self):
        for gpu_db in SUPPORTED_GPU_DBS:
            with self.subTest(GPU_DB=type(gpu_db).__name__):
                self.assertTrue(gpu_db.check_db())


class PCIDeviceTests(unittest.TestCase):
    def test_hash(self):
        self.assertEqual(hash(PCIDevice(0x1234, 0x5678, 0x9a)),
                         hash((0x1234, 0x5678, 0x9a, 0, 0)))

        self.assertEqual(hash(PCIDevice(0x1234, 0x5678, 0x9a, 0xbcde, 0xf012)),
                         hash((0x1234, 0x5678, 0x9a, 0xbcde, 0xf012)))

    def test_str(self):
        self.assertEqual(str(PCIDevice(0x1234, 0x5678, 0x9a)), "0x1234:0x5678:0x9a")
        self.assertEqual(str(PCIDevice(0x1234, 0x5678, 0x9a, 0xbcde, 0xf012)),
                         "0x1234:0x5678:0x9a:0xbcde:0xf012")

    def test_from_str(self):
        self.assertEqual(PCIDevice.from_str("1234:5678:9a"), PCIDevice(0x1234, 0x5678, 0x9a))
        self.assertEqual(PCIDevice.from_str("0x1234:0x5678:0x9a"), PCIDevice(0x1234, 0x5678, 0x9a))

        self.assertEqual(PCIDevice.from_str("0x1234:5678"), PCIDevice(0x1234, 0x5678, 0x0))

        with self.assertRaises(ValueError):
            self.assertEqual(PCIDevice.from_str("0x1234:5678:0x12:045"), PCIDevice(0x1234, 0x5678, 0x0))


class DeviceTreeGPUTests(unittest.TestCase):
    def setUp(self):
        self.gpu = DeviceTreeGPU.from_compatible_str("brcm,bcm2711-vc5\0brcm,bcm2835-vc4\0")
        self.known_gpu = DeviceTreeGPU.from_compatible_str("qcom,adreno-43050a01\0qcom,adreno\0")

    def test_codename(self):
        self.assertIsNone(self.gpu.codename)
        self.assertEqual(self.known_gpu.codename, "a740")

    def test_base_name(self):
        self.assertEqual(self.gpu.base_name, "brcm-bcm2711-vc5")
        self.assertEqual(self.known_gpu.base_name, "qcom-a740")

    def test_pciid(self):
        self.assertIsNone(self.gpu.pciid)

    def test_pci_device(self):
        self.assertIsNone(self.gpu.pci_device)

    def test_tags(self):
        self.assertEqual(self.gpu.tags, {"dt_gpu:vendor:brcm", "dt_gpu:model:bcm2711-vc5"})
        self.assertEqual(self.known_gpu.tags, {"dt_gpu:vendor:qcom", "dt_gpu:model:adreno-43050a01",
                                               "dt_gpu:codename:a740"})

    def test_structured_tags(self):
        self.assertEqual(self.gpu.structured_tags,
                         {"type": "devicetree",
                          "vendor": "brcm",
                          "model": "bcm2711-vc5"})

        self.assertEqual(self.known_gpu.structured_tags,
                         {"type": "devicetree",
                          "vendor": "qcom",
                          "model": "adreno-43050a01",
                          "codename": "a740"})

    def test_str(self):
        self.assertEqual(str(self.gpu), "<DeviceTreeGPU: brcm/bcm2711-vc5>")
        self.assertEqual(str(self.known_gpu), "<DeviceTreeGPU: qcom/a740>")

    def test_from_compatible_str(self):
        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            self.assertIsNone(DeviceTreeGPU.from_compatible_str("brcm,bcm2711-vc5,extra"))

        self.assertEqual(f.getvalue(), ("ERROR: The compatible 'brcm,bcm2711-vc5,extra' is not "
                                        "following the expected format 'vendor,model'\n"))

    def test_unknown_fields(self):
        self.assertEqual(self.gpu.unknown_fields, set())


class AMDGPUTests(unittest.TestCase):
    def setUp(self):
        self.pci_device = PCIDevice(vendor_id=0x1002, product_id=0x163F, revision=0xAE)
        self.gpu = AMDGPU(pci_device=self.pci_device, asic_type="GFX10_3_3",
                          is_APU=True, marketing_name="AMD Custom GPU 0405 / Steam Deck")

    def test_pciid(self):
        assert self.gpu.pciid == str(self.pci_device)

    def test_some_devices(self):
        self.assertEqual(self.gpu.codename, "VANGOGH")
        self.assertIsNone(self.gpu.family)
        self.assertEqual(self.gpu.architecture, "RDNA2")
        self.assertEqual(self.gpu.base_name, "gfx10-vangogh")
        self.assertTrue(self.gpu.is_APU)
        self.assertEqual(self.gpu.unknown_fields, set())
        self.assertEqual(self.gpu.tags, {'amdgpu:generation:10', 'amdgpu:architecture:RDNA2',
                                         'amdgpu:codename:VANGOGH', 'amdgpu:pciid:0x1002:0x163f:0xae',
                                         'amdgpu:integrated'})
        self.assertEqual(self.gpu.structured_tags, {
            'APU': True,
            'architecture': 'RDNA2',
            'codename': 'VANGOGH',
            'family': None,
            'generation': 10,
            'gfxversion': 'gfx10',
            'integrated': True,
            'marketing_name': "AMD Custom GPU 0405 / Steam Deck",
            'pciid': '0x1002:0x163f:0xae',
            'type': 'amdgpu'
        })

        renoir = AMDGPU(pci_device=self.pci_device, asic_type="GFX9_0_C", is_APU=True, marketing_name="Marketing name")
        self.assertEqual(renoir.codename, "RENOIR")
        self.assertEqual(renoir.family, "AI")
        self.assertEqual(renoir.architecture, "GCN5.1")
        self.assertEqual(renoir.base_name, "gfx9-renoir")
        self.assertTrue(renoir.is_APU)
        self.assertEqual(renoir.unknown_fields, set())
        self.assertEqual(renoir.tags, {'amdgpu:generation:9', 'amdgpu:architecture:GCN5.1',
                                       'amdgpu:codename:RENOIR', 'amdgpu:pciid:0x1002:0x163f:0xae',
                                       'amdgpu:integrated', 'amdgpu:family:AI'})
        self.assertEqual(renoir.structured_tags, {
            'APU': True,
            'architecture': 'GCN5.1',
            'codename': 'RENOIR',
            'family': "AI",
            'generation': 9,
            'gfxversion': 'gfx9',
            'integrated': True,
            'marketing_name': 'Marketing name',
            'pciid': '0x1002:0x163f:0xae',
            'type': 'amdgpu'
        })
        self.assertEqual(str(renoir), "<AMDGPU: PCIID 0x1002:0x163f:0xae - RENOIR - AI - GCN5.1 - gfx9>")

        navi31 = AMDGPU(pci_device=self.pci_device, asic_type="GFX11_0_0", is_APU=False,
                        marketing_name="AMD Radeon RX 7900 XTX")
        self.assertEqual(navi31.codename, "NAVI31")
        self.assertEqual(navi31.family, None)
        self.assertEqual(navi31.architecture, "RDNA3")
        self.assertEqual(navi31.base_name, "gfx11-navi31")
        self.assertFalse(navi31.is_APU)
        self.assertEqual(navi31.unknown_fields, set())
        self.assertEqual(navi31.tags, {'amdgpu:generation:11', 'amdgpu:architecture:RDNA3',
                                       'amdgpu:codename:NAVI31', 'amdgpu:discrete',
                                       'amdgpu:pciid:0x1002:0x163f:0xae'})
        self.assertEqual(navi31.structured_tags, {
            'APU': False,
            'architecture': 'RDNA3',
            'codename': 'NAVI31',
            'generation': 11,
            'gfxversion': 'gfx11',
            'integrated': False,
            'marketing_name': 'AMD Radeon RX 7900 XTX',
            'pciid': '0x1002:0x163f:0xae',
            'type': 'amdgpu',
            'family': None,
        })
        self.assertEqual(str(navi31), "<AMDGPU: PCIID 0x1002:0x163f:0xae - NAVI31 - None - RDNA3 - gfx11>")


class AmdGpuDeviceDBTests(unittest.TestCase):
    @patch('builtins.open')
    def test_db_missing(self, open_mock):
        def side_effect(*args, **kwargs):
            if len(args) > 1 and args[1] == 'r':
                raise FileNotFoundError()
            else:
                return MagicMock()
        open_mock.side_effect = side_effect

        # DB missing, but download works
        db = AmdGpuDeviceDB()
        self.assertGreater(len(db.devices), 1)
        self.assertTrue(db.check_db())

        # DB missing, and URL failed
        with patch('valve_gfx_ci.gfxinfo.gpudb.requests.get', side_effect=ValueError()):
            db = AmdGpuDeviceDB()
            self.assertEqual(len(db.devices), 1)
            self.assertFalse(db.check_db())

    def test_update(self):
        db = AmdGpuDeviceDB()
        db.cache_db = MagicMock()

        # Check that the DB is marked as not up to date by default
        self.assertFalse(db.is_up_to_date)

        # Check that calling update() calls cache_db() and marks the DB as up to date
        self.assertTrue(db.update())
        db.cache_db.assert_called_once_with()
        self.assertTrue(db.is_up_to_date)

        # Check that further update() calls don't lead to more calls to cache_db()
        self.assertTrue(db.update())
        db.cache_db.assert_called_once_with()

    def test_check_db(self):
        db = AmdGpuDeviceDB()

        # Check that the DB is complete by default
        self.assertTrue(db.check_db())

        # Add an incomplete GPU, if we did not disable the completeness check
        pci_device = PCIDevice(vendor_id=0x1002, product_id=0x0001, revision=0x42)
        db.devices[pci_device] = AMDGPU(pci_device=pci_device, asic_type="GFX10_3_42",
                                        is_APU=True, marketing_name="GPU with non-existant architecture")
        ret = db.check_db()
        if 'GFXINFO_SKIP_DB_COMPLETENESS_CHECK' not in os.environ:  # pragma: nocover
            # NOTE: Ignore the check when the DB completeness checks are disabled, as it would otherwise return True
            self.assertFalse(ret)

    def test_db_name(self):
        self.assertEqual(AmdGpuDeviceDB().db_name, "AmdGpuDeviceDB")


class IntelGpuTests(unittest.TestCase):
    def test_raw_codenames(self):
        pci_device = PCIDevice(vendor_id=0x1002, product_id=0x0001, revision=0x42)

        unsupported_format = IntelGPU(pci_device=pci_device, raw_codename="_IDONTEXIST")
        self.assertEqual(unsupported_format.short_architecture, "_IDONTEXIST")
        self.assertIsNone(unsupported_format.variant)
        self.assertIsNone(unsupported_format.gt)
        self.assertIsNone(unsupported_format.human_name)
        self.assertTrue(unsupported_format.is_integrated)
        self.assertEqual(unsupported_format.unknown_fields, {"gen_version", "architecture"})
        self.assertEqual(unsupported_format.base_name, 'intel-unk-_idontexist')
        self.assertEqual(unsupported_format.tags, {'intelgpu:pciid:0x1002:0x1:0x42',
                                                   'intelgpu:raw_codename:_IDONTEXIST'})
        self.assertEqual(unsupported_format.structured_tags, {'pciid': '0x1002:0x1:0x42', 'raw_codename': '_IDONTEXIST',
                                                              'type': 'intelgpu'})

        ats_m75 = IntelGPU(pci_device=pci_device, raw_codename="ATS_M75")
        self.assertEqual(ats_m75.short_architecture, "ATS")
        self.assertEqual(ats_m75.variant, "M75")
        self.assertIsNone(ats_m75.gt)
        self.assertEqual(ats_m75.human_name, "Arctic Sound M75")
        self.assertEqual(ats_m75.architecture, "ARCTICSOUND")
        self.assertFalse(ats_m75.is_integrated)
        self.assertEqual(ats_m75.base_name, 'intel-gen12-ats-m75')
        self.assertEqual(ats_m75.tags, {'intelgpu:pciid:0x1002:0x1:0x42', 'intelgpu:gen:12',
                                        'intelgpu:codename:ATS-M75', 'intelgpu:discrete',
                                        'intelgpu:architecture:ARCTICSOUND'})

        adlp = IntelGPU(pci_device=pci_device, raw_codename="ADLP")
        self.assertEqual(adlp.short_architecture, "ADL")
        self.assertEqual(adlp.variant, "P")
        self.assertIsNone(adlp.gt)
        self.assertEqual(adlp.human_name, "Alder Lake P")
        self.assertEqual(adlp.architecture, "ALDERLAKE")
        self.assertTrue(adlp.is_integrated)
        self.assertEqual(adlp.base_name, 'intel-gen12-adl-p')
        self.assertEqual(adlp.structured_tags, {'architecture': 'ALDERLAKE', 'codename': 'ADL-P', 'generation': 12,
                                                'integrated': True, 'marketing_name': 'Alder Lake P',
                                                'pciid': '0x1002:0x1:0x42', 'type': 'intelgpu'})

        whl_u_gt2 = IntelGPU(pci_device=pci_device, raw_codename="WHL_U_GT2")
        self.assertEqual(whl_u_gt2.short_architecture, "WHL")
        self.assertEqual(whl_u_gt2.variant, "U")
        self.assertEqual(whl_u_gt2.gt, 2)
        self.assertEqual(whl_u_gt2.human_name, "Whisky Lake U GT2")
        self.assertEqual(whl_u_gt2.architecture, "WHISKYLAKE")
        self.assertTrue(whl_u_gt2.is_integrated)
        self.assertEqual(whl_u_gt2.base_name, 'intel-gen9-whl-u-gt2')
        self.assertEqual(str(whl_u_gt2), "<IntelGPU: PCIID 0x1002:0x1:0x42 - gen9 - Whisky Lake U GT2>")

        bdw_gt1 = IntelGPU(pci_device=pci_device, raw_codename="BDW_GT1")
        self.assertEqual(bdw_gt1.short_architecture, "BDW")
        self.assertIsNone(bdw_gt1.variant)
        self.assertEqual(bdw_gt1.gt, 1)
        self.assertEqual(bdw_gt1.human_name, "Broadwell GT1")
        self.assertEqual(bdw_gt1.architecture, "BROADWELL")
        self.assertTrue(bdw_gt1.is_integrated)
        self.assertEqual(bdw_gt1.base_name, 'intel-gen8-bdw-gt1')
        self.assertEqual(bdw_gt1.tags, {'intelgpu:pciid:0x1002:0x1:0x42', 'intelgpu:gen:8',
                                        'intelgpu:codename:BDW-GT1', 'intelgpu:integrated',
                                        'intelgpu:architecture:BROADWELL', 'intelgpu:GT:1'})

        vlv = IntelGPU(pci_device=pci_device, raw_codename="VLV")
        self.assertEqual(vlv.short_architecture, "VLV")
        self.assertIsNone(vlv.variant)
        self.assertIsNone(vlv.gt)
        self.assertEqual(vlv.human_name, "Valley View")
        self.assertEqual(vlv.architecture, "VALLEYVIEW")
        self.assertTrue(vlv.is_integrated)
        self.assertEqual(vlv.base_name, 'intel-gen7-vlv')
        self.assertEqual(str(vlv), "<IntelGPU: PCIID 0x1002:0x1:0x42 - gen7 - Valley View>")


class IntelI915GpuDeviceDBTests(unittest.TestCase):
    def test_db_name(self):
        self.assertEqual(IntelI915GpuDeviceDB().db_name, "IntelI915GpuDeviceDB")

    def test_cache_db(self):
        self.assertIsNotNone(IntelI915GpuDeviceDB().cache_db())

    def test_update(self):
        self.assertTrue(IntelI915GpuDeviceDB().update())

    def test_check_db(self):
        self.assertTrue(IntelI915GpuDeviceDB().check_db())

    def test_from_pciid(self):
        pci_device = PCIDevice(vendor_id=0x8086, product_id=0x3e9b, revision=0)
        dev = IntelI915GpuDeviceDB().from_pciid(pci_device)

        self.assertEqual(dev.codename, "CFL-H-GT2")

        # Make sure that in the presence of an unknown revision, we only use the vendor_id/product_id
        pci_device2 = PCIDevice(vendor_id=0x8086, product_id=0x3e9b, revision=42)
        self.assertEqual(dev, IntelI915GpuDeviceDB().from_pciid(pci_device2))


class NvidiaGPUTests(unittest.TestCase):
    def setUp(self):
        self.pci_device = PCIDevice(vendor_id=0x10de, product_id=0x2704, revision=0)
        self.rtx_4080 = NvidiaGPU(pci_device=self.pci_device, marketing_name="NVIDIA GeForce RTX 4080",
                                  vdpau="K")

    def test_db_url(self):
        # Check that failing to get the latest driver version reverts to a known existing version
        with patch('valve_gfx_ci.gfxinfo.gpudb.requests.get', side_effect=ValueError()):
            # Make sure it is a valid URL
            url = urlparse(NvidiaGpuDeviceDB.db_url())

            # Make sure the url does not contain `//` which would indicate a missing version
            self.assertNotIn("//", url.path)

    def test_raw_codenames(self):
        # RTX 4080
        self.assertEqual(self.rtx_4080.base_name, "ada-ad103")
        self.assertEqual(self.rtx_4080.codename, "AD103")
        self.assertEqual(self.rtx_4080.tags, {'nvidia:codename:AD103', 'nvidia:architecture:Ada',
                                              'nvidia:pciid:0x10de:0x2704:0x0', 'nvidia:discrete'})
        self.assertEqual(self.rtx_4080.structured_tags, {
            'architecture': 'Ada',
            'codename': 'AD103',
            'integrated': False,
            'marketing_name': "NVIDIA GeForce RTX 4080",
            'pciid': '0x10de:0x2704:0x0',
            'type': 'nvidia',
            'vdpau_features': 'K'
        })
        self.assertEqual(str(self.rtx_4080), "<NVIDIA: PCIID 0x10de:0x2704:0x0 - AD103 - Ada>")
        self.assertEqual(self.rtx_4080.unknown_fields, set())

        # Integrated GPU
        pci_device = PCIDevice(vendor_id=0x10de, product_id=0x7e0, revision=0)
        mcp73 = NvidiaGPU(pci_device=pci_device, marketing_name="GeForce 7150 / nForce 630i")
        self.assertEqual(mcp73.base_name, "curie-mcp73")
        self.assertEqual(mcp73.codename, "MCP73")
        self.assertEqual(mcp73.tags, {'nvidia:codename:MCP73', 'nvidia:architecture:Curie',
                                      'nvidia:pciid:0x10de:0x7e0:0x0', 'nvidia:integrated'})
        self.assertEqual(mcp73.structured_tags, {
            'architecture': "Curie",
            'codename': "MCP73",
            'integrated': True,
            'marketing_name': "GeForce 7150 / nForce 630i",
            'pciid': '0x10de:0x7e0:0x0',
            'type': 'nvidia',
            'vdpau_features': None
        })
        self.assertEqual(str(mcp73), "<NVIDIA: PCIID 0x10de:0x7e0:0x0 - MCP73 - Curie>")
        self.assertEqual(mcp73.unknown_fields, set())

        # Future GPU
        pci_device = PCIDevice(vendor_id=0x10de, product_id=0xffff, revision=0)
        unk_gpu = NvidiaGPU(pci_device=pci_device, marketing_name="NVIDIA GeForce RTX 9999", vdpau="Z")
        self.assertEqual(unk_gpu.base_name, "nv-unk")
        self.assertEqual(unk_gpu.codename, None)
        self.assertEqual(unk_gpu.tags, {'nvidia:codename:None', 'nvidia:architecture:None',
                                        'nvidia:pciid:0x10de:0xffff:0x0', 'nvidia:discrete'})
        self.assertEqual(unk_gpu.structured_tags, {
            'architecture': None,
            'codename': None,
            'integrated': None,
            'marketing_name': "NVIDIA GeForce RTX 9999",
            'pciid': '0x10de:0xffff:0x0',
            'type': 'nvidia',
            'vdpau_features': 'Z'
        })
        self.assertEqual(str(unk_gpu), "<NVIDIA: PCIID 0x10de:0xffff:0x0 - None - None>")
        self.assertEqual(unk_gpu.unknown_fields, set(['architecture', 'codename']))


class TestNvidiaGpuDeviceDB(unittest.TestCase):
    def test_db_name(self):
        self.assertEqual(NvidiaGpuDeviceDB().db_name, "NvidiaGpuDeviceDB")

    def test_check_db(self):
        self.assertTrue(NvidiaGpuDeviceDB().check_db())

    def test_from_pciid(self):
        pci_device = PCIDevice(vendor_id=0x10de, product_id=0x2191, revision=0)
        dev = NvidiaGpuDeviceDB().from_pciid(pci_device)
        self.assertEqual(dev.pci_device, pci_device)
        self.assertEqual(dev.codename, "TU116")
        self.assertEqual(dev.marketing_name, "NVIDIA GeForce GTX 1660 Ti")

        # Make sure that in the presence of an unknown subsys, we revert to just vendor/product/rev
        pci_device2 = PCIDevice(vendor_id=0x10de, product_id=0x2191, revision=0,
                                subsys_vendor_id=0xdead, subsys_product_id=0xbeef)
        self.assertEqual(dev, NvidiaGpuDeviceDB().from_pciid(pci_device2))

        # Make sure that the marketing name is indeed updated when we use a correct subsys id
        pci_device3 = PCIDevice(vendor_id=0x10de, product_id=0x2191, revision=0,
                                subsys_vendor_id=0x1028, subsys_product_id=0x949)
        dev = NvidiaGpuDeviceDB().from_pciid(pci_device3)
        self.assertEqual(dev.codename, "TU116")
        self.assertEqual(dev.marketing_name, "NVIDIA GeForce GTX 1660 Ti with Max-Q Design")


class VirtGPUTests(unittest.TestCase):
    def setUp(self):
        self.pci_device = PCIDevice(vendor_id=0x1af4, product_id=0x1050, revision=0)
        self.gpu = VirtGPU(pci_device=self.pci_device)

    def test_some_devices(self):
        self.assertEqual(self.gpu.base_name, "virtio")
        self.assertEqual(self.gpu.codename, "VIRTIO")
        self.assertEqual(self.gpu.tags, {'virtio:codename:VIRTIO', 'virtio:family:VIRTIO',
                                         'virtio:pciid:0x1af4:0x1050:0x0'})
        self.assertEqual(self.gpu.structured_tags, {
            'architecture': 'VIRTIO',
            'codename': 'VIRTIO',
            'generation': 1,
            'integrated': True,
            'marketing_name': "VirtIO",
            'pciid': '0x1af4:0x1050:0x0',
            'type': 'virtio'
        })
        self.assertEqual(str(self.gpu), "<VirtGPU: PCIID 0x1af4:0x1050:0x0>")


class RadeonTests(unittest.TestCase):
    def setUp(self):
        self.pci_device = PCIDevice(vendor_id=0x1002, product_id=0x71C0, revision=0)
        self.gpu = RadeonGPU(pci_device=self.pci_device, codename="RV530",
                             is_mobility=False, is_IGP=False)

    def test_pciid(self):
        assert self.gpu.pciid == str(self.pci_device)

    def test_some_devices(self):
        self.assertEqual(self.gpu.codename, "RV530")
        self.assertEqual(self.gpu.architecture, "R500")
        self.assertEqual(self.gpu.gfx_version, 2)
        self.assertEqual(self.gpu.base_name, "gfx2-rv530")
        self.assertFalse(self.gpu.is_mobility)
        self.assertFalse(self.gpu.is_IGP)
        self.assertEqual(self.gpu.unknown_fields, set())
        self.assertEqual(self.gpu.tags, {'radeon:generation:2', 'radeon:codename:RV530',
                                         'radeon:architecture:R500', 'radeon:discrete',
                                         'radeon:pciid:0x1002:0x71c0:0x0'})
        self.assertEqual(self.gpu.structured_tags, {
            'codename': 'RV530',
            'architecture': 'R500',
            'generation': 2,
            'integrated': False,
            'pciid': '0x1002:0x71c0:0x0',
            'type': 'radeon'
        })

        sumo = RadeonGPU(pci_device=self.pci_device, codename="SUMO", is_IGP=True, is_mobility=False)
        self.assertEqual(sumo.codename, "SUMO")
        self.assertEqual(sumo.architecture, "Evergreen")
        self.assertTrue(sumo.is_IGP)
        self.assertFalse(sumo.is_mobility)
        self.assertEqual(sumo.unknown_fields, set())
        self.assertEqual(sumo.tags, {'radeon:generation:4', 'radeon:codename:SUMO',
                                     'radeon:architecture:Evergreen', 'radeon:integrated',
                                     'radeon:pciid:0x1002:0x71c0:0x0'})
        self.assertEqual(sumo.structured_tags, {
            'codename': 'SUMO',
            'architecture': "Evergreen",
            'generation': 4,
            'integrated': True,
            'pciid': '0x1002:0x71c0:0x0',
            'type': 'radeon'
        })
        self.assertEqual(str(sumo), "<RadeonGPU: PCIID 0x1002:0x71c0:0x0 - SUMO - Evergreen - gfx4>")

        r100 = RadeonGPU(pci_device=self.pci_device, codename="KAVERI", is_IGP=False, is_mobility=True)
        self.assertEqual(r100.codename, "KAVERI")
        self.assertEqual(r100.architecture, "SeaIslands")
        self.assertFalse(r100.is_IGP)
        self.assertTrue(r100.is_mobility)
        self.assertEqual(r100.unknown_fields, set())
        self.assertEqual(r100.tags, {'radeon:generation:7', 'radeon:codename:KAVERI',
                                     'radeon:architecture:SeaIslands', 'radeon:integrated',
                                     'radeon:pciid:0x1002:0x71c0:0x0'})
        self.assertEqual(r100.structured_tags, {
            'codename': 'KAVERI',
            'architecture': "SeaIslands",
            'generation': 7,
            'integrated': True,
            'pciid': '0x1002:0x71c0:0x0',
            'type': 'radeon'
        })
        self.assertEqual(str(r100), "<RadeonGPU: PCIID 0x1002:0x71c0:0x0 - KAVERI - SeaIslands - gfx7>")

        # Future GPU
        pci_device = PCIDevice(vendor_id=0x1002, product_id=0xffff, revision=0)
        unk_gpu = RadeonGPU(pci_device=pci_device, codename="GOODE", is_IGP=False, is_mobility=False)
        self.assertEqual(unk_gpu.base_name, "gfxnone-goode")
        self.assertEqual(unk_gpu.tags, {'radeon:codename:GOODE', 'radeon:architecture:None',
                                        'radeon:generation:None', 'radeon:pciid:0x1002:0xffff:0x0',
                                        'radeon:discrete'})
        self.assertEqual(unk_gpu.structured_tags, {
            'architecture': None,
            'codename': "GOODE",
            'generation': None,
            'integrated': False,
            'pciid': '0x1002:0xffff:0x0',
            'type': 'radeon',
        })
        self.assertEqual(str(unk_gpu), "<RadeonGPU: PCIID 0x1002:0xffff:0x0 - GOODE - None - gfxNone>")
        self.assertEqual(unk_gpu.unknown_fields, set(['architecture', 'gfx_version']))


class RadeonGpuDeviceDBTests(unittest.TestCase):
    def test_db_name(self):
        self.assertEqual(RadeonGpuDeviceDB().db_name, "RadeonGpuDeviceDB")

    def test_cache_db(self):
        self.assertIsNotNone(RadeonGpuDeviceDB().cache_db())

    def test_update(self):
        self.assertTrue(RadeonGpuDeviceDB().update())

    def test_check_db(self):
        self.assertTrue(RadeonGpuDeviceDB().check_db())

    def test_from_pciid(self):
        pci_device = PCIDevice(vendor_id=0x1002, product_id=0x71C0, revision=0)
        dev = RadeonGpuDeviceDB().from_pciid(pci_device)

        self.assertEqual(dev.codename, "RV530")

        # Make sure that in the presence of an unknown revision, we only use the vendor_id/product_id
        pci_device2 = PCIDevice(vendor_id=0x1002, product_id=0x71C0, revision=42)
        self.assertEqual(dev, RadeonGpuDeviceDB().from_pciid(pci_device2))
