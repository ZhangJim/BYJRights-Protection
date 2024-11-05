#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, redirect, url_for, request, session
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
from functools import wraps
import random
import string
import uuid

app = Flask(__name__)
CORS(app)
app.secret_key = 'your-secret-key'  # 添加 secret key 用于 session

def get_db_connection():
    conn = sqlite3.connect('database/cases.db')
    conn.row_factory = sqlite3.Row
    return conn

# 添加登录验证装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 添加首页路由
@app.route('/')
def index():
    return redirect(url_for('cases'))

# 案例列表路由
@app.route('/cases')
@login_required
def cases():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT case_id, title, type, platform, amount, victim_count, status 
            FROM cases 
            ORDER BY created_at DESC
        """)
        cases = cur.fetchall()
        return render_template('case_list.html', cases=cases)
    finally:
        conn.close()

# 功能清单页面路由
@app.route('/features')
@login_required
def feature_list():
    features = [
        # 已实现的功能
        {
            'id': 1,
            'title': '用户登录管理',
            'description': '支持用户登录和退出，保护系统安全',
            'status': '已实现',
            'type': 'implemented',
            'category': '基础功能'
        },
        {
            'id': 2,
            'title': '案例列表展示',
            'description': '展示所有维权案例的基本信息，支持查看详情',
            'status': '已实现',
            'type': 'implemented',
            'category': '基础功能'
        },
        {
            'id': 3,
            'title': '案例详情查看',
            'description': '查看案例的详细信息、证据材料、处理进展和相关新闻',
            'status': '已实现',
            'type': 'implemented',
            'category': '基础功能'
        },
        {
            'id': 4,
            'title': '案例信息编辑',
            'description': '支持编辑案例的所有信息，包括基本信息、证据、进展和新闻',
            'status': '已实现',
            'type': 'implemented',
            'category': '基础功能'
        },
        {
            'id': 5,
            'title': '证据材料管理',
            'description': '支持添加、编辑和删除案例相关的证据材料',
            'status': '已实现',
            'type': 'implemented',
            'category': '管理功能'
        },
        {
            'id': 6,
            'title': '案件进展跟踪',
            'description': '记录和管理案件处理的各个阶段和结果',
            'status': '已实现',
            'type': 'implemented',
            'category': '管理功能'
        },
        {
            'id': 7,
            'title': '焦点新闻管理',
            'description': '管理案例相关的新闻报道和媒体关注',
            'status': '已实现',
            'type': 'implemented',
            'category': '管理功能'
        },
        {
            'id': 8,
            'title': '处罚结果记录',
            'description': '记录和展示案件的最终处罚结果',
            'status': '已实现',
            'type': 'implemented',
            'category': '管理功能'
        },
        # 计划中的功能
        {
            'id': 9,
            'title': '数据统计分析',
            'description': '提供案件数据的统计和分析功能',
            'status': '计划中',
            'type': 'planned',
            'category': '统计分析'
        },
        {
            'id': 10,
            'title': '批量导入导出',
            'description': '支持案例数据的批量导入和导出',
            'status': '计划中',
            'type': 'planned',
            'category': '管理功能'
        },
        {
            'id': 11,
            'title': '智能推荐',
            'description': '基于案例特征推荐相似案例和处理方案',
            'status': '计划中',
            'type': 'planned',
            'category': '智能推荐'
        },
        {
            'id': 12,
            'title': '全文检索',
            'description': '支持对案例内容进行全文检索',
            'status': '计划中',
            'type': 'planned',
            'category': '基础功能'
        },
        {
            'id': 13,
            'title': '数据可视化',
            'description': '通过图表直观展示数据分析结果',
            'status': '计划中',
            'type': 'planned',
            'category': '统计分析'
        },
        {
            'id': 14,
            'title': '用户权限管理',
            'description': '细粒度的用户权限控制和管理',
            'status': '计划中',
            'type': 'planned',
            'category': '管理功能'
        },
        # 添加新的数据处理相关功能
        {
            'id': 15,
            'title': '案例数据爬取',
            'description': '自动从各大电商平台、社交媒体和新闻网站爬取维权案例信息，支持定时任务和增量更新，确保数据及时性',
            'status': '计划中',
            'type': 'planned',
            'category': '数据采集'
        },
        {
            'id': 16,
            'title': '案例数据清洗',
            'description': '对爬取的原始数据进行结构化处理，包括格式统一、去重、信息提取、数据标准化等，提高数据质量和可用性',
            'status': '计划中',
            'type': 'planned',
            'category': '数据处理'
        },
        {
            'id': 17,
            'title': '案例数据核实',
            'description': '通过多源数据交叉验证、人工审核等方式，对案例信息进行真实性和准确性核查，建立数据可信度评估体系',
            'status': '计划中',
            'type': 'planned',
            'category': '数据处理'
        },
        # 添加数据爬取第一期功能
        {
            'id': 18,
            'title': '官方数据采集',
            'description': '支持从市场监管总局、各地监管局、法院判决文书网等官方渠道自动采集案例数据',
            'status': '计划中',
            'type': 'planned',
            'category': '数据采集'
        },
        {
            'id': 19,
            'title': '数据解析引擎',
            'description': '对采集的数据进行智能解析，提取案件标题、类型、金额、处罚结果等关键信息',
            'status': '计划中',
            'type': 'planned',
            'category': '数据处理'
        },
        {
            'id': 20,
            'title': '定时任务管理',
            'description': '支持设置数据采集任务的执行频率、时间段，自动调度和执行采集任务',
            'status': '计划中',
            'type': 'planned',
            'category': '数据采集'
        },
        {
            'id': 21,
            'title': '数据入库管理',
            'description': '将采集的数据按照系统数据结构进行转换和存储，支持增量更新',
            'status': '计划中',
            'type': 'planned',
            'category': '数据处理'
        },
        {
            'id': 22,
            'title': '采集监控面板',
            'description': '展示数据采集任务的运行状态、成功率、数据量等关键指标',
            'status': '计划中',
            'type': 'planned',
            'category': '数据采集'
        }
    ]
    
    # 获取所有分类
    categories = sorted(set(f['category'] for f in features))
    
    return render_template('feature_list.html', 
                         features=features, 
                         categories=categories)

@app.route('/api/cases/<case_id>/detail')
def case_detail_api(case_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 获取案例基本信息
        cur.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,))
        case_data = cur.fetchone()
        
        if not case_data:
            return jsonify({
                'success': False,
                'error': '未找到该案例'
            }), 404

        # 将 Row 对象转换为字典
        case = {}
        for idx, col in enumerate(cur.description):
            case[col[0]] = case_data[idx]

        # 获取证据材料
        cur.execute("""
            SELECT * FROM evidence 
            WHERE case_id = ? 
            ORDER BY upload_time DESC
        """, (case_id,))
        evidence = []
        for row in cur.fetchall():
            item = {}
            for idx, col in enumerate(cur.description):
                item[col[0]] = row[idx]
            evidence.append(item)
        
        # 获取案件进展
        cur.execute("""
            SELECT * FROM case_progress 
            WHERE case_id = ? 
            ORDER BY date DESC
        """, (case_id,))
        progress = []
        for row in cur.fetchall():
            item = {}
            for idx, col in enumerate(cur.description):
                item[col[0]] = row[idx]
            progress.append(item)
        
        # 获取焦点新闻
        cur.execute("""
            SELECT * FROM case_news 
            WHERE case_id = ? 
            ORDER BY importance DESC, publish_date DESC
        """, (case_id,))
        news = []
        for row in cur.fetchall():
            item = {}
            for idx, col in enumerate(cur.description):
                item[col[0]] = row[idx]
            news.append(item)

        return jsonify({
            'success': True,
            'data': {
                'case': case,
                'evidence': evidence,
                'progress': progress,
                'news': news
            }
        })
        
    except Exception as e:
        print(f"Error in case_detail_api: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 这里添加用户验证逻辑
        if username == 'admin' and password == 'password':  # 示例验证
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('cases'))
        else:
            return render_template('login.html', error='用户名或密码错误')
    
    return render_template('login.html')

# 添加登出路由
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/cases/<case_id>', methods=['PUT'])
def update_case(case_id):
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            # 使用 with 语句自动处理事务
            with conn:
                # 1. 更新案例基本信息
                cur.execute("""
                    UPDATE cases 
                    SET title = ?, type = ?, platform = ?, amount = ?, 
                        victim_count = ?, status = ?, punishment_result = ?,
                        updated_at = datetime('now')
                    WHERE case_id = ?
                """, (
                    data['title'], data['type'], data['platform'], data['amount'],
                    data['victim_count'], data['status'], data.get('punishment_result'),
                    case_id
                ))

                # 2. 更新证据材料
                if 'evidence' in data:
                    cur.execute("DELETE FROM evidence WHERE case_id = ?", (case_id,))
                    for evidence in data['evidence']:
                        cur.execute("""
                            INSERT INTO evidence (
                                evidence_id, case_id, type, description, 
                                file_path, upload_time
                            ) VALUES (?, ?, ?, ?, ?, datetime('now'))
                        """, (
                            evidence.get('id') or str(uuid.uuid4()),
                            case_id,
                            evidence['type'],
                            evidence['description'],
                            evidence.get('file_path', ''),
                        ))

                # 3. 更新案件进展
                if 'progress' in data:
                    cur.execute("DELETE FROM case_progress WHERE case_id = ?", (case_id,))
                    for progress in data['progress']:
                        cur.execute("""
                            INSERT INTO case_progress (
                                progress_id, case_id, stage, description,
                                result, date, operator
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            progress.get('id') or str(uuid.uuid4()),
                            case_id,
                            progress['stage'],
                            progress['description'],
                            progress.get('result'),
                            progress.get('date', datetime.now().isoformat()),
                            progress['operator']
                        ))

                # 4. 更新焦点新闻
                if 'news' in data:
                    cur.execute("DELETE FROM case_news WHERE case_id = ?", (case_id,))
                    for news in data['news']:
                        cur.execute("""
                            INSERT INTO case_news (
                                news_id, case_id, title, source,
                                url, publish_date, summary, importance
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            news.get('id') or str(uuid.uuid4()),
                            case_id,
                            news['title'],
                            news['source'],
                            news['url'],
                            news.get('publish_date', datetime.now().isoformat()),
                            news['summary'],
                            news.get('importance', 1)
                        ))

            return jsonify({
                'success': True,
                'message': '保存成功'
            })

        except Exception as e:
            print(f"Error in transaction: {str(e)}")
            raise

    except Exception as e:
        print(f"Error updating case: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        conn.close()

def generate_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@app.route('/cases/data')
@login_required
def cases_data():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT case_id, title, type, platform, amount, victim_count, status 
            FROM cases 
            ORDER BY created_at DESC
        """)
        cases = [dict(zip([column[0] for column in cur.description], row)) 
                for row in cur.fetchall()]
        return jsonify({'success': True, 'cases': cases})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(port=5001, debug=True) 