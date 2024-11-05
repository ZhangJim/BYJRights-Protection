from evidence_manager import EvidenceManager

def test_save_evidence():
    # 初始化证据管理器
    manager = EvidenceManager("evidence")
    
    # 保存一个测试文件
    test_file = "test_evidence.jpg"  # 这里替换为你的实际文件
    result = manager.save_evidence(
        case_id="BJ2023001",
        file_path=test_file,
        evidence_type="images"
    )
    
    print("证据保存结果：", result)

if __name__ == "__main__":
    test_save_evidence() 