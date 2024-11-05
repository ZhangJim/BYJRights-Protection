import os

def create_sample_files():
    """创建示例证据文件"""
    sample_dir = "evidence/samples"
    os.makedirs(sample_dir, exist_ok=True)
    
    # 创建示例图片
    with open(os.path.join(sample_dir, "live_screenshot.jpg"), 'w') as f:
        f.write("This is a sample screenshot")
    
    # 创建示例PDF
    with open(os.path.join(sample_dir, "chat_record.pdf"), 'w') as f:
        f.write("This is a sample chat record")
    
    with open(os.path.join(sample_dir, "product_test.pdf"), 'w') as f:
        f.write("This is a sample product test report")

if __name__ == "__main__":
    create_sample_files() 