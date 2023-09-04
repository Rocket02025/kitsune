import sys
import re
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLineEdit, QToolBar, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GPTbrowsingservice")

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)
        self.setCentralWidget(self.tab_widget)

        self.tabs = []  # List to store references to QWebEngineView objects

        self.create_toolbar()
        self.create_actions()

        self.create_new_tab("https://www.google.com", "Google")  # Load Google homepage on startup

    def create_toolbar(self):
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.back_action = QAction(QIcon("back.png"), "", self)
        self.back_action.triggered.connect(self.navigate_back)
        self.toolbar.addAction(self.back_action)

        self.forward_action = QAction(QIcon("forward.png"), "", self)
        self.forward_action.triggered.connect(self.navigate_forward)
        self.toolbar.addAction(self.forward_action)

        self.reload_action = QAction(QIcon("reload.png"), "", self)
        self.reload_action.triggered.connect(self.reload_page)
        self.toolbar.addAction(self.reload_action)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Type what you want to search for in the URL bar and press Enter.")
        self.url_input.returnPressed.connect(self.load_url)
        self.toolbar.addWidget(self.url_input)

        self.new_tab_action = QAction(QIcon("new_tab.png"), "", self)
        self.new_tab_action.triggered.connect(self.create_new_tab)
        self.toolbar.addAction(self.new_tab_action)

        self.fullscreen_action = QAction(QIcon("fullscreen.png"), "", self)
        self.fullscreen_action.triggered.connect(self.toggle_fullscreen)
        self.toolbar.addAction(self.fullscreen_action)

    def create_actions(self):
        self.quit_action = QAction("Quit", self)
        self.quit_action.triggered.connect(self.quit_application)
        self.addAction(self.quit_action)

    def create_new_tab(self, url=None, title="New Tab"):
        web_view = QWebEngineView()
        web_view.urlChanged.connect(self.update_url_input)
        web_view.titleChanged.connect(lambda title: self.update_tab_title(web_view))

        self.tabs.append(web_view)  # Store reference to the QWebEngineView object

        tab_index = self.tab_widget.addTab(web_view, title)
        self.tab_widget.setCurrentIndex(tab_index)

        if url:
            web_view.load(QUrl(url))

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            web_view = self.tabs[index]  # Get the reference to the QWebEngineView object
            web_view.titleChanged.disconnect()  # Disconnect the titleChanged signal
            web_view.deleteLater()  # Explicitly delete the QWebEngineView object
            self.tabs.pop(index)  # Remove the reference from the list
            self.tab_widget.removeTab(index)

    def tab_changed(self, index):
        web_view = self.tabs[index]  # Get the reference to the QWebEngineView object
        self.update_url_input(web_view.url())

        title = web_view.title() or "New Tab"
        self.setWindowTitle(title)

    def navigate_back(self):
        web_view = self.tabs[self.tab_widget.currentIndex()]  # Get the reference to the current QWebEngineView object
        web_view.back()

    def navigate_forward(self):
        web_view = self.tabs[self.tab_widget.currentIndex()]  # Get the reference to the current QWebEngineView object
        web_view.forward()

    def reload_page(self):
        web_view = self.tabs[self.tab_widget.currentIndex()]  # Get the reference to the current QWebEngineView object
        web_view.reload()

    def load_url(self):
        url = self.url_input.text()
        if self.is_valid_url(url):
            if not url.startswith("http"):
                url = "http://" + url
            web_view = self.tabs[self.tab_widget.currentIndex()]  # Get the reference to the current QWebEngineView object
            web_view.load(QUrl(url))
        else:
            search_query = "https://www.google.com/search?q=" + url.replace(" ", "+")  # Replace spaces with '+'
            web_view = self.tabs[self.tab_widget.currentIndex()]  # Get the reference to the current QWebEngineView object
            web_view.load(QUrl(search_query))

    def is_valid_url(self, url):
        pattern = r"^(https?://)?[\w.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, url)

    def quit_application(self):
        QApplication.quit()

    def update_url_input(self, url):
        self.url_input.setText(url.toString())

    def update_tab_title(self, web_view):
        index = self.tabs.index(web_view)
        title = web_view.title() or "New Tab"
        self.tab_widget.setTabText(index, title)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = BrowserWindow()
    window.show()

    sys.exit(app.exec_())
