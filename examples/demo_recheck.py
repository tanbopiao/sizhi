"""端到端演示：命→覆→直，一致销案、不符直陈偏差。

运行：python examples/demo_recheck.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sizhi import Sizhi


def main():
    gate = Sizhi()

    # 案一：首测与独立复测一致 → 销案
    c1 = gate.file("函数 square(3) 返回 9", expected=9, first_result=9, checker="原测组")
    gate.recheck_independent(c1["claim_id"], 9, path="3*3 直算")
    v1 = gate.judge(c1["claim_id"])
    print("[案一] %s → %s" % (v1["subject"], v1["verdict"]))

    # 案二：首测记错（15），独立复测为 16 → 直其曲
    c2 = gate.file("函数 square(4) 返回 16", expected=16, first_result=15, checker="原测组")
    gate.recheck_independent(c2["claim_id"], 16, path="4*4 直算")
    v2 = gate.judge(c2["claim_id"])
    print("[案二] %s → %s" % (v2["subject"], v2["verdict"]))
    d = v2["deviation"]
    print("  偏差所在：%s" % d["where"])
    print("  首测=%s  复测=%s（路径：%s）" % (d["first"], d["recheck"], d["evidence"]["recheck_path"]))

    print("\n判例册共 %d 条，只增不覆盖。" % len(gate.verdict_ledger))
    return 0


if __name__ == "__main__":
    sys.exit(main())
