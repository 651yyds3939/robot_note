# 机器人全链路系统 (Full-Stack Robotics System)
> **使用说明**：在VS Code中打开此Markdown文件，按 `Ctrl+Shift+O`（Windows/Linux）或 `Cmd+Shift+O`（Mac）即可调出大纲面板，或点击左侧活动栏的「大纲」图标查看完整树状结构。

## 一、感知层（传感器系统 - Perception Layer）
### 1.1 环境感知 (Exteroception)
#### 1.1.1 视觉类 (Vision)
- 单目相机 (Monocular Camera)
- 双目相机 (Stereo Camera)
- 深度相机 (RGB-D Camera，如 Kinect、Realsense)
- 激光雷达 (LiDAR - 2D/3D)
- 红外相机 (IR Camera)
#### 1.1.2 距离与测距 (Proximity & Ranging)
- 超声波传感器 (Ultrasonic)
- 飞行时间传感器 (ToF - Time of Flight)
- 红外测距 (IR Ranging)
#### 1.1.3 环境状态 (Environmental)
- 温湿度传感器
- 气压/高度计 (Barometer)
- 气体传感器

### 1.2 本体感知 (Proprioception)
#### 1.2.1 运动学状态 (Kinematics)
- 编码器 (Encoder：增量式 Incremental、绝对式 Absolute)
- 惯性测量单元 (IMU)
- 陀螺仪 (Gyroscope)
- 加速度计 (Accelerometer)
#### 1.2.2 动力学状态 (Dynamics)
- 六维力矩传感器 (6-Axis F/T Sensor)
- 一维张力/拉压传感器
- 触觉传感器 (Tactile Sensor)
#### 1.2.3 全局定位 (Localization)
- RTK-GPS / GNSS
- UWB 室内定位系统
- 磁力计/电子罗盘 (Magnetometer)

### 1.3 特殊与交互传感器
#### 1.3.1 语音与声学
- 麦克风阵列 (Mic Array)
#### 1.3.2 离散接触类
- 防撞边 / 触边开关 (Bumper)
- 机械限位开关 (Limit Switch)

## 二、决策层（上位机系统 - Decision/High-level System）
### 2.1 计算硬件平台 (Computing Hardware)
#### 2.1.1 单板计算机 (SBC)
- 树莓派 (Raspberry Pi)
- Nvidia Jetson (Nano/Xavier/Orin)
- RK3588 (瑞芯微)
#### 2.1.2 工业与通用计算机
- x86 架构工控机 (IPC)
- 标准工作站 (Ubuntu/Windows)
#### 2.1.3 硬件加速单元
- FPGA 开发板
- AI NPU/TPU 算力棒

### 2.2 操作系统与运行环境 (OS & Middleware)
#### 2.2.1 通用操作系统 (GPOS)
- Ubuntu / Debian (Linux 核心)
- Yocto (定制化嵌入式 Linux)
#### 2.2.2 实时操作系统 (RTOS)
- RT-Preempt (Linux 实时补丁)
- FreeRTOS (常用于高算力下位机)
- VxWorks
#### 2.2.3 机器人中间件 (Middleware)
- ROS 2 (Humble / Iron)
- ROS 1 (Noetic)

### 2.3 核心算法功能 (Core Algorithms)
#### 2.3.1 导航与建图 (Navigation & Mapping)
- SLAM (同步定位与建图: 激光2D/3D, V-SLAM)
- 状态估计 (State Estimation / 滤波融合)
#### 2.3.2 感知与AI (Perception)
- 目标检测与跟踪 (Object Detection & Tracking)
- 语义分割 (Semantic Segmentation)
#### 2.3.3 规划与控制 (Planning)
- 全局路径规划 (Global Routing)
- 局部避障轨迹规划 (Local Trajectory Planning)
- 行为树决策 (Behavior Trees)

## 三、控制层（下位机系统 - Control/Low-level System）
### 3.1 控制硬件平台 (Control Boards)
#### 3.1.1 微控制器 (MCU)
- ARM Cortex-M 系列 (STM32 等)
- ESP32 (带无线功能)
- Arduino (AVR)
#### 3.1.2 专业运动控制器 (Motion Controllers)
- 工业 PLC
- 专用多轴运动控制卡
#### 3.1.3 定制化底板 (Carrier Boards)
- 传感器接口板
- 电源分配与控制一体板

### 3.2 核心逻辑功能
#### 3.2.1 实时闭环控制 (Real-time Closed-loop)
- PID 控制律
- 运动学逆解算 (Inverse Kinematics - 基础版)
- 里程计推算 (Odometry Calculation)
#### 3.2.2 底层硬件接口
- PWM 信号生成
- ADC 模拟量采集
- 硬件中断处理 (Interrupts)

