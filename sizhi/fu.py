"""覆·复测官——司直三算子之二。

道统映射：覆者，覆核也。复测走独立路径重算，不读首测过程，只对结论——
覆测官手里只有案卷号与自己重算出的值，看不到首测怎么算的。
这是「独立第二遍」的结构保证：不是提醒复测者别偷看，而是根本不给他看。

只增不覆盖：每次复测记录留痕，不因后续裁决而改写。
"""

import time


class Fu:
    """覆·复测官：独立路径重算，只对结论。"""

    def __init__(self):
        self._records = {}  # claim_id -> [复测记录，只增]
        self._order = []

    def recheck(self, claim_id, recomputed, path="独立路径"):
        """登记一条独立复测。

        claim_id   案卷号（只作对号，不携带首测内容）
        recomputed 复测者按独立路径重算出的结论
        path       复测路径说明（与首测路径相区别）
        """
        if not path or path == "原测路径":
            raise ValueError("复测必须声明独立路径，不得沿用原测路径")
        stamp = time.time()
        record = {
            "claim_id": claim_id,
            "recomputed": recomputed,
            "path": path,
            "rechecked_at": stamp,
        }
        self._records.setdefault(claim_id, []).append(record)
        self._order.append(claim_id)
        return dict(record)

    def records_for(self, claim_id):
        """取某案全部复测记录（拷贝）。"""
        return [dict(r) for r in self._records.get(claim_id, [])]

    @property
    def records(self):
        """全部复测记录（按登记序，拷贝列表）。"""
        out = []
        for recs in self._records.values():
            out.extend(dict(r) for r in recs)
        return out
