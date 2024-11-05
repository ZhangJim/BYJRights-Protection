import sqlite3

def update_database_schema():
    conn = sqlite3.connect('database/cases.db')
    cur = conn.cursor()
    
    try:
        # 为 cases 表添加处罚结果字段
        cur.execute('''
        ALTER TABLE cases ADD COLUMN punishment_result TEXT;
        ''')
        print("Added punishment_result column to cases table")
    except sqlite3.OperationalError as e:
        print("Note:", e)

    try:
        # 为 case_progress 表添加结果字段
        cur.execute('''
        ALTER TABLE case_progress ADD COLUMN result TEXT;
        ''')
        print("Added result column to case_progress table")
    except sqlite3.OperationalError as e:
        print("Note:", e)

    try:
        # 创建焦点新闻表
        cur.execute('''
        CREATE TABLE IF NOT EXISTS case_news (
            news_id VARCHAR(50) PRIMARY KEY,
            case_id VARCHAR(20),
            title VARCHAR(200),
            source VARCHAR(100),
            url VARCHAR(500),
            publish_date TIMESTAMP,
            summary TEXT,
            importance INT,
            FOREIGN KEY (case_id) REFERENCES cases(case_id)
        )
        ''')
        print("Created case_news table")
    except sqlite3.OperationalError as e:
        print("Note:", e)

    conn.commit()
    conn.close()
    print("Schema update completed")

if __name__ == '__main__':
    update_database_schema() 