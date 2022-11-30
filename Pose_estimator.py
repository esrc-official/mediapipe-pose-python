import mediapipe as mp
import cv2
import numpy as np
import pandas as pd

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


class PoseEstimator:
    def __init__(self):
        self.model = mp.solutions.pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.landmarks = None
        self.raw_result = None
        self.is_detected = False

    def feed(self, img):
        img.flags.writeable = False
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.model.process(img)

        if not results.pose_world_landmarks:
            print("Not Detected Pose Landmark")
            self.landmarks = None
            self.is_detected = False
        else:
            self.is_detected = True

            lm_x = []
            lm_y = []
            lm_z = []
            for lm in results.pose_world_landmarks.landmark:
                x = lm.x
                y = lm.y
                z = lm.z
                lm_x.append(x)
                lm_y.append(y)
                lm_z.append(z)

            self.landmarks = PoseLandmark(x=np.array(lm_x), y=np.array(lm_y), z=np.array(lm_z))
            self.raw_result = results

    def getPoseLandamrk(self):
        return self.landmarks

    def visualizePose(self, img):
        img.flags.writeable = True
        # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            img,
            self.raw_result.pose_landmarks,
            mp.solutions.pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        return img

    def visalizeWorldPose(self):
        mp_drawing.plot_landmarks(
            self.raw_result.pose_world_landmarks, mp.solutions.pose.POSE_CONNECTIONS)


class PoseLandmark:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        # self.vis = vis

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    # def to_excel(self, file_name):
    #     columns = ['{}_x'.format(i) for i in range(0, 33)] + ['{}_y'.format(i) for i in range(0, 33)]
    #
    #     df = pd.DataFrame(columns=columns)



    # def getVis(self):
    #     return self.vis



