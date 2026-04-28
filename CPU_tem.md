# Ryzen 7 5800H 笔记本 CPU 限频与控温（Linux / Ubuntu）

## 🎯 目标

在运行 Gazebo / ROS / 仿真任务时：

* 防止 CPU 频率过高（Boost 到 4GHz）
* 避免温度达到 100°C
* 保持性能基本不损失
* 提高系统稳定性

---

## 🧠 问题背景

在笔记本 CPU（如 Ryzen 7 5800H）上：

* 默认会开启 **Turbo Boost**
* 即使 CPU 占用不高，也会冲到 4GHz+
* 导致：

  * 温度迅速升到 95~100°C
  * 风扇狂转
  * 长时间运行不稳定

⚠️ 关键点：
`cpufreq-set -u` **无法限制 Boost 频率**

---

## ✅ 最终解决方案（核心步骤）

### 1️⃣ 关闭 CPU Boost（最关键）

```bash
echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost
```

---

### 2️⃣ 设置最高频率

```bash
sudo cpufreq-set -r -u 3.2GHz
```

---

### 3️⃣ 设置最低频率（可选）

```bash
sudo cpufreq-set -r -d 1.8GHz
```

---

### 4️⃣ 设置调度策略（governor）

```bash
sudo cpufreq-set -r -g powersave
```

---

## 🔍 验证是否生效

```bash
watch -n 1 "cat /proc/cpuinfo | grep MHz"
```

---

## 🌡️ 实际效果（参考）

| 状态       | 优化前        | 优化后        |
| -------- | ---------- | ---------- |
| CPU频率    | 3.9~4.0GHz | 3.0~3.2GHz |
| 温度       | 95~100°C   | 75~85°C    |
| 噪音       | 很大         | 明显降低       |
| Gazebo帧率 | 正常         | 基本无影响      |

---

## ⚠️ 常见问题

### ❌ 限频后仍然 4GHz？

👉 没关闭 Boost

---

### ❌ cpufreq-set 报错？

👉 没用 sudo

---

### ❌ governor 设置无效？

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors
```

---

## 🚀 一键执行

```bash
echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost
sudo cpufreq-set -r -u 3.2GHz
sudo cpufreq-set -r -d 1.8GHz
sudo cpufreq-set -r -g powersave
```

---

# 🔥 开机自动执行（systemd 推荐方案）

## 🎯 目标

让上述限频策略在**每次开机自动生效**

---

## 1️⃣ 创建脚本

```bash
sudo nano /usr/local/bin/cpu-limit.sh
```

写入：

```bash
#!/bin/bash

echo 0 > /sys/devices/system/cpu/cpufreq/boost
cpufreq-set -r -u 3.2GHz
cpufreq-set -r -d 1.8GHz
cpufreq-set -r -g powersave
```

---

## 2️⃣ 添加执行权限

```bash
sudo chmod +x /usr/local/bin/cpu-limit.sh
```

---

## 3️⃣ 创建 systemd 服务

```bash
sudo nano /etc/systemd/system/cpu-limit.service
```

写入：

```ini
[Unit]
Description=CPU Limit Service
After=multi-user.target

[Service]
Type=oneshot
ExecStartPre=/bin/sleep 5
ExecStart=/usr/local/bin/cpu-limit.sh

[Install]
WantedBy=multi-user.target
```

---

## 4️⃣ 启用开机自启动

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable cpu-limit.service
```

---

## 5️⃣ 立即测试（无需重启）

```bash
sudo systemctl start cpu-limit.service
```

---

## 6️⃣ 验证是否生效

```bash
cat /sys/devices/system/cpu/cpufreq/boost
```

应输出：

```
0
```

---

## ❌ 关闭自启动（恢复默认）

```bash
sudo systemctl disable cpu-limit.service
```

---

# 🧩 总结

👉 笔记本高温的本质不是性能不够，而是 **Boost 过激**

核心策略：

> **关 Boost + 限频 = 稳定运行**

---

# 📌 适用场景

* ROS / ROS2
* Gazebo 仿真
* 多线程程序开发
* 长时间运行任务

---

# 🏁 一句话总结

👉 **不要硬压散热，要主动控功耗**

