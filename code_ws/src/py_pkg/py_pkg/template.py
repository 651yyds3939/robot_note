# ROS2 节点程序的本质是：先初始化底层通信环境，创建一个附带有发布者和订阅者的节点类，
# 然后进入一个事件循环，当订阅的话题有消息到达时，系统自动调用你预先注册的回调函数，在回调里处理消息（可以重新发布），最后在退出时清理所有资源。
#这个节点模板封装程度很高，调用已经有的库，一环套一环，让代码很简洁，不需要自己写具体的方法，然后很多个节点一起运行，互相发布，订阅，就构成了ros2的通信机制
'''
启动脚本
  │
  ├─ rclpy.init() ──► 初始化通信、全局上下文
  │
  ├─ my_node = MyNode()
  │     │
  │     ├─ super().__init__() ──► 在 DDS 中注册节点
  │     │
  │     ├─ create_publisher() ──► 创建发布者，注册到 DDS
  │     │
  │     └─ create_subscription() ──► 创建订阅者，注册回调
  │
  ├─ rclpy.spin(my_node) ──► 进入事件循环
  │     │
  │     └─ while rclpy.ok():
  │            ├─ 等待事件（消息、定时器...）
  │            ├─ 收到 input_topic 消息
  │            ├─ 调用 self.callback(msg)
  │            │      ├─ 打印日志
  │            │      └─ self.publisher.publish(msg) ──► 消息发出到 output_topic
  │            └─ 继续等待
  │
  ├─ 用户 Ctrl+C ──► rclpy.ok() 变为 False，退出 spin
  │
  ├─ my_node.destroy_node() ──► 清理节点及子对象
  │
  └─ rclpy.shutdown() ──► 全局清理，程序结束
'''

#先把基础模板刻在脑子里，然后遇到新需求时，就知道“在这个位置加几行代码”即可
import rclpy # 导入 ROS2 Python 客户端库的核心模块
from rclpy.node import Node # 从 rclpy.node 模块中导入 Node 基类，所有自定义节点都需要继承它
from std_msgs.msg import String # 导入标准消息类型 String，用于在话题上收发字符串数据

class MyNode(Node): # 定义自己的节点类，继承自 rclpy.node.Node
    def __init__(self):
        # 调用父类 Node 的构造函数，并给当前节点起名为 'my_node_name'
        # 该名称会在 ROS2 网络中唯一标识这个节点
        #直接继承到了父类里面的所有属性和方法
        super().__init__('my_node_name')

        # 通过节点的工厂方法创建一个发布者（Publisher）
        # - 方法：create_publisher 是 Node 基类（即包名.模块名.类名：rclpy.node.Node）提供的工厂方法，用于简化发布者的创建过程
        # - 原理：create_publisher 方法内部封装了复杂的初始化过程（如分配句柄、设置 QoS 等），
        #         最终方法会自动导入并使用 Publisher(self, ...)类来构造一个新对象，并将其赋值给实例属性 self.publisher。
        # - 方法内部参数：
        #   * 消息类型：String
        #   * 话题名称：'output_topic'
        #   * 队列大小：10（发布过快时最多缓存10条待发送消息）

        # - 返回值：rclpy.publisher.Publisher 类型的发布者对象，该对象已注册到 ROS2 底层通信系统
        # - 后续使用：可通过 self.publisher.publish(msg) 发布消息
        self.publisher = self.create_publisher(String, 'output_topic', 10) 

        # 通过节点的工厂方法创建一个订阅者（Subscription）
        # - 方法：create_subscription 是 Node 基类（即 rclpy.node.Node）提供的工厂方法，用于简化订阅者的创建过程
        # - 原理：create_subscription 方法内部封装了底层订阅注册、回调绑定等复杂过程，
        #         最终方法会自动导入并使用 Subscription(self, ...) 类来构造一个新对象，并将其赋值给实例属性 self.subscription。
        # - 方法内部参数：
        #   * 消息类型：String
        #   * 话题名称：'input_topic'
        #   * 回调函数：self.callback（收到消息时自动调用，传入 msg 参数）
        #   * 队列大小：10（缓存最多 10 条尚未处理的传入消息）
        # - 返回值：rclpy.subscription.Subscription 类型的订阅者对象，该对象已注册到 ROS2 底层通信系统
        # - 后续使用：每当 'input_topic' 上有消息到达，ROS2 会自动执行 self.callback(msg)
        # 只在订阅者里面传入回调函数因为我们想实现的功能是只有当收到了其他节点的信息才会调用这个回调函数里面的发布者方法，转发收到的信息
        self.subscription = self.create_subscription(String, 'input_topic', self.callback, 10)

    # 回调函数，每当 'input_topic' 上收到消息时自动执行
    def callback(self, msg):

        # 1. msg：是接收到的话题消息对象，其类型与订阅时声明的消息类型一致。 在本模板中，订阅的是 String 类型，所以 msg 就是一个 String 类的实例（对象）。
        # 2. msg.data：访问 msg 实例中 data 字段所存储的值，在 String 类型中它就是一个字符串。 
        # 3. self.get_logger()：继承自父类 Node 的方法，返回一个 Logger 对象（日志记录器）。
        # 4. Logger 对象：属于 rclpy 库中由 pybind11 封装的、对应底层 rclcpp::Logger 的 Python 类（在 Python 中常表现为 Pybind11Logger 类型）。
        # 5. .info(...)：Logger 对象的方法，用于输出 INFO 级别的日志信息。
        # 6. 整体作用：通过节点的日志记录器输出一条信息，内容为 f"Received: {msg.data}"。
        self.get_logger().info(f"Received: {msg.data}")

        # self.publisher：节点在 __init__ 中创建的发布者类的对象（Publisher 实例）。
        # .publish(msg)：发布者对象的方法。
        # 整体作用：将接收到的消息对象 msg 原封不动地发布出去。所有订阅了 output_topic 的其他节点都会收到这条消息。
        # 逻辑详解：
        # 1. 当我们通过订阅者收到其他节点的信息时，我们是订阅者角色。
        # 2. 在回调函数中调用 self.publisher.publish(msg) 后，我们就变成了发布者角色，把收到的信息转发出去。
        # 3. 其他节点要想收到我们转发的信息，它们的订阅者必须订阅相同的话题名称，即 'output_topic'。
        # 4. 消息具体内容是 msg，'output_topic' 只是这个消息的一个标题（话题名），用于标识消息的流向。
        # 5. 至于消息内容（msg），其他节点的回调函数会通过 msg.data 获得。
        # 6. 当两个节点的发布话题与订阅话题互相匹配时，就会形成无限循环套娃（A 发布到 B，B 发布到 A），见.md里面的图片。所以在实际应用中要注意避免这种情况，除非你确实需要它。
        self.publisher.publish(msg)

