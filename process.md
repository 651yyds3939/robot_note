### ROS2 开发流程笔记 (C++ & Python)

#### 1. 创建工作空间 (Workspace)
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

#### 2. 创建功能包 (Package)
根据使用的语言，选择不同的编译类型：

* **2.1 C++ (ament_cmake):**
    ```bash
    cd ~/ros2_ws/src
    ros2 pkg create --build-type ament_cmake cpp_node_pkg --dependencies rclcpp
    ```
* **2.2 Python (ament_python):**
    ```bash
    cd ~/ros2_ws/src
    ros2 pkg create --build-type ament_python py_node_pkg --dependencies rclpy
    ```

---

#### 3. 创建节点与编写代码-以最基础的空节点为例子，具体节点模板见`code_ws`

* **3.1 C++ 节点:** 在 `cpp_node_pkg/src` 下创建 `my_node.cpp`。
    ```cpp
    #include "rclcpp/rclcpp.hpp"
    int main(int argc, char **argv) {
        rclcpp::init(argc, argv);
        auto node = rclcpp::Node::make_shared("cpp_node");
        RCLCPP_INFO(node->get_logger(), "Hello ROS2 from C++!");
        rclcpp::shutdown();
        return 0;
    }
    ```

* **3.2 Python 节点:** 在 `py_node_pkg/py_node_pkg` (第二个同名文件夹) 下创建 `my_py_node.py`。
    ```python
    import rclpy
    from rclpy.node import Node

    def main(args=None):
        rclpy.init(args=args)
        node = Node("py_node")
        node.get_logger().info("Hello ROS2 from Python!")
        rclpy.shutdown()

    if __name__ == '__main__':
        main()
    ```

---

#### 4. 修改配置文件

* **4.1 C++ (CMakeLists.txt):**
    ```cmake
    add_executable(cpp_executable src/my_node.cpp)
    ament_target_dependencies(cpp_executable rclcpp)
    install(TARGETS cpp_executable DESTINATION lib/${PROJECT_NAME})
    ```

* **4.2 Python (setup.py):**
    找到 `entry_points` 字典，添加控制台脚本：
    ```python
    entry_points={
        'console_scripts': [
            'py_executable = py_node_pkg.my_py_node:main',
        ],
    },
    ```

---

#### 5. 编译 (Build)
```bash
cd ~/ros2_ws
colcon build
# 推荐 Python 开发时使用 --symlink-install，这样修改 py 文件后无需重复编译
# colcon build --symlink-install
```

#### 6. 环境配置 (Source)
```bash
source install/setup.bash
```

#### 7. 运行节点 (Run)
* **7.1运行 C++ 节点:**
    ```bash
    ros2 run cpp_node_pkg cpp_executable
    ```
* **7.2运行 Python 节点:**
    ```bash
    ros2 run py_node_pkg py_executable
    ```

#### 8. 查看节点状态 (Node List)
```bash
ros2 node list
```

---

**提示：**
- C++ 侧重于性能，通常放在 `src` 文件夹下。
- Python 侧重于快速开发，代码文件通常放在功能包内的同名子目录下，且必须在 `setup.py` 中配置 `entry_points` 才能通过 `ros2 run` 启动。