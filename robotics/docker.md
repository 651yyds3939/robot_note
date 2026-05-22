#  📦 Docker 容器化与系统欺骗高级指南

> **核心摘要**：Docker 不是虚拟机（Virtual Machine），它是利用 Linux 内核特性实现的**进程隔离**。理解它，是进入企业级机器人开发的第一道门槛。本笔记涵盖了容器挂载逻辑、权限陷阱、网络代理配置以及高阶环境打包方案。

---

## 一、 Docker 核心基石：Namespaces 与 Cgroups

*   **Namespaces（命名空间）**：Docker 的“障眼法”。它让容器内的进程以为自己拥有独立的 PID（进程号 1）、独立的网络接口和独立的文件系统。你在 Docker 里看到的 `/`（根目录），其实只是宿主机硬盘深处（`/var/lib/docker/overlay2/`）的一个普通文件夹。
*   **Cgroups（控制组）**：Docker 的“紧箍咒”。它限制这个容器最多只能用宿主机（如 笔记本电脑有多少 CPU 核心和多少内存。

---

## 二、 挂载逻辑（Volume Mounting）：跨越次元的传送门

Docker 容器一旦销毁，里面的数据就会灰飞烟灭（无状态化）。为了保留代码，必须使用挂载。

*   **映射指令**：`-v /home/lwy/kuavo-ros-opensource:/root/kuavo_ws`
*   **底层机制（Bind Mount）**：Docker 强制将容器内的 `/root/kuavo_ws` 目录的 inode 指针，强行指向宿主机的 `/home/lwy/kuavo-ros-opensource`。
*   **唯一入口铁律**：容器启动时，入口就已经焊死。如果你在宿主机把代码放在了 `kuavo-clean`，而容器挂载的是 `kuavo-ros-opensource`，那么容器内部绝无可能看到 `kuavo-clean` 里的东西。这就好比投影仪只能照着一张幻灯片。

---

## 三、 权限错位综合征：那个讨厌的“红色小锁”

这是 Docker 与宿主机文件系统交互时最常见的陷阱。

*   **身份的割裂**：
    *   **宿主机（外界）**：你是普通用户 `lwy`，系统底层身份代码为 `UID 1000`。
    *   **Docker（内部）**：你是超级管理员 `root`，身份代码为 `UID 0`。
*   **锁的诞生**：当你在 Docker 内部执行 `catkin_make` 或 `touch` 创建文件时，Linux 内核会把这些文件的拥有者标记为 `UID 0`。当你回到宿主机图形界面，Ubuntu 发现你是 `UID 1000`，为了保护 `root` 的财产，直接给你挂上红锁，甚至拒绝刷新文件夹内容（导致“文件消失”的错觉）。
*   **终极解药**：永远记得在宿主机使用 `sudo chown -R lwy:lwy <目录>` 把文件的所有权抢回来。

---

## 四、 高阶进阶：Docker 开发环境与项目打包

不仅要在无菌环境里开发，还要能把自己的成果打包成“数字集装箱”，发给任何人都能一键运行。

### 4.1 方案 A：使用 Dev Containers 进行“无痕开发”
让 VS Code 直接在容器里写代码，本机无需安装复杂环境（如 ROS 2）：
1.  本机安装 Docker，并在 VS Code 中安装 **Dev Containers** 插件。
2.  在项目根目录按 `Ctrl+Shift+P`，搜索 `Dev Containers: Add Dev Container Configuration Files` -> 选择所需环境（如 `ROS 2 Humble`）。
3.  点击弹出的 **"Reopen in Container"**。代码补全和编译都在容器内完成，与本机彻底隔离。

### 4.2 方案 B：将自己的项目打包成发行镜像（核心发版能力）
当你的项目写完了，想部署到实车或者发给别人展示，请在你工作空间的根目录下，新建一个 `Dockerfile`：
```dockerfile
# 1. 声明底层环境 (自带 ROS 2 Humble)
FROM osrf/ros:humble-desktop

# 2. 设置容器内的工作目录
WORKDIR /my_robot_ws

# 3. 把你当前电脑的源码 (src) 拷贝到镜像里
COPY src/ ./src/

# 4. 安装属于你项目的特定依赖
RUN apt-get update && rosdep update && \
    rosdep install --from-paths src --ignore-src -y

# 5. 编译你的项目 (注意：要先 source 一下系统 ROS 2 环境)
RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build"

# 6. 配置启动脚本 (ENTRYPOINT)
# 这一步保证了别人一旦 run 这个镜像，环境就已经挂载好了
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "source /my_robot_ws/install/setup.bash" >> ~/.bashrc

# 7. 默认执行的命令 (可选项，比如启动你的主节点)
# CMD ["ros2", "launch", "my_package", "main.launch.py"]
```

