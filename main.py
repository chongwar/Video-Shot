import PySimpleGUI as sg
import warnings
from video_shot import VideoShot

warnings.filterwarnings('ignore')


def window():
    sg.theme('Reddit')
    layout = [[sg.Text('Please choose a video file')],
              [sg.Input('', key='video_path'), sg.FileBrowse()],
              [sg.Text('Please choose a save path')],
              [sg.Input('', key='save_path'), sg.FolderBrowse()],
              [sg.Text('Start time:', size=(17, 1), tooltip='e.g. 112:54 as 11254'),
               sg.Text('End time:', size=(18, 1)),
               sg.Text('Interval', size=(10, 1), tooltip='Frames per second')],
              [sg.Input('1', size=(20, 10), key='start'),
               sg.Input('2', size=(20, 10), key='end'),
               sg.Input('1', size=(10, 10), key='interval')],
              [sg.Button('Save', key='save'), sg.Exit()]]

    window = sg.Window('Video Shot', layout)
    window_1_active = False
    while True:
        event, values = window.Read()
        if event in ['Exit', None]:
            break

        if event == 'save' and not window_1_active:
            video_path = values['video_path']
            save_path = values['save_path']
            min_start = values['start']
            min_end = values['end']
            interval = values['interval']

            video_shot = VideoShot(video_path, save_path, min_start, min_end, interval)

            window_1_active = True
            layout_1 = [[sg.Text('Waiting', key='info')],
                        [sg.ProgressBar(100, orientation='h', size=[20, 20], key='progbar')],
                        [sg.Cancel()]]
            window_1 = sg.Window('', layout_1)

            while True:
                event_1, values_1 = window_1.Read(timeout=0)
                if event_1 == 'Cancel':
                    window_1.Close()
                    window_1_active = False
                    break
                video_shot.video2image(window_1)
                window_1.Close()
                window_1_active = False
                break


if __name__ == '__main__':
    window()
