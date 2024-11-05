# 案例管理系统部署指南

## 一、本地开发环境部署

### 1.1 环境要求
- Python 3.8+
- SQLite 3
- Git

### 1.2 安装步骤
1. 克隆代码仓库
git clone https://github.com/your-org/case-management.git
cd case-management

2. 创建并激活虚拟环境
# Windows
python -m venv venv
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

3. 安装依赖包
pip install -r requirements.txt

### 1.3 配置文件设置
1. 复制配置文件模板
cp config/config.example.yml config/config.yml

2. 修改配置文件(config/config.yml)
# 数据库配置
database:
  type: sqlite
  path: database/case_management.db

# 服务器配置
server:
  host: 0.0.0.0
  port: 8000
  debug: true

# 日志配置
logging:
  level: INFO
  path: logs/app.log
  
# JWT配置
jwt:
  secret_key: your-secret-key
  token_expire_minutes: 1440

# 文件上传配置
upload:
  allowed_extensions: ['.jpg', '.png', '.pdf', '.doc', '.docx']
  max_size_mb: 10
  save_path: uploads/

### 1.4 数据库初始化
1. 创建数据库表
python scripts/init_db.py

2. 导入初始数据(可选)
python scripts/import_initial_data.py

### 1.5 启动应用
python app.py

## 二、生产环境部署

### 2.1 环境准备
- Linux服务器(推荐Ubuntu 20.04+)
- Nginx
- Supervisor
- Python 3.8+
- SQLite 3

### 2.2 安装系统依赖
sudo apt update
sudo apt install python3-pip python3-venv nginx supervisor

### 2.3 部署步骤
1. 创建应用目录
sudo mkdir /opt/case-management
sudo chown -R $USER:$USER /opt/case-management

2. 克隆代码并安装依赖
cd /opt/case-management
git clone https://github.com/your-org/case-management.git .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. 配置Supervisor
创建文件: /etc/supervisor/conf.d/case-management.conf

[program:case-management]
directory=/opt/case-management
command=/opt/case-management/venv/bin/gunicorn app:app -w 4 -b 127.0.0.1:8000
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/case-management/supervisor.err.log
stdout_logfile=/var/log/case-management/supervisor.out.log

4. 配置Nginx
创建文件: /etc/nginx/sites-available/case-management

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /opt/case-management/static;
    }

    location /uploads {
        alias /opt/case-management/uploads;
    }
}

5. 启用Nginx配置
sudo ln -s /etc/nginx/sites-available/case-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

6. 启动服务
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start case-management

### 2.4 日常维护
- 查看日志
tail -f /var/log/case-management/supervisor.out.log

- 重启服务
sudo supervisorctl restart case-management

- 更新代码
cd /opt/case-management
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart case-management

## 三、常见问题处理

### 3.1 数据库备份
# 备份
sqlite3 database/case_management.db .dump > backup.sql

# 恢复
sqlite3 database/case_management.db < backup.sql

### 3.2 日志清理
# 清理超过30天的日志
find /var/log/case-management -type f -mtime +30 -delete

### 3.3 性能优化建议
1. 配置数据库索引
2. 启用缓存系统
3. 配置适当的工作进程数
4. 定期清理临时文件和日志

## 四、Git版本管理配置

### 4.1 IDE中Git配置
1. 配置Git全局信息