import pandas as pd
import matplotlib.pyplot as plt
import math
import glob

PILOT_DATA = './result/LSH'

LEFT_ELBOW = [11, 13, 15]
RIGHT_ELBOW = [12, 14, 16]
LEFT_KNEE = [23, 25, 27]
RIGHT_KNEE = [24, 26, 28]
LEFT_HIP = [11, 23, 25]
RIGHT_HIP = [12, 24, 26]
LEFT_ANKLE = [25, 27, 29]
RIGHT_ANKLE = [26, 28, 32]

Columns = 'LEFT_ELBOW_roll,LEFT_ELBOW_pitch,LEFT_ELBOW_yaw,RIGHT_ELBOW_roll,RIGHT_ELBOW_pitch,RIGHT_ELBOW_yaw' + ',' +\
          'LEFT_KNEE_roll,LEFT_KNEE_pitch,LEFT_KNEE_yaw,RIGHT_KNEE_roll,RIGHT_KNEE_pitch,RIGHT_KNEE_yaw' + ',' + \
          'LEFT_HIP_roll,LEFT_HIP_pitch,LEFT_HIP_yaw,RIGHT_HIP_roll,RIGHT_HIP_pitch,RIGHT_HIP_yaw' + ',' + \
          'LEFT_ANKLE_roll,LEFT_ANKLE_pitch,LEFT_ANKLE_yaw,RIGHT_ANKLE_roll,RIGHT_ANKLE_pitch,RIGHT_ANKLE_yaw'


def calc_angles_on_3d(p1, p2, p3):
    angle_xy = calc_angle_on_2d((p1[0], p1[1]),
                                (p2[0], p2[1]),
                                (p3[0], p3[1]))
    angle_yz = calc_angle_on_2d((p1[1], p1[2]),
                                (p2[1], p2[2]),
                                (p3[1], p3[2]))
    angle_zx = calc_angle_on_2d((p1[2], p1[0]),
                                (p2[2], p2[0]),
                                (p3[2], p3[0]))

    return (angle_xy, angle_yz, angle_zx)


def calc_angle_on_2d(p1, p2, p3):
    w = p3[0] - p2[0]
    h = p1[1] - p3[1]
    radian = math.atan2(h, w)
    angle = radian * 180. / math.pi

    return angle


def main():
    file_paths = glob.glob(PILOT_DATA + "/*-skeleton3D.csv")
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        vid_pose_landmarks = (df.values).reshape(df.shape[0], -1, 3)

        f = open(file_path.replace('-skeleton3D', '-angles'), 'w')

        f.write(Columns + "\n")

        for pose_landmarks in vid_pose_landmarks:
            row = ''
            for pose_landmark in [LEFT_ELBOW, RIGHT_ELBOW, LEFT_KNEE, RIGHT_KNEE, LEFT_HIP, RIGHT_HIP, LEFT_ANKLE, RIGHT_ANKLE]:
                _roll, _pitch, _yaw = calc_angles_on_3d(pose_landmarks[pose_landmark[0]],
                                                        pose_landmarks[pose_landmark[1]],
                                                        pose_landmarks[pose_landmark[2]])
                row = row + "{},{},{},".format(_roll, _pitch, _yaw)

            f.write(row[:-1] + "\n")

        f.close()


    # _row_front = (side_df.iloc[0].values).reshape((-1, 3))

    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # for row in _row_front:
    #     ax.scatter3D(row[0], row[1], row[2])
    #
    # for target_angle in [LEFT_ELBOW, RIGHT_ELBOW, LEFT_KNEE, RIGHT_KNEE, LEFT_HIP, RIGHT_HIP, LEFT_ANKLE, RIGHT_ANKLE]:
    #     _roll, _pitch, _yaw = calc_angles_on_3d(_row_front[target_angle[0]],
    #                                             _row_front[target_angle[1]],
    #                                             _row_front[target_angle[2]])
    #
    #     print(_roll, _pitch, _yaw)
    #






    # angles = calc_angles_on_3d(p1, p2, p3)
    # print(angles)
    #
    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # ax.scatter3D(p1[0], p1[1], p1[2])
    # ax.scatter3D(p2[0], p2[1], p2[2])
    # ax.scatter3D(p3[0], p3[1], p3[2])
    # plt.show()


if __name__ == '__main__':
    main()