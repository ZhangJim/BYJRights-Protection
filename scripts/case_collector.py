import os
import json
from datetime import datetime
from db_config import db_manager
from evidence_manager import EvidenceManager

class CaseCollector:
    def __init__(self, base_path="evidence"):
        self.evidence_manager = EvidenceManager(base_path)
        self.db = db_manager
        self.case_data_path = "database/cases"
    
    def create_case(self, case_info):
        """创建新案例"""
        case_id = self._generate_case_id(case_info)
        now = datetime.now().isoformat()
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # 插入案例基本信息
        cursor.execute('''
        INSERT INTO cases (case_id, title, type, platform, amount, victim_count, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            case_id,
            case_info['title'],
            case_info['case_type'],
            case_info['platform'],
            case_info['amount'],
            case_info['victim_count'],
            case_info['status'],
            now,
            now
        ))
        
        conn.commit()
        conn.close()
        return case_id
    
    def add_evidence(self, case_id, file_path, evidence_type, description=""):
        """添加证据"""
        result = self.evidence_manager.save_evidence(
            case_id=case_id,
            file_path=file_path,
            evidence_type=evidence_type
        )
        
        # 更新案例信息
        case_data = self._load_case_data(case_id)
        if "evidence_list" not in case_data:
            case_data["evidence_list"] = []
        
        case_data["evidence_list"].append({
            "file_path": result["file_path"],
            "file_hash": result["file_hash"],
            "upload_time": result["upload_time"].isoformat(),
            "type": evidence_type,
            "description": description
        })
        
        self._save_case_data(case_id, case_data)
        return result
    
    def _generate_case_id(self, case_info):
        """生成案件编号"""
        timestamp = datetime.now().strftime("%Y%m")
        location = case_info.get("location", "BJ")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cases")
        count = cursor.fetchone()[0] + 1
        conn.close()
        
        return f"{location}{timestamp}{count:04d}"
    
    def _save_case_data(self, case_id, data):
        """保存案例数据"""
        file_path = os.path.join(self.case_data_path, f"{case_id}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_case_data(self, case_id):
        """加载案例数据"""
        file_path = os.path.join(self.case_data_path, f"{case_id}.json")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f) 