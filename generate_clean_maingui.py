#!/usr/bin/env python
"""
Script to generate a clean maingui.py for Coursera Helper v1.0
Includes all UI fixes: 900x800 window, proper spacing, and layout adjustments.
"""

content = '''__version__ = "1.0"

import sys, requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QRadioButton,
    QComboBox, QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QAction, QGroupBox, QTextBrowser, QProgressBar, QTextEdit
)
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QObject

from utils import process_notification_html
import general
from coursera_dl import main_f

import livedb
from threading import Thread
import webbrowser
from os import path


class DownloadWorker(QObject):
    """Worker thread for running downloads"""
    progress_update = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd
    
    def run(self):
        try:
            from coursera_dl import main_f
            main_f(self.cmd)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    
    # Signals
    show_update_message = pyqtSignal(str, str, str)
    show_notification_signal = pyqtSignal(str)
    download_progress = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coursera Helper v1.0")
        
        # Set fixed size - extra wide and tall to prevent ANY text cutoff or overlap
        self.setFixedSize(900, 800)
        
        # Disable maximize button for cleaner UI
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        
        icon_path = path.abspath(path.join(path.dirname(__file__), 'icon/icon.ico'))
        self.setWindowIcon(QIcon(icon_path))

        self.notification = ""
        self.download_thread = None
        self.download_worker = None
        self.is_downloading = False
        self.sllangschoices = general.LANG_NAME_TO_CODE_MAPPING
        self.allowed_browsers = general.ALLOWED_BROWSERS

        from localdb import SimpleDB
        self.localdb  = SimpleDB('data.bin')
        self.argdict = self.localdb.get_full_db()['argdict']
        
        # Apply modern dark theme
        self.apply_dark_theme()
        
        self.initUI()

        # signals
        self.show_update_message.connect(self.display_update_message)
        self.show_notification_signal.connect(self.show_notification)

        # PRIVACY: Remote database connection disabled - no tracking/telemetry
        # Thread(target=self.connect_to_db, daemon=True).start()
        
        # Show disclaimer on first startup
        self.show_startup_disclaimer()
        
        # Force resize to ensure dimensions are applied
        self.resize(900, 800)

    def apply_dark_theme(self):
        """Apply glassmorphism dark theme"""
        QApplication.setStyle('Fusion')
        stylesheet = """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
            }
            QWidget {
                background-color: transparent;
                color: #e0e0e0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 13px;
                background: transparent;
            }
            QLineEdit {
                padding: 12px;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                background: rgba(45, 45, 45, 0.6);
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(33, 150, 243, 0.8);
                background: rgba(45, 45, 45, 0.8);
            }
            QComboBox {
                padding: 10px;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                background: rgba(45, 45, 45, 0.6);
                color: #ffffff;
                font-size: 13px;
            }
            QPushButton {
                padding: 14px 28px;
                border-radius: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2196F3, stop:1 #21CBF3);
                color: white;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1976D2, stop:1 #1CB5E0);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0D47A1, stop:1 #0D7EA1);
            }
            QPushButton:disabled {
                background: rgba(100, 100, 100, 0.4);
                color: rgba(255, 255, 255, 0.4);
            }
            QPushButton#selectFolderBtn {
                background: rgba(66, 66, 66, 0.6);
                padding: 10px 20px;
            }
            QPushButton#selectFolderBtn:hover {
                background: rgba(97, 97, 97, 0.7);
            }
            QPushButton#cancelBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f44336, stop:1 #e91e63);
            }
            QPushButton#cancelBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #d32f2f, stop:1 #c2185b);
            }
            QRadioButton {
                color: #e0e0e0;
                spacing: 10px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                background: rgba(45, 45, 45, 0.6);
            }
            QRadioButton::indicator:checked {
                border: 2px solid #2196F3;
                border-radius: 10px;
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
                    fx:0.5, fy:0.5, stop:0 #2196F3, stop:1 #1976D2);
            }
            QGroupBox {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                margin-top: 14px;
                padding-top: 20px;
                padding-bottom: 15px;
                background: rgba(45, 45, 45, 0.4);
                font-weight: bold;
                color: #2196F3;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }
            QProgressBar {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                text-align: center;
                background: rgba(30, 30, 30, 0.6);
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2196F3, stop:1 #21CBF3);
                border-radius: 7px;
            }
            QTextEdit, QTextBrowser {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                background: rgba(30, 30, 30, 0.6);
                color: #e0e0e0;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
            }
            QMenuBar {
                background: rgba(45, 45, 45, 0.8);
                color: #e0e0e0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            QMenuBar::item:selected {
                background: rgba(33, 150, 243, 0.7);
            }
            QMenu {
                background: rgba(45, 45, 45, 0.95);
                color: #e0e0e0;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QMenu::item:selected {
                background: rgba(33, 150, 243, 0.7);
            }
        """
        self.setStyleSheet(stylesheet)

    def initUI(self):
        # Menu
        menubar = self.menuBar()
        menu = menubar.addMenu("Menu")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)
        menu.addAction(about_action)
        menu.addAction(help_action)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)
        
        # Optimized spacing for 900x800 window
        layout.setSpacing(15)
        layout.setContentsMargins(25, 20, 25, 20)

        # Header
        title = QLabel("Coursera Helper")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2196F3; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        info = QLabel("Log in to coursera.org in your browser before downloading courses.")
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: #aaa; font-size: 12px; padding-bottom: 10px;")
        layout.addWidget(info)

        # Course Info
        course_group = QGroupBox("Course Information")
        course_layout = QVBoxLayout()
        course_group.setLayout(course_layout)
        
        url_label = QLabel("Course URL:")
        self.classname_edit = QLineEdit(self.localdb.read('argdict')['classname'])
        self.classname_edit.setPlaceholderText("https://www.coursera.org/learn/course-name")
        course_layout.addWidget(url_label)
        course_layout.addWidget(self.classname_edit)
        
        browser_label = QLabel("Browser (where you're logged in):")
        self.browser_combo = QComboBox()
        self.browser_combo.addItems(self.allowed_browsers)
        default_browser = self.localdb.read('browser')
        if default_browser in self.allowed_browsers:
            self.browser_combo.setCurrentText(default_browser)
        course_layout.addWidget(browser_label)
        course_layout.addWidget(self.browser_combo)
        
        layout.addWidget(course_group)

        # Settings
        settings_group = QGroupBox("Download Settings")
        settings_layout = QVBoxLayout()
        settings_group.setLayout(settings_layout)
        
        folder_label = QLabel("Download Folder:")
        self.path_btn = QPushButton("Select Folder")
        self.path_btn.setObjectName("selectFolderBtn")
        self.path_btn.setMinimumHeight(45)  # Ensure button has height
        self.path_btn.clicked.connect(self.getPath)
        
        self.path_label = QLabel(self.localdb.read('argdict')['path'] or "No folder selected")
        self.path_label.setStyleSheet("color: #aaa; font-size: 11px; padding: 8px 0;")
        self.path_label.setWordWrap(True)
        self.path_label.setMinimumHeight(20) # Min height to prevent squashing but not too tall
        
        settings_layout.addWidget(folder_label)
        settings_layout.addWidget(self.path_btn)
        settings_layout.addSpacing(5) # Add spacing between button and label
        settings_layout.addWidget(self.path_label)
        
        res_label = QLabel("Video Quality:")
        res_buttons = QHBoxLayout()
        self.res_720 = QRadioButton("HD (720p)")
        self.res_540 = QRadioButton("SD (540p)")
        self.res_360 = QRadioButton("Low (360p)")
        res_buttons.addWidget(self.res_720)
        res_buttons.addWidget(self.res_540)
        res_buttons.addWidget(self.res_360)
        res_buttons.addStretch()
        
        if self.localdb.read('argdict')['video_resolution'] == '540p':
            self.res_540.setChecked(True)
        elif self.localdb.read('argdict')['video_resolution'] == '360p':
            self.res_360.setChecked(True)
        else:
            self.res_720.setChecked(True)
        
        settings_layout.addWidget(res_label)
        settings_layout.addLayout(res_buttons)
        
        subtitle_label = QLabel("Subtitle Language:")
        self.sl_combo = QComboBox()
        self.sl_combo.addItems(sorted(self.sllangschoices.keys()))
        key = next((k for k, v in self.sllangschoices.items() if v == self.localdb.read('argdict')['sl']), None)
        self.sl_combo.setCurrentText(key if key else 'English')
        settings_layout.addWidget(subtitle_label)
        settings_layout.addWidget(self.sl_combo)
        
        layout.addWidget(settings_group)

        # Notification area
        self.notification_area = QTextBrowser()
        self.notification_area.setMaximumHeight(80)
        self.notification_area.setVisible(False)
        layout.addWidget(self.notification_area)

        # Progress Panel
        self.progress_panel = QGroupBox("Download Progress")
        self.progress_panel.setVisible(False)
        progress_layout = QVBoxLayout()
        self.progress_panel.setLayout(progress_layout)
        
        self.current_course_label = QLabel("Preparing download...")
        self.current_course_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2196F3;")
        progress_layout.addWidget(self.current_course_label)
        
        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet("color: #aaa; font-size: 12px;")
        progress_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMinimumHeight(8)
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_log = QTextEdit()
        self.progress_log.setReadOnly(True)
        self.progress_log.setMaximumHeight(150)
        progress_layout.addWidget(self.progress_log)
        
        layout.addWidget(self.progress_panel)

        layout.addStretch(1)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        
        self.download_btn = QPushButton("Start Download")
        self.download_btn.setMinimumSize(200, 50)
        self.download_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.download_btn.clicked.connect(self.downloadBtnHandler)
        button_layout.addWidget(self.download_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.setMinimumSize(120, 50)
        self.cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancel_btn.clicked.connect(self.cancelDownload)
        self.cancel_btn.setVisible(False)
        button_layout.addWidget(self.cancel_btn)
        
        button_layout.addStretch(1)
        layout.addLayout(button_layout)

        # Footer
        self.footer_label = QLabel('<a href="https://coursera-downloader.rf.gd/" style="color:#2196F3;">coursera-downloader.rf.gd</a>')
        self.footer_label.setOpenExternalLinks(True)
        self.footer_label.setAlignment(Qt.AlignCenter)
        self.footer_label.setStyleSheet("padding: 10px; font-size: 11px;")
        layout.addWidget(self.footer_label)

    def connect_to_db(self):
        pass

    def display_update_message(self, latest_version, latest_version_build_url=None, update_msg=None):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Update Available")
        msg_box.setText(f"A new version ({latest_version}) is available.")
        msg_box.exec_()

    def show_notification(self, notification):
        self.notification = notification
        if not notification:
            self.notification_area.hide()
        else:
            processed = process_notification_html(notification)
            self.notification_area.setHtml(processed)
            self.notification_area.setVisible(True)

    def show_about(self):
        from gui_components.about_text import get_about_text
        dlg = QMessageBox(self)
        dlg.setWindowTitle("About - Coursera Helper v1.0")
        dlg.setTextFormat(Qt.RichText)
        dlg.setText(get_about_text(__version__))
        dlg.exec_()

    def show_help(self):
        from gui_components.help_text import get_help_text
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Help - Coursera Helper v1.0")
        dlg.setTextFormat(Qt.RichText)
        dlg.setText(get_help_text())
        dlg.exec_()

    def show_startup_disclaimer(self):
        disclaimer = QMessageBox(self)
        disclaimer.setWindowTitle("Important Notice - Responsible Use")
        disclaimer.setIcon(QMessageBox.Warning)
        
        disclaimer_text = """<html><body>
        <h3 style='color: #2196F3;'>Coursera Helper - Responsible Use Policy</h3>
        <p><b>IMPORTANT DISCLAIMER</b></p>
        <p>This tool is for <b>personal learning purposes only</b>.</p>
        <ul>
        <li>We respect Coursera's Terms & Conditions</li>
        <li>Use Coursera's default download options when available</li>
        <li>Bulk downloading may lead to account suspension</li>
        <li>Please respect creator's hard work</li>
        </ul>
        <p style='font-style: italic; color: #f44336; font-weight: bold;'>
        "With great power comes great responsibility." - Uncle Ben
        </p>
        <p><b>DO NOT:</b></p>
        <ul>
        <li>Share downloaded content publicly</li>
        <li>Redistribute materials to others</li>
        <li>Use for commercial purposes</li>
        <li>Violate copyright laws</li>
        </ul>
        <p><b>DO:</b></p>
        <ul>
        <li>Download for personal study only</li>
        <li>Take breaks between downloads</li>
        <li>Support creators by enrolling legitimately</li>
        </ul>
        <p style='color: #888; font-size: 11px;'>
        <i>The developer is not responsible for misuse.<br>
        By clicking 'I Understand', you agree to use this tool responsibly.</i>
        </p>
        </body></html>"""
        
        disclaimer.setText(disclaimer_text)
        disclaimer.setTextFormat(Qt.RichText)
        
        understand_btn = disclaimer.addButton("I Understand & Agree", QMessageBox.AcceptRole)
        cancel_btn = disclaimer.addButton("Exit", QMessageBox.RejectRole)
        
        disclaimer.exec_()
        
        if disclaimer.clickedButton() == cancel_btn:
            sys.exit(0)
    
    def show_completion_disclaimer(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Download Complete")
        dlg.setIcon(QMessageBox.Information)
        
        complete_text = """<html><body>
        <h3 style='color: #4CAF50;'>Download Complete!</h3>
        <p><b>Final Reminder:</b></p>
        <p>Materials are for <b>your personal learning only</b>.</p>
        <ul>
        <li><b>DO NOT</b> share these files</li>
        <li><b>DO NOT</b> upload to file-sharing platforms</li>
        <li><b>DO NOT</b> redistribute</li>
        <li><b>DO</b> use for your own education</li>
        </ul>
        <p style='color: #f44336; font-weight: bold;'>
        Respect creators. Support education. Learn responsibly.
        </p>
        <p style='color: #888;'><i>Thank you for using Coursera Helper ethically!</i></p>
        </body></html>"""
        
        dlg.setText(complete_text)
        dlg.setTextFormat(Qt.RichText)
        dlg.exec_()

    def downloadBtnHandler(self):
        browser = self.browser_combo.currentText()
        cauth = general.loadcauth('coursera.org', browser)
        if not cauth:
            QMessageBox.warning(self, "Error", "Could not load authentication.\\nRun as administrator and ensure you're logged in.")
            return
        
        self.localdb.update('argdict.ca', cauth)
        self.localdb.update('browser', browser)
        self.localdb.update('argdict.classname', self.classname_edit.text())
        self.localdb.update('argdict.path', self.path_label.text())
        
        if self.res_720.isChecked():
            self.localdb.update('argdict.video_resolution', '720p')
        elif self.res_540.isChecked():
            self.localdb.update('argdict.video_resolution', '540p')
        else:
            self.localdb.update('argdict.video_resolution', '360p')
        
        self.localdb.update('argdict.sl', self.sl_combo.currentText())

        if not self.localdb.read('argdict')['path']:
            QMessageBox.warning(self, "Error", "Please select a download folder")
            return

        self.argdict = {}
        for key, value in self.localdb.get_full_db()['argdict'].items():
            if key == 'classname':
                courseurl = self.localdb.read('argdict')['classname']
                cname = general.urltoclassname(courseurl)
                if not cname:
                    QMessageBox.warning(self, "Error", "Invalid course URL")
                    return
                self.argdict[key] = cname
            elif key == 'sl':
                langcode = self.sllangschoices[self.localdb.read('argdict')['sl']]
                if not langcode:
                    self.argdict['ignore-formats'] = "srt"
                    self.argdict[key] = 'en'
                else:
                    self.argdict[key] = langcode
            else:
                self.argdict[key] = value

        self.localdb.update('argdict', self.argdict)

        cmd = []
        self.argdict = general.move_to_first(self.argdict, 'ca')
        for item in self.argdict.items():
            if item[0] in ('video_resolution', 'path'):
                flag = '--' + item[0]
            else:
                flag = '-' + item[0]
            flag = flag.replace('_', '-')
            if 'classname' not in flag:
                cmd.append(flag)
            cmd.append(item[1])

        cmd.extend(['--download-quizzes', '--download-notebooks', 
                    '--disable-url-skipping', '--unrestricted-filenames',
                    '--combined-section-lectures-nums', '--jobs', '1'])

        try:
            main_f(cmd)
            self.show_completion_disclaimer()
        except KeyboardInterrupt:
            QMessageBox.information(self, "Stopped", "Download stopped")
        except requests.exceptions.ConnectionError:
            QMessageBox.warning(self, "Error", "Connection error. Check your internet.")
        except requests.exceptions.HTTPError as e:
            QMessageBox.warning(self, "Error", f"HTTP Error: {e}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error: {e}")

    def cancelDownload(self):
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.terminate()
            self.download_thread.wait()
        
        self.is_downloading = False
        self.progress_panel.setVisible(False)
        self.download_btn.setEnabled(True)
        self.cancel_btn.setVisible(False)
        QMessageBox.information(self, "Cancelled", "Download cancelled")

    def getPath(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Download Folder", "")
        self.path_label.setText(dir)


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
'''

# Write the clean file
with open('maingui.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Clean maingui.py generated successfully!")
