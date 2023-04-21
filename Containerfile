FROM ros:foxy
RUN apt-get update && apt-get install python3-serial screen -y

COPY ./ /ros2_ws/src/garmin_ros2

WORKDIR /ros2_ws/
RUN rosdep install -i --from-path src --rosdistro foxy -y
#RUN . /opt/ros/foxy/local_setup.sh
#RUN colcon build 
#RUN source install/setup.bash
