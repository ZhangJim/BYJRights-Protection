import json
import sqlite3
from db_config import db_manager

def view_case(case_id):
    """查看案例详情"""
    # 从数据库读取基本信息
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,))
    case_info = cursor.fetchone()
    
    # 读取JSON文件中的详细信息
    with open(f"database/cases/{case_id}.json", 'r', encoding='utf-8') as f:
        case_detail = json.load(f)
    
    print("=== 案件基本信息 ===")
    print(f"案件编号: {case_info[0]}")
    print(f"案件标题: {case_info[1]}")
    print(f"案件类型: {case_info[2]}")
    print(f"涉案平台: {case_info[3]}")
    print(f"涉案金额: {case_info[4]}")
    print(f"受害人数: {case_info[5]}")
    print(f"案件状态: {case_info[6]}")
    
    print("\n=== 证据清单 ===")
    for evidence in case_detail.get('evidence_list', []):
        print(f"类型: {evidence['type']}")
        print(f"描述: {evidence['description']}")
        print(f"文件路径: {evidence['file_path']}")
        print(f"上传时��: {evidence['upload_time']}")
        print("---")

if __name__ == "__main__":
    view_case("BJ202403001") 