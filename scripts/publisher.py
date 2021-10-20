#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import random
from geometry_msgs.msg import Point

data_x = 0.0
data_y = 0.0
data_yaw = 0.0

def talker():
    
    global name, data_x, data_y, data_yaw, data
    pub = rospy.Publisher('person', String, queue_size=1)
    rospy.init_node('pedestrain_behavior', anonymous=True)
    hz=20
    rate = rospy.Rate(hz) # 1hz
    while not rospy.is_shutdown():
        data = String()
        n=input()
        if n==-1:
            data.data = "clear"
            rospy.loginfo(data)
            pub.publish(data)
            break
        elif n==0:
            a=0
            for i in range(5*hz):
                rate.sleep()
                if i%2==0:
                    a=not a
                if a==0:
                    data.data="personR,-1,1"
                else:
                    data.data="personR,-0.5,0.5,personL,1.5,1.5,personL,-1.5,1.5,personR,1.5,1.5"
                rospy.loginfo(data)
                pub.publish(data)
        elif n==1:
            data.data="personR,-1,1"
            rospy.loginfo(data)
            pub.publish(data)
        elif n==2:
            for i in range(3):
                rate.sleep()
                name = "L"
                data_x = random.uniform(0.25,0.3)
                data_y = random.uniform(0.5,1.0)
                data.data = name+","+str(data_x)+","+str(data_y)
                rospy.loginfo(data)
                pub.publish(data)
        elif n==3:
            name = "R"
            data_x = random.uniform(0.1,0.5)
            data_y = random.uniform(0.5,1.0)
            data.data = name+","+str(data_x)+","+str(data_y)
            rospy.loginfo(data)
            pub.publish(data)
        elif n==4:
            name = "L"
            data_x = random.uniform(-0.5,-0.1)
            data_y = random.uniform(0.5,1.0)
            data.data = name+","+str(data_x)+","+str(data_y)
            rospy.loginfo(data)
            pub.publish(data)
            
        rospy.loginfo("-------------")
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
