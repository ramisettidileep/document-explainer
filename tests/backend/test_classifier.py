import unittest
from backend.functions.classifier.classifier import DocumentClassifier

class TestClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = DocumentClassifier()

    def test_medical_classification(self):
        text = "Patient serum hemoglobin was 13.4 g/dL. Clinical findings verified."
        res = self.classifier.classify(text)
        self.assertEqual(res["document_type"], "medical")

    def test_banking_classification(self):
        text = "Account statement showing total deposits of 5000 and closing balance is 3000."
        res = self.classifier.classify(text)
        self.assertEqual(res["document_type"], "banking")

    def test_general_fallback(self):
        text = "Quarterly team planning retrospective notes and schedule."
        res = self.classifier.classify(text)
        self.assertEqual(res["document_type"], "general")

if __name__ == "__main__":
    unittest.main()