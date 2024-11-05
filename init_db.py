import sqlite3
import os
from datetime import datetime

def init_database():
    # 确保database目录存在
    if not os.path.exists('database'):
        os.makedirs('database')
    
    # 连接到数据库
    conn = sqlite3.connect('database/cases.db')
    cur = conn.cursor()

    # 创建表（使用 IF NOT EXISTS）
    with open('database/sql/schema.sql', 'r') as f:
        schema = f.read()
        cur.executescript(schema)

    # 检查是否需要添加新的测试数据
    cur.execute("SELECT COUNT(*) FROM case_news")
    news_count = cur.fetchone()[0]

    if news_count == 0:
        # 只插入焦点新闻的测试数据
        cur.execute('''
        INSERT OR IGNORE INTO case_news (
            news_id, case_id, title, source, url, publish_date, summary, importance
        ) VALUES 
            ('N001', 'KS202301', '快手主播推广权健产品被查处', '新华网', 'https://news.example.com/001', 
             datetime('now'), '某快手主播因推广权健产品被处以50万元罚款', 1),
            ('N002', 'KS202301', '权健产品推广案件调查进展', '法制日报', 'https://news.example.com/002', 
             datetime('now'), '权健产品推广案件详细调查过程公布', 2),
            ('N003', 'KS202302', '快手打击违禁药品推广', '中国网', 'https://news.example.com/003', 
             datetime('now'), '快手平台联合监管部门打击违禁药品推广行为', 1)
        ''')

    # 检查是否需要更新现有案例的处罚结果
    cur.execute("SELECT case_id FROM cases WHERE punishment_result IS NULL")
    cases_without_punishment = cur.fetchall()
    
    if cases_without_punishment:
        # 更新示例处罚结果
        punishment_data = {
            'KS202301': '罚款50万元，永久关闭账号',
            'KS202302': '罚款20万元，封禁账号6个月'
        }
        
        for case_id, in cases_without_punishment:
            if case_id in punishment_data:
                cur.execute("""
                    UPDATE cases 
                    SET punishment_result = ? 
                    WHERE case_id = ?
                """, (punishment_data[case_id], case_id))

    # 提交事务并关闭连接
    conn.commit()
    conn.close()
    print("数据库更新完成")

if __name__ == '__main__':
    init_database()