# 🌿 Git 与 GitHub 工业级代码管理与多分支操作指南

> **核心摘要**：在大型协作项目（如机器人二次开发、算法迭代）中，Git 不仅仅是用来备份的，它是管理代码冲突、追溯 Bug 责任的“司法系统”。本笔记详细记录了 Git 底层架构、GitHub 纯净仓库的构建、多分支的安全切换以及子模块（Submodule）的连环陷阱防范。

---

## 一、 Git 三层架构与快照机制

与 Windows 的复制粘贴不同，Git 采用的是**快照（Snapshot）加差分**机制，极度轻量。代码在本地存在于三个核心区域：
1.  **工作区（Working Directory）**：你当前在 VS Code 里编辑的文件。
2.  **暂存区（Staging Area / Index）**：执行 `git add` 后，文件被打包准备上车。这给了你反悔的机会。
3.  **本地仓库（Local Repository）**：执行 `git commit` 后，代码正式写入 `.git` 隐藏目录，生成了一个不可篡改的 SHA-1 哈希值（如 `3cd6834`）。
*   **GitHub 的角色**：它只是一个装有 Git 环境的远端服务器，`git push` 就是把本地 `.git` 里的历史记录同步过去。

---

## 二、 基础实战：从零重建纯净仓库推送到 GitHub

当你 clone 了别人的大型项目，想修改后上传到自己的 GitHub，但遭遇大文件（`.git` 过大）或嵌套子仓库污染时，请严格按照此流程操作。

**🚨 铁律：Git 只适合存代码，严禁存放 `.bag`, `.tar.gz`, `build/`, `log/`。**

### 2.1 物理隔离与旧历史抹除
```bash
# 复制出纯净副本进行操作
cd ~
cp -r kuavo-ros-opensource kuavo-clean
cd kuavo-clean

# 彻底删除旧项目的 Git 历史包袱
rm -rf .git
```

### 2.2 构建免疫系统 (`.gitignore`)
创建并编辑 `.gitignore`，阻止垃圾文件进入暂存区：
```bash
nano .gitignore
```

```gitignore
# ROS 衍生文件
build/
install/
log/
# 数据与压缩包
*.bag
*.db3
*.tar.gz
*.zip
*.7z
```

### 2.3 处理嵌套 Git 仓库（极其重要）
如果报错 `warning: adding embedded git repository`，说明别人的工程里套了别人的工程，必须暴力拆解：
```bash
git rm --cached -r -f src/apriltag
git rm --cached -r -f src/aws-robomaker-hospital-world

rm -rf src/apriltag/.git
rm -rf src/aws-robomaker-hospital-world/.git
```

### 2.4 重建、提交与分支修正
```bash
git init
git add .
git commit -m "clean project & fix nested repos"

# 修正可能出现的主分支名称不匹配错误
git branch -M main
```

### 2.5 GitHub 绑定与推送 (Token 认证)
*   **创建仓库**：在 GitHub 创建私有仓库，**不要勾选** README/gitignore/license 初始化。
*   **Token 登录**：GitHub 已禁止密码推送，必须生成 `Tokens (classic)`（勾选 `repo` 权限）。
*   **推流**：
```bash
git remote add origin [https://github.com/你的用户名/仓库名.git](https://github.com/你的用户名/仓库名.git)
git push -u origin main
# 登录时 Password 输入 Token

# 强烈建议保存 Token 免密登录：
git config --global credential.helper store
```

---

## 三、 高阶实战：Git 多分支切换与现场保留全场景指南

在切换不同分支（如算法分支与比赛分支）时，盲目切换极易导致环境崩溃。请严格执行以下五个阶段。

### 第零阶段：摸清底牌
```bash
git status
git diff
```

### 第一阶段：处理当前现场（根据需求二选一）
*   **方案 A：纯净重置（放弃修改）**
    ```bash
    sudo chown -R $USER:$USER .  # 解决 Docker 遗留的权限锁
    git checkout .               # 清除追踪文件修改
    git clean -fd                # 强制清理未追踪的新文件（慎用！）
    ```
*   **方案 B：打包带走（暂存本地修改）**
    ```bash
    git stash -u                 # 强力暂存（包含新建的未追踪文件）
    git stash list               # 确认入库
    ```

### 第二阶段：刷新与精准跳跃
```bash
git fetch --all              # 强制刷新远程最新状态
git branch -a                # 查看本地与远程路线图
git checkout <目标分支名>      # 例如 git checkout main
```

### 第三阶段：同步外包模型（极其致命的子模块陷阱！）
**必须执行**。人形机器人依赖大量第三方库，分支切换后，必须让当前分支的子模块文件夹也切换到对应的特定 Commit ID，否则模型会丢失。
```bash
git submodule update --init --recursive
```

### 第四阶段：恢复现场（仅针对选了“方案 B”的人）
```bash
git stash pop                # 弹出修改并应用（若有 Merge conflict 需去 VSCode 解决冲突）
```

---

## 四、 细节警惕：大小写的绝对严谨
*   Windows 不区分大小写（`readme.md` = `README.md`）。
*   Linux 的 Ext4 文件系统严格校验 ASCII 码。因此，官方的 `readme.md` 和你自创的 `READEME.md` 可以完美并存在同一个文件夹里，只是在红锁权限遮蔽下，图形界面可能优先折叠了你新创建的那个。

---

## 五、 高阶终端指令速查字典 (Git篇)

```bash
# 1. 克隆时顺便把所有嵌套的子模块（如别人写的驱动）一起拉下来
git clone --recursive [https://github.com/xxxxx.git](https://github.com/xxxxx.git)

# 2. 如果克隆时忘了加 recursive，用这行命令亡羊补牢
git submodule update --init --recursive

# 3. 开发新功能前，永远记得先开辟平行时空（分支），不要污染主线
git checkout -b lwy_feature_slam

# 4. 全局搜索“失踪”的文件（忽略那些 permission denied 的废话警告）
sudo find / -name "my_first_package" 2>/dev/null

# 5. 模糊搜索包含某个关键词的文件
sudo find ~/ -iname "*READ*" -ls

# 6. 查找最近 60 分钟内被修改过的所有文件（破案专用）
find ~/ -mmin -60 -type f




## 1. 源码与代码仓库获取 (Git & VCS)
机器人项目经常包含大量子模块，必须掌握递归克隆。

```bash
# --- Git 基础 ---
git clone <url>                # 克隆仓库
git pull origin <branch>       # 拉取最新代码
git clone --recursive <url>    # 递归克隆（带子模块，机器人开发常用）

# --- 强制对齐远程仓库 (本地乱了时的救命稻草) ---
git fetch --all
git reset --hard origin/main   # 放弃所有本地修改，强制同步远程

# --- VCS (多仓库管理，ROS必备) ---
vcs import src < my.repos      # 批量导入 .repos 文件中的仓库
vcs pull src                   # 批量拉取所有仓库更新

```