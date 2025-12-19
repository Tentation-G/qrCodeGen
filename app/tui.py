import pandas as pd

from textual.app import App, ComposeResult
from textual.widgets import Static, DirectoryTree, DataTable, Header, Footer, OptionList
from textual.containers import Container


class FileExplorer(ComposeResult):
    #DEFAULT_CLASSES = "box-item"
    BORDER_TITLE = "File Explorer"
    def compose(self) -> ComposeResult:
        yield DirectoryTree("/")

EXCEL_PATH = "data_samples/ExcelParsingSample.xlsx"
SHEET_NAME = 0  # None/0 pour avoir la premiere, else nom de la feuille

class SheetsTables(Container):
    BORDER_TITLE = "Data Tables"
    def compose(self) -> ComposeResult:
        yield DataTable(id="excel_table")

    def on_mount(self) -> None:
        table = self.query_one("#excel_table", DataTable)

        table.cursor_type = "row"
        table.zebra_stripes = True
        table.clear(columns=True)

        try:
            df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)
            # Colonnes
            table.add_columns(*[str(c) for c in df.columns])
            # Lignes
            for row in df.itertuples(index=False, name=None):
                table.add_row(*[("" if pd.isna(v) else str(v)) for v in row])

        except FileNotFoundError:
            # Fichier introuvable -> table vide + message discret
            table.add_columns("Info")
            table.add_row("Fichier Excel introuvable")

        except ValueError:
            # Feuille introuvable
            table.add_columns("Info")
            table.add_row(f"Feuille '{SHEET_NAME}' introuvable")

        table.focus()

class ThemePanel(Container):
    BORDER_TITLE = "Themes"
    def compose(self) -> ComposeResult:
        yield OptionList(id="theme_list")

class Content(Container):
    BORDER_TITLE = "Content Section"
    DEFAULT_CLASSES = "box-item"
    #def compose(self) -> ComposeResult:


class Main(Container):
    def compose(self) -> ComposeResult:
        with Container(id="sidebar-wrapper"):
            tree = DirectoryTree("/", classes="box-item")
            tree.border_title = "File Explorer"
            yield tree

            file_select = Static("", classes="box-item")
            file_select.border_title = "File Selection"
            yield file_select

        with Container(id="content-wrapper"):
            with Container(id="section1"):
                yield Content()

                yield ThemePanel()

            with Container(id="section2"):
                loading_bar = Static("", id="loading-bar", classes="box-item")
                loading_bar.border_title = "Loading Bar"
                yield loading_bar

                file_picker = Static("", id="File-Picker", classes="box-item")
                file_picker.border_title = "File-Picker"
                yield file_picker


            yield SheetsTables()

class LayoutQrCodeGen(App):
    CSS_PATH = "tui/style.tcss"

    BINDINGS = [
        ("ctrl+q", "quit", "Quitter l'application"),
        ("ctrl+t", "change_theme", "Changer de theme"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Main()
        yield Footer()
    def on_mount(self) -> None:
        self.title = "qrCodeGen"
        self.sub_title = "Alpha 0.1"

if __name__ == "__main__":
    LayoutQrCodeGen().run()


