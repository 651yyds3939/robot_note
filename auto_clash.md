# Ubuntu 开发环境自动化完全手册 (Jupyter & Clash & ROS2)

## 1. Jupyter Notebook 路径与环境配置
# 生成配置文件（如果已生成则跳过）
jupyter-notebook --generate-config

# 修改配置文件：gedit ~/.jupyter/jupyter_notebook_config.py
# 找到并取消注释（删掉#），修改为：
c.ServerApp.notebook_dir = '/home/lwy/Jupyter_notes'

# 配置终端快捷启动别名：gedit ~/.bashrc
# 在文件末尾添加以下一行，实现一键激活环境并启动：
alias jpt='conda activate ros2 && source /opt/ros/humble/setup.bash && jupyter-notebook'

# 使配置生效
source ~/.bashrc

./clash -d .

## 2. Clash 系统服务自动化 (Systemd)
# 创建并编辑服务文件：sudo gedit /etc/systemd/system/clash.service
# 将以下内容完整粘贴进文件：
[Unit]
Description=Clash 自动启动服务
After=network.target

[Service]
Type=simple
User=lwy
WorkingDirectory=/home/lwy/clash
ExecStart=/home/lwy/clash/clash -d .
Restart=on-failure

[Install]
WantedBy=multi-user.target

# 激活并启动后台服务指令：
sudo systemctl daemon-reload      # 重新加载系统服务配置
sudo systemctl enable clash        # 设置开机自动启动
sudo systemctl start clash         # 立即启动服务
sudo systemctl status clash        # 查看服务状态（绿色 active 为正常）
sudo systemctl restart clash       # 重启服务（修改配置后使用）
journalctl -u clash -f             # 实时查看 Clash 运行日志
sudo systemctl stop clash          #暂时关闭

# 取消clash开机自启动：
sudo systemctl stop clash # 1. 停止当前正在运行的服务
sudo systemctl disable clash # 2. 禁用开机自启（下次开机就不会自动运行了）
sudo rm /etc/systemd/system/clash.service # 3. (可选) 彻底删除服务文件
sudo systemctl daemon-reload


## 3. ROS2 环境、参数管理及文件维护
# 激活 ROS2 底层环境
source /opt/ros/humble/setup.bash

# 导出当前节点参数到文件（备份/记录）
ros2 param dump /turtlesim > ~/Jupyter_notes/turtlesim.yaml

# 启动节点时加载指定的参数文件
ros2 run turtlesim turtlesim_node --ros-args --params-file ~/Jupyter_notes/turtlesim.yaml

# 生成当前系统的坐标树结构图（产生 .gv 和 .pdf 文件）
ros2 run tf2_tools view_frames

# 批量归档主目录散落的笔记与调试文件
mv ~/*.ipynb ~/Jupyter_notes/
mv ~/*.pdf ~/*.gv ~/*.png ~/Jupyter_notes/

# 递归修复文件夹读写权限（确保 Jupyter 能正常保存）
sudo chown -R lwy:lwy ~/Jupyter_notes
