"""司直（SIZHI）算子单测：名帖完整、行为达标、只增不覆盖。"""
import unittest

from sizhi import Sizhi


class TestSizhi(unittest.TestCase):
    def setUp(self):
        self.op = Sizhi()

    def test_describe(self):
        d = self.op.describe()
        self.assertEqual(d["repo"], "sizhi")
        self.assertEqual(d["code"], "SIZHI")
        self.assertTrue(d["anchor"].startswith("Ω₀⊂⊙∞⊂Ω"))
        self.assertTrue(d["mingwen"])

    def test_recheck(self):
        ok = self.op.recheck({"expected": 42}, {"actual": 42})
        self.assertEqual(ok["verdict"], "confirmed")
        bad = self.op.recheck({"expected": 42}, {"actual": 24})
        self.assertEqual(bad["verdict"], "refuted")


if __name__ == "__main__":
    unittest.main()
