import os
import cv2


class LoadVideo: 
    def __init__(self, path, img_size=(1088, 608)) -> None:
        """
        Input:
        - path: A string representing the file path to the video.
        - img_size: A tuple representing the target width and height for resizing video frames (default is (1088, 608)).

        Output:
        - Initializes the video capture object and extracts key properties such as frame rate, width, height, and total frame count.
        - No return value, but sets instance variables for video properties and target image size.
        """
        if not os.path.isfile(path):
            raise FileExistsError

        self.cap = cv2.VideoCapture(path)
        self.frame_rate = int(round(self.cap.get(cv2.CAP_PROP_FPS)))
        self.vw = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.vh = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.vn = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = img_size[0]
        self.height = img_size[1]
        self.count = 0

    def get_VideoLabels(self):
        # This method returns key properties of the loaded video:
        # - self.cap: the video capture object
        # - self.frame_rate: the frame rate (frames per second) of the video
        # - self.vw: the width of the video frames
        # - self.vh: the height of the video frames
        # - self.vn: the total number of frames in the video
        return self.cap, self.frame_rate, self.vw, self.vh, self.vn