**打包与导出分享指令：**
```bash
# 构建你自己的镜像 (打上 v1.0 标签)
docker build -t my_robot_project:v1.0 .

# 将镜像导出为压缩包，用 U 盘拷给任何人！
docker save -o my_robot_project_v1.0.tar my_robot_project:v1.0

# 别人拿到压缩包后的加载与运行命令：
docker load -i my_robot_project_v1.0.tar
docker run -it --net=host my_robot_project:v1.0 /bin/bash
```

---

## 五、 高阶终端指令速查字典 (Docker篇)

这些指令必须融入肌肉记忆，是应对开发底层问题的最强武器。

---

### 5.1 Docker 深度交互与挂载逻辑控制

这些指令是开发者深入容器底层、解决挂载冲突和环境隔离的最强武器。

#### 1. 运行状态与挂载寻踪（诊断位）

在调试多个工作空间映射时，首先确认“我在哪”以及“物理路径在哪”。

```bash
# 【查看】列出当前正在运行的容器（获取 CONTAINER ID 或 NAME）
docker ps

# 【透视】核心：像 X 光片一样，透视容器到底挂载了宿主机的哪个文件夹
# 过滤掉干扰项，直接定位 Source 物理路径
docker inspect <容器ID或名字> | grep -C 5 "Source" | grep -v "/dev"

```

#### 2. 宿主机与容器的“跨空搬运”（数据位）

无需通过 Git 或 U 盘，直接在两个物理隔离的文件系统间传输权重模型或日志。

```bash
# 从容器往外拿（例：提取训练日志到宿主机）
docker cp <容器名>:/root/fast_lio_ws /home/lwy/

# 往容器里送（例：把新炼好的 ONNX 模型送入部署环境）
docker cp /home/lwy/my_file.txt <容器名>:/root/

```

#### 3. 开发环境的一键起航（启动位）

针对 Kuavo 机器人的不同场景，选择最合适的进入方式。

```bash
# A. 官方快捷方式（依赖仓库内的脚本）
xhost +local:docker
./docker/run.sh

# B. 【推荐】手动全功率模式（暴力拆解挂载逻辑，强制开启 GPU 和显示投影）
docker run -it  \
    --name kuavo_container \
    --gpus all \
    --privileged \
    --network host \
    --env="DISPLAY" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $(pwd):/root/kuavo_ws \
    kuavo_opensource_mpc_wbc_img:1.3.0 \
    zsh

```

#### 4. 容器生命周期二次进入（管理位）

当容器已存在但处于后台时，无需重新 `run`，直接唤醒。

```bash
#查看已有哪些容器
docker ps -a

#查看每个容器占用的空间
docker ps -as

# 唤醒已停止的容器
docker start kuavo_container

# 以 Zsh 终端身份钻入正在运行的后台容器
docker exec -it kuavo_container zsh

# (备用) 以 Bash 身份钻入
docker exec -it kuavo_container /bin/bash

#删除某个容器，需要先查看已有容器的名字
docker rm 容器名如：6211bcba5b9e

```


### 5.2 docker网络走代理
```bash
clash打开允许局域网连接
export http_proxy=http://172.17.0.1:7890
export https_proxy=http://172.17.0.1:7890

unset http_proxy https_proxy
```

---

## 六、 附录：实战案例复盘 —— Docker 内外的相对论

*   **案情**：在宿主机终端输入 `cd ~/fast_lio_ws/src` 报错“没有该目录”。
*   **排查**：`fast_lio_ws` 是在 Docker 容器最上层的私有读写层中创建的，并未通过 `-v` 映射到宿主机。宿主机的 `~/` 是 `/home/lwy`，而 Docker 的 `~/` 是 `/root`。
*   **破局**：理解“内外结界”。对于未挂载的纯容器内部数据，必须钻入容器 (`docker exec`) 才能访问；或者使用 `docker cp` 将其提取到宿主机。
