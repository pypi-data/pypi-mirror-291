import unittest
from infvariation.variation import Variation

class TestVariation(unittest.TestCase):

    def setUp(self):
        self.var = Variation()

    def test_typosquatting(self):
        result = self.var.typosquatting("cacaushow.google.com")
        self.assertIsInstance(result, list)
        # Adicione mais assertivas aqui, dependendo dos resultados esperados

    def test_generate_leet(self):
        result = self.var.generate_leet("cacaushow")
        self.assertIsInstance(result, list)
        self.assertIn("c4c4ush0w", result)

    def test_generate_variations(self):
        result = self.var.generate_variations("cacaushow")
        self.assertIsInstance(result, list)
        self.assertIn("Cacaushow", result)
        self.assertIn("cacaushow1", result)
        self.assertIn("cacaush_ow", result)

if __name__ == "__main__":
    unittest.main()
