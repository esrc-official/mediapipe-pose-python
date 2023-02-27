import mediapipe as mp
import cv2
import numpy as np
from tqdm import tqdm
import math

from ..archimodule import ArchiModule

LEFT_ELBOW = [11, 13, 15]
RIGHT_ELBOW = [12, 14, 16]
LEFT_KNEE = [23, 25, 27]
RIGHT_KNEE = [24, 26, 28]
LEFT_HIP = [11, 23, 25]
RIGHT_HIP = [12, 24, 26]
LEFT_ANKLE = [25, 27, 29]
RIGHT_ANKLE = [26, 28, 32]
ANGLES = [LEFT_ELBOW, RIGHT_ELBOW,
          LEFT_KNEE, RIGHT_KNEE,
          LEFT_HIP, RIGHT_HIP,
          LEFT_ANKLE, RIGHT_ANKLE]

LANDMARK_2D_COLUMNS = ["landmark" + str(ldx) + "_" + dim for ldx in range(33) for dim in ["x", "y"]]
LANDMARK_3D_COLUMNS = ["landmark" + str(ldx) + "_" + dim for ldx in range(33) for dim in ["x", "y", "z"]]
ANGLE_2D_COLUMNS = [joint + "_" + dim for joint in (
                    ["left_elbow", "right_elbow", "left_knee", "right_knee", "left_hip", "right_hip", "left_ankle", "right_ankle"])
                    for dim in ["roll"]]
ANGLE_3D_COLUMNS = [joint + "_" + dim for joint in (
                    ["left_elbow", "right_elbow", "left_knee", "right_knee", "left_hip", "right_hip", "left_ankle", "right_ankle"])
                    for dim in ["roll", "pitch", "yaw"]]


class PoseModule(ArchiModule):
    n_landmarks = 33
    n_dims = 3

    def __init__(self,
                 min_detection_confidence: float,
                 min_tracking_confidence: float,
                 swap_rb: bool,
                 relative_coordinate: bool):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.model = mp.solutions.pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence)
        self.swap_rb = swap_rb
        self.relative_coordinate = relative_coordinate
        if relative_coordinate:
            self.n_dims = 3
        else:
            self.n_dims = 2

    def predict_step(self, batch):
        if self.swap_rb:
            batch = cv2.cvtColor(batch, cv2.COLOR_BGR2RGB)
        pred = self.model.process(batch)
        return pred

    def predict(self, dataset, logger):
        for idx in tqdm(range(dataset.len()), "Predicting dataset"):
            frames = dataset.getitem(idx)
            results = []
            preds = []
            angles = []
            for frame in tqdm(frames, "Predicting data[" + str(idx) + "]"):
                # Predict landmarks
                result = self.predict_step(frame)

                # If relative coordinates
                if self.relative_coordinate:
                    landmarks, angle = self.__extract_landmarks_and_angles_on_relative_coordinates(result)
                # If absolute coordinates
                else:
                    landmarks, angle = self.__extract_landmarks_and_angles_on_absolute_coordinates(result, frame)

                # Add results
                results.append(result)
                preds.append(landmarks)
                angles.append(angle)

            # Visualize results
            vis_frames = self.__visualize__(frames, results)

            if logger:
                name = dataset.getname(idx)
                if self.relative_coordinate:
                    logger.save_landmarks(name, preds, LANDMARK_3D_COLUMNS)
                    logger.save_angles(name, angles, ANGLE_3D_COLUMNS)
                else:
                    logger.save_landmarks(name, preds, LANDMARK_2D_COLUMNS)
                    logger.save_angles(name, angles, ANGLE_2D_COLUMNS)
                logger.save_videos(name, vis_frames, dataset.getmeta(idx))

    def __visualize__(self, frames, results):
        vis_frames = []
        for frame, result in tqdm(zip(frames, results), "Visualizing result"):
            frame.flags.writeable = True
            if result.pose_world_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    result.pose_landmarks,
                    mp.solutions.pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
            vis_frames.append(frame)
        return vis_frames

    def __extract_landmarks_and_angles_on_relative_coordinates(self, result):
        landmarks = [np.nan for _ in range(self.n_landmarks * self.n_dims)]
        angle = [np.nan for _ in range(len(ANGLE_3D_COLUMNS))]
        # Arrange landmarks
        if result.pose_world_landmarks is not None:
            for ldx, landmark in enumerate(result.pose_world_landmarks.landmark):
                landmarks[ldx * self.n_dims] = landmark.x
                landmarks[ldx * self.n_dims + 1] = landmark.y
                landmarks[ldx * self.n_dims + 2] = landmark.z

                # Analyze angle
                for adx, ldx in enumerate(ANGLES):
                    roll, pitch, yaw = self.__calc_angles_on_3d__(
                        (landmarks[ldx[0] * self.n_dims], landmarks[ldx[0] * self.n_dims + 1],
                         landmarks[ldx[0] * self.n_dims + 2]),
                        (landmarks[ldx[1] * self.n_dims], landmarks[ldx[1] * self.n_dims + 1],
                         landmarks[ldx[1] * self.n_dims + 2]),
                        (landmarks[ldx[2] * self.n_dims], landmarks[ldx[2] * self.n_dims + 1],
                         landmarks[ldx[2] * self.n_dims + 2]))
                    angle[adx * self.n_dims] = roll
                    angle[adx * self.n_dims + 1] = pitch
                    angle[adx * self.n_dims + 2] = yaw

        return landmarks, angle

    def __extract_landmarks_and_angles_on_absolute_coordinates(self, result, frame):
        landmarks = [np.nan for _ in range(self.n_landmarks * self.n_dims)]
        angle = [np.nan for _ in range(len(ANGLE_2D_COLUMNS))]
        # Arrange landmarks
        image_rows, image_cols, _ = frame.shape
        if result.pose_landmarks is not None:
            for ldx, landmark in enumerate(result.pose_landmarks.landmark):
                landmarks[ldx * self.n_dims] = landmark.x * image_cols
                landmarks[ldx * self.n_dims + 1] = landmark.y * image_rows

                # Analyze angles
                for adx, ldx in enumerate(ANGLES):
                    roll = self.__calc_angle_on_2d__(
                        (landmarks[ldx[0] * self.n_dims], landmarks[ldx[0] * self.n_dims + 1]),
                        (landmarks[ldx[1] * self.n_dims], landmarks[ldx[1] * self.n_dims + 1]),
                        (landmarks[ldx[2] * self.n_dims], landmarks[ldx[2] * self.n_dims + 1]))
                    angle[adx] = roll

        return landmarks, angle

    def __calc_angles_on_3d__(self, p1, p2, p3):
        angle_xy = self.__calc_angle_on_2d__((p1[0], p1[1]),
                                             (p2[0], p2[1]),
                                             (p3[0], p3[1]))
        angle_yz = self.__calc_angle_on_2d__((p1[1], p1[2]),
                                             (p2[1], p2[2]),
                                             (p3[1], p3[2]))
        angle_zx = self.__calc_angle_on_2d__((p1[2], p1[0]),
                                             (p2[2], p2[0]),
                                             (p3[2], p3[0]))

        return (angle_xy, angle_yz, angle_zx)

    def __calc_angle_on_2d__(self, p1, p2, p3):
        w = p3[0] - p2[0]
        h = p1[1] - p3[1]
        radian = math.atan2(h, w)
        angle = radian * 180. / math.pi

        return angle
