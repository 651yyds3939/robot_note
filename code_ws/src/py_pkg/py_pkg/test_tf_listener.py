# =================================================================
# RCLPY: TF2 学习模板
# 描述: 本模板演示了 TF2 监听器的基本用法及 transforms3d 库的配合。
# 依赖: ros-humble-tf2-ros, ros-humble-tf2-geometry-msgs, transforms3d
# =================================================================

import rclpy
from rclpy.node import Node
import numpy as np

# 1. 导入 TF2 相关库
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from geometry_msgs.msg import PointStamped
import tf2_geometry_msgs  # 必须导入，它为 PointStamped 注入了 .transform 方法

# 2. 导入变换数学库 (需执行: pip install transforms3d)
from transforms3d.quaternion import quat2mat

class TF2ListenerNode(Node):
    def __init__(self):
        super().__init__("tf2_listener_node")

        # 【核心】初始化 Buffer 和 Listener
        # Buffer 存储坐标变换树，Listener 负责从 /tf 话题接收并更新数据
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)

    def demonstrate_transform(self):
        # --- 2. 应用变换示例 ---
        p1 = PointStamped()
        p1.header.frame_id = "source_frame"
        p1.point.x = 1.0
        p1.point.y = 2.0
        p1.point.z = 0.0

        try:
            # 【关键修改】必须通过 self.buffer 调用，且需确保 target_frame 存在
            # 这里的 transform 方法是由 tf2_geometry_msgs 提供的
            p2 = self.buffer.transform(p1, "target_frame")
            self.get_logger().info(f"变换后的坐标: {p2.point}")
        except Exception as e:
            self.get_logger().warn(f"变换失败: {str(e)}")

    def demonstrate_rotation(self):
        # --- 3. 变换数学计算 (使用 transforms3d) ---
        # 假设我们有一个四元数 [w, x, y, z]
        q = [1.0, 0.0, 0.0, 0.0] 
        
        # 将四元数转换为旋转矩阵
        R = quat2mat(q)
        
        # 待旋转的向量 [x, y, z]
        v_raw = [1.0, 0.0, 0.0]
        V = np.array(v_raw).reshape((3, 1))
        
        # 矩阵点乘实现旋转
        M = np.dot(R, V)
        
        # 将结果写回 ROS 消息
        p = PointStamped()
        p.point.x = float(M[0, 0])
        p.point.y = float(M[1, 0])
        p.point.z = float(M[2, 0])

def main():
    rclpy.init()
    node = TF2ListenerNode()
    # 这里通常会配合定时器或回调函数使用
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    # main() # 暂时注释掉，防止直接运行报错
    pass