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
| `failed to push some refs` | 远端有你没有的提交 | `git pull --rebase` 再 push |
| `Authentication failed` | 凭据失效 | `cmdkey /delete:git:https://github.com` 重来 |
| `Repository not found` | 用户名/仓库名写错 | `git remote -v` 检查 |
| `nothing to commit` | 没有改动 / 没 add | 先改文件或 `git add` |
| `LF will be replaced by CRLF` | Windows 换行警告 | **可以忽略** |
| 中文文件名显示成八进制 | quotepath | `git config --global core.quotepath false` |

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
```

---

## 一句话

> **`commit` 是给未来的自己留证据：证明"当时是这样"。**
>
> 改坏了能回去，改对了能追溯，这就是全部意义。

---

*写于 2026-11-08 · 配套：`learning-notes` 仓库*
