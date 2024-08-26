import cv2
import numpy as np


class VideoWriter:
    writer: cv2.VideoWriter = cv2.VideoWriter()
    file_size: int = 0
    is_color: bool = True

    def __init__(self,
                 filename: str,
                 fourcc: int,
                 fps: float = 30,
                 force_size: tuple[int, int] = None,
                 api_preference: int = cv2.CAP_ANY):

        self.filename: str = filename
        self.fourcc: int = fourcc
        self.fps: float = fps
        self.do_resize: bool = force_size is not None
        self.frame_size: tuple[int, int] = force_size if self.do_resize else (0, 0)
        self.api_preference: int = api_preference

    def __call__(self, frame: np.ndarray):
        self.write(frame)

    def __del__(self):
        self.release()

    def write(self, frame: np.ndarray):
        if not self.is_initialized():
            self._initialize(frame)

        if self.do_resize:
            frame = cv2.resize(frame, self.frame_size)
        elif frame.shape[0] != self.frame_size[0] or frame.shape[1] != self.frame_size[1]:
            raise ValueError(
                f'The size of the given frame ({frame.shape[1]}x{frame.shape[0]}) is different from the initialized '
                f'size ({self.frame_size[1]}x{self.frame_size[0]}).')

        # Check if the frame is in the correct color format
        frame = self._fix_color(frame)

        self.writer.write(frame)

    def release(self):
        if self.is_initialized():
            self.writer.release()

    def is_initialized(self):
        return self.writer.isOpened()

    def _initialize(self, frame: np.ndarray):
        self.frame_size = frame.shape[:2] if not self.do_resize else self.frame_size
        self.is_color = frame.ndim == 3
        self.writer.open(filename=self.filename,
                         fourcc=self.fourcc,
                         fps=self.fps,
                         frameSize=self.frame_size[::-1],
                         apiPreference=self.api_preference,
                         isColor=self.is_color)

        if not self.writer.isOpened():
            raise ValueError(f'There was some error with the configuration of the VideoWriter, check the parameters '
                             f'and the file path.')

    def _fix_color(self, frame: np.ndarray) -> np.ndarray:
        if frame.ndim == 2 and self.is_color:
            return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif frame.ndim == 3 and not self.is_color:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif frame.ndim == 3 and self.is_color or frame.ndim == 2 and not self.is_color:
            return frame

        raise ValueError(f'The color format of the frame is not compatible with the initialized VideoWriter.')


if __name__ == '__main__':
    import cv2
    import numpy as np
    import VideoWriter

    writer = VideoWriter('test.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30)

    for i in range(100):
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        writer.write(frame)
