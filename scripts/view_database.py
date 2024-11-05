from db_config import db_manager

def view_all_data():
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    print("\n=== 案例信息 ===")
    cursor.execute("SELECT * FROM cases")
    for row in cursor.fetchall():
        print(f"案件编号: {row[0]}")
        print(f"标题: {row[1]}")
        print(f"类型: {row[2]}")
        print(f"平台: {row[3]}")
        print(f"涉案金额: {row[4]}")
        print(f"受害人数: {row[5]}")
        print(f"状态: {row[6]}\n")
    
    print("\n=== 证据材料 ===")
    cursor.execute("SELECT * FROM evidence")
    for row in cursor.fetchall():
        print(f"证据编号: {row[0]}")
        print(f"案件编号: {row[1]}")
        print(f"类型: {row[2]}")
        print(f"文件路径: {row[3]}")
        print(f"描述: {row[6]}\n")
    
    print("\n=== 外部链接 ===")
    cursor.execute("SELECT * FROM external_links")
    for row in cursor.fetchall():
        print(f"链接编号: {row[0]}")
        print(f"案件编号: {row[1]}")
        print(f"标题: {row[2]}")
        print(f"URL: {row[3]}")
        print(f"类型: {row[4]}\n")
    
    print("\n=== 案件进展 ===")
    cursor.execute("SELECT * FROM case_progress")
    for row in cursor.fetchall():
        print(f"进展编号: {row[0]}")
        print(f"案件编号: {row[1]}")
        print(f"阶段: {row[2]}")
        print(f"描述: {row[3]}")
        print(f"操作人: {row[5]}\n")
    
    conn.close()

if __name__ == "__main__":
    view_all_data() 