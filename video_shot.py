import cv2
import os

video_path = r'path/to/the/video'
save_path = r'path/to/save/image'
min_start = 124
min_end = 126
interval = 2


class VideoShot():
    def __init__(self, video_path, save_path, min_start, min_end, interval):
        """
        :param video_path: path to the video file
        :param save_path: path to save the screen shot
        :param min_start: start time(e.g. 14:57 input as 1457)
        :param min_end: end time
        :param interval: saved frames per second
        """
        self.video_path = video_path
        self.save_path = save_path
        self.min_start = int(min_start)
        self.min_end = int(min_end)
        self.interval = int(interval)

    def min2sec(self):
        sec_start = (self.min_start // 100) * 60 + (self.min_start % 100)
        sec_end = (self.min_end // 100) * 60 + (self.min_end % 100)
        return sec_start, sec_end

    def video2image(self, window):
        """
        :param window: second window to show the progress
        """
        sec_start, sec_end = self.min2sec()
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        count = 0
        img_count = 0
        interval = self.interval
        while cap.isOpened():
            ret, frame = cap.read()
            count += 1

            if count < sec_start * fps:
                if count % round(fps) == 0:
                    # print(f'\r{(count/(sec_start * fps) * 100):.2f}%', end='', flush=True)
                    window['progbar'].update_bar(count / (sec_start * fps) * 100)
                continue

            if count == sec_start * round(fps):
                # print(f'\r100.00%')
                window['progbar'].update_bar(100)
                window['info'].update('Saving')
                event, values = window.read(timeout=0)
                img_count += 1
                _save_path = os.path.join(self.save_path, f'{img_count:>05d}.png')
                cv2.imwrite(_save_path, frame)
                continue

            if count >= sec_end * fps:
                break

            # save interval frames per second
            if count % interval == 0:
                img_count += 1
                _save_path = os.path.join(self.save_path, f'{img_count:>05d}.png')
                cv2.imwrite(_save_path, frame)
                bar_value = img_count * interval / ((sec_end - sec_start) * fps) * 100
                window['progbar'].update_bar(bar_value)

            cv2.waitKey(1)

        cap.release()
        window['progbar'].update_bar(100)
        window['info'].update('Done')
        event, values = window.read(timeout=2000)


if __name__ == '__main__':
    VideoShot(video_path, save_path, min_start, min_end, interval)
