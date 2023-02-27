from typing import List
import glob
import cv2
from tqdm import tqdm

from ..dataset import Dataset


class PoseDataset(Dataset):
    def __init__(self, data_path: str, extension: str, flip_x: bool, flip_y: bool):
        super().__init__()
        self.extension = extension
        self.data_list = self.load_data(data_path, extension)
        self.flip_x = flip_x
        self.flip_y = flip_y

    def len(self):
        return len(self.data_list)

    def getitem(self, idx):
        capture = cv2.VideoCapture(self.data_list[idx])
        if not capture.isOpened():
            raise FileNotFoundError(str(self.data_list[idx]) + " is not found")

        num_of_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        data_tqdm = tqdm(total=num_of_frames, desc="Loading data[" + str(idx) + "]")

        frames = []
        while capture.isOpened():
            ret, frame = capture.read()
            if not ret:
                break
            if self.flip_x:
                frame = cv2.flip(frame, 1)
            if self.flip_y:
                frame = cv2.flip(frame, 0)
            frames.append(frame)
            data_tqdm.update(1)
        capture.release()

        data_tqdm.close()
        return frames

    def getname(self, idx):
        name = self.data_list[idx].split("/")[-1].replace(self.extension, "")
        return name

    def getmeta(self, idx):
        capture = cv2.VideoCapture(self.data_list[idx])
        if not capture.isOpened():
            raise FileNotFoundError(str(self.data_list[idx]) + " is not found")
        frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = capture.get(cv2.CAP_PROP_FPS)
        return frame_width, frame_height, fps

    @staticmethod
    def load_data(data_path: str, extension: str) -> List:
        data_list = glob.glob(data_path + "/videos/*" + extension)
        # data_list = glob.glob(data_path + "/*" + extension)
        return data_list
