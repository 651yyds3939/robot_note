# 1. 创建 8G 的交换文件
sudo dd if=/dev/zero of=/swapfile bs=1M count=8192

# 2. 设置权限
sudo chmod 600 /swapfile

# 3. 格式化并启用
sudo mkswap /swapfile
sudo swapon /swapfile

# 4. (可选) 永久生效：将其写入系统配置
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 5. 验证是否看到 Swap 有 8G 左右
free -h
