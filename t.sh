source ~/catkin_ws/devel/setup.bash
gnome-terminal -t "bringup" -x bash -c "roscore & roslaunch rbx1_bringup fake_turtlebot.launch;exec bash"
sleep 3

gnome-terminal -t "loadmap" -x bash -c "roslaunch rbx1_nav fake_amcl.launch map:=test_map.yaml;exec bash"
sleep 3
gnome-terminal -t "rviz" -x bash -c "rosrun rviz rviz -d `rospack find rbx1_nav`/amcl.rviz;exec bash"
#gnome-terminal -t "go" -x bash -c "rosrun rbx1_nav timed_out_and_back.py;exec bash"

