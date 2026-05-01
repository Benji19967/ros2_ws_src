# ROS 2 Workspace

## Tutorial

https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html

Installing the examples:
```
git clone https://github.com/ros2/examples src/examples -b jazzy
```

Installing the dependencies (rosdep will look for all deps in the `package.xml` files):
```
rosdep install -i --from-path src --rosdistro jazzy -y
```

## Creating a package

```
ros2 pkg create --build-type ament_python --license Apache-2.0 --node-name my_node ros2_py_package_sandbox
```

## Building a package

```
colcon build --symlink-install --packages-select ros2_py_package_sandbox
```

## Using a package

In a NEW terminal:

```
source install/local_setup.bash
```

```
ros2 run ros2_py_package_sandbox my_node
```
