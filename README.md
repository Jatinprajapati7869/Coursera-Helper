# 🎓 Coursera Helper

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/github/license/Jatinprajapati7869/Coursera-Helper)
![Status](https://img.shields.io/badge/status-active-success)

**Coursera Helper** is a robust, user-friendly desktop application designed to streamline the process of downloading Coursera course materials for offline learning. Built with Python and PyQt5, it offers a modern, dark-themed GUI that makes archiving your learning resources effortless.

> **⚠️ Disclaimer**: This tool is intended for **personal learning and archiving purposes only**. Please respect Coursera's Terms of Service and the intellectual property rights of instructors. Do not redistribute downloaded content.

---

## ✨ Features

- **🖥️ Modern GUI**: A sleek, glassmorphism-inspired dark interface built with PyQt5.
- **📦 Bulk Download**: Download entire courses, including:
  - 📹 Lecture Videos (MP4)
  - 📝 Subtitles (SRT) in multiple languages
  - 📓 Jupyter Notebooks and supplementary materials
  - 📄 Quizzes and references
- **⚙️ Flexible Quality**: Choose your preferred video resolution:
  - **HD (720p)** for best clarity
  - **SD (540p)** for balanced size/quality
  - **Low (360p)** for bandwidth saving
- **🗣️ Multi-language Subtitles**: Automatically download subtitles in English, Chinese, Spanish, and more.
- **⏯️ Smart Resume**: Interrupted downloads? No problem. The tool resumes right where it left off.
- **🔐 Secure Login**: Supports authentication via cookies from your browser (Chrome, Firefox, Edge, Brave).

---

## 🚀 Installation

### Prerequisites
- **Python 3.8** or higher installed on your system.
- **FFmpeg** installed and added to your system PATH (required for processing some video formats).

### Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Jatinprajapati7869/Coursera-Helper.git
    cd Coursera-Helper
    ```

2.  **Set up a Virtual Environment (Recommended)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 📖 Usage

### Method 1: The Easy Way (Windows)
Simply double-click the `Launch-Coursera-Helper.bat` file. It will automatically handle administrator privileges (if needed) and launch the application.

### Method 2: Command Line
```bash
python run.py
```

### 📝 How to Download a Course

1.  **Log in to Coursera**: Open your web browser (Chrome, Firefox, Edge, or Brave) and log in to your Coursera account.
2.  **Get Course URL**: Navigate to the course you want to download and copy the URL (e.g., `https://www.coursera.org/learn/machine-learning`).
3.  **Launch App**: Open Coursera Helper.
4.  **Configure**:
    - Paste the **Course URL**.
    - Select the **Browser** you used to log in.
    - Choose a **Download Folder**.
    - Select **Video Quality** and **Subtitle Language**.
5.  **Start**: Click **Start Download** and watch the progress!

---

## 🛠️ Troubleshooting

**Q: I get an authentication error.**
A: Ensure you are logged into Coursera in the selected browser. If using Chrome/Edge, try closing the browser before starting the download to release the cookie database lock.

**Q: The download stops or fails.**
A: Check your internet connection. The tool supports resuming, so just click "Start Download" again to pick up where you left off.

**Q: "FFmpeg not found" error.**
A: You need to install FFmpeg and add it to your System Environment Variables (PATH).

---

## 🤝 Contributing

Contributions are welcome! We love seeing the community help improve this project.

### How to Contribute
1.  **Fork** the repository.
2.  Create a new **Branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/amazing-feature
    ```
3.  **Commit** your changes:
    ```bash
    git commit -m "Add some amazing feature"
    ```
4.  **Push** to the branch:
    ```bash
    git push origin feature/amazing-feature
    ```
5.  Open a **Pull Request** on GitHub.

### Guidelines
- Follow PEP 8 style guidelines for Python code.
- Ensure your code runs without errors.
- Update documentation if you change functionality.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Based on the powerful [coursera-dl](https://github.com/coursera-dl/coursera-dl) tool.
- Thanks to all contributors and users for their feedback.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/Jatinprajapati7869">Jatin Prajapati</a>
</p>
