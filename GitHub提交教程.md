# GitHub 提交教程（Windows · 手把手）

> 面向：会打字、但没系统用过 Git 的人。
> 环境：Windows + VS Code + PowerShell + Git for Windows。
> 目标：**能把本地文件安全地提交到 GitHub，并且知道出错时怎么退。**

---

## 第 0 章 · 先搞懂四个地方

Git 让人迷糊，是因为文件会同时存在于**四个地方**：

```
① 工作区（你看到、改动的文件）
        ↓ git add
② 暂存区（"候选清单"，等着提交）
        ↓ git commit
③ 本地仓库（.git 目录，有历史记录）
        ↓ git push
④ 远端仓库（GitHub 上的那份）
```

| 你在哪 | 命令 | 结果 |
| --- | --- | --- |
| 改完文件 | `git status` | 红字：未跟踪 / 已修改 |
| 挑好要交的 | `git add` | 变绿：等待提交 |
| 拍快照 | `git commit` | 进本地历史 |
| 传出去 | `git push` | GitHub 上能看到 |

**关键认知：`commit` 不等于 `push`。**

- `commit` = 存到本机，**断网也能做**
- `push` = 传给 GitHub，**需要网络和权限**

**可以 commit 十次再 push 一次。**

---

## 第 1 章 · 一次性准备（只做一次）

### 1.1 设置身份

```powershell
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的用户名@users.noreply.github.com"
```

**验证：**

```powershell
git config --global user.name
git config --global user.email
```

**为什么要设：**

| 字段 | 作用 |
| --- | --- |
| `user.name` | 每个提交里记录的作者名 |
| `user.email` | 用来把提交关联到你的 GitHub 账号 |
| `--global` | 写进 `~/.gitconfig`，所有仓库通用 |

**为什么用 `noreply` 邮箱**：提交会公开显示作者邮箱，用 noreply 不会暴露真实邮箱，但 GitHub 仍能识别是你。

### 1.2 修掉中文显示问题

```powershell
git config --global core.quotepath false
```

否则 `git status` 里中文文件名会变成 `"\345\255\246\344\271\240..."` 这种八进制。

### 1.3 检查换行符设置

```powershell
git config --global core.autocrlf
```

输出 `true` 就对了（Windows 标准配置）。

---

## 第 2 章 · 第一次：从零推到 GitHub

### 2.1 在网页上建空仓库

```
https://github.com/new
├─ Repository name：英文、短横线，例如 learning-notes
├─ Public / Private：自己选
├─ 不要勾 "Add a README file"
└─ Create repository
```

**为什么不勾 README**：勾了会生成一个提交，你本地 `push` 时会因为"历史不一致"被拒，得先 `pull`。**新手最容易卡在这。**

### 2.2 本地准备目录

```powershell
cd D:\Backup\Documents\deepseek-harness
mkdir learning-notes
copy "default-workspace\学习编程-完整路线.md" "learning-notes\"
cd learning-notes
```

**验证：**

```powershell
dir
```

看到文件就对了。

### 2.3 初始化仓库

```powershell
git init
```

输出：

```
Initialized empty Git repository in D:\...\learning-notes\.git\
```

**`.git` 目录是全部历史，删了就全没了。**

### 2.4 写 `.gitignore`（重要）

```powershell
@"
# 系统文件
Thumbs.db
desktop.ini

# 编辑器
.vscode/
*.swp

# 凭据 —— 永远不要提交
*.token
.env
.dsh-backup-token
"@ | Set-Content .gitignore -Encoding UTF8
```

**为什么必须先做**：凭据一旦进了 git 历史，**每个提交里都有一份**，删不干净。

### 2.5 看状态

```powershell
git status
```

**会看到：**

```
On branch master

No commits yet

Untracked files:
        .gitignore
        学习编程-完整路线.md

nothing added to commit but untracked files present
```

**逐句读：**

| 输出 | 意思 |
| --- | --- |
| `On branch master` | 当前在 `master` 分支（老默认名） |
| `No commits yet` | 还没有任何提交 |
| `Untracked files` | 这些文件 git 知道存在，但没开始管理 |

### 2.6 加入暂存区

```powershell
git add .
```

**没有输出是正常的。**

**再查：**

```powershell
git status
```

```
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   .gitignore
        new file:   学习编程-完整路线.md
```

**`Untracked` → `Changes to be committed` = 成功。**

### 2.7 提交

```powershell
git commit -m "docs: 学习笔记（Day 1-6 + Markdown 速查）"
```

**成功输出：**

```
[master (root-commit) 44f65f2] docs: 学习笔记（Day 1-6 + Markdown 速查）
 2 files changed, 1305 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 学习编程-完整路线.md
```

`root-commit` = 第一个提交（没有父提交）。

