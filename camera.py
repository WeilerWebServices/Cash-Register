"""
Webcam capture functionality for ID verification
"""

import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class CameraHandler:
    def __init__(self):
        """Initialize webcam capture"""
        self.camera = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.captured_image = None
        
    def start_capture(self, display_label):
        """
        Start displaying webcam feed on the given label
        :param display_label: QLabel to display the camera feed
        """
        self.display_label = display_label
        self.timer.timeout.connect(lambda: self.update_frame(display_label))
        self.timer.start(20)  # Update every 20ms
        
    def update_frame(self, label):
        """Update the displayed camera frame"""
        ret, frame = self.camera.read()
        if ret:
            # Convert to RGB for display
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            label.setPixmap(QPixmap.fromImage(qt_image))
    
    def capture_image(self, save_path='id_images/'):
        """
        Capture current frame and save as ID image
        :param save_path: Directory to save captured images
        :return: Path to saved image
        """
        ret, frame = self.camera.read()
        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{save_path}id_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            self.captured_image = filename
            return filename
        return None
    
    def release(self):
        """Release camera resources"""
        self.timer.stop()
        self.camera.release()