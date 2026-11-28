"""司直（SIZHI）· VAL-01 对照复测：覆核复测、直其曲。

命名即种子：司直＝汉代掌督察纠弹之官，「直其曲也」。
逻辑本体：凡结论必有独立第二遍对照复测，复测不符即直其曲（指出偏差所在）。

三算子：
- 命（ming.Ming）    原测官：受理断言，登记首测结论。
- 覆（fu.Fu）        复测官：独立路径重算，不读首测过程，只对结论。
- 直（zhi.Zhi）      裁决官：一致则销案，不符则直陈偏差与证据。

三算子合枢于 Sizhi 门面（file / recheck_independent / judge）。
原单文件骨架 API（describe / recheck）收编保留，行为不变。
"""

from .legacy import Sizhi as _LegacySizhi
from .ming import Ming
from .fu import Fu
from .zhi import Zhi

__all__ = ["Sizhi", "Ming", "Fu", "Zhi"]


class Sizhi(_LegacySizhi):
    """司直门面：原 v1 API 之上长出命/覆/直三算子。"""

    def __init__(self, config=None):
        super().__init__(config)
        self._ming = Ming()
        self._fu = Fu()
        self._zhi = Zhi()

    # ---- 命：受理断言，登记首测结论 ----
    def file(self, subject, expected, first_result, checker="原测"):
        return self._ming.file(subject, expected, first_result, checker=checker)

    # ---- 覆：独立路径重算，不读首测过程只对结论 ----
    def recheck_independent(self, claim_id, recomputed, path="独立路径"):
        record = self._fu.recheck(claim_id, recomputed, path=path)
        self._ming.mark(claim_id, "rechecked")
        self.events.append({"event": "recheck_independent", "claim_id": claim_id})
        return record

    # ---- 直：对照裁决，一致则销、不符则直陈偏差 ----
    def judge(self, claim_id):
        claim = self._ming.get(claim_id)
        records = self._fu.records_for(claim_id)
        if not records:
            raise ValueError("案卷 %s 尚无独立复测，不可裁" % claim_id)
        verdict = self._zhi.judge(claim, records[-1])
        self._ming.mark(claim_id, "dismissed" if verdict["verdict"] == "confirmed" else "deviation")
        self.events.append({"event": "judge", "claim_id": claim_id,
                            "verdict": verdict["verdict"]})
        return verdict

    @property
    def claims(self):
        return self._ming.claims

    @property
    def recheck_records(self):
        return self._fu.records

    @property
    def verdict_ledger(self):
        return self._zhi.verdicts
