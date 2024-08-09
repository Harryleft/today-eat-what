# -*- coding: utf-8 -*-
import json
import tkinter as tk
from tkinter import ttk, filedialog

from src.config.config import DEFAULT_FONT, CANTEEN_NAMES, CANTEEN_FLOORS
from src.db.canteen_db import CanteenDatabase


class CanteenManagementGUI:
    def __init__(self, master, show_quick_selection_callback):
        """Initializes the CanteenManagementGUI class.

        Args:
            master: The parent window object.
            show_quick_selection_callback: Callback function to switch to the quick selection interface.
        """
        self.master = master
        self.frame = ttk.Frame(master, padding="10")
        self.db = CanteenDatabase()
        self.show_quick_selection_callback = show_quick_selection_callback
        self.create_widgets()

    def create_widgets(self):
        """Creates the GUI components."""
        # 标题
        ttk.Label(self.frame, text="今天吃什么 | 后台信息管理界面",
                  font=(DEFAULT_FONT, 16, "bold")).grid(row=0, column=0,
                                                        columnspan=4, pady=10,
                                                        sticky="w")

        # 信息显示标签
        self.info_label = ttk.Label(self.frame, text="",
                                    font=("Helvetica", 10))
        self.info_label.grid(row=0, column=3, pady=10, sticky="e")

        # 添加新档口
        ttk.Label(self.frame, text="添加新内容",
                  font=(DEFAULT_FONT, 12, "bold")).grid(row=1, column=0,
                                                        columnspan=4, pady=10,
                                                        sticky="w")

        ttk.Label(self.frame, text="食堂名称:").grid(row=2, column=0,
                                                     sticky="e", padx=5,
                                                     pady=2)
        self.canteen_combobox = ttk.Combobox(self.frame, values=CANTEEN_NAMES,
                                             width=15)
        self.canteen_combobox.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        self.canteen_combobox.bind("<<ComboboxSelected>>",
                                   self.toggle_floor_input)

        ttk.Label(self.frame, text="楼层:").grid(row=2, column=2, sticky="e",
                                                 padx=5, pady=2)
        self.floor_combobox = ttk.Combobox(self.frame, values=CANTEEN_FLOORS,
                                           width=15)
        self.floor_combobox.grid(row=2, column=3, sticky="w", padx=5, pady=2)

        ttk.Label(self.frame, text="菜品:").grid(row=3, column=0,
                                                 sticky="e", padx=5, pady=2)
        self.stall_entry = ttk.Entry(self.frame, width=18)
        self.stall_entry.grid(row=3, column=1, sticky="w", padx=5, pady=2)

        ttk.Button(self.frame, text="添加", command=self.add_stall).grid(row=3,
                                                                         column=2,
                                                                         columnspan=2,
                                                                         pady=2,
                                                                         padx=5,
                                                                         sticky="e")

        # 显示所有档口
        ttk.Label(self.frame, text="所有信息",
                  font=(DEFAULT_FONT, 12, "bold")).grid(row=4, column=0,
                                                        columnspan=4, pady=10,
                                                        sticky="w")

        self.tree = ttk.Treeview(self.frame,
                                 columns=("Canteen", "Floor", "Stall"),
                                 show="headings", selectmode="extended")
        self.tree.heading("Canteen", text="食堂")
        self.tree.heading("Floor", text="楼层")
        self.tree.heading("Stall", text="菜品")
        self.tree.grid(row=5, column=0, columnspan=4, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical",
                                  command=self.tree.yview)
        scrollbar.grid(row=5, column=4, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.load_stalls()

        # 删除选中的档口
        ttk.Button(self.frame, text="删除选中的信息",
                   command=self.delete_selected_stalls).grid(row=6, column=0,
                                                             padx=(0, 5),
                                                             pady=10,
                                                             sticky='e')

        # 返回快速选择界面按钮
        ttk.Button(self.frame, text="返回首页",
                   command=self.show_quick_selection_callback).grid(row=6,
                                                                    column=1,
                                                                    padx=(
                                                                        5, 0),
                                                                    pady=10,
                                                                    sticky='w')
        # 添加导出按钮
        ttk.Button(self.frame, text="导出为JSON",
                   command=self.export_to_json).grid(row=6, column=2,
                                                     padx=(5, 0), pady=10,
                                                     sticky='w')
        # 添加导入按钮
        ttk.Button(self.frame, text="导入JSON",
                   command=self.import_from_json).grid(row=6, column=3,
                                                       padx=(5, 0), pady=10,
                                                       sticky='w')
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(5, weight=1)

    def export_to_json(self):
        """Exports the canteen data to a JSON file."""
        stalls = self.db.get_all_stalls()
        data = {
            "canteens": []
        }
        for stall in stalls:
            canteen = next((c for c in data["canteens"] if
                            c["name"] == stall.canteen_name), None)
            if not canteen:
                canteen = {
                    "name": stall.canteen_name,
                    "floors": []
                }
                data["canteens"].append(canteen)
            floor = next((f for f in canteen["floors"] if
                          f["number"] == stall.floor_number), None)
            if not floor:
                floor = {
                    "number": stall.floor_number,
                    "stalls": []
                }
                canteen["floors"].append(floor)
            floor["stalls"].append(stall.stall_name)

        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 initialfile="canteens_dataset.json",
                                                 filetypes=[
                                                     ("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.show_info("导出成功", "green")
        else:
            self.show_info("导出取消", "red")

    def import_from_json(self):
        """Imports the canteen data from a JSON file."""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for canteen in data.get("canteens", []):
                    for floor in canteen.get("floors", []):
                        for stall in floor.get("stalls", []):
                            # Check if the stall already exists
                            if self.db.stall_exists(canteen["name"],
                                                    floor["number"],
                                                    stall):
                                self.show_info(f"已跳过重复项", "red")
                            else:
                                self.db.add_stall(canteen["name"],
                                                  floor["number"], stall)
                                self.load_stalls()
                                self.show_info("导入成功", "green")
            except Exception as e:
                self.show_info(f"导入失败: {str(e)}", "red")
        else:
            self.show_info("导入取消", "red")

    def toggle_floor_input(self, event):
        """Toggles the floor input based on the selected canteen.

        Args:
            event: The event object.
        """
        selected_canteen = self.canteen_combobox.get()
        if selected_canteen == "龙祥街":
            self.floor_combobox.grid_remove()
        else:
            self.floor_combobox.grid()

    def show(self):
        """Displays the interface."""
        self.frame.pack(fill="both", expand=True)
        self.master.pack_propagate(False)

    def hide(self):
        """Hides the interface."""
        self.frame.pack_forget()

    def show_info(self, message, color):
        """Displays an information message.

        Args:
            message: The message to display.
            color: The color of the message text.
        """
        self.info_label.config(text=message, foreground=color)
        self.frame.after(3000, self.clear_info)  # 3秒后清除消息

    def clear_info(self):
        """Clears the information message."""
        self.info_label.config(text="")

    def add_stall(self):
        """Adds a new stall to the database."""
        canteen = self.canteen_combobox.get()
        if canteen == "龙祥街":
            floor = "0"
        else:
            floor = self.floor_combobox.get()
        stall = self.stall_entry.get()

        if not canteen or not floor or not stall:
            self.show_info("请填写所有字段", "red")
            return

        try:
            floor = int(floor)
        except ValueError:
            self.show_info("楼层必须是一个数字", "red")
            return

        try:
            self.db.add_stall(canteen, floor, stall)
            self.load_stalls()
            self.clear_entries()
            self.show_info("新档口已添加", "green")
        except Exception as e:
            self.show_info(f"添加失败: {str(e)}", "red")

    def load_stalls(self):
        """Loads all stalls from the database and displays them in the treeview."""
        self.tree.delete(*self.tree.get_children())
        stalls = self.db.get_all_stalls()
        for stall in stalls:
            self.tree.insert("", "end", values=(
                stall.canteen_name, stall.floor_number, stall.stall_name))

    def clear_entries(self):
        """Clears the input fields."""
        self.canteen_combobox.delete(0, tk.END)
        self.floor_combobox.delete(0, tk.END)
        self.stall_entry.delete(0, tk.END)

    def delete_selected_stalls(self):
        """Deletes the selected stalls from the database."""
        selected_items = self.tree.selection()
        if not selected_items:
            self.show_info("请先选择至少一个档口", "red")
            return

        deleted_count = 0
        for item in selected_items:
            values = self.tree.item(item)['values']
            try:
                self.db.delete_stall(values[0], values[1], values[2])
                deleted_count += 1
            except Exception as e:
                self.show_info(f"删除失败: {str(e)}", "red")
                return

        self.load_stalls()
        self.show_info(f"成功删除 {deleted_count} 个档口", "green")
