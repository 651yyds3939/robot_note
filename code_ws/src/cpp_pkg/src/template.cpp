// 引入 rclcpp 核心头文件，包含了 ROS 2 节点开发所需的所有基础类和函数
#include <rclcpp/rclcpp.hpp>

namespace my_pkg
{

/**
 * MyComponent 类继承自 rclcpp::Node
 * 这种继承方式是 ROS 2 推荐的写法，便于封装功能和重用代码
 */
class MyComponent : public rclcpp::Node
{
public:
  /**
   * 构造函数：必须包含 rclcpp::NodeOptions 
   * 这是为了让组件容器（Component Container）在加载时能传递参数（如参数重映射、自动声明等）
   */
  MyComponent(const rclcpp::NodeOptions& options)
  : rclcpp::Node("node_name", options) // 调用父类构造函数，初始化节点名称为 "node_name"
  {
    /**
     * 注意：在构造函数中，绝对不能调用 shared_from_this()。
     * 原因：ROS 2 的定时器或订阅通常需要一个指向自身的智能指针。
     * 但在构造函数执行时，对象尚未完全构造完成，智能指针系统还没准备好。
     * 如果非要用，通常建议在构造函数结束后，由外部调用初始化函数，或者使用 lambda 捕获 this。
     */
     
    // 在这里进行初始化操作，例如：
    // RCLCPP_INFO(this->get_logger(), "节点已启动！");
  }
};

}  // 命名空间 my_pkg

// 引入组件注册宏，这是将该类变为“可动态加载插件”的关键
#include "rclcpp_components/register_node_macro.hpp"

// 使用宏注册该组件。第一个参数是类的全名（带命名空间）
// 这样编译出的库文件就可以被 ROS 2 的组件管理器（Component Manager）识别并加载
RCLCPP_COMPONENTS_REGISTER_NODE(my_pkg::MyComponent)
