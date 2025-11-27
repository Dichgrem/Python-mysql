# main.py
from database import create_database_manager


def main():
    db_manager = create_database_manager()
    if not db_manager.connect():
        print("无法连接到数据库，请检查配置")
        return
    print("数据库连接成功")

    # 创建数据表（如果不存在）
    if not db_manager.create_tables():
        print("创建数据表失败")
        db_manager.close()
        return

    y = input("是否初始化示例数据（会插入若干示例记录）? (y/n): ").strip().lower()
    if y == "y":
        if db_manager.insert_initial_data():
            print("示例数据插入成功")
        else:
            print("示例数据插入失败")

    db_manager.close()
    print("完成。")


if __name__ == "__main__":
    main()
