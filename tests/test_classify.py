import unittest
from colorado_permits.models import Permit
from colorado_permits.classify import classify_permit

class ClassificationTests(unittest.TestCase):
    def test_multifamily(self):
        p=Permit(state="CO",jurisdiction="Aurora",permit_number="1",issued_date="2026-08-01",permit_type="Multi-Family Building",valuation=5_000_000,units=24)
        classify_permit(p); self.assertTrue(p.qualifies); self.assertEqual(p.classification,"MULTIFAMILY"); self.assertGreaterEqual(p.score,60)
    def test_single_family(self):
        p=Permit(state="CO",jurisdiction="Aurora",permit_number="2",issued_date="2026-08-01",permit_type="Single-Family Detached",valuation=600_000)
        classify_permit(p); self.assertTrue(p.qualifies); self.assertEqual(p.classification,"SINGLE_FAMILY")
    def test_commercial(self):
        p=Permit(state="CO",jurisdiction="Aurora",permit_number="3",issued_date="2026-08-01",permit_type="Business Use Building",valuation=1_200_000)
        classify_permit(p); self.assertTrue(p.qualifies); self.assertEqual(p.classification,"COMMERCIAL")
    def test_excludes_tenant_finish(self):
        p=Permit(state="CO",jurisdiction="Aurora",permit_number="4",issued_date="2026-08-01",permit_type="Tenant Finish-NT1")
        classify_permit(p); self.assertFalse(p.qualifies)

if __name__ == "__main__": unittest.main()
