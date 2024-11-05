import os
import hashlib
import shutil
from datetime import datetime

class EvidenceManager:
    def __init__(self, base_path):
        self.base_path = base_path
        
    def save_evidence(self, case_id, file_path, evidence_type):
        """保存证据文件并生成哈希值"""
        # 创建目标目录
        dest_dir = os.path.join(self.base_path, evidence_type, case_id)
        os.makedirs(dest_dir, exist_ok=True)
        
        # 复制文件并计算哈希值
        file_hash = self._calculate_hash(file_path)
        file_ext = os.path.splitext(file_path)[1]
        new_filename = f"{case_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}{file_ext}"
        dest_path = os.path.join(dest_dir, new_filename)
        
        shutil.copy2(file_path, dest_path)
        return {
            'file_path': dest_path,
            'file_hash': file_hash,
            'upload_time': datetime.now()
        }
    
    def _calculate_hash(self, file_path):
        """计算文件的SHA256哈希值"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()