import os
import random
import sqlite3
import json


class CanteenDataBase:
    def __init__(self):
        self.conn = sqlite3.connect("canteens.db")
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        self.create_db()
        self.load_default_data()

    def create_db(self):
        """创建数据库"""
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS Canteens
            (canteen_name text, floor_number integer, stalls text, PRIMARY KEY (canteen_name, floor_number))
        """
        )
        self.conn.commit()

    def load_default_data(self):
        """加载默认数据"""
        if not os.path.exists("canteens_dataset.json"):
            return
        with open("canteens_dataset.json", "r", encoding="utf-8") as file:
            default_canteens = json.load(file)
            for canteen_name, floors in default_canteens.items():
                for floor in floors["楼层"]:
                    self.insert_canteen(
                        canteen_name,
                        floor["楼层号"],
                        floor["档口"]
                    )

    def insert_canteen(self, canteen_name, floor_number, stalls):
        """插入食堂信息"""
        try:
            self.c.execute(
                "INSERT INTO Canteens VALUES (?, ?, ?)",
                (canteen_name, floor_number, json.dumps(stalls)),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def select_canteen(self, canteen_name=None, floor_number=None,
                       stall_name=None):
        """查询食堂信息"""
        query = "SELECT * FROM Canteens WHERE 1=1"
        params = []

        if canteen_name:
            query += " AND canteen_name = ?"
            params.append(canteen_name)
        if floor_number:
            query += " AND floor_number = ?"
            params.append(floor_number)
        if stall_name:
            query += " AND stalls LIKE ?"
            params.append(f"%{stall_name}%")

        self.c.execute(query, params)
        results = self.c.fetchall()
        decoded_results = []
        for result in results:
            canteen_name, floor_number, stalls = result
            decoded_stalls = json.loads(stalls)
            decoded_results.append(
                (canteen_name, floor_number, decoded_stalls))
        return decoded_results

    def update_canteen(self, canteen_name, floor_number, stalls):
        """更新食堂信息"""
        self.c.execute(
            "UPDATE Canteens SET stalls = ? WHERE canteen_name = ? AND floor_number = ?",
            (json.dumps(stalls), canteen_name, floor_number),
        )
        self.conn.commit()

    def delete_canteen(self, canteen_name, floor_number):
        """删除食堂信息"""
        self.c.execute(
            "DELETE FROM Canteens WHERE canteen_name = ? AND floor_number = ?",
            (canteen_name, floor_number),
        )
        self.conn.commit()

    def random_select_stall(self):
        """从所有食堂中随机选择一个档口"""
        self.c.execute("SELECT canteen_name, floor_number,"
                       " stalls FROM Canteens")
        all_canteens = self.c.fetchall()
        if not all_canteens:
            return None
        canteen_name, floor_number, stalls = random.choice(all_canteens)
        stalls = json.loads(stalls)
        stall = random.choice(stalls)
        return f"{canteen_name}{floor_number}楼{stall}"

    def close(self):
        """关闭连接"""
        self.conn.close()
