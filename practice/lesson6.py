"""
第 6 课 · 字典 —— 实践任务

规则：把标着 TODO 的地方改好，然后运行它。

运行方式（在 VS Code 终端里）：
    C:\\Users\\Administrator\\.dsh\\dsh-runtimes\\dsh-primary-runtime\\dependencies\\python\\python.exe lesson6.py

跑完把输出（或报错）贴给我。
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
# 任务 1：统计粉丝总数
#
# 现在这行直接 a["card"]["fans"]，如果某个账号没有 fans 字段就会 KeyError。
# TODO：改成 .get() 的安全写法，缺失时当 0。
# ---------------------------------------------------------------
total = 0
for a in snap:
    fans = a["card"].get("fans") or 0      # ← 改这一行
    total = total + fans
print("任务 1 · 粉丝总数:", f"{total:,}")


# ---------------------------------------------------------------
# 任务 2：找出粉丝最多的 3 个账号
#
# 提示：先做成 (粉丝数, 名字) 的元组列表，再 sort(reverse=True)。
#       fans 可能是 None，所以用 (a["card"].get("fans") or 0)。
# TODO：把 rows 里那行写完（现在只 append 了 None，是错的）。
# ---------------------------------------------------------------
rows = []
for a in snap:
    rows.append((a["card"].get("fans") or 0, a.get("name")))               # ← 改成 (粉丝数, 名字)
rows.sort(reverse=True)

print("\n任务 2 · 粉丝最多的 3 个:")
for i, (fans, name) in enumerate(rows[:3], 1):
    print(f"  {i}. {name}: {fans:,}")


# ---------------------------------------------------------------
# 任务 3：统计所有账号的视频总播放量
#
# 结构是：snap 是列表 → 每个元素是字典 → a["videos"] 是列表
#          → 列表里每个元素是字典 → v["play"] 是播放量
#
# 注意：v["play"] 可能不存在，用 .get("play") or 0
# TODO：把循环体补完。
# ---------------------------------------------------------------
plays = 0
for a in snap:
    for v in a.get("videos", []):
        plays = plays + (v.get("play") or 0)      # ← 在这里把 v 的播放量加进 plays        
print("\n任务 3 · 视频总播放:", f"{plays:,}")


# ---------------------------------------------------------------
# 任务 4（加分）：哪些账号的视频数据不完整？
#
# a["complete"] 是 True / False。
# TODO：打印出  为 False 的账号名（可能一个都没有）。
# ---------------------------------------------------------------

print("\n任务 4 · 数据不完整的账号:")
for a in snap:
    if a.get("complete") is False:
        print(" -", a.get("name"))