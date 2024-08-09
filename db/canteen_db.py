# -*- coding: utf-8 -*-

import logging
import os
import json
import random
from sqlalchemy import create_engine, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from db.models import Base, CanteenInfo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CanteenDatabase:
    def __init__(self):
        self.db_file = 'canteens.db'
        self.json_file = 'canteens_dataset.json'
        self.engine = create_engine(f'sqlite:///{self.db_file}')
        self.Session = sessionmaker(bind=self.engine)

        if not os.path.exists(self.db_file):
            self.create_database()
        else:
            logger.info("Database file already exists.")

        # 检查数据库是否为空，如果为空则尝试加载默认数据
        if self.is_database_empty():
            logger.info("Database is empty. Attempting to load default data.")
            self.load_default_data()

    def create_database(self):
        logger.info("Creating new database.")
        Base.metadata.create_all(self.engine)

    def is_database_empty(self):
        session = self.Session()
        try:
            count = session.query(CanteenInfo).count()
            return count == 0
        finally:
            session.close()

    def load_default_data(self):
        if not os.path.exists(self.json_file):
            logger.error(f"JSON file {self.json_file} not found.")
            return

        with open(self.json_file, "r", encoding="utf-8") as file:
            try:
                default_canteens = json.load(file)
            except json.JSONDecodeError:
                logger.error("Error decoding JSON file.")
                return

        session = self.Session()
        try:
            for canteen_name, floors in default_canteens.items():
                if not isinstance(floors, dict) or "楼层" not in floors:
                    logger.error(
                        f"Invalid data format for canteen {canteen_name}")
                    continue

                for floor in floors["楼层"]:
                    if not isinstance(floor,
                                      dict) or "楼层号" not in floor or "档口" not in floor:
                        logger.error(
                            f"Invalid floor data for canteen {canteen_name}")
                        continue

                    floor_number = floor["楼层号"]
                    for stall_name in floor["档口"]:
                        info = CanteenInfo(canteen_name=canteen_name,
                                           floor_number=floor_number,
                                           stall_name=stall_name)
                        session.add(info)

            session.commit()
            logger.info("Default data loaded successfully.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error loading default data: {str(e)}")
        finally:
            session.close()

    def random_select_all(self):
        session = self.Session()
        try:
            result = session.query(CanteenInfo).order_by(func.random()).first()
            if result:
                return f"{result.canteen_name} {result.floor_number}楼 {result.stall_name}"
            return "没有可用的选项"
        finally:
            session.close()

    def random_select_from_canteen(self, canteen_name):
        session = self.Session()
        try:
            results = session.query(CanteenInfo).filter_by(canteen_name=canteen_name).all()
            if results:
                result = random.choice(results)
                return result.canteen_name, result.floor_number, result.stall_name
            else:
                return canteen_name, None, "没有可用的选项"
        except Exception as e:
            logger.error(f"Error in random_select_from_canteen: {str(e)}")
            return canteen_name, None, f"选择时发生错误: {str(e)}"
        finally:
            session.close()

    # def get_all_canteens(self):
    #     session = self.Session()
    #     try:
    #         canteens = session.query(CanteenInfo.canteen_name).distinct().all()
    #         return [canteen[0] for canteen in canteens]
    #     finally:
    #         session.close()

    def add_stall(self, canteen_name, floor_number, stall_name):
        session = self.Session()
        try:
            new_stall = CanteenInfo(canteen_name=canteen_name,
                                    floor_number=floor_number,
                                    stall_name=stall_name)
            session.add(new_stall)
            session.commit()
            logger.info(
                f"Added new stall: {canteen_name} - Floor {floor_number} - {stall_name}")
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error adding new stall: {str(e)}")
            raise
        finally:
            session.close()

    def delete_stall(self, canteen_name, floor_number, stall_name):
        session = self.Session()
        try:
            stall = session.query(CanteenInfo).filter_by(
                canteen_name=canteen_name,
                floor_number=floor_number,
                stall_name=stall_name
            ).first()
            if stall:
                session.delete(stall)
                session.commit()
                logger.info(
                    f"Deleted stall: {canteen_name} - Floor {floor_number} - {stall_name}")
            else:
                logger.warning(
                    f"Stall not found: {canteen_name} - Floor {floor_number} - {stall_name}")
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error deleting stall: {str(e)}")
            raise
        finally:
            session.close()

    def get_all_stalls(self):
        session = self.Session()
        try:
            stalls = session.query(CanteenInfo).all()
            return stalls
        finally:
            session.close()