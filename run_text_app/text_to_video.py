import cv2
import numpy as np

FRAMES_PER_SECOND = 24
VIDEO_LENGTH_SECONDS = 10
TEXT_SPEED = 7


def text_to_video(message: str, filename: str, width: int = 300, height: int = 100) -> None:
    out = cv2.VideoWriter(filename, cv2.VideoWriter.fourcc(*'mp4v'), FRAMES_PER_SECOND, (width, height))

    frame = np.zeros((height, width, 3), dtype=np.uint8)

    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (255, 255, 255)
    text_size = cv2.getTextSize(message, fontFace=font, fontScale=font_scale, thickness=font_thickness)
    text_width = text_size[0][0]

    x, y = width + TEXT_SPEED, height // 2
    for t in range(FRAMES_PER_SECOND * VIDEO_LENGTH_SECONDS):
        frame.fill(0)
        x = x - TEXT_SPEED if x > -text_width else width
        cv2.putText(frame, message, (x, y), font, font_scale, font_color, font_thickness)
        out.write(frame)

    out.release()