### 2.8 改分支名

```powershell
git branch -M main
```

**GitHub 现在用 `main`，老 Git 默认 `master`。**
**必须在 push 之前改**，否则远端会建出一个 `master` 分支。

**验证：**

```powershell
git branch
```

输出 `* main` 就对了。

### 2.9 连接远端

```powershell
git remote add origin https://github.com/你的用户名/learning-notes.git
```

**验证：**

```powershell
git remote -v
```

```
origin  https://github.com/你的用户名/learning-notes.git (fetch)
origin  https://github.com/你的用户名/learning-notes.git (push)
```

**`origin` 只是"远端的一个代号"**，可以叫别的名字，但习惯上叫 origin。

### 2.10 推送

```powershell
git push -u origin main
```

**第一次可能弹窗：**

| 选项 | 说明 |
| --- | --- |
| **Sign in with your browser** | 推荐，浏览器授权一次 |
| Personal access token | 粘贴 token |

**`-u`** = 记住"以后 push 默认推到 origin/main"，**之后只需 `git push`**。

**成功输出：**

```
Writing objects: 100% (4/4), 16.85 KiB
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

### 2.11 验证

```powershell
git log --oneline
```

```
44f65f2 (HEAD -> main, origin/main) docs: 学习笔记（Day 1-6 + Markdown 速查）
```

- `HEAD -> main`：本地当前提交
- `origin/main`：远端也在同一位置

**两个都在同一行 = 完全同步。**

---

## 第 3 章 · 日常四步

**以后每次改完文件，就这四行：**

```powershell
git status              # 1. 我改了什么
git add .               # 2. 全部加入暂存区
git commit -m "说明"     # 3. 拍快照
git push                # 4. 推上去
```

**如果只是本地存档、暂不分享，第 4 步可以跳过。**

### 只想提交部分文件

```powershell
git add 文件A.md          # 只加 A
git commit -m "只改 A"    # 只提交 A，B 留着
```

**这就是"暂存区"存在的意义。**

---

## 第 4 章 · 看懂 `git status` 的三种红绿

### 情况一：新文件

```
Untracked files:
        new-file.md
```

**处理**：`git add new-file.md`

### 情况二：改过的文件

```
Changes not staged for commit:
        modified:   README.md
```

**处理**：`git add README.md`

### 情况三：已暂存

```
Changes to be committed:
        modified:   README.md
```

**处理**：`git commit -m "..."`

**记忆法：**

```
红字 = 还没准备好
绿字 = 准备好了，可以 commit
```

---

## 第 5 章 · 提交信息怎么写

**格式：**

```
类型: 简短说明
```

| 类型 | 什么时候用 |
| --- | --- |
| `feat` | 加了新东西 |
| `fix` | 修了 bug |
| `docs` | 只改文档 |
| `chore` | 杂项（配置、依赖） |
| `refactor` | 重构，行为不变 |

**好的例子：**

```
docs: 补 Day 6 缓存三层笔记
fix: SW 把 /vk-1/api/ 当静态资源缓存
feat: 加登录后补跑备份
```

**坏的例子：**

```
更新              ← 更新了什么？
改一下            ← 改哪里？
asdfasdf          ← 以后你也不懂
```

**为什么认真写**：三个月后你只会看到这行字，**它是唯一的线索**。

---

## 第 6 章 · 撤销与回退（救命技巧）

### 6.1 撤回还没提交的修改

```powershell
# 只看某个文件改了什么
git diff README.md

