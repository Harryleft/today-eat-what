# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from config import DEFAULT_FONT, CANTEEN_NAMES, CANTEEN_FLOORS
from db.canteen_db import CanteenDatabase


class CanteenManagementGUI:
    def __init__(self, master, show_quick_selection_callback):
        self.master = master
        self.frame = ttk.Frame(master, padding="10")
        self.db = CanteenDatabase()
        self.show_quick_selection_callback = show_quick_selection_callback
        self.create_widgets()

    def create_widgets(self):
        # 标题
        ttk.Label(self.frame, text="今天吃什么 | 后台信息管理界面",
                  font=(DEFAULT_FONT, 16, "bold")).grid(row=0, column=0,
                                                       columnspan=2, pady=10,
                                                       sticky="w")

        # 信息显示标签
        self.info_label = ttk.Label(self.frame, text="",
                                    font=("Helvetica", 10))
        self.info_label.grid(row=0, column=2, pady=10, sticky="e")

        # 添加新档口
        ttk.Label(self.frame, text="添加新档口",
                  font=(DEFAULT_FONT, 12, "bold")).grid(row=1, column=0,
                                                       columnspan=2, pady=10,
                                                       sticky="w")

        ttk.Label(self.frame, text="食堂名称:").grid(row=2, column=0,
                                                     sticky="e", padx=5,
                                                     pady=2)
        self.canteen_combobox = ttk.Combobox(self.frame, values=CANTEEN_NAMES,
                                             width=15)
        self.canteen_combobox.grid(row=2, column=1, sticky="w", padx=5, pady=2)


        ttk.Label(self.frame, text="楼层:").grid(row=3, column=0, sticky="e",
                                                 padx=5, pady=2)
        self.floor_combobox = ttk.Combobox(self.frame, values=CANTEEN_FLOORS,
                                             width=15)
        self.floor_combobox.grid(row=3, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(self.frame, text="档口名称:").grid(row=4, column=0,
                                                     sticky="e", padx=5,
                                                     pady=2)
        self.stall_entry = ttk.Entry(self.frame, width=18)
        self.stall_entry.grid(row=4, column=1, sticky="w", padx=5, pady=2)

        ttk.Button(self.frame, text="添加", command=self.add_stall).grid(row=5,
                                                                         column=0,
                                                                         columnspan=2,
                                                                         pady=10)

        # 显示所有档口
        ttk.Label(self.frame, text="所有档口",
                  font=(DEFAULT_FONT, 12, "bold")).grid(row=6, column=0,
                                                       columnspan=2, pady=10,
                                                       sticky="w")

        self.tree = ttk.Treeview(self.frame,
                                 columns=("Canteen", "Floor", "Stall"),
                                 show="headings", selectmode="extended")
        self.tree.heading("Canteen", text="食堂")
        self.tree.heading("Floor", text="楼层")
        self.tree.heading("Stall", text="档口")
        self.tree.grid(row=7, column=0, columnspan=3, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical",
                                  command=self.tree.yview)
        scrollbar.grid(row=7, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.load_stalls()

        # 删除选中的档口
        # 删除选中的档口按钮
        ttk.Button(self.frame, text="删除选中的档口",
                   command=self.delete_selected_stalls).grid(row=8, column=0,
                                                             padx=(0, 5),
                                                             pady=10,
                                                             sticky='e')

        # 返回快速选择界面按钮
        ttk.Button(self.frame, text="返回快速选择",
                   command=self.show_quick_selection_callback).grid(row=8,
                                                                    column=1,
                                                                    padx=(
                                                                    5, 0),
                                                                    pady=10,
                                                                    sticky='w')

        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(7, weight=1)

    def show(self):
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def hide(self):
        self.frame.grid_forget()

    def show_info(self, message, color):
        self.info_label.config(text=message, foreground=color)
        self.frame.after(3000, self.clear_info)  # 3秒后清除消息

    def clear_info(self):
        self.info_label.config(text="")

    def add_stall(self):
        canteen = self.canteen_combobox.get()
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
        self.tree.delete(*self.tree.get_children())
        stalls = self.db.get_all_stalls()
        for stall in stalls:
            self.tree.insert("", "end", values=(
            stall.canteen_name, stall.floor_number, stall.stall_name))

    def clear_entries(self):
        self.canteen_combobox.delete(0, tk.END)
        self.floor_combobox.delete(0, tk.END)
        self.stall_entry.delete(0, tk.END)

    def delete_selected_stalls(self):
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