## 四、执行层（执行器系统 - Actuator System）
### 4.1 动力与驱动核心 (Power & Drive)
- **4.1.1 驱动控制算法**
    - 矢量控制 (FOC - Field Oriented Control) —— *心脏算法*
    - 方波控制 (Trapezoidal / 六步换相)
    - 步进脉冲控制
- **4.1.2 功率变换电路 (Power Electronics)**
    - MOSFET/IGBT 逆变桥 (Inverter Bridge)
    - 预驱动电路 (Gate Driver)

### 4.2 运动执行器 (Motion Actuators)
#### 4.2.1 旋转类 (Rotary)
- 直流无刷电机 (BLDC) / 永磁同步电机 (PMSM)
- 直流有刷电机 (Brushed DC)
- 步进电机 (Stepper Motor)
- 伺服电机系统 (Servo System - 驱动电机编码器一体化)
#### 4.2.2 直线与流体类 (Linear & Fluid)
- 直线电机 (Linear Motor)
- 电动推杆 (Linear Actuator)
- 气缸 (Pneumatic Cylinder) 与 气动肌肉 (PAM)
- 液压缸 (Hydraulic Actuator)

### 4.3 传动与关节模组 (Transmission & Joints)
#### 4.3.1 精密减速器 (Precision Reducers)
- 谐波减速器 (Harmonic Drive) —— *机械臂高精传动*
- RV 减速器 (Rotary Vector) —— *高负载传动*
- 行星减速器 (Planetary Gearbox)
#### 4.3.2 关节制动 (Braking)
- 电磁抱闸 (Electromagnetic Brake)

### 4.4 操作与末端执行器 (Manipulators)
- 机械平行夹爪 (Parallel Gripper)
- 柔性抓取器 (Soft Gripper)
- 真空吸盘 (Vacuum Cup)

### 4.5 辅助执行器 (Auxiliary)
- 声光指示 (LED / 蜂鸣器 Buzzer)
- 开关执行 (继电器 Relay / 电磁阀 Solenoid Valve)

## 五、机械结构层 (Mechanical Structure Layer)
### 5.1 承载主体 (Chassis & Frame)
#### 5.1.1 移动底盘 (Mobile Chassis)
- 轮式 (差速 Differential、阿克曼 Ackermann、全向 Omni/Mecanum)
- 履带式 (Tracked)
- 腿式 (单足、双足 Bipedal、四足 Quadruped)
#### 5.1.2 骨架与外壳 (Frame & Shell)
- 铝合金型材/碳纤维框架
- 3D 打印/注塑结构件

### 5.2 宏观传动机构 (Macro Transmission)
- 同步带传动 (Timing Belt)
- 齿轮齿条 (Gear & Rack)
- 滚珠丝杠 (Ball Screw)
- 连杆机构 (Linkage Mechanism)

### 5.3 结构辅助件 (Hardware Fasteners)
- 轴承 (Bearings)
- 联轴器 (Couplings)
- 减震器 (Shock Absorbers)

## 六、通信系统 (Communication System)
### 6.1 内部总线与网络 (Internal Bus)
#### 6.1.1 高速实时总线
- EtherCAT (工业级高速互联)
- CAN / CAN FD 总线 (高可靠性车规级)
#### 6.1.2 板级通信 (Board-Level)
- UART (串口)
- SPI / I2C
#### 6.1.3 数据中间层通信
- DDS (Data Distribution Service - ROS2核心通信机制)
- TCP/UDP 以太网

### 6.2 外部遥测与交互 (Telemetry & External)
#### 6.2.1 近场通信 (Near-Field)
- Wi-Fi (局域网调试)
- Bluetooth (蓝牙)
#### 6.2.2 远距离与广域网
- 4G/5G 蜂窝网络
- LoRa/ZigBee (低功耗物联网)

## 七、电源系统 (Power System)
### 7.1 能源储备 (Energy Storage)
- 动力锂电池组 (Li-ion/LiPo Pack)
- 超级电容 (Supercapacitor - 瞬时大电流)

### 7.2 电池管理系统 (BMS - Battery Management System)
- 电芯均衡控制 (Cell Balancing)
- 充放电保护 (过压/欠压/过流保护)
- 电量计 (SOC 状态估算)

### 7.3 电源转换与分配 (Power Distribution)
- DC-DC 降压模块 (Buck Converter)
- DC-DC 升压模块 (Boost Converter)
- PDU (电源分配单元 Power Distribution Unit)
- 急停开关 (E-Stop) 与 熔断器 (Fuse)