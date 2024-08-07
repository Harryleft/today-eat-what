from canteen_db import CanteenDataBase
import tkinter as tk
from tkinter import ttk, messagebox
import re

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

        # 创建快捷按钮框架
        shortcut_frame = ttk.LabelFrame(self.master, text="快捷选择")
        shortcut_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # 添加快捷按钮
        ttk.Button(shortcut_frame, text="嘉园",
                   command=lambda: self.fill_canteen_info("嘉园", 1,
                                                          "面食部,炒菜部,水果店")).grid(
            row=0, column=0, padx=5, pady=5)
        ttk.Button(shortcut_frame, text="乾园",
                   command=lambda: self.fill_canteen_info("乾园", 1,
                                                          "自选餐")).grid(
            row=0, column=1, padx=5, pady=5)
        ttk.Button(shortcut_frame, text="菁园",
                   command=lambda: self.fill_canteen_info("菁园", 1,
                                                          "中式快餐,西式快餐,沙拉吧")).grid(
            row=0, column=2, padx=5, pady=5)

        # 创建操作按钮
        button_frame = ttk.Frame(self.master)
        button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Button(button_frame, text="添加", command=self.add_canteen).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="查询", command=self.query_canteen).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="更新", command=self.update_canteen).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="删除", command=self.delete_canteen).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(button_frame, text="随机选择", command=self.random_select).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(button_frame, text="清除输入", command=self.clear_inputs).grid(row=0, column=5, padx=5, pady=5)

        # 创建结果显示区
        result_frame = ttk.LabelFrame(self.master, text="今天在这儿吃：")
        result_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.result_text = tk.Text(result_frame, height=10, width=70)
        self.result_text.pack(padx=5, pady=5)

        # 配置网格权重
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(2, weight=1)

    def fill_canteen_info(self, name, floor, stalls):
        self.canteen_name.delete(0, tk.END)
        self.canteen_name.insert(0, name)
        self.floor_number.delete(0, tk.END)
        self.floor_number.insert(0, str(floor))
        self.stalls.delete(0, tk.END)
        self.stalls.insert(0, stalls)

    def validate_inputs(self):
        name = self.canteen_name.get().strip()
        floor = self.floor_number.get().strip()
        stalls = [s.strip() for s in self.stalls.get().split(",") if s.strip()]

        if not name or len(name) > 4 or not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9\s]+$', name):
            messagebox.showerror("错误", "请输入有效的食堂名称（例如嘉园、乾园、菁园）")
            return None, None, None

        if not floor or not floor.isdigit() or int(floor) < 1 or int(floor) > 5:
            messagebox.showerror("错误", "请输入有效的楼层数（1-5之间的整数）")
            return None, None, None

        if not stalls:
            messagebox.showerror("错误", "请输入至少一个档口")
            return None, None, None

        for stall in stalls:
            if len(stall) > 30 or not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9\s]+$', stall):
                messagebox.showerror("错误", f"无效的档口名称：{stall}（限30个字符，只允许中文、英文、数字和空格）")
                return None, None, None

        return name, int(floor), stalls

    def add_canteen(self):
        name, floor, stalls = self.validate_inputs()
        if name is None:
            return

        try:
            if self.canteen.insert_canteen(name, floor, stalls):
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "添加成功")
            else:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "添加失败，可能是重复条目")
        except Exception as e:
            messagebox.showerror("错误", f"添加食堂信息时发生错误：{str(e)}")

    def query_canteen(self):
        name = self.canteen_name.get().strip()
        floor = self.floor_number.get().strip()
        stall = self.stalls.get().strip()

        floor_number = None
        if floor:
            try:
                floor_number = int(floor)
                if floor_number < 1 or floor_number > 5:
                    raise ValueError("楼层数必须在1-5之间")
            except ValueError as e:
                messagebox.showerror("错误", f"无效的楼层数：{str(e)}")
                return

        try:
            results = self.canteen.select_canteen(name, floor_number, stall)
            self.result_text.delete(1.0, tk.END)
            if results:
                for result in results:
                    canteen_name, floor_number, stalls = result
                    stalls_str = ", ".join(stalls)
                    self.result_text.insert(tk.END, f"{canteen_name} {floor_number}楼 档口: {stalls_str}\n")
            else:
                self.result_text.insert(tk.END, "未找到匹配的食堂信息")
        except Exception as e:
            messagebox.showerror("错误", f"查询食堂信息时发生错误：{str(e)}")

    def update_canteen(self):
        name, floor, stalls = self.validate_inputs()
        if name is None:
            return

        try:
            if self.canteen.update_canteen(name, floor, stalls):
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "更新成功")
            else:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "更新失败，可能是食堂信息不存在")
        except Exception as e:
            messagebox.showerror("错误", f"更新食堂信息时发生错误：{str(e)}")

    def delete_canteen(self):
        name = self.canteen_name.get().strip()
        floor = self.floor_number.get().strip()

        if not name or len(name) > 50 or not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9\s]+$', name):
            messagebox.showerror("错误", "请输入有效的食堂名称（限50个字符，只允许中文、英文、数字和空格）")
            return

        if not floor or not floor.isdigit() or int(floor) < 1 or int(floor) > 100:
            messagebox.showerror("错误", "请输入有效的楼层数（1-100之间的整数）")
            return

        floor_number = int(floor)

        if messagebox.askyesno("确认", f"确定要删除 {name} {floor_number}楼 的食堂信息吗？"):
            try:
                if self.canteen.delete_canteen(name, floor_number):
                    self.result_text.delete(1.0, tk.END)
                    self.result_text.insert(tk.END, "删除成功")
                else:
                    self.result_text.delete(1.0, tk.END)
                    self.result_text.insert(tk.END, "删除失败，可能是食堂信息不存在")
            except Exception as e:
                messagebox.showerror("错误", f"删除食堂信息时发生错误：{str(e)}")

    def random_select(self):
        try:
            result = self.canteen.random_select_stall()
            self.result_text.delete(1.0, tk.END)
            if result:
                self.result_text.insert(tk.END, result)
            else:
                self.result_text.insert(tk.END, "数据库中没有食堂信息")
        except Exception as e:
            messagebox.showerror("错误", f"随机选择食堂时发生错误：{str(e)}")

    def clear_inputs(self):
        self.canteen_name.delete(0, tk.END)
        self.floor_number.delete(0, tk.END)
        self.stalls.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)