# 丢掉某个文件的修改（不可恢复！）
git checkout -- README.md
```

**⚠️ `checkout --` 是**丢弃**，不是"暂存"，丢完找不回。**

### 6.2 取消暂存（还没 commit）

```powershell
git restore --staged README.md
```

**效果**：从"待提交"退回"已修改"，**内容还在**。

### 6.3 撤销上一次提交（保留改动）

```powershell
git reset --soft HEAD~1
```

**效果：**

```
提交没了 → 改动回到了暂存区 → 文件内容一个字没丢
```

**这是最安全的撤销方式。**

### 6.4 撤销上一次提交（连改动一起丢）

```powershell
git reset --hard HEAD~1
```

**⚠️ 改动会永久消失。** 除非你确定不要了。

### 6.5 已经 push 了怎么办

```powershell
git revert HEAD
git push
```

**`revert` 不是删历史，而是"新增一个反向提交"**——把上一次的改动抵消掉。

**为什么不直接 `reset` 后强推**：强推会改写别人的历史，团队协作里是禁忌。

---

## 第 7 章 · 分支（知道有这回事就行）

```powershell
git branch                  # 看有哪些分支
git branch test             # 新建 test 分支
git switch test             # 切过去
git switch main             # 切回来
git merge test              # 把 test 合进当前分支
```

**个人小仓库其实可以一直用 `main`。**

**什么时候需要分支**：想试一个改动但不确定要不要，就开个分支折腾，不满意直接删。

---

## 第 8 章 · 两个配置文件

### `.gitignore` —— 哪些文件不进仓库

```
node_modules/       # 依赖
*.log               # 日志
.env                # 环境变量
*.token             # 凭据
Thumbs.db           # 系统缩略图
```

**已经被跟踪的文件，加进 .gitignore 不会失效**，要先：

```powershell
git rm --cached 文件名
```

### `.gitattributes` —— 换行符统一

```
* text=auto
*.md text eol=lf
*.ps1 text eol=crlf
```

**作用**：消除 `LF will be replaced by CRLF` 警告，让格式可预测。

| 文件 | 仓库里 | 检出后 |
| --- | --- | --- |
| `.md` | LF | LF |
| `.ps1` | LF | CRLF |

---

## 第 9 章 · 常见错误对照表

| 报错 | 原因 | 解决 |
| --- | --- | --- |
| `Please tell me who you are` | 没配身份 | `git config --global user.name/email` |
| `fatal: not a git repository` | 不在仓库目录 | `cd` 到有 `.git` 的目录 |
| `src refspec main does not match any` | 还没 commit 就 push | 先 `git commit` |
| `failed to push some refs` | 远端有你没有的提交 | `git pull --rebase` 再 push（详见第 9.5 章） |
| `Authentication failed` | 凭据失效 | `cmdkey /delete:git:https://github.com` 重来 |
| `Repository not found` | 用户名/仓库名写错 | `git remote -v` 检查 |
| `nothing to commit` | 没有改动 / 没 add | 先改文件或 `git add` |
| `LF will be replaced by CRLF` | Windows 换行警告 | **可以忽略** |
| 中文文件名显示成八进制 | quotepath | `git config --global core.quotepath false` |

---

## 第 9.5 章 · push 被拒绝（`fetch first`）

**这是最常见、也最容易被误解的错误。**

### 报错长什么样

```
To https://github.com/你的用户名/learning-notes.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '...'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
```

### 为什么会这样

**远端多了一个你本地没有的提交。** 常见来源：

| 来源 | 例子 |
| --- | --- |
| 在 GitHub 网页上直接改文件 | 用 `Add file` 加了 README |
| 网页上加了 LICENSE | 许可证选择器自动生成的提交 |
| 另一台设备 push 过 | 手机、另一台电脑 |
| 你开了两个目录 | 同一个仓库在两处改了不同东西 |

**用图看：**

```
远端：  A ── B ── C        ← 网页上加了 C
本地：  A ── B ── D        ← 本地提交了 D

git push 想让远端变成 A─B─D
但 D 的位置已经被 C 占了
→ 拒绝（怕覆盖 C，让 C 消失）
```

**git 的默认态度是「不猜」：宁可拒绝，也不悄悄覆盖。**

### 修复：先合并，再推送

```powershell
git fetch origin
git log --oneline origin/main -3
```

**先看看远端到底多了什么**，确认是不是你自己改的。

然后：

```powershell
git pull --rebase
```

**两种结果：**

#### 情况 A：没有冲突（大多数）

```
Successfully rebased and updated refs/heads/main.
```

```powershell
git push
```

**完成。**

#### 情况 B：报冲突

```
CONFLICT (content): Merge conflict in README.md
error: could not apply abc1234...
```

**说明两边改了同一个文件。**

**① 打开冲突文件，会看到：**

```text
<<<<<<< HEAD
你本地的改动
=======
远端（网页上）的改动
>>>>>>> origin/main
```

**② 手工决定保留什么**（可以两边都留，也可以只留一边），**删掉那三行标记**。

**③ 继续：**

```powershell
git add .
```

```powershell
git rebase --continue
```

**如果弹出编辑器（vim）：** 输入 `:wq` 回车退出。

**④ 推送：**

```powershell
git push
```

### 搞乱了想重来

```powershell
git rebase --abort
```

**回到 pull 之前的状态**，然后重新判断。

### `--rebase` 和默认的区别

| 命令 | 结果 |
| --- | --- |
| `git pull`（默认 merge） | `A─B─C─M`（多一个合并提交，历史分叉） |
| `git pull --rebase` | `A─B─C─D`（一条直线，更干净） |

**个人项目统一用 `--rebase`。**

### 怎么预防

**养成一个习惯：动手前先拉。**

```powershell
git pull
```

**尤其在这些时候：**

- 刚在网页上改过文件
- 换了台设备
- 隔了几天没提交

**另一个原则：同一份文件，别同时在网页和本地改。**

### 一句话

> **`rejected (fetch first)` 不是"你错了"，是"有人先到"——先合并，再排队。**

