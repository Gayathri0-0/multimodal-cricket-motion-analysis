import mediapipe as mp

mp_pose = mp.solutions.pose

def extract_keypoints(landmarks):
    return {
        "nose": landmarks[mp_pose.PoseLandmark.NOSE.value],
        "left_shoulder": landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
        "right_shoulder": landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
        "left_hip": landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
        "right_hip": landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
        "left_knee": landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
        "right_knee": landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
        "left_ankle": landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value],
        "right_ankle": landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value],
    }


