# Sandbox

## IMU

Read the data from the arduino and publish to `imu/data_raw`:
```
ros2 run ros2_py_package_sandbox imu
```

Read data from `imu/data_raw` and use madgwick filter to compute 
quaternions and publish to `imu/data`.
```
ros2 run imu_filter_madgwick imu_filter_madgwick_node --ros-args \
    -p use_mag:=false \
    -p publish_tf:=true \
    -p fixed_frame:=map \
    -r /imu/data_raw:=/imu/data_raw \
    -r /imu/data:=/imu/data
```

Echo the imu data:
```
ros2 topic echo imu/data
```

