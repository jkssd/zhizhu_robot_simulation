cmake_minimum_required(VERSION 3.8)
project(zhizhu_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

# Install assets so `package://zhizhu_description/meshes/zhizhu.stl` resolves
# to <install_prefix>/share/zhizhu_description/meshes/zhizhu.stl at runtime.
install(
  DIRECTORY meshes urdf launch rviz worlds config
  DESTINATION share/${PROJECT_NAME}
)

# Gait node (executable Python script)
install(
  PROGRAMS scripts/gait_node.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
