import threading, time, serial, rospy
from std_msgs.msg import String, Int8
from colorama import Fore

Q_SIZE = 10
PORT = '/dev/ttyUSB0'
BAUD = 112500

  
def read_from_port(ser, gsr_pub, button_pub, hr_pub):
    while True:
        text = ser.readline().decode()
        if text:
            if text[0] == 'g':
                val = text[1:len(text)]
                print(Fore.YELLOW + '[GSR]' + val)
                gsr_pub.publish(val)

            elif text[0] == 'b':
                val = text[1:len(text)]
                print(Fore.RED + '[BTN]' + val)
                button_pub.publish(val)

            elif text[0] == 'h':
                val = text[1:len(text)]
                print(Fore.GREEN + '[HEART]' + val)
                hr_pub.publish(val)
                 
            #elif text[0] == 'k':

        time.sleep(0.3)

def handle_req(req):
    pass

def pub():

    gsr_pub = rospy.Publisher('gsr', String, queue_size= Q_SIZE)
    rospy.loginfo('* created gsr publisher')

    hr_pub = rospy.Publisher('hr', String, queue_size= Q_SIZE)
    rospy.loginfo('* created hr publisher')

    button_pub = rospy.Publisher('btn', String, queue_size= Q_SIZE)
    rospy.loginfo('* created btn publisher')
    
    return gsr_pub, hr_pub, button_pub

def server():
    srv = rospy.Service('haptic_out', haptic, handle_req)
    rospy.spin()
    

if __name__ == '__main__':
    rospy.init_node('bridge')
     
    ack_queue = []
    
    try:
        gsr_pub, hr_pub, button_pub = pub()
        server()
        
        serial_port = serial.Serial(PORT, BAUD, timeout=0)
        thread = threading.Thread(target=read_from_port, args=(serial_port, gsr_pub, hr_pub, button_pub, ack_queue,  ))
        thread.start()
    
        
    except rospy.ROSInterruptException:
        pass

