# -*- coding: utf-8 -*-
"""
Configuration file for the canteen project.

This file contains constants used throughout the project, including canteen names,
canteen floors, default font settings, and paths to the database and JSON dataset.
"""

# List of canteen names in Chinese
CANTEEN_NAMES = ["嘉园", "乾园", "菁园", "龙祥街"]

# List of canteen floor numbers as strings
CANTEEN_FLOORS = ["1", "2", "3", "4"]

# Default font used in the application
DEFAULT_FONT = "Simsun"

# Path to the SQLite database file
DATABASE_PATH = "canteens.db"

# Path to the default JSON dataset file, Only used when the database is empty
DEFAULT_JSON_FILE = "canteens_dataset.json"