## 目的
为患有选择困难症的高校学生，特别是那些在决策“今天吃什么”方面遇到困难的用户。通过提供快速、随机的餐饮选择，帮助用户轻松解决用餐难题。

## 环境要求
- Python 3.8+

## 安装依赖
在项目根目录下运行以下命令安装所需依赖：
```sh
pip install -r requirements.txt
```
## 文件结构
```ssh
project_root/
│
├── src/
│   ├── config/
│   │   └── config.py
│   ├── db/
│   │   ├── canteen_db.py
│   │   ├── models.py
│   │   
│   ├── gui/
│   │   ├── canteen_management_gui.py
│   │   ├── quick_selection_gui.py
│   │   
│   ├── main.py
│   ├── canteen_dataset.json
│   ├── canteens.db
├── requirements.txt
└── README.md
```
## 自定义指南
1. 修改或添加食堂：修改`src/config.py`文件中的`CANTEEN_NAMES`数组
2. 修改楼层信息：修改`src/config.py`文件中的`CANTEEN_FLOORS`数组
3. 如要添加非高校食堂信息，例如："龙祥街"，则需进行如下修改：
   - `src/gui/canteen_management_gui.py`中`toggle_floor_input`函数和`add_stall`函数中相应的逻辑代码
   - `src/gui/quick_selection_gui.py`中`random_select_from_canteen`函数和`random_select_all`函数中相应的逻辑代码

## 使用指南
1. 下载最新版本：前往发布页面，获取最新的[v1.0.0版本](https://github.com/Harryleft/today-eat-what/releases/tag/1.0.0)。
2. 解压文件：使用`winRAR`或其他解压工具解压下载的文件。
3. 安装程序：双击`set_up.exe`。


## 页面功能说明
1. 首页：
- 用户可以从所有地点或指定地点中快速、随机选择一条餐饮信息。
- 示例输出格式为：_食堂-楼层-菜品_。

![image](https://github.com/user-attachments/assets/f2c3d673-567a-4689-8e5d-4fd02ef39320)

2. 后台管理界面：
- 允许用户添加、删除和查看不同地点和楼层的菜品信息。
- 支持以 JSON 格式导入和导出数据，方便与他人共享数据。

![image](https://github.com/user-attachments/assets/6ae01085-5752-4475-8357-9feef4406a93)

## 许可证
本项目采用 MIT 许可证。

  
