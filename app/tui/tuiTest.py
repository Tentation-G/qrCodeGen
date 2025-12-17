from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Vertical
from textual.containers import Horizontal

class BoxApp(App):
    CSS = """
    Screen {
        padding: 1;
    }

    .box {
        border: round white;
        height: 5;
        margin: 1;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Static("Boîte 1", classes="box")
            yield Static("Boîte 2", classes="box")
            yield Static("Boîte 3", classes="box")

if __name__ == "__main__":
    BoxApp().run()

