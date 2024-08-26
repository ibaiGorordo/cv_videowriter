# cv_videowriter
Wrapper around OpenCV VideoWriter with some extra features.

## Features
- Raise an exception if the video file is not created due to wrong configuration parameters.
- Automatically select the video size based on the first written frame.
- Raise an exception if the passed frame has a different size than the video size.
- Add force resize option to resize the frame to a predefined size.
- It will run cvtColor if the frame color is not the same as the video color. Or it will raise an exception if the frame color is not convertible to the video color.

## Installation [![PyPI](https://img.shields.io/pypi/v/cv_videowriter?color=2BAF2B)](https://pypi.org/project/cv_videowriter/)
```bash
pip install cv_videowriter
```

## Usage

```python
import cv2
import numpy as np
from cv_videowriter import VideoWriter

writer = VideoWriter('test.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30)

for i in range(10):
    frame = np.random.randint(0, 255, (460, 640, 3), dtype=np.uint8)
    writer.write(frame)
```

## Parameters
- `filename`: str - Path to the video file.
- `fourcc`: int - FourCC code of the codec used to compress the frames.
- `fps`: float (default: 30) - Frame rate of the created video.
- `force_resize`: tuple[int, int] (default: None) - Resize the frame to the specified size (height, width) before writing it to the video file.
- `api_preference`: int (default: cv2.CAP_ANY) - API backends for video capturing.

