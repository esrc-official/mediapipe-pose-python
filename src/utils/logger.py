import os
import pandas as pd
import cv2
from tqdm import tqdm


class Logger:
    def __init__(self, log_path):
        self.landmark_dir = log_path + "/landmarks"
        self.video_dir = log_path + "/videos"
        self.angle_dir = log_path + "/angles"
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_extension = ".mp4"
        if not os.path.exists(self.landmark_dir):
            os.makedirs(self.landmark_dir)
        if not os.path.exists(self.video_dir):
            os.makedirs(self.video_dir)
        if not os.path.exists(self.angle_dir):
            os.makedirs(self.angle_dir)

    def save_landmarks(self, name, landmarks, columns):
        df = pd.DataFrame(landmarks, columns=columns)
        df.to_csv(self.landmark_dir + "/" + name + ".csv")

    def save_videos(self, name, frames, meta):
        writer = cv2.VideoWriter(self.video_dir + "/" + name + self.video_extension, self.fourcc, meta[2], (meta[0], meta[1]))
        for frame in tqdm(frames, "Saving videos"):
            writer.write(frame)
        writer.release()

    def save_angles(self, name, angles, columns):
        df = pd.DataFrame(angles, columns=columns)
        df.to_csv(self.angle_dir + "/" + name + ".csv")
