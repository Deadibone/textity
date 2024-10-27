import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox, QMenu, QInputDialog
)
from PyQt5.QtGui import QFont


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Textity")
        self.setGeometry(100, 100, 800, 600)

        self.current_file = None

        self.text_area = QTextEdit(self)
        self.setCentralWidget(self.text_area)

        self.menu_bar = self.menuBar()

        self.file_menu = self.menu_bar.addMenu("📁File")
        self.new_action = QAction("🆕New", self)
        self.new_action.triggered.connect(self.new_file)
        self.file_menu.addAction(self.new_action)

        self.open_action = QAction("📖Open", self)
        self.open_action.triggered.connect(self.open_file)
        self.file_menu.addAction(self.open_action)

        self.save_action = QAction("💾Save", self)
        self.save_action.triggered.connect(self.save_file)
        self.file_menu.addAction(self.save_action)

        self.save_as_action = QAction("📥Save As", self)
        self.save_as_action.triggered.connect(self.save_file_as)
        self.file_menu.addAction(self.save_as_action)

        self.file_menu.addSeparator()

        self.quit_action = QAction("🚫Quit", self)
        self.quit_action.triggered.connect(self.quit)
        self.file_menu.addAction(self.quit_action)

        self.edit_menu = self.menu_bar.addMenu("✏️Edit")
        self.undo_action = QAction("↩️Undo", self)
        self.undo_action.triggered.connect(self.text_area.undo)
        self.edit_menu.addAction(self.undo_action)

        self.redo_action = QAction("↪️Redo", self)
        self.redo_action.triggered.connect(self.text_area.redo)
        self.edit_menu.addAction(self.redo_action)

        self.edit_menu.addSeparator()

        self.cut_action = QAction("✂️Cut", self)
        self.cut_action.triggered.connect(self.text_area.cut)
        self.edit_menu.addAction(self.cut_action)

        self.copy_action = QAction("📑Copy", self)
        self.copy_action.triggered.connect(self.text_area.copy)
        self.edit_menu.addAction(self.copy_action)

        self.paste_action = QAction("📋Paste", self)
        self.paste_action.triggered.connect(self.text_area.paste)
        self.edit_menu.addAction(self.paste_action)

        self.edit_menu.addSeparator()

        self.find_action = QAction("🔎Find", self)
        self.find_action.triggered.connect(self.find)
        self.edit_menu.addAction(self.find_action)

        self.format_menu = self.menu_bar.addMenu("🔡Format")
        self.increase_font_action = QAction("➕Increase Font Size", self)
        self.increase_font_action.triggered.connect(self.increase_font_size)
        self.format_menu.addAction(self.increase_font_action)

        self.decrease_font_action = QAction("➖Decrease Font Size", self)
        self.decrease_font_action.triggered.connect(self.decrease_font_size)
        self.format_menu.addAction(self.decrease_font_action)

        self.input_menu = self.menu_bar.addMenu("✍🏻Input")
        self.kaomojis_menu = QMenu("𐙚Kaomojis", self)
        self.input_menu.addMenu(self.kaomojis_menu)

        kaomojis = ["(¬‿¬)", "( ͡° ͜ʖ ͡°)", "(╯°□°）╯︵ ┻━┻", "¯\_(ツ)_/¯", "(づ￣ ³￣)づ", "ಠ_ಠ", "(ง'̀-'́)ง", "ʕ•ᴥ•ʔ", "(⌐■_■)", "( ˶ˆᗜˆ˵ )", "( ｡ •̀ ᴖ •́ ｡)", "⛏", "?"]
        for kaomoji in kaomojis:
            kaomoji_action = QAction(kaomoji, self)
            kaomoji_action.triggered.connect(lambda checked, k=kaomoji: self.insert_kaomoji(k))
            self.kaomojis_menu.addAction(kaomoji_action)

        self.show()

    def new_file(self):
        self.text_area.clear()
        self.current_file = None

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*.*)")
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.setText(file.read())
            self.current_file = file_path

    def save_file(self):
        if self.current_file:
            content = self.text_area.toPlainText()
            with open(self.current_file, "w") as file:
                file.write(content)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*.*)")
        if file_path:
            content = self.text_area.toPlainText()
            with open(file_path, "w") as file:
                file.write(content)
            self.current_file = file_path

    def quit(self):
        reply = QMessageBox.question(self, "Quit", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def increase_font_size(self):
        font = self.text_area.font()
        font_size = font.pointSize()
        font.setPointSize(font_size + 1)
        self.text_area.setFont(font)

    def decrease_font_size(self):
        font = self.text_area.font()
        font_size = font.pointSize()
        font.setPointSize(font_size - 1)
        self.text_area.setFont(font)

    def find(self):
        text_to_find, ok = QInputDialog.getText(self, "Find", "Enter text to find:")
        if ok and text_to_find:
            cursor = self.text_area.textCursor()
            cursor = self.text_area.document().find(text_to_find, cursor)
            if not cursor.isNull():
                self.text_area.setTextCursor(cursor)
                self.text_area.ensureCursorVisible()

    def insert_kaomoji(self, kaomoji):
        self.text_area.insertPlainText(kaomoji)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    sys.exit(app.exec_())