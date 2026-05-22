明白，大哥！是我刚才想复杂了，咱们直接来干货。

这是一个**全能型指令大合集**。涵盖了你从拉取代码到清理 Docker 垃圾的所有必备动作。建议你直接**一键复制**，存进你的笔记应用里。

```markdown
# 🚀 Ubuntu 资源获取与系统清理全指南 (2026 极致实战版)

本指南专为机器人开发者（ROS2, Isaac Sim, AI）设计，特别针对 16G 内存系统优化。

---

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

---

## 2. 容器镜像拉取 (Docker)

针对 nvcr.io 等国外私有仓库，灵活使用代理是关键。

```bash
# --- 拉取镜像 ---
docker pull <image_name>:<tag>

# --- 使用代理前缀加速 (2026 常用) ---
docker pull docker.1ms.run/nvcr.io/nvidia/isaac-sim:4.2.0

# --- 镜像管理 ---
docker images                  # 查看本地所有镜像
docker ps -a                   # 查看所有容器（包括已停止的）
docker tag <old> <new>         # 重命名标签（适配脚本）

```

---

## 3. 软件包与环境管理 (APT, Pip, Conda)

这些工具的缓存非常占空间，务必定期清理。

```bash
# --- APT (系统级) ---
sudo apt update && sudo apt install <package>  # 安装
sudo apt-get download <package>                # 仅下载 .deb 包不安装

# --- Pip (Python) ---
pip install <package>
pip install -e .                               # 以可编辑模式安装本地包

# --- Conda (环境管理) ---
conda create -n <name> python=3.10             # 创建环境
conda env create -f environment.yml            # 从配置文件恢复环境

```

---

## 4. 通用下载工具 (Wget & Curl)

下载大文件时，一定要开启**断点续传**。

```bash
# --- Wget ---
wget -c <url>                  # 断点续传（网络不稳时必用）
wget -b <url>                  # 后台下载，关掉终端也能跑

# --- Curl ---
curl -C - -O <url>             # 断点续传下载

```

---

## 5. 深度清理与残留删除 (回血神技)

**16G 内存系统的生存保障**。在运行 Isaac Sim 前，先执行这些命令。

```bash
# --- Docker 深度清理 (清理下载残留、废弃容器) ---
docker system prune -a         # 删除所有未使用的镜像、容器和网络
docker builder prune           # 清理构建缓存（能腾出好几个G）
docker rmi <image_id>          # 强制删除指定镜像

# --- 系统清理 (APT) ---
sudo apt autoremove            # 删除不再需要的依赖包
sudo apt clean                 # 清除 /var/cache/apt/archives 下的缓存包

# --- Python 缓存清理 (Isaac Sim 依赖包非常大) ---
pip cache purge                # 清理 Pip 下载缓存
conda clean --all              # 清理 Conda 无用包和索引缓存

# --- Git 清理 ---
git clean -df                  # 递归删除仓库中未跟踪的文件

```

---

## 6. 存储空间诊断

随时监控，防止磁盘写满导致系统崩溃。

```bash
df -h                          # 查看磁盘分区剩余空间
du -sh * | sort -h             # 查看当前目录下文件夹大小并排序
watch -n 2 df -h               # 每 2 秒刷新一次空间，下载大文件时盯着它用

```

```

### 💡 给大哥的最后一点建议：

你现在那 16G 内存的 **R9000P** 就像一辆载重有限的货车，Isaac Sim 是一个超大货物。

* **下载完镜像后**，先跑一下上面的 `pip cache purge` 和 `docker builder prune`。
* 把磁盘空间和内存水位“回满血”后，再启动训练脚本。

如果你在执行上面的 `docker system prune -a` 时提示“正在使用中”，记得先用 `docker stop $(docker ps -a -q)` 关掉所有容器。

```