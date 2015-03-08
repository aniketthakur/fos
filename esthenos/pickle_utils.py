__author__ = 'prathvi'
import cv2
import pickle
import gzip

def save(object, filename, protocol = 0):
    """Saves a compressed object to disk
    """
    file = gzip.GzipFile(filename, 'wb')
    file.write(pickle.dumps(object, protocol))
    file.close()

def load(filename):
    """Loads a compressed object from disk
    """
    file = gzip.GzipFile(filename, 'rb')
    buffer = ""
    while True:
            data = file.read()
            if data == "":
                    break
            buffer += data
    object = pickle.loads(buffer)
    file.close()
    return object

def keypoint2str(keypoint):
    """ convert OpenCV Keypoints into string to pickle the data"""
    keypoint_str = []
    keypoint_str.append(float(keypoint.pt[0]))
    keypoint_str.append(float(keypoint.pt[1]))
    keypoint_str.append(float(keypoint.size))
    keypoint_str.append(float(keypoint.angle))
    keypoint_str.append(float(keypoint.response))
    keypoint_str.append(float(keypoint.octave))
    keypoint_str.append(float(keypoint.class_id))
    return keypoint_str

def str2keypoint(keypoint_str):
    """ convert OpenCV Keypoints from string into keypoint-type to process
    after unpickle the data"""
    keypoint = cv2.KeyPoint(float(keypoint_str[0]), float(keypoint_str[1]), float(keypoint_str[2]),
            float(keypoint_str[3]), float(keypoint_str[4]), int(keypoint_str[5]),
            int(keypoint_str[6]), )
    return keypoint


def keypoints2list(kps):
    kp_list = list()
    for kp in kps:
        kp_list.append(keypoint2str(kp))
    return  kp_list

def list2keypoints(kp_list_str):
    kp_list = list()
    for kp_str in kp_list_str:
        kp_list.append(str2keypoint(kp_str))
    return kp_list