import cv2
import sys


def play_video(video_path):
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("错误：无法打开！")
        sys.exit()

    # 获取视频的帧率和尺寸
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 创建一个窗口
    cv2.namedWindow("Maymplayer", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Maymplayer", frame_width, frame_height)

    paused = False
    while True:
        if not paused:
            ret, frame = video.read()
            if not ret:
                print("播放结束！")
                break

            cv2.imshow("Maymplayer", frame)

        key = cv2.waitKey(int(1000 / fps)) & 0xFF

        if key == ord('q') or key == 27:  # 按 'q' 退出
            break
        elif key == ord(' '):  # 按空格暂停/继续
            paused = not paused
        elif key == ord('r'):  # 按 'r' 重新开始
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_path = input("请输入视频路径：")
    play_video(video_path)