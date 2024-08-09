# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from src.config.config import CANTEEN_NAMES
from src.db.canteen_db import CanteenDatabase


class QuickSelectionGUI:
    def __init__(self, master, show_management_callback):
        self.master = master
        self.frame = ttk.Frame(master)
        self.canteen_db = CanteenDatabase()
        self.show_management_callback = show_management_callback
        self.create_widgets()

    def create_widgets(self):
        # 创建随机选择按钮
        random_frame = ttk.LabelFrame(self.frame, text="随机选择")
        random_frame.pack(padx=10, pady=10, fill="x")

        ttk.Button(random_frame, text="随机选择食堂", command=self.random_select_all).pack(pady=5, expand=True, fill="x")

        # 创建食堂选择按钮
        canteen_frame = ttk.LabelFrame(self.frame, text="指定食堂随机选择")
        canteen_frame.pack(padx=10, pady=10, fill="x")

        for canteen in CANTEEN_NAMES:
            ttk.Button(canteen_frame, text=canteen, command=lambda c=canteen: self.random_select_from_canteen(c)).pack(pady=2, expand=True, fill="x")

        # 创建结果显示区
        result_frame = ttk.LabelFrame(self.frame, text="今天在这儿吃：")
        result_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.result_text = tk.Text(result_frame, height=5, width=50)
        self.result_text.pack(padx=5, pady=5, fill="both", expand=True)

        # 添加进入管理界面的按钮
        ttk.Button(self.frame, text="进入后台管理界面", command=self.show_management_callback).pack(pady=10)

        self.add_copyright_label()

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()

    def random_select_all(self):
        """从所有食堂中随机选择一个档口"""
        result = self.canteen_db.random_select_all()
        if result:
            self.display_result(result)
            canteen, floor, stall = result.split()
            if canteen == "龙祥街":
                self.display_result(f"{canteen} {stall}")
            else:
                self.display_result(f"{canteen} {floor} {stall}")

    def random_select_from_canteen(self, canteen_name):
        result = self.canteen_db.random_select_from_canteen(canteen_name)
        if "请到后台管理界面添加相关信息" in result or "选择时发生错误" in result:
            self.display_result(result)
        else:
            canteen, floor, stall = result.split()
            if canteen == "龙祥街":
                self.display_result(f"{canteen} {stall}")
            else:
                self.display_result(f"{canteen} {floor}楼 {stall}")

    def display_result(self, result):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

    def add_copyright_label(self):
        copyright_label = tk.Label(self.master, text="© Dongchao Shen",
                                   font=("Times New Roman", 10))
        copyright_label.pack(side="bottom", pady=5)