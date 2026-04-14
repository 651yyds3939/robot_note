# ==================== 基础参数示例 ====================
# 说明：参数是 ROS 2 节点中可配置的变量，可以在运行时动态修改（如果支持）。
# 以下代码展示了如何声明一个参数、获取它的值。

# 假设已经创建了 rclpy.node.Node 实例，名为 node
# node = rclpy.create_node('example_node')

# 声明一个参数：参数名为 "my_param_name"，默认值为 42
# 如果该参数未被外部设置过，节点将使用这个默认值。
node.declare_parameter("my_param_name", 42)

# 获取参数对象，再通过 .value 属性取得实际的值（此处为整数 42 或其他被设置的值）
param = node.get_parameter("my_param_name").value


# ==================== 动态参数（带回调验证）示例 ====================
# 说明：允许外部在运行时修改参数，但通过回调函数对修改请求进行合法性检查。
# 只有检查通过的参数值才会被真正更新。

# 从 ROS 2 接口模块导入参数设置结果的消息类型
from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.node import Node

# 自定义节点类，继承自 rclpy.node.Node
class MyNode(Node):

    def __init__(self):
        # 调用父类构造函数，指定节点名称为 'my_node_name'
        super().__init__('my_node_name')

        # 声明一个参数 "my_param_name"，默认值为 42
        self.declare_parameter("my_param_name", 42)

        # 注册参数设置回调函数。
        # 每当有外部请求（如通过 ros2 param set 命令）修改本节点的参数时，
        # 这个回调函数会被自动调用，用于验证参数是否合法。
        self.set_parameters_callback(self.callback)
    
    # 参数回调函数，接收一个参数列表（包含所有被请求修改的参数）
    # 返回值必须是 SetParametersResult 对象，指明是否接受修改及原因。
    def callback(self, parameters):
        # 默认认为修改成功，先创建成功的返回对象
        result = SetParametersResult(successful=True)

        # 遍历所有请求修改的参数
        for p in parameters:
            # 检查参数名是否为 "my_param_name"
            if p.name == "my_param_name":
                # 检查参数类型：必须是整数类型（p.Type.INTEGER）
                if p.type_ != p.Type.INTEGER:
                    # 类型不匹配：设置修改失败，并给出失败原因
                    result.successful = False
                    result.reason = 'my_param_name must be an Integer'
                    return result  # 立即返回，拒绝本次所有参数修改
                
                # 检查参数值：必须大于等于 20
                if p.value < 20:
                    result.successful = False
                    result.reason = "my_param_name must be >= 20"
                    return result

        # 所有参数都通过了检查，返回成功。
        # 节点内部会应用这些新值，后续通过 get_parameter() 获取到的将是更新后的值。
        return result


#和节点模板合二为一，实现一个既有参数又有发布订阅功能的节点示例
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MyConfigurableNode(Node):

    def __init__(self):
        super().__init__('my_node_name')

        # ---------- 1. 声明参数（来自参数模板）----------
        self.declare_parameter("publish_frequency", 1.0)   # Hz
        self.declare_parameter("output_topic", "output_topic")
        self.declare_parameter("input_topic", "input_topic")
        self.declare_parameter("enable_logging", True)

        # 获取参数值，用于后续逻辑
        pub_topic = self.get_parameter("output_topic").value
        sub_topic = self.get_parameter("input_topic").value

        # ---------- 2. 创建发布者、订阅者（来自节点模板）----------
        self.publisher = self.create_publisher(String, pub_topic, 10)
        self.subscription = self.create_subscription(
            String,
            sub_topic,
            self.callback,
            10)

        # 使用参数创建定时器，控制发布频率
        freq = self.get_parameter("publish_frequency").value
        self.timer = self.create_timer(1.0 / freq, self.timer_callback)

        # 可选：注册动态参数回调，使修改立即生效
        self.set_parameters_callback(self.param_callback)

    def callback(self, msg):
        # 使用参数控制是否打印日志
        if self.get_parameter("enable_logging").value:
            self.get_logger().info("Received: %s" % msg.data)
        # 这里可以做其他处理，比如根据参数决定是否转发
        self.publisher.publish(msg)

    def timer_callback(self):
        # 定时发布的逻辑（示例）
        msg = String()
        msg.data = "Hello from timer"
        self.publisher.publish(msg)

    def param_callback(self, params):
        # 当参数被动态修改时，可以动态调整定时器频率等
        for p in params:
            if p.name == "publish_frequency" and p.value > 0:
                # 重新创建定时器（实际更优雅的做法是取消旧定时器再创建新定时器）
                self.timer.cancel()
                self.timer = self.create_timer(1.0 / p.value, self.timer_callback)
        return rclpy.parameter.SetParametersResult(successful=True)


if __name__ == "__main__":
    rclpy.init()
    node = MyConfigurableNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()