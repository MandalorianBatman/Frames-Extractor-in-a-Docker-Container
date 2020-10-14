from datetime import datetime
from pathlib import Path

import numpy as np
from cv2 import cv2

class videoUtility():
    def __init__(self, video_source = 0):
        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)
        self.output_path = './images'
        
    def __enter__(self): return self
    
    def __exit__(self, type, value, traceback):
        self.destroy()
    
    def destroy(self):
        self.cap.release()
        cv2.destroyAllWindows()
        
    def saveFrames(self, frames_to_skip, output_path = None):
        if output_path:
            self.output_path = output_path
            
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        self.__saveFramesFromCamera(frames_to_skip) if self.video_source == 0 else self.__saveFramesFromVideo(frames_to_skip)

    def __saveFramesFromCamera(self, frames_to_skip: int = 5):
        try:
            frame_no = 0
            while True:
                frame_no += 1
                ret, frame = self.cap.read()
                if not ret:
                    break
                else:
                    cv2.imshow("Video Source (Press 'Q' to quit)", frame)
                    if frame_no % frames_to_skip == 0:
                        file_name = datetime.now().strftime('%H%M%S-%m%d%Y')
                        cv2.imwrite(f'{self.output_path}/img-{file_name}-{int(frame_no)}.jpg', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if frame_no > 1000: break
        except Exception as e:
            print(e)
    
    def __saveFramesFromVideo(self, frames_to_skip: int = 5):
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                else:
                    frame_no = self.cap.get(1)
                    file_name = datetime.now().strftime('%H%M%S-%m%d%Y')
                    cv2.imwrite(f'{self.output_path}/img-{file_name}-{int(frame_no)}.jpg', frame)
                    self.cap.set(1, (frame_no + (frames_to_skip - 1)))
        except Exception as e:
            print(e)

def main():
    video_source_input = str(input("\nEnter the Path for video (Leave blank for Video Camera): \n"))
    video_source = video_source_input if video_source_input else None
    
    output_path_input = str(input("\nEnter the Path for output folder (Leave blank for using current directory): \n"))
    output_path = output_path_input if output_path_input else None
    
    frames_to_skip = int(input("\nEnter the number of frames to skip: "))
    
    with videoUtility(video_source) as video:
        video.saveFrames(frames_to_skip, output_path)
        
if __name__ == '__main__':
    main()