"""命·原测官——司直三算子之一。

道统映射：司直掌督察，先有所「命」而后能「覆」——原测官受理待验断言，
登记首测结论。命而不覆是独断，故每条断言必入覆测之册。

只增不覆盖：登记即立档，档成后首测结论不改不删。
"""

import hashlib
import time


class Ming:
    """命·原测官：受理断言，登记首测结论。"""

    def __init__(self):
        self._claims = {}   # claim_id -> claim 档
        self._order = []    # 立案顺序，只增

    def file(self, subject, expected, first_result, checker="原测"):
        """命案登记：一条待验断言＋首测结论。

        subject       断言主题（如「函数 f(3) 返回 9」）
        expected      首测宣称的结论
        first_result  首测实际记录的结论
        checker       首测执行者标识
        """
        if not subject:
            raise ValueError("断言主题不可为空")
        stamp = time.time()
        raw = "%s|%s|%s|%s" % (subject, repr(expected), repr(first_result), stamp)
        claim_id = "SZ-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
        claim = {
            "claim_id": claim_id,
            "subject": subject,
            "expected": expected,
            "first_result": first_result,
            "checker": checker,
            "filed_at": stamp,
            "status": "filed",  # filed -> rechecked -> dismissed / deviation
        }
        self._claims[claim_id] = claim
        self._order.append(claim_id)
        return dict(claim)

    def get(self, claim_id):
        """取案卷副本（防外改，返回拷贝）。"""
        if claim_id not in self._claims:
            raise KeyError("无此案卷：%s" % claim_id)
        return dict(self._claims[claim_id])

    def mark(self, claim_id, status):
        """覆测官回写状态（仅限法定状态流转）。"""
        if status not in ("rechecked", "dismissed", "deviation"):
            raise ValueError("非法状态：%s" % status)
        claim = self._claims[claim_id]
        claim["status"] = status
        return dict(claim)

    @property
    def claims(self):
        """全部案卷（按立案序，返回拷贝列表）。"""
        return [dict(self._claims[cid]) for cid in self._order]
