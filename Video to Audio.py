from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog,
                             QProgressBar, QMessageBox, QComboBox, QHBoxLayout, QListWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon
from moviepy.editor import VideoFileClip
import os
import time

class ConvertThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)

    def __init__(self, video_paths, output_format, output_dir, bitrate):
        super().__init__()
        self.video_paths = video_paths
        self.output_format = output_format
        self.output_dir = output_dir
        self.bitrate = bitrate
        self.total_files = len(video_paths)
        self.current_file_index = 0
        self.is_running = True

    def run(self):
        try:
            for video_path in self.video_paths:
                if not self.is_running:
                    break  # Stop conversion if the thread is no longer running
                video = VideoFileClip(video_path)
                audio_file = os.path.join(self.output_dir, os.path.basename(video_path).split('.')[0] + '.' + self.output_format)

                # Convert audio
                video.audio.write_audiofile(audio_file, bitrate=f"{self.bitrate}k")

                # Update progress after each file is converted
                self.current_file_index += 1
                progress = int((self.current_file_index / self.total_files) * 100)
                self.progress_signal.emit(progress)

            # Emit success when all files are converted
            self.finished_signal.emit("Conversion successful")

        except Exception as e:
            self.finished_signal.emit(f"Error during conversion: {str(e)}")

    def stop(self):
        self.is_running = False

class VideoToAudioApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video to Audio Converter")
        self.setGeometry(300, 200, 500, 400)
        self.setWindowIcon(QIcon('icons/Video to Audio.png'))  # Ensure you have an 'icons' folder with the icon file
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Video selection list
        self.video_list = QListWidget(self)
        layout.addWidget(self.video_list)

        select_layout = QHBoxLayout()

        self.select_btn = QPushButton("Select Videos", self)
        self.select_btn.setIcon(QIcon('icons/add.png'))
        self.select_btn.clicked.connect(self.open_file_dialog)
        select_layout.addWidget(self.select_btn)

        self.clear_btn = QPushButton("Clear List", self)
        self.clear_btn.setIcon(QIcon('icons/clear.png'))
        self.clear_btn.clicked.connect(self.clear_video_list)
        select_layout.addWidget(self.clear_btn)

        layout.addLayout(select_layout)

        # Output format
        format_layout = QHBoxLayout()
        self.format_label = QLabel("Output Format:", self)
        format_layout.addWidget(self.format_label)

        self.format_combo = QComboBox(self)
        self.format_combo.addItems(['mp3', 'wav', 'aac'])
        format_layout.addWidget(self.format_combo)

        layout.addLayout(format_layout)

        # Bitrate selection as a dropdown
        bitrate_layout = QHBoxLayout()
        self.bitrate_label = QLabel("Bitrate:", self)
        bitrate_layout.addWidget(self.bitrate_label)

        self.bitrate_combo = QComboBox(self)
        self.bitrate_combo.addItems(['64', '128', '192', '256', '320'])  # Common bitrates in kbps
        bitrate_layout.addWidget(self.bitrate_combo)

        layout.addLayout(bitrate_layout)

        # Output folder
        self.output_btn = QPushButton("Select Output Folder", self)
        self.output_btn.setIcon(QIcon('icons/folder.png'))
        self.output_btn.clicked.connect(self.select_output_folder)
        layout.addWidget(self.output_btn)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("Progress: 0%", self)
        layout.addWidget(self.progress_label)

        # Convert button
        self.convert_btn = QPushButton("Convert", self)
        self.convert_btn.setIcon(QIcon('icons/convert.png'))
        self.convert_btn.clicked.connect(self.start_conversion)
        layout.addWidget(self.convert_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.video_paths = []
        self.output_dir = None

    def open_file_dialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Video Files", "", "Video Files (*.mp4 *.avi *.mov *.mkv)", options=options)
        if files:
            self.video_paths = files
            self.video_list.clear()
            self.video_list.addItems([os.path.basename(file) for file in files])

    def clear_video_list(self):
        self.video_list.clear()
        self.video_paths = []

    def select_output_folder(self):
        self.output_dir = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if self.output_dir:
            QMessageBox.information(self, "Folder Selected", f"Output folder set to: {self.output_dir}")

    def start_conversion(self):
        if not self.video_paths or not self.output_dir:
            QMessageBox.warning(self, "Error", "Please select video files and an output folder.")
            return

        output_format = self.format_combo.currentText()
        bitrate = self.bitrate_combo.currentText()  # Get selected bitrate from the dropdown

        self.convert_thread = ConvertThread(self.video_paths, output_format, self.output_dir, bitrate)
        self.convert_thread.progress_signal.connect(self.update_progress)
        self.convert_thread.finished_signal.connect(self.handle_conversion_finished)
        self.convert_thread.start()

        # Initialize a timer to simulate progress updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(100)  # Update every 100ms

    def update_timer(self):
        # Here you can adjust how you simulate the progress
        if self.convert_thread.isRunning():
            current_progress = self.progress_bar.value()
            if current_progress < 100:
                self.progress_bar.setValue(current_progress + 1)
                self.progress_label.setText(f"Progress: {current_progress + 1}%")

    def update_progress(self, value):
        self.timer.stop()  # Stop the timer once we receive a valid update
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"Progress: {value}%")

    def handle_conversion_finished(self, message):
        self.timer.stop()  # Stop the timer when conversion finishes
        if message == "Conversion successful":
            QMessageBox.information(self, "Complete", "All videos converted successfully!")
            self.reset_gui()
        else:
            QMessageBox.critical(self, "Error", message)
            self.reset_gui()

    def reset_gui(self):
        self.video_list.clear()
        self.progress_bar.setValue(0)
        self.progress_label.setText("Progress: 0%")
        self.video_paths = []
        self.output_dir = None

if __name__ == '__main__':
    app = QApplication([])
    window = VideoToAudioApp()
    window.show()
    app.exec_()