---

## 第 9.6 章 · rebase 卡住了怎么办

**`git status` 突然显示这些话，说明仓库卡在一个"未完成的 rebase"里：**

```text
You are currently editing a commit while rebasing branch 'main' on 'd408aea'.
  (use "git commit --amend" to amend the current commit)
  (use "git rebase --continue" once you are satisfied with your changes)

nothing to commit, working tree clean
```

**或者：**

```text
interactive rebase in progress; onto 1a2b3c4
```

**这时候你看到的是「旧状态」——上一次 rebase 中途被打断了。**

### 三个出口（选一个，不要放着不管）

| 命令 | 做什么 | 什么时候用 |
| --- | --- | --- |
| `git rebase --continue` | 继续往下执行 | 你已经解决完冲突/改完了 |
| `git rebase --quit` | **清掉 rebase 状态，但提交和分支都不动** | 你发现状态是残留的、HEAD 已经是对的 |
| `git rebase --abort` | 回到 rebase 开始前的状态 | 整个 rebase 不想要了 |

### 最关键的一条：怎么选

**先看提交还在不在远端：**

```powershell
git rev-parse HEAD
git branch -r --contains HEAD
```

**如果输出里有 `origin/main`，说明当前提交已经在远端了——那就不该用 `--abort`（它会把分支退回去，让你本地丢掉这些提交）。**

**这种情况用：**

```powershell
git rebase --quit
```

**它只清除"rebase 进行中"这个状态标记，一个提交都不动。**

### 一个真实例子

```powershell
# 卡住时看到的
You are currently editing a commit while rebasing branch 'main' on 'd408aea'

# 先确认提交在远端
git branch -r --contains HEAD
#   origin/HEAD -> origin/main,  origin/main     ← 在！

# 所以用 --quit，而不是 --abort
git rebase --quit

# 结果：分支名回到 main，提交全在，工作区 clean
```

### 卡住时不要做的事

| ❌ 动作 | 后果 |
| --- | --- |
| 继续 `git commit` | 会往临时 HEAD 上叠提交，可能重复或丢失 |
| 直接 `git push` | 被拒，或推错分支 |
| `git switch` 别的分支 | git 会拒绝（uncommitted changes / rebase in progress） |
| 手删 `.git/rebase-merge` 目录 | 能用，但不如 `--quit` 干净 |

**规则：先处理 rebase 状态，再做任何提交操作。**

### 怎么避免走到这一步

**rebase 中途打断的两大原因：**

1. **冲突没解决完就关掉了终端**
2. **冲突解决后忘了 `git add` 就 `--continue`**

**正确流程：**

```powershell
git pull --rebase
# 如果有冲突
#   → 手工改文件，删掉 <<<<<<< ======= >>>>>>> 标记
git add .
git rebase --continue
# 如果又冲突，重复上面
```

### 一句话

> **rebase 卡住不是坏了，是暂停了——`--continue` 继续、`--quit` 收摊、`--abort` 重来，三个总得选一个。**

---

## 第 10 章 · 图形界面（不想打命令时）


**VS Code 里也有完整流程：**

```
1. 左侧「源代码管理」图标（三个分叉）
2. 文件列表里点 "+" 加入暂存
3. 上方输入框写提交说明 → 点 ✓ 提交
4. 点 "..." → Push
```

**同样的四步，只是图形化。**

**⚠️ 最容易误点的是「Discard Changes」**——那是**丢弃修改**，没有确认框，丢完找不回。

---

## 速查卡

```powershell
# —— 一次性 ——
git config --global user.name  "名字"
git config --global user.email "邮箱"
git config --global core.quotepath false

# —— 新仓库 ——
git init
git add .
git commit -m "init"
git branch -M main
git remote add origin <URL>
git push -u origin main

# —— 日常 ——
git pull                   # 动手前先拉（尤其网页上改过）
git status
git add .
git commit -m "说明"
git push

# —— 查看 ——
git log --oneline          # 提交历史
git diff                   # 未暂存的改动
git diff --staged          # 已暂存的改动

# —— 撤销 ——
git restore --staged <file>     # 取消暂存
git checkout -- <file>          # 丢弃修改（危险）
git reset --soft HEAD~1         # 撤销提交，保留改动
git revert HEAD                 # 反向提交（已 push 后）

# —— rebase 卡住时，三选一 ——
git rebase --continue           # 继续
git rebase --quit               # 只清状态，提交不动（HEAD 已对时用这个）
git rebase --abort              # 整体退回 rebase 之前
```

---

## 一句话

> **`commit` 是给未来的自己留证据：证明"当时是这样"。**
>
> 改坏了能回去，改对了能追溯，这就是全部意义。

---

*写于 2026-11-08 · 配套：`learning-notes` 仓库*
