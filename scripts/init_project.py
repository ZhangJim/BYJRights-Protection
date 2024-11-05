import os
from db_config import db_manager
from evidence_manager import EvidenceManager

def init_database():
    """初始化SQLite数据库"""
    print("初始化数据库...")
    db_manager.init_database()
    print("数据库初始化完成！")

def init_folders():
    """初始化文件夹结构"""
    folders = [
        'evidence/video',
        'evidence/images',
        'evidence/documents',
        'evidence/records',
        'database/cases'
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"创建目录：{folder}")

def main():
    print("开始初始化项目...")
    
    # 初始化文件夹
    print("创建文件夹结构...")
    init_folders()
    
    # 初始化数据库
    init_database()
    
    print("项目初始化完成！")

if __name__ == "__main__":
    main() 