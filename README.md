# Video to Audio Converter



## Overview

**Video to Audio Converter** is a user-friendly Python application that allows users to easily convert video files into audio formats like MP3, WAV, and AAC. The application supports batch conversion, customizable bitrates, and displays real-time progress during the conversion process.

## Features

- Convert multiple video files (MP4, AVI, MOV, MKV) to audio formats (MP3, WAV, AAC).
- Customizable audio bitrate (64, 128, 192, 256, 320 kbps).
- Progress bar with percentage updates for real-time feedback.
- Selectable output directory for converted audio files.
- Clear and simple user interface (built with PyQt5).
- Icons for buttons and improved visual layout.
- Support for multiple video files with batch conversion.

## Screenshots

![App Interface](https://github.com/NSTechBytes/Projects-Templates/blob/main/Applications/Video%20to%20Audio/Untitled%20design.png)
*Sample interface of the Video to Audio Converter.*

## Installation

To install and run the Video to Audio Converter, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/NSTechBytes/Video-to-Audio.git
   cd Video-to-Audio
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

## Dependencies

- [PyQt5](https://pypi.org/project/PyQt5/)
- [moviepy](https://pypi.org/project/moviepy/)

To install dependencies manually:
```bash
pip install PyQt5 moviepy
```

## Usage

1. Open the application and select one or more video files using the "Select Videos" button.
2. Choose the output audio format (MP3, WAV, or AAC) from the dropdown.
3. Select the desired audio bitrate from the available options (64 kbps to 320 kbps).
4. Choose an output folder for the converted audio files.
5. Click the "Convert" button to start the conversion process. A progress bar will show the conversion status.
6. Once the conversion is complete, a message will notify you of the success or any errors.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add feature'`).
4. Push the changes to your branch (`git push origin feature-branch`).
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Icons used in the application are sourced from free and open-source icon sets.
- The application uses the [MoviePy](https://zulko.github.io/moviepy/) library for video and audio processing.

## Contact

For any inquiries or feedback, please feel free to reach out via nstechbytes@gmail.com or create an issue on the GitHub repository.

---

*Made with ❤️ by Nasir Shahbaz.*
