import tkinter as tk
from db.canteen_db import CanteenDatabase
from canteen_management_gui import CanteenManagementGUI
from quick_selection_gui import QuickSelectionGUI


class MainApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("今天吃什么？")
        self.master.geometry("600x450")

        self.quick_selection_gui = QuickSelectionGUI(master,
                                                     self.show_management_gui)
        self.management_gui = CanteenManagementGUI(master,
                                                   self.show_quick_selection_gui)

        self.show_quick_selection_gui()  # 默认显示快速选择界面

    def show_management_gui(self):
        self.quick_selection_gui.hide()
        self.management_gui.show()

    def show_quick_selection_gui(self):
        self.management_gui.hide()
        self.quick_selection_gui.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()