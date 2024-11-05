-- 案例基础信息表
CREATE TABLE IF NOT EXISTS cases (
    case_id VARCHAR(20) PRIMARY KEY,    -- 案件编号
    title VARCHAR(200),                 -- 案件标题
    type VARCHAR(50),                   -- 案件类型
    platform VARCHAR(50),               -- 发生平台
    amount DECIMAL(10,2),               -- 涉案金额
    victim_count INT,                   -- 受害人数
    status VARCHAR(20),                 -- 案件状态
    punishment_result TEXT,             -- 新增：处罚结果
    created_at TIMESTAMP,               -- 创建时间
    updated_at TIMESTAMP               -- 更新时间
);

-- 证据材料表
CREATE TABLE IF NOT EXISTS evidence (
    evidence_id VARCHAR(50) PRIMARY KEY,
    case_id VARCHAR(20),
    type VARCHAR(20),                   -- 证据类型
    file_path VARCHAR(500),             -- 文件路径
    file_hash VARCHAR(64),              -- 文件哈希值
    upload_time TIMESTAMP,
    description TEXT,
    FOREIGN KEY (case_id) REFERENCES cases(case_id)
);

-- 外部链接表
CREATE TABLE IF NOT EXISTS external_links (
    link_id VARCHAR(50) PRIMARY KEY,
    case_id VARCHAR(20),
    title VARCHAR(200),
    url VARCHAR(500),
    type VARCHAR(50),                   -- 链接类型（新闻/判决书等）
    status VARCHAR(20),                 -- 链接状态
    archive_url VARCHAR(500),           -- 存档链接
    last_check TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES cases(case_id)
);

-- 案件进展表
CREATE TABLE IF NOT EXISTS case_progress (
    progress_id VARCHAR(50) PRIMARY KEY,
    case_id VARCHAR(20),
    stage VARCHAR(50),                  -- 进展阶段
    description TEXT,                   -- 进展描述
    result TEXT,                        -- 新增：处理结果
    date TIMESTAMP,
    operator VARCHAR(50),
    FOREIGN KEY (case_id) REFERENCES cases(case_id)
);

-- 新增：焦点新闻表
CREATE TABLE IF NOT EXISTS case_news (
    news_id VARCHAR(50) PRIMARY KEY,
    case_id VARCHAR(20),
    title VARCHAR(200),                -- 新闻标题
    source VARCHAR(100),               -- 新闻来源
    url VARCHAR(500),                  -- 新闻链接
    publish_date TIMESTAMP,            -- 发布时间
    summary TEXT,                      -- 新闻摘要
    importance INT,                    -- 重要程度（用于排序）
    FOREIGN KEY (case_id) REFERENCES cases(case_id)
); 