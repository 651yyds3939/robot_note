打开VPN指令： `~/clash$    ./clash -d .`

新建文件指令  `touch 文件名称`

打开base环境`conda activate base`
打开base里面的ros2环境`conda activate ros2`
退出base环境`conda deactivate`
打开Julyter `jupyter-notebook`
打开rqt `rqt`

`source install/setup.bash`

wget http://fishros.com/install -O fishros && . fishros

# Git 基础操作全流程笔记 (ROS2 项目实战版)

本笔记涵盖了从本地初始化、忽略文件配置、日常存档到远程 GitHub 同步的完整工作流。

## 1. 环境准备与初始化 (仅需执行一次)
# 配置全局身份标识（建议与 GitHub 账号一致）
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱@example.com"
# 进入你的 ROS2 工作空间并初始化仓库
cd ~/d2lros2/chapt5/chapt5_ws
git init

## 2. 忽略文件配置 (.gitignore)
# 在工作空间根目录下创建 .gitignore 文件，防止记录编译产物
# 内容如下：
build/
install/
log/
.vscode/
.DS_Store
*.pyc

## 3. 日常开发存档流程 (核心循环)
# [步骤 1] 查看当前改动状态
git status
# [步骤 2] 将改动添加到暂存区
git add .
# [步骤 3] 正式提交存档 (必须写清楚备注)
git commit -m "feat: 完成了话题订阅者节点的编写与测试"
# [步骤 4] 查看存档历史记录
git log --oneline

## 4. 撤销与“后悔药” (救命指令)
# 场景 1：代码改乱了，想一键回到上一次 commit 的状态
git checkout .
# 场景 2：add 错文件了，想撤回 add (代码不会丢)
git reset HEAD <文件名>
# 场景 3：刚刚 commit 完发现备注写错了，想修改备注
git commit --amend -m "更新后的正确备注"

## 5. 云端同步 (GitHub 联动)
# [步骤 1] 关联远程 GitHub 仓库 (仅需执行一次)
git remote add origin https://github.com/用户名/仓库名.git
# [步骤 2] 第一次推送代码并设定主分支
git push -u origin master
# [步骤 3] 以后日常一键推送
git push
# [步骤 4] 从云端拉取最新代码到本地
git pull

## 💡 ROS2 开发金律
# 1. 先编译再存档：确保 colcon build 通过后再进行 git commit。
# 2. 多存档少痛苦：每一个小功能实现就存一次档，不要攒一天才存。
# 3. 保护 .git：永远不要手动修改 .git 文件夹里的内容。
