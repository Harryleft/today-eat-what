from canteen_db import CanteenDataBase
import tkinter as tk
from tkinter import ttk, messagebox


class CanteenGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("今天吃什么？(高校版)")
        self.master.geometry("600x400")
        self.canteen = CanteenDataBase()
        self.create_widgets()

    def create_widgets(self):
        # 创建标签框架
        input_frame = ttk.LabelFrame(self.master, text="输入信息")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # 创建输入字段
        ttk.Label(input_frame, text="食堂名称:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.canteen_name = ttk.Entry(input_frame)
        self.canteen_name.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(input_frame, text="楼层:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.floor_number = ttk.Entry(input_frame)
        self.floor_number.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(input_frame, text="档口(用逗号分隔):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.stalls = ttk.Entry(input_frame, width=40)
        self.stalls.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # 创建按钮
        button_frame = ttk.Frame(self.master)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Button(button_frame, text="添加", command=self.add_canteen).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="查询", command=self.query_canteen).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="更新", command=self.update_canteen).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="删除", command=self.delete_canteen).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(button_frame, text="随机选择", command=self.random_select).grid(row=0, column=4, padx=5, pady=5)

        # 创建结果显示区
        result_frame = ttk.LabelFrame(self.master, text="今天在这儿吃：")
        result_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.result_text = tk.Text(result_frame, height=10, width=70)
        self.result_text.pack(padx=5, pady=5)

        # 配置网格权重
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(2, weight=1)

    def add_canteen(self):
        name = self.canteen_name.get()
        floor = self.floor_number.get()
        stalls = [s.strip() for s in self.stalls.get().split(',')]

        if name and floor and stalls:
            if self.canteen.insert_canteen(name, int(floor), stalls):
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "添加成功")
            else:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "添加失败，可能是重复条目")
        else:
            messagebox.showerror("错误", "请填写所有字段")

    def query_canteen(self):
        name = self.canteen_name.get()
        if name:
            results = self.canteen.select_canteen(name)
            self.result_text.delete(1.0, tk.END)
            for result in results:
                self.result_text.insert(tk.END, f"{result[0]} {result[1]}楼 档口: {result[2]}\n")
        else:
            messagebox.showerror("错误", "请输入食堂名称")

    def update_canteen(self):
        name = self.canteen_name.get()
        floor = self.floor_number.get()
        stalls = [s.strip() for s in self.stalls.get().split(',')]

        if name and floor and stalls:
            self.canteen.update_canteen(name, int(floor), stalls)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "更新成功")
        else:
            messagebox.showerror("错误", "请填写所有字段")

    def delete_canteen(self):
        name = self.canteen_name.get()
        floor = self.floor_number.get()

        if name and floor:
            self.canteen.delete_canteen(name, int(floor))
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "删除成功")
        else:
            messagebox.showerror("错误", "请输入食堂名称和楼层")

    def random_select(self):
        result = self.canteen.random_select_stall()
        if result:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "数据库中没有食堂信息")
