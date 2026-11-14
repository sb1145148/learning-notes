"""
第 7 课 · 函数 —— 实践任务

规则：把 TODO 补上，然后运行。

运行方式（VS Code 终端）：
    C:\\Users\\Administrator\\.dsh\\dsh-runtimes\\dsh-primary-runtime\\dependencies\\python\\python.exe lesson7.py

跑完把输出贴给我。
"""

import json
import glob
import os

BILI = r"D:\Backup\Documents\deepseek-harness\default-workspace\bili"
snap_file = sorted(glob.glob(os.path.join(BILI, "snapshots", "snapshot-*.json")))[-1]
snap = json.load(open(snap_file, encoding="utf-8"))

print("数据文件:", os.path.basename(snap_file), " 账号数:", len(snap))
print()


# ---------------------------------------------------------------
# 任务 1：写一个算百分比的函数
#
# 要求：
#   pct(100, 50)  → "+100.0%"
#   pct(10, 0)    → "—"          （除数是 0，不能算）
#   pct(50, 100)  → "-50.0%"
#   pct(1, 3)     → "-66.7%"
#
# 提示：公式是 100.0 * (新 - 旧) / 旧，用 f"{x:+.1f}%" 格式化。
# TODO：把函数体写完（现在只会返回 None）。
# ---------------------------------------------------------------

# 未修改：
# def pct(new, old):
#     if not old:
#          return "-"
#     return f"{100.0 * (new - old) / old:+.1f}"

def pct(new, old):
    if not old:
         return "——"
    return f"{100.0 * (new - old) / old:+.1f}%"

print("任务 1 · pct（自己的测试）:")
for args in [(100, 50), (10, 0), (50, 100), (1, 3)]:
    print(f"  pct{args} = {pct(*args)!r}")


# ---------------------------------------------------------------
# 任务 2：写一个格式化数字的函数

# 要求：
#   fmt_num(283827)   → "283,827"
#   fmt_num(0)        → "0"
#   fmt_num(1234567)  → "1,234,567"

# 提示：f"{n:,}" 就是千分位。注意参数可能是 None。
# TODO：写完函数体。
# ---------------------------------------------------------------
def fmt_num(n):
    if not n:
        return "0"
    elif n:
        return f"{n:,}"


print("\n任务 2 · fmt_num:")
for n in [283827, 0, 1234567, None]:
    print(f"  fmt_num({n!r}) = {fmt_num(n)!r}")


# ---------------------------------------------------------------
# 任务 3：写一个「取前 n 名」的函数 —— 带默认参数
#
# 要求：
#   top_n(snap)      → 粉丝最多的 3 个（默认参数 n=3）
#   top_n(snap, 5)   → 前 5 个
#   返回值是 [(名字, 粉丝数), ...]，已按粉丝从多到少排好
#
# 提示：
#   - 用 a["card"].get("fans") or 0 取粉丝
#   - 先做成 (粉丝, 名字) 列表，，再切片 [:n]
#   - 注意返回值里要把顺序换成 (名字, 粉丝)
# TODO：写完函数体。
# ---------------------------------------------------------------
# 原来：
# def top_n(data, n=5):
#     for a in snap:
#         fans = a["card"].get("fans") or 0
#         name = a["card"].get("name") or 0
#         return f"{"name", "fans":+.1f}"

# 修1
# def top_n(data, n=3):
#     for a in data:
#         fans = a["card"].get("fans") or 0
#         name = a["card"].get("name") or 0
#     rows = []
#     data.append[("fans", "name")]
#     sort(key=lambda x: x[1])
#     return ("name", "fans")

# 完全
def top_n(data, n=3):
    rows = []
    for a in data:
        fans = a["card"].get("fans") or 0
        name = a.get("name") or a["card"].get("name")
        rows.append((fans, name))
    rows.sort(reverse=True)
    return [(name, fans) for fans, name in rows[:n]]

print("\n任务 3 · top_n(snap)（默认 3 个）:")
for name, fans in top_n(snap):
    print(f"  {name}: {fans:,}")

print("\n任务 3 · top_n(snap, 5)（前 5 个）:")
for i, (name, fans) in enumerate(top_n(snap, 5), 1):
    print(f"  {i}. {name}: {fans:,}")


# ---------------------------------------------------------------
# 任务 4：写一个统计总播放的函数
#
# 要求：
#   返回整数（所有账号所有视频的 play 之和）
#   play 缺失时当 0
#
# 提示：两层 for 循环 + 一个累加变量，最后 return 它。
# TODO：写完函数体。
# ---------------------------------------------------------------
def total_plays(data):
    plays = 0
    for a in data:
        for v in a.get("videos", []):
            plays = plays + (v.get("play") or 0)
    return plays
            
            


print("\n任务 4 · total_plays(snap):")
print("  总播放 =", fmt_num(total_plays(snap)))


# ---------------------------------------------------------------
# 任务 5（加分）：写一个「排行榜」函数，返回格式化好的字符串列表
#
# 要求：
#   rank_lines(snap, 3) → ["1. 鲸鱼娘: 284,336", "2. ...", "3. ..."]
#
# 提示：复用 top_n 和 fmt_num（这就是函数的好处 —— 不用重写逻辑）。
# TODO：写完函数体。
# ---------------------------------------------------------------
def rank_lines(data, n=3):
    lines = []
    for i, (name, fans) in enumerate(top_n(data, n), 1):
        lines.append(f"{i}. {name}: {fmt_num(fans)}")
    return lines

print("\n任务 5 · rank_lines(snap):")
for line in rank_lines(snap):
    print("  " + line)
