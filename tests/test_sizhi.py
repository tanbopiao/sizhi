"""司直三算子单测：命/覆/直各司其职，独立性与只增不覆盖。

运行：python -m unittest discover -s tests -v
"""
import unittest

from sizhi import Sizhi, Ming, Fu, Zhi


class TestMing(unittest.TestCase):
    def test_file_and_get(self):
        m = Ming()
        claim = m.file("f(3) 返回 9", expected=9, first_result=9, checker="甲")
        self.assertTrue(claim["claim_id"].startswith("SZ-"))
        self.assertEqual(claim["status"], "filed")
        got = m.get(claim["claim_id"])
        self.assertEqual(got["first_result"], 9)
        self.assertIsNot(got, m._claims[claim["claim_id"]])  # 返回拷贝，防外改

    def test_file_requires_subject(self):
        with self.assertRaises(ValueError):
            Ming().file("", expected=1, first_result=1)

    def test_mark_only_legal_status(self):
        m = Ming()
        claim = m.file("x", expected=1, first_result=1)
        m.mark(claim["claim_id"], "rechecked")
        self.assertEqual(m.get(claim["claim_id"])["status"], "rechecked")
        with self.assertRaises(ValueError):
            m.mark(claim["claim_id"], "随便改")


class TestFu(unittest.TestCase):
    def test_recheck_requires_independent_path(self):
        f = Fu()
        with self.assertRaises(ValueError):
            f.recheck("SZ-x", 42, path="原测路径")

    def test_records_append_only(self):
        f = Fu()
        f.recheck("SZ-a", 42, path="换条公式重算")
        f.recheck("SZ-a", 43, path="再换条路径")
        self.assertEqual(len(f.records_for("SZ-a")), 2)
        self.assertEqual(len(f.records), 2)


class TestZhi(unittest.TestCase):
    def test_confirm_and_deviation(self):
        z = Zhi()
        ok = z.judge({"claim_id": "SZ-1", "subject": "s", "first_result": 9, "checker": "甲"},
                     {"claim_id": "SZ-1", "recomputed": 9, "path": "独立路径"})
        self.assertEqual(ok["verdict"], "confirmed")
        self.assertNotIn("deviation", ok)
        bad = z.judge({"claim_id": "SZ-2", "subject": "s", "first_result": 9, "checker": "甲"},
                      {"claim_id": "SZ-2", "recomputed": 8, "path": "独立路径"})
        self.assertEqual(bad["verdict"], "deviation")
        self.assertEqual(bad["deviation"]["first"], 9)
        self.assertEqual(bad["deviation"]["recheck"], 8)
        self.assertIn("evidence", bad["deviation"])

    def test_judge_rejects_mismatched_claim(self):
        z = Zhi()
        with self.assertRaises(ValueError):
            z.judge({"claim_id": "SZ-1", "first_result": 1},
                    {"claim_id": "SZ-2", "recomputed": 1, "path": "独立路径"})

    def test_verdict_ledger_append_only(self):
        z = Zhi()
        z.judge({"claim_id": "SZ-1", "first_result": 1},
                {"claim_id": "SZ-1", "recomputed": 1, "path": "p"})
        z.judge({"claim_id": "SZ-2", "first_result": 2},
                {"claim_id": "SZ-2", "recomputed": 3, "path": "p"})
        self.assertEqual(len(z.verdicts), 2)


class TestSizhiFacade(unittest.TestCase):
    def setUp(self):
        self.gate = Sizhi()

    def test_legacy_api_preserved(self):
        d = self.gate.describe()
        self.assertEqual(d["repo"], "sizhi")
        self.assertEqual(d["code"], "SIZHI")
        ok = self.gate.recheck({"expected": 42}, {"actual": 42})
        self.assertEqual(ok["verdict"], "confirmed")

    def test_full_flow_confirm(self):
        claim = self.gate.file("f(3) 返回 9", expected=9, first_result=9)
        self.gate.recheck_independent(claim["claim_id"], 9, path="换法重算")
        verdict = self.gate.judge(claim["claim_id"])
        self.assertEqual(verdict["verdict"], "confirmed")
        self.assertEqual(self.gate.claims[0]["status"], "dismissed")

    def test_full_flow_deviation(self):
        claim = self.gate.file("g(4) 返回 16", expected=16, first_result=15)
        self.gate.recheck_independent(claim["claim_id"], 16, path="乘法直算")
        verdict = self.gate.judge(claim["claim_id"])
        self.assertEqual(verdict["verdict"], "deviation")
        self.assertEqual(verdict["deviation"]["first"], 15)
        self.assertEqual(verdict["deviation"]["recheck"], 16)
        self.assertEqual(self.gate.claims[0]["status"], "deviation")

    def test_judge_requires_recheck(self):
        claim = self.gate.file("h(1)", expected=1, first_result=1)
        with self.assertRaises(ValueError):
            self.gate.judge(claim["claim_id"])

    def test_events_append_only(self):
        self.gate.recheck({"expected": 1}, {"actual": 1})  # 遗留 API 留痕
        claim = self.gate.file("k", expected=1, first_result=1)
        self.gate.recheck_independent(claim["claim_id"], 1)
        self.gate.judge(claim["claim_id"])
        kinds = [e["event"] for e in self.gate.events]
        self.assertIn("recheck", kinds)      # 遗留 API 留痕
        self.assertIn("recheck_independent", kinds)
        self.assertIn("judge", kinds)


if __name__ == "__main__":
    unittest.main()
