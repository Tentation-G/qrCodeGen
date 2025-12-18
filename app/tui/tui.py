import textual

from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Container


class QrCodeGen(App):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        yield Static("HEADER", id="header")

        with Container(id="main"):

            with Container(id="sidebar-wrapper"):
                yield Static("SIDEBAR", id="sidebar")
                yield Static("File-Select", id="file-select")

            with Container(id="content-wrapper"):
                yield Static("CONTENT", id="content")
                yield Static("loading-bar", id="loading-bar")
                yield Static("sheets-tables", id="sheets-tables")

        yield Static("FOOTER", id="footer")

app = QrCodeGen()
if __name__ == "__main__":
    app.run()

