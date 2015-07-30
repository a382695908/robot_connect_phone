#!/usr/bin/env python

import socket
import sys
import os
import subprocess
import time
import string
from thread import *

HOST='' 
PORT=21567

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
print 'Socket created'
#Bind socket to local host and port
try:
	s.bind((HOST,PORT))
except socket.error, msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' +msg[1]
	sys.exit()
print 'Socket bind complete'
#Start listening on socket
s.listen(10)
status=0
print 'Socket now listening'
#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client	
	conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
	global status	
	#infinite loop so that function do not terminate and thread do not edn
	while True:		
		#Receving from client
		data = conn.recv(1024)
		reply= 'OK...'+data
		if not data:
			break
		elif str(data) == 'start':
			if status==1:
				conn.sendall("I am ready to go to anywhere!")
			else:
				conn.sendall(reply)
				os.system("echo \"start!!!\"")
				status=1
				
				os.system("sh ./t.sh")
				#bringup=subprocess.Popen('''gnome-terminal -t "bringup" -x bash -c "roslaunch rbx1_bringup fake_turtlebot.launch;exec bash"''',shell=True)
				#bringup.wait()
				#time.sleep(3)
				#load=subprocess.Popen('''gnome-terminal -t "loadmap" -x bash -c "roslaunch rbx1_nav fake_amcl.launch map:=test_map.yaml;exec bash"''',shell=True)
				#load.wait()
				#time.sleep(3)
				#rviz=subprocess.Popen('''gnome-terminal -t "rviz" -x bash -c "rosrun rviz rviz -d `rospack find rbx1_nav`/amcl.rviz;exec bash"''',shell=True)
				#rviz.wait()
				conn.sendall('over')
		elif str(data)=='go_0':
			if status==0:
				conn.sendall("please start the robot first!")
			else:
				conn.sendall(reply)
				os.system("echo \"go to origin!!!\"")
				#conn.sendall('Yes, I am going to move as your order!')
				#os.system("sh /home/viki/shell_script/go.sh")
				os.system("""rostopic pub -1 /move_base_simple/goal geometry_msgs/PoseStamped '{ header: { frame_id: "map" }, pose: { position: { x: 0, y: 0, z: 0 }, orientation: { x: 0, y: 0, z: 0, w: 1 } } }'""")
			
				conn.sendall('over')
				#conn.sendall(reply)
		elif str(data)=='go_1':
			if status==0:
				conn.sendall("please start the robot first!")
			else:
				conn.sendall(reply)
				os.system("echo \"go to pose1!!!\"")
				#conn.sendall('Yes, I am going to move as your order!')
				#os.system("sh /home/viki/shell_script/go.sh")
				os.system("""rostopic pub -1 /move_base_simple/goal geometry_msgs/PoseStamped '{ header: { frame_id: "map" }, pose: { position: { x: 2.0, y: 2.0, z: 0 }, orientation: { x: 0, y: 0, z: 0, w: 1 } } }'""")			
				conn.sendall('over')
				#conn.sendall(reply)
		elif str(data)=='go_2':
			if status==0:
				conn.sendall("please start the robot first!")
			else:
				conn.sendall(reply)
				os.system("echo \"go to pose2!!!\"")
				#conn.sendall('Yes, I am going to move as your order!')
				#os.system("sh /home/viki/shell_script/go.sh")
				os.system("""rostopic pub -1 /move_base_simple/goal geometry_msgs/PoseStamped '{ header: { frame_id: "map" }, pose: { position: { x: 0.0, y: 4.0, z: 0 }, orientation: { x: 0, y: 0, z: 0.5, w: 0.5 } } }'""")			
				conn.sendall('over')
		elif str(data)=='go_3':
			if status==0:
				conn.sendall("please start the robot first!")
			else:
				conn.sendall(reply)
				os.system("echo \"go to pose3!!!\"")
				#conn.sendall('Yes, I am going to move as your order!')
				#os.system("sh /home/viki/shell_script/go.sh")
				os.system("""rostopic pub -1 /move_base_simple/goal geometry_msgs/PoseStamped '{ header: { frame_id: "map" }, pose: { position: { x: -4.0, y: 3.0, z: 0 }, orientation: { x: 0, y: 0, z: -0.5, w: 0.5 } } }'""")			
				conn.sendall('over')
		elif str(data)=='stop':
			if status==0:
				conn.sendall("please start the robot first!")
			else:
				conn.sendall(reply)
				#tcpCliSock.send('%s' % data)
				os.system("echo \"stop !!!\"")
				conn.sendall('ok, I am goning to stop myself!')
				os.system("rostopic pub -1 /cmd_vel geometry_msgs/Twist '{}'")
				conn.sendall('over')
		elif str(data)=='pose':
			if status==0:
				conn.sendall("please start the robot first!")
			else:
				#conn.sendall(reply)
				os.system("echo \"report robot's pose!!!\"")
				#os.system("rostopic echo -n 1 /odom/pose | out.log")
				child1=subprocess.Popen("rostopic echo -n 1 /odom/pose",shell=True,stdout=subprocess.PIPE)
				out1=child1.communicate()
				strout1=str(out1)
				index1=strout1.find('covar')
				posesend=strout1[2:index1]
				#print type(posesend)
				posesend1=posesend.replace('\\n','')
				#print posesend1
				#split_pose=posesend.split('\\n')
				#print split_pose
				#posesend1=''.join(split_pose)
				print posesend1
				child2=subprocess.Popen("rostopic echo -n 1 /move_base/status/status_list",shell=True,stdout=subprocess.PIPE)
				out2=child2.communicate()
				strout=str(out2)
				index=strout.find('status')
				outsend=strout[index:index+9]
				print outsend	
				conn.sendall(posesend1+'    '+outsend)	
				conn.sendall('over')
		elif str(data)=='sleep':
			if status==0:
				conn.sendall("I am sleeping! call me, please say start!")
			else:			
				#conn.sendall('sorry, wrong order. Please try "start, go , stop"')
				conn.sendall(reply)
				os.system("killall rviz")
				os.system("killall roslaunch")
				time.sleep(2)
				os.system("killall bash")
				status=0
				conn.sendall('over')
		#conn.sendall(reply)	
	#came out of loop
	sys.exit(conn.close())
#now keep talking with the client 
while 1:
	#waiting to accept a connection  - blocking call
	conn,addr= s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	#start new thread takes 1st argument as function name to be run, second is the tuple of arguments to the funciton 
	start_new_thread(clientthread ,(conn,))
sys.exit(s.close())

