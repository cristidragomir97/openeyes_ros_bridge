from hw_bridge.srv import *
import rospy


def HapticServiceClient(motor, effects):
    rospy.wait_for_service('HapticService')
    try:
        haptic_service_handler = rospy.ServiceProxy('HapticService', HapticService)
        response = haptic_service_handler(motor, len(effects), effects)
        print(response)
    except rospy.ServiceException as e:
        print('ceva({}) nu-ii bine'.format(e))




if __name__ == "__main__":
    HapticServiceClient(motor = 0, effects = [1, 0, 1, 0])
    HapticServiceClient(motor = 1, effects = [78, 0, 1, 0])
    HapticServiceClient(motor = 2, effects = [1, 0, 78, 0])
