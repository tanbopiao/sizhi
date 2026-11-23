"""司直（SIZHI）算子骨架单测：名帖完整、桩位齐整、只增不覆盖。"""
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

    def test_recheck_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.recheck(None, None)


if __name__ == "__main__":
    unittest.main()
