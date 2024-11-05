# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys

# 添加父目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.db_config import db_manager

def init_db():
    try:
        # 初始化数据库和表
        db_manager.init_database()
        print("数据库初始化成功！")
        
        conn = db_manager.get_connection()
        conn.text_factory = str  # 设置text_factory
        cursor = conn.cursor()
        
        # 清空现有数据
        cursor.execute('DELETE FROM case_progress')
        cursor.execute('DELETE FROM external_links')
        cursor.execute('DELETE FROM evidence')
        cursor.execute('DELETE FROM cases')
        
        # 案例1：快手"权健"事件
        cursor.execute('''
            INSERT INTO cases (case_id, title, type, platform, amount, victim_count, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ''', ('KS202301', u'快手主播推广权健产品案', u'虚假宣传', u'快手', 890000.00, 156, u'已结案'))
        
        cursor.execute('''
            INSERT INTO evidence (evidence_id, case_id, type, file_path, file_hash, upload_time, description)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
        ''', ('EV202301', 'KS202301', u'新闻报道', u'/evidence/news/KS202301/report.pdf', 
              'hash1', u'天津市市场监督管理委员会发布的行政处罚决定书'))
              
        cursor.execute('''
            INSERT INTO external_links (link_id, case_id, title, url, type, status, archive_url, last_check)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', ('LK202301', 'KS202301', u'权健案件宣判', u'https://www.court.gov.cn/zixun-xiangqing-212871.html', 
              u'判决书', u'有效', u'https://archive.is/xxxxx'))
        
        # 添加案件进展数据
        cursor.execute('''
            INSERT INTO case_progress (progress_id, case_id, stage, description, date, operator)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
        ''', ('PG202301', 'KS202301', '立案', '接到举报，开始调查', '张警官'))
        
        cursor.execute('''
            INSERT INTO case_progress (progress_id, case_id, stage, description, date, operator)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
        ''', ('PG202302', 'KS202301', '调查', '完成现场取证', '李调查员'))
        
        cursor.execute('''
            INSERT INTO case_progress (progress_id, case_id, stage, description, date, operator)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
        ''', ('PG202303', 'KS202301', '结案', '下达行政处罚决定', '王科长'))
        
        # 案例2：快手"减肥药"事件
        cursor.execute('''
            INSERT INTO cases (case_id, title, type, platform, amount, victim_count, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ''', ('KS202302', u'快手主播推广违禁减肥药案', u'违禁产品', u'快手', 235000.00, 89, u'已结案'))
        
        cursor.execute('''
            INSERT INTO evidence (evidence_id, case_id, type, file_path, file_hash, upload_time, description)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
        ''', ('EV202302', 'KS202302', u'行政处罚', u'/evidence/doc/KS202302/penalty.pdf', 
              'hash2', u'市场监督管理局行政处罚决定书'))
        
        # 案例3：快手"假冒品牌服装"事件
        cursor.execute('''
            INSERT INTO cases (case_id, title, type, platform, amount, victim_count, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ''', ('KS202303', u'快手主播售假名牌服装案', u'假冒伪劣', u'快手', 567000.00, 234, u'处理中'))
        
        cursor.execute('''
            INSERT INTO evidence (evidence_id, case_id, type, file_path, file_hash, upload_time, description)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
        ''', ('EV202303', 'KS202303', u'投诉记录', u'/evidence/doc/KS202303/complaint.pdf', 
              'hash3', u'消费者集体投诉材料'))
        
        conn.commit()
        conn.close()
        print("真实案例数据插入成功！")
        
    except Exception as e:
        print("初始化失败：%s" % str(e))

if __name__ == "__main__":
    init_db() 