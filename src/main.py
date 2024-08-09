import os
import sys
import tkinter as tk

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.gui.canteen_management_gui import CanteenManagementGUI
from src.gui.quick_selection_gui import QuickSelectionGUI


class MainApplication:
    def __init__(self, master):
        """Initializes the MainApplication class.

        Args:
            master: The parent window object.
        """
        self.master = master
        self.master.title("今天吃什么？")
        self.master.geometry("600x450")

        self.quick_selection_gui = QuickSelectionGUI(master,
                                                     self.show_management_gui)
        self.management_gui = CanteenManagementGUI(
            master, self.show_quick_selection_gui
        )

        self.show_quick_selection_gui()  # 默认显示快速选择界面

    def show_management_gui(self):
        """Switches to the management GUI."""
        self.quick_selection_gui.hide()
        self.management_gui.show()

    def show_quick_selection_gui(self):
        """Switches to the quick selection GUI."""
        self.management_gui.hide()
        self.quick_selection_gui.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()