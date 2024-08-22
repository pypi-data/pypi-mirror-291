import os

import cv2
import numpy as np
from pupil_apriltags import Detector


def detect_apriltags(image_path, tag_family='tag36h11', render=True, show=True, save=False):
    """
    Detect the apriltags in image and return the positions of the tags.

    Args:
        image_path: Path to the image file
        tag_family: Tag family to detect
        render: Render the detected tags on the image or not
        show: Show the detected image or not
        save: Save the detected image or not
    """
    tag_pos = {}

    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image")
        return

    # Image resolution
    height, width, _ = image.shape
    print(f"Image resolution: {width}x{height} (Width x Height)")

    # Detect tags in the image
    detector = Detector(families=tag_family, nthreads=4)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    tags = detector.detect(gray)

    # Iterate over detected tags
    for tag in tags:
        # Calculate the center of the tag
        center = np.mean(tag.corners, axis=0)
        corners = np.int32(tag.corners)

        # Draw the tag ID with a background and border
        if render:
            tag_position = (int(corners[0][0]), int(corners[0][1]) - 10)  # Adjust position above the tag
            text = f"{tag.tag_id}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 5
            font_thickness = 14
            text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
            text_x, text_y = tag_position
            # Draw black border
            cv2.rectangle(image, (text_x - 20, text_y - text_size[1] - 20), (text_x + text_size[0] + 10, text_y + 30),
                          (0, 0, 0), -1)
            # Draw white background
            cv2.rectangle(image, (text_x - 10, text_y - text_size[1] - 10), (text_x + text_size[0], text_y + 20),
                          (255, 255, 255), -1)
            # Put black text
            cv2.putText(image, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness)

        # Print the center position
        x = float(f'{center[0] / width:.4f}')
        y = float(f'{center[1] / height:.4f}')
        print(f"Person ID {tag.tag_id} center position: [{x}, {y}]")
        tag_pos[tag.tag_id] = [x, y]

    # Show the result
    if show:
        cv2.imshow('AprilTag Detection', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Save detected image
    if save:
        dirname, filename = os.path.split(image_path)
        name, ext = os.path.splitext(filename)
        save_path = os.path.join(dirname, f"{name}_detected{ext}")
        cv2.imwrite(save_path, image)
        print(f"Detected image saved as {save_path}")

    return tag_pos
