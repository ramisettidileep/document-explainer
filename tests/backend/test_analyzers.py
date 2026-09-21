import unittest
from backend.analyzers.medical import MedicalAnalyzer
from backend.analyzers.banking import BankingAnalyzer
from backend.analyzers.legal import LegalAnalyzer
from backend.utils.parsing import parse_raw_text

class TestAnalyzers(unittest.TestCase):
    def test_medical_analyzer(self):
        doc = parse_raw_text("Hemoglobin: 14.2 g/dL (12-16)")
        analyzer = MedicalAnalyzer()
        res = analyzer.analyze(doc)
        self.assertEqual(res["doc_type"], "medical")
        self.assertTrue(len(res["key_fields"]) > 0)

    def test_banking_analyzer(self):
        doc = parse_raw_text("Opening balance: 1000\nTotal deposits: 500\nTotal withdrawals: 200\nClosing balance: 1300")
        analyzer = BankingAnalyzer()
        res = analyzer.analyze(doc)
        self.assertEqual(res["doc_type"], "banking")
        self.assertEqual(res["calculations"][0]["status"], "verified")

    def test_legal_analyzer(self):
        doc = parse_raw_text("Either party may terminate this agreement with notice of 30 days.")
        analyzer = LegalAnalyzer()
        res = analyzer.analyze(doc)
        self.assertEqual(res["doc_type"], "legal")
        self.assertTrue(len(res["evidence"]) > 0)

if __name__ == "__main__":
    unittest.main()