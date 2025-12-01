# Coursera Helper

A powerful and user-friendly tool to download Coursera courses for personal offline learning.

## Features
- **GUI Interface**: Easy to use graphical interface.
- **Bulk Download**: Download entire courses including videos, subtitles, and notebooks.
- **Quality Selection**: Choose between 360p, 540p, and 720p.
- **Subtitle Support**: Download subtitles in your preferred language.
- **Resume Capability**: Resume interrupted downloads.

## Installation

1. **Install Python**: Ensure you have Python 3.8 or later installed.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **FFmpeg**: Ensure FFmpeg is installed and added to your system PATH (required for some video processing).

## Usage

### Running the Application
You can run the application using the provided batch file or directly via Python:

**Option 1: Batch File (Windows)**
Double-click `Launch-Coursera-Helper.bat`.

**Option 2: Python**
```bash
python run.py
```

### How to Download
1. **Login to Coursera**: Open your web browser and log in to Coursera.
2. **Select Course**: Copy the URL of the course you want to download (e.g., `https://www.coursera.org/learn/python`).
3. **Configure**:
   - Paste the URL into the "Course URL" field.
   - Select the browser you are logged into.
   - Choose your download folder and quality settings.
4. **Start**: Click "Start Download".

## Disclaimer
This tool is for **personal learning purposes only**. Please respect Coursera's Terms of Service and the intellectual property rights of the content creators. Do not redistribute downloaded materials.

## License
[MIT License](LICENSE)
