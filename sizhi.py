"""司直（SIZHI）· VAL-01 对照复测：覆核复测、直其曲直。典出汉代司直「佐举不法」

道统出处：元极恒一·术语缩影表 T057 ｜ 第六批
体系锚：Ω₀⊂⊙∞⊂Ω｜DID-BR-000002

工程映射：VAL-01 对照复测：覆核复测、直其曲直。典出汉代司直「佐举不法」。

边界：本件为算子 v1——骨架桩已按命名映射补齐实现；遵循元法第四条「只增不覆盖」，
方法只增不改名不删，行为变更走新版本；凭据不入档，宣称与事实分离。
"""

class Sizhi:
    """司直（SIZHI）算子 v1。"""

    ANCHOR = "Ω₀⊂⊙∞⊂Ω｜DID-BR-000002"
    CODE = "SIZHI"

    def __init__(self, config=None):
        self.config = dict(config or {})
        self.events = []  # 只增不覆盖：会话内事件留痕

    def describe(self):
        """构件名帖：名、代号、职责、铭文、体系锚。"""
        return {
            "repo": "sizhi",
            "cn": "司直",
            "code": self.CODE,
            "duty": "VAL-01 对照复测：覆核复测、直其曲直。典出汉代司直「佐举不法」",
            "mingwen": "重验是非，直道而行",
            "anchor": self.ANCHOR,
        }

    def recheck(self, claim, evidence):
        """重验是非：主张对证直其曲直。"""
        expected = (claim or {}).get("expected")
        actual = (evidence or {}).get("actual")
        confirmed = expected == actual
        verdict = {"claim": claim, "verdict": "confirmed" if confirmed else "refuted",
                   "expected": expected, "actual": actual}
        self.events.append({"event": "recheck", "verdict": verdict["verdict"]})
        return verdict
