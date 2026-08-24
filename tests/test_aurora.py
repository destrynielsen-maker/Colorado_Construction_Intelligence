import unittest
from colorado_permits.collectors.aurora import AuroraCollector

class AuroraTests(unittest.TestCase):
    def test_money(self): self.assertEqual(AuroraCollector._money("$1,234,567"),1234567.0)
    def test_date(self): self.assertEqual(AuroraCollector._date(1787529600000),"2026-08-24")

if __name__ == "__main__": unittest.main()
