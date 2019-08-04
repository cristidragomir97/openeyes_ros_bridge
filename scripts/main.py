import threading, time, serial, rospy
from std_msgs.msg import String, Int8
from colorama import Fore
from hw_bridge.srv import *

Q_SIZE = 10
PORT = '/dev/ttyUSB0'
BAUD = 112500

global serial_port
  
def read_from_port(ser, gsr_pub, button_pub, hr_pub, ack_queue):
    while True:
        text = ser.readline().decode()
     
        if text:
            if text[0] == 'k':
                print(Fore.RED + 'Got ACK : {}'.format(text) + Fore.RESET )

            elif text[0] == 'g':
                val = text[1:len(text)]
                gsr_pub.publish(val)

            elif text[0] == 'b':
                val = text[1:len(text)]
                button_pub.publish(val)

            elif text[0] == 'h':
                val = text[1:len(text)]
                hr_pub.publish(val)
                

        time.sleep(0.1)

def handle_req(req):
    message = 'h{}{}'.format(req.device, req.n)
  
    for effect in req.effects:
       message = '{},{}'.format(message, effect)

    print(message)
    serial_port.write(str.encode(message + '\n'))
    return True

def pub():

    gsr_pub = rospy.Publisher('gsr', String, queue_size= Q_SIZE)
    rospy.loginfo('* created gsr publisher')

    hr_pub = rospy.Publisher('hr', String, queue_size= Q_SIZE)
    rospy.loginfo('* created hr publisher')

    button_pub = rospy.Publisher('btn', String, queue_size= Q_SIZE)
    rospy.loginfo('* created btn publisher')
    
    return gsr_pub, hr_pub, button_pub

def server():
    srv = rospy.Service('HapticService', HapticService,  handle_req)
    rospy.spin()
    

if __name__ == '__main__':
    rospy.init_node('bridge')
    ack_queue = []
    
    try:
        gsr_pub, hr_pub, button_pub = pub()
    
        serial_port = serial.Serial(PORT, BAUD, timeout=0)
        thread = threading.Thread(target=read_from_port, args=(serial_port, gsr_pub, hr_pub, button_pub, ack_queue,  ))
        thread.start()
        server()
        
    except rospy.ROSInterruptException:
        pass

