from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit, QLabel, QMessageBox
)
import sys
from youtube_caption import fetch_captions
from gpt_summarizer import summarize

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("야옹준호의 YouTube 자막 요약기 v1.0")
        self.resize(600, 800)

        # 레이아웃 설정
        main_layout = QVBoxLayout(self)

        # 1) URL 입력 부분
        input_layout = QHBoxLayout()
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("유튜브 영상 URL을 입력하세요")
        self.go_btn = QPushButton("요약 실행")
        self.go_btn.clicked.connect(self.on_summarize)
        input_layout.addWidget(self.url_edit)
        input_layout.addWidget(self.go_btn)
        main_layout.addLayout(input_layout)

        # 2) 요약 결과 표시 부분
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)         # 읽기 전용이지만, 드래그·복사 가능
        main_layout.addWidget(self.result_edit)

    def on_summarize(self):
        url = self.url_edit.text().strip()
        if not url:
            QMessageBox.warning(self, "경고", "URL을 입력해주세요.")
            return

        # 버튼 이중 클릭 방지 및 UI 갱신
        self.go_btn.setEnabled(False)
        QApplication.processEvents()

        # 1) 자막 추출
        subs = fetch_captions(url)
        if not subs:
            self.result_edit.setPlainText("자막을 찾을 수 없습니다.")
        else:
            # 2) GPT 요약
            summary = summarize(subs)
            # 3) 결과 출력 (드래그 복사 가능)
            self.result_edit.setPlainText(summary)

        self.go_btn.setEnabled(True)