from Pose_estimator import PoseEstimator
import cv2
import glob
import timeit
import pandas as pd

# Video_dir = glob.glob('videos/LSH/*.mp4')
Video_dir = 0
fourcc = cv2.VideoWriter_fourcc(*'FMP4')


def readSkeleton3D(filename):
    df = pd.read_csv(filename)
    print(df.head())


def main(video_paths):
    pose_model = PoseEstimator()

    # for video_path in video_paths:
    #     cap = cv2.VideoCapture(video_path)
    #     result_video_path = video_path.replace('videos', 'result')
    #     print("Start : ", video_path)
        # video = cv2.VideoWriter(result_video_path, fourcc, 20.0, (1920, 1080))
        # f = open(result_video_path.replace('.mp4', '-skeleton3D.csv'), 'w')
        # columns = "0_x,0_y,0_z"
        # for i in range(1, 33):
        #     columns = columns + ","
        #     columns = columns + "{}_x,{}_y,{}_z".format(i, i, i)
        #
        # f.write(columns + "\n")

    cap = cv2.VideoCapture(0)

    while True:
        # start_t = timeit.default_timer()

        ret, frame = cap.read()

        if not ret:
            print("카메라를 찾을 수 없습니다.")
            # 동영상을 불러올 경우는 'continue' 대신 'break'를 사용합니다.
            break

        pose_model.feed(img=frame)

        if pose_model.is_detected:
            pose_landmarks = pose_model.getPoseLandamrk()
            x = pose_landmarks.getX()
            y = pose_landmarks.getY()
            z = pose_landmarks.getZ()

            # saveSkeleton3D(x, y, z, video_path.replace('.mp4', '-skeleton3D.csv'))
            row = ""
            for _x, _y, _z in zip(x, y, z):
                row = row + "{},{},{}".format(_x, _y, _z)
                row = row + ","

            # f.write(row[:-1] + "\n")

            pose_img = pose_model.visualizePose(frame)

            # pose_model.visalizeWorldPose()

            cv2.imshow('MediaPipe Pose', cv2.flip(pose_img, 1))

            # video.write(pose_img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        # terminate_t = timeit.default_timer()
        # FPS = int(1. / (terminate_t - start_t))
        # print("FPS: ", FPS)

    # f.close()
    # video.release()
    cap.release()


if __name__ == '__main__':
    main(video_paths=Video_dir)