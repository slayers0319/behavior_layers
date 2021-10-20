#!/usr/bin/env python
import math
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Point

def abs_vector(x, y):
    """
    return absolute value of velocity
    """
    return math.sqrt(math.pow(x,2) + math.pow(y,2))

def scale(c, point):
    return Point(c*point.x, c*point.y,0)

def normalize_vector(point):
    return Point(point.x/abs_vector(point.x, point.y),point.y/abs_vector(point.x, point.y),0)

def rotate_vector(point, angle):
    P=Point()
    P.x=point.x*math.cos(angle*math.pi/180)-point.y*math.sin(angle*math.pi/180)
    P.y=point.x*math.sin(angle*math.pi/180)+point.y*math.cos(angle*math.pi/180)
    return P

def predict(data):
    if data.data=="clear":
        rospy.loginfo(data.data)
        pub_point.publish("clear")
        return
    elif len(data.data)==0:
        return

    #data.data="R,x,y,L,x,y"
    result = ""
    splited = data.data.split(',')
    for i in range(len(splited)/3):
        if splited[i*3]=="personR":
            if float(splited[i*3+1])>0:
                continue
            else:
                vector=Point(0,0.3,0)
                center = Point(float(splited[i*3+1])+0.3,float(splited[i*3+2]),0)
                
                if len(result)==0:
                    result=result+"Point,"+str(center.x+vector.x)+","+str(center.y+vector.y)
                else:
                    result=result+",new,"+str(center.x+vector.x)+","+str(center.y+vector.y)

                for j in range(4):
                    vector = rotate_vector(vector, 45)
                    result=result+",Point,"+str(center.x+vector.x)+","+str(center.y+vector.y)

                result=result+",Point,"+str(-(center.x-0.3))+","+str(center.y-0.3) 
                result=result+",Point,"+str(-(center.x-0.3))+","+str(center.y+0.3)               
        elif splited[i*3]=="personL":
            if float(splited[i*3+1])<0:
                continue
            else:
                vector=Point(0,-0.3,0)
                center = Point(float(splited[i*3+1])-0.3,float(splited[i*3+2]),0)
                
                if len(result)==0:
                    result=result+"Point,"+str(center.x+vector.x)+","+str(center.y+vector.y)
                else:
                    result=result+",new,"+str(center.x+vector.x)+","+str(center.y+vector.y)

                for j in range(4):
                    vector = rotate_vector(vector, 45)
                    result=result+",Point,"+str(center.x+vector.x)+","+str(center.y+vector.y)

                result=result+",Point,"+str(-(center.x+0.3))+","+str(center.y+0.3)
                result=result+",Point,"+str(-(center.x+0.3))+","+str(center.y-0.3)
        else:
            continue
    
    if len(result)==0:
        return
    rospy.loginfo(result)
    pub_point.publish(result)


rospy.init_node('behavior_predict',anonymous=True)
rospy.Subscriber('/person', String, predict)
pub_point = rospy.Publisher('/behavior', String, queue_size=10)

r = rospy.Rate(5)

while not rospy.is_shutdown():
    r.sleep()