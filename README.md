# sizhi · 司直

**VAL-01 对照复测：覆核复测、直其曲。**

> 命名即种子：司直＝汉代掌督察纠弹之官，「直其曲也」。名字所对应的逻辑与架构，是从种子长出来的。

## 命名映射（道统 → 架构）

| 道 | 义 | 算子 |
|----|----|------|
| 命 | 受理断言，登记首测结论 | `Ming` 原测官 |
| 覆 | 独立路径重算，不读首测过程，只对结论 | `Fu` 复测官 |
| 直 | 一致则销案，不符则直陈偏差与证据 | `Zhi` 裁决官 |

逻辑本体：**凡结论必有独立第二遍对照复测，复测不符即直其曲。**
覆测官手里只有案卷号与自己重算出的值——不是提醒复测者别偷看，而是结构上就不给他看。

## 安装

零第三方依赖，仅 Python 3.10+ 标准库。

```bash
git clone https://github.com/tanbopiao/sizhi.git
cd sizhi
python -m unittest discover -s tests -v   # 自测
python examples/demo_recheck.py           # 端到端演示
```

## 用法

```python
from sizhi import Sizhi

gate = Sizhi()

# 命：受理断言，登记首测结论
claim = gate.file("函数 square(4) 返回 16", expected=16, first_result=15, checker="原测组")

# 覆：独立路径重算（不读首测过程，只对结论）
gate.recheck_independent(claim["claim_id"], 16, path="4*4 直算")

# 直：对照裁决——不符则直陈偏差与证据
verdict = gate.judge(claim["claim_id"])
print(verdict["verdict"])      # deviation
print(verdict["deviation"])    # 偏差在哪、两边各是什么、证据何在
```

原单文件骨架 API（`describe()` / `recheck()`）收编保留，行为不变。

## 自测

```bash
python -m unittest discover -s tests -v
```

## 许可

MIT
