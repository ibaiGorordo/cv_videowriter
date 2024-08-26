import unittest
import cv2
import numpy as np
from cv_videowriter import VideoWriter


class TestVideoWriter(unittest.TestCase):

    def setUp(self):
        self.path = 'test.mp4'
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.test_size = (480, 640)

    def test_creation_does_not_initialize(self):
        writer = VideoWriter(self.path, self.fourcc)
        self.assertFalse(writer.is_initialized())

    def test_write_frame_initializes(self):
        writer = VideoWriter(self.path, self.fourcc)
        writer.write(np.zeros((self.test_size[0], self.test_size[1], 3), np.uint8))
        self.assertTrue(writer.is_initialized())

    def test_write_multiple_frames(self):
        writer = VideoWriter(self.path, self.fourcc)
        num_frames = 10
        for i in range(num_frames):
            frame = np.random.randint(0, 255, (self.test_size[0], self.test_size[1], 3), np.uint8)
            writer.write(frame)
        self.assertTrue(writer.is_initialized())

    def test_write_frame_resize(self):
        writer = VideoWriter(self.path, self.fourcc, force_size=self.test_size)
        self.assertFalse(writer.is_initialized())
        writer.write(np.zeros((100, 100, 3), np.uint8))
        self.assertEqual(writer.frame_size, self.test_size)
        self.assertTrue(writer.is_initialized())

    def test_write_frame_size_mismatch(self):
        writer = VideoWriter(self.path, self.fourcc)
        writer.write(np.zeros((self.test_size[0], self.test_size[1], 3), np.uint8))
        with self.assertRaises(ValueError):
            writer.write(np.zeros((100, 100, 3), np.uint8))

    def test_write_frame_color_conversion(self):
        writer = VideoWriter(self.path, self.fourcc)
        writer.write(np.zeros((self.test_size[0], self.test_size[1], 3), np.uint8))
        writer.write(np.zeros((self.test_size[0], self.test_size[1]), np.uint8))
        self.assertTrue(writer.is_initialized())

    def test_custom_params(self):
        custom_path = 'custom.avi'
        custom_fourcc = cv2.VideoWriter_fourcc(*'XVID')
        custom_fps = 25
        custom_size = (240, 320)
        custom_api = cv2.CAP_FFMPEG
        writer = VideoWriter(custom_path,
                             custom_fourcc,
                             fps=custom_fps,
                             force_size=custom_size,
                             api_preference=custom_api)

        self.assertFalse(writer.is_initialized())
        self.assertEqual(writer.fps, custom_fps)
        self.assertEqual(writer.frame_size, custom_size)
        self.assertEqual(writer.api_preference, custom_api)

    def test_wrong_configuration_should_raise(self):
        writer = VideoWriter(self.path, self.fourcc, api_preference=-1)
        with self.assertRaises(ValueError):
            writer.write(np.zeros((self.test_size[0], self.test_size[1], 3), np.uint8))


if __name__ == '__main__':
    unittest.main()
