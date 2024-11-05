# -*- coding: utf-8 -*-
from __future__ import print_function
import sqlite3
import os

class DatabaseManager:
    def __init__(self):
        # Make sure database directory exists
        try:
            os.makedirs('database')
        except OSError:
            if not os.path.isdir('database'):
                raise
        self.db_path = 'database/rights_protection.db'
        
    def get_connection(self):
        print("Connecting to database: %s" % self.db_path)
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        print("Initializing database: %s" % self.db_path)
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create cases table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            case_id TEXT PRIMARY KEY,
            title TEXT,
            type TEXT,
            platform TEXT,
            amount REAL,
            victim_count INTEGER,
            status TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
        ''')
        
        # Create evidence table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS evidence (
            evidence_id TEXT PRIMARY KEY,
            case_id TEXT,
            type TEXT,
            file_path TEXT,
            file_hash TEXT,
            upload_time TIMESTAMP,
            description TEXT,
            FOREIGN KEY (case_id) REFERENCES cases(case_id)
        )
        ''')
        
        # Create external links table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS external_links (
            link_id TEXT PRIMARY KEY,
            case_id TEXT,
            title TEXT,
            url TEXT,
            type TEXT,
            status TEXT,
            archive_url TEXT,
            last_check TIMESTAMP,
            FOREIGN KEY (case_id) REFERENCES cases(case_id)
        )
        ''')
        
        # Create case progress table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS case_progress (
            progress_id TEXT PRIMARY KEY,
            case_id TEXT,
            stage TEXT,
            description TEXT,
            date TIMESTAMP,
            operator TEXT,
            FOREIGN KEY (case_id) REFERENCES cases(case_id)
        )
        ''')
        
        conn.commit()
        conn.close()

# 创建全局实例
db_manager = DatabaseManager()

# 导出实例
__all__ = ['db_manager']