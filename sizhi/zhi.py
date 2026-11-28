"""直·裁决官——司直三算子之三。

道统映射：直其曲也。对照首测结论与独立复测结论：一致则销案（confirmed），
不符则直陈偏差（deviation）——偏差在哪、两边各是什么、证据何在，一一写明。
裁决只认两个结论的对照，不认任何一方的身份或说辞。

只增不覆盖：判词一经作出即入判例册，不改不删。
"""

import time


class Zhi:
    """直·裁决官：对照裁决，直陈偏差。"""

    def __init__(self):
        self._verdicts = []  # 判例册，只增

    def judge(self, claim, recheck_record):
        """对照裁决一条案卷。

        claim           命官案卷（含首测结论 first_result）
        recheck_record  覆官复测记录（含重算结论 recomputed）
        """
        if claim.get("claim_id") != recheck_record.get("claim_id"):
            raise ValueError("案卷号不符，不予对审")
        first = claim.get("first_result")
        second = recheck_record.get("recomputed")
        consistent = first == second
        stamp = time.time()
        verdict = {
            "claim_id": claim["claim_id"],
            "subject": claim.get("subject"),
            "verdict": "confirmed" if consistent else "deviation",
            "first": first,
            "recheck": second,
            "recheck_path": recheck_record.get("path"),
            "judged_at": stamp,
        }
        if not consistent:
            # 直其曲：偏差所在、两边结论、证据，一一写明
            verdict["deviation"] = {
                "where": "首测结论与独立复测结论不符",
                "first": first,
                "recheck": second,
                "evidence": {
                    "checker": claim.get("checker"),
                    "recheck_path": recheck_record.get("path"),
                },
            }
        self._verdicts.append(verdict)
        return dict(verdict)

    @property
    def verdicts(self):
        """判例册（拷贝列表，只增不覆盖）。"""
        return [dict(v) for v in self._verdicts]
