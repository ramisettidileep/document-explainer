import unittest
from backend.functions.verifier.calculator import verify_sum, verify_balance

class TestVerifier(unittest.TestCase):
    def test_verify_sum_exact(self):
        res = verify_sum([10.50, 20.25, 4.25], 35.00)
        self.assertEqual(res["status"], "verified")
        self.assertEqual(res["difference"], 0.0)

    def test_verify_sum_mismatch(self):
        res = verify_sum([10.0, 5.0], 20.0)
        self.assertEqual(res["status"], "mismatch")
        self.assertEqual(res["difference"], 5.0)

    def test_verify_balance_exact(self):
        res = verify_balance(1000, 500, 200, 1300)
        self.assertEqual(res["status"], "verified")

    def test_verify_balance_mismatch(self):
        res = verify_balance(1000, 500, 200, 1500)
        self.assertEqual(res["status"], "mismatch")

if __name__ == "__main__":
    unittest.main()