# Python 的标准入口保护：只有当该脚本被直接运行时才执行以下代码
# （如果作为模块被导入，则不会执行）
if __name__ == "__main__":
    # 初始化 ROS2 客户端库，必须在使用任何 ROS2 功能前调用
    rclpy.init()

    # 创建 MyNode 类的实例，此时节点已经注册到 ROS2 系统中
    my_node = MyNode()

    # rclpy.spin(my_node) 的作用与内部机制：
    # 1. 方法内部封装了一个复杂的无限循环（简化流程如下）：
    #    while rclpy.ok():                     # 检查全局标志是否正常
    #        # 等待任何订阅者、定时器、服务等有事件到达（可设置超时）
    #        events = wait_for_events(node, timeout)
    #        for event in events:
    #            if event.type == 'subscription':
    #                msg = take_message(event.subscription)
    #                event.subscription.callback(msg)   # 调用你注册的回调
    #            elif event.type == 'timer':
    #                event.timer.callback()
    #            # ... 其他事件类型
    # 
    # 2. 在创建节点后调用，通常放在主程序的最后（清理代码之前）
    # 3. 这个方法里面封装了一个比较复杂的无限循环，我们只用调用这个方法，可以不用深究。
    # 4. 作用：阻塞当前线程，反复检查并处理节点的所有传入消息、定时器、服务请求等事件，直到节点被关闭。
    # 5. “阻塞”的含义：如果这个节点暂时没有接收或发布任务，就一直挂着，保持运行，但不用太耗资源（线程进入睡眠，由操作系统唤醒），直到又有活要干了或者用户退出。
    # 6. 总结：进入 spinning 无限循环，节点开始持续等待并处理消息、定时器等事件。该函数会阻塞，直到收到中断信号（如 Ctrl+C）或节点被关闭。
    rclpy.spin(my_node)

    # destroy_node() 是 rclpy.node.Node 父类的一个实例方法
    # my_node.destroy_node() 本质上就是把 my_node 实例作为 self 参数传入 Node 类的 destroy_node 方法
    # 退出 spinning 后，显式销毁节点，释放其占用的资源（发布者、订阅者等）
    my_node.destroy_node()

    # 关闭 ROS2 客户端库，进行全局清理（终止后台线程、关闭通信等）
    rclpy.shutdown()

    #可以用下面的整体模板来替换上面的最后两行，增加了异常处理和自定义清理逻辑：
    """
    try:
        rclpy.spin(my_node)
    except KeyboardInterrupt:
        pass
    finally:
        my_node.on_shutdown()  # do any custom cleanup
        my_node.destroy_node()
        rclpy.shutdown()
    """

