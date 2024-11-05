from case_collector import CaseCollector

def collect_first_case():
    collector = CaseCollector()
    
    # 案例基本信息
    case_info = {
        "title": "某主播保健品虚假宣传案",
        "location": "BJ",
        "platform": "快手",
        "streamer": "李某",
        "followers": "200万+",
        "time_period": "2023-01 至 2023-06",
        "victim_count": 2800,
        "amount": 4200000,
        "product_type": "保健品",
        "case_type": "虚假宣传",
        "status": "已结案",
        "summary": """
        主播宣称产品有速效降糖功能，可替代降糖药物。
        通过伪造专家背书、虚假用户好评等方式诱导购买。
        多位老年人停用降糖药，导致病情加重。
        产品检测发现含有违禁西药成分。
        """,
        "result": """
        主播被刑事立案，获刑3年
        平台下架所有相关产品
        商家被罚款150万元
        受害者获得全额赔偿
        """,
        "external_links": [
            {
                "title": "快手主播售假药被刑拘 涉案金额超400万元",
                "url": "https://www.chinanews.com.cn/sh/2023/08-21/10058679.shtml",
                "type": "news"
            }
        ]
    }
    
    # 创建案例
    case_id = collector.create_case(case_info)
    print(f"案例创建成功，案件编号：{case_id}")
    
    # 添加证据（这里用示例文件路径）
    evidence_files = [
        ("evidence/samples/live_screenshot.jpg", "images", "直播截图"),
        ("evidence/samples/chat_record.pdf", "documents", "聊天记录"),
        ("evidence/samples/product_test.pdf", "documents", "产品检测报告")
    ]
    
    for file_path, evidence_type, description in evidence_files:
        try:
            result = collector.add_evidence(case_id, file_path, evidence_type, description)
            print(f"证据添加成功：{description}")
        except FileNotFoundError:
            print(f"警告：证据文件不存在：{file_path}")

if __name__ == "__main__":
    collect_first_case() 