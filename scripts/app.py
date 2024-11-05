from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from db_config import db_manager
import sqlite3
import os

app = Flask(__name__, 
    template_folder='../templates',
    static_folder='../static'
)
app.secret_key = 'your-secret-key'  # 请更改为安全的密钥

# 登录页面
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 简单的用户验证（实际应用中需要更安全的方式）
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('case_list'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

# 案例列表页面
@app.route('/cases')
def case_list():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT case_id, title, type, platform, amount, victim_count, status 
        FROM cases
        ORDER BY created_at DESC
    ''')
    cases = cursor.fetchall()
    conn.close()
    
    return render_template('case_list.html', cases=cases)

# 案例详情页面
@app.route('/case/<case_id>')
def case_detail(case_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # 获取案例基本信息
    cursor.execute('SELECT * FROM cases WHERE case_id = ?', (case_id,))
    case = cursor.fetchone()
    
    # 获取证据列表
    cursor.execute('SELECT * FROM evidence WHERE case_id = ?', (case_id,))
    evidence = cursor.fetchall()
    
    # 获取外部链接
    cursor.execute('SELECT * FROM external_links WHERE case_id = ?', (case_id,))
    links = cursor.fetchall()
    
    # 获取案件进展
    cursor.execute('SELECT * FROM case_progress WHERE case_id = ?', (case_id,))
    progress = cursor.fetchall()
    
    conn.close()
    
    return render_template('case_detail.html', 
        case=case, 
        evidence=evidence,
        links=links,
        progress=progress
    )

# 产品功能清单页面
@app.route('/features')
def feature_list():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # 功能清单数据
    features = {
        'implemented': {
            '数据管理': [
                {'name': '案例基础信息管理', 'status': True, 'description': '支持案例的创建、查看、编辑'},
                {'name': '证据材料管理', 'status': True, 'description': '支持证据的上传、存储、查看'},
                {'name': '外部链接管理', 'status': True, 'description': '支持相关链接的添加和状态追踪'},
                {'name': '案件进展管理', 'status': True, 'description': '记录案件处理的各个阶段'}
            ],
            '用户功能': [
                {'name': '用户登录', 'status': True, 'description': '基础的用户认证'},
                {'name': '案例列表查看', 'status': True, 'description': '查看所有案例'},
                {'name': '案例详情查看', 'status': True, 'description': '查看单个案例的详细信息'}
            ]
        },
        'planned': {
            '系统管理': [  # 新增系统管理分类
                {'name': '人员管理', 'status': False, 'description': '管理系统用户，包括添加、编辑、删除和查看用户信息'},
                {'name': '权限管理', 'status': False, 'description': '管理用户权限，设置不同角色的操作权限'},
                {'name': '系统日志', 'status': False, 'description': '记录和查看系统操作日志，追踪用户行为'}
            ],
            '数据采集': [
                {'name': '自动化数据采集', 'status': False, 'description': '自动从各平台收集维权案例'},
                {'name': '智能数据分类', 'status': False, 'description': '自动对案例进行分类'},
                {'name': '证据自动保全', 'status': False, 'description': '自动保存相关证据'}
            ],
            '用户功能': [
                {'name': '用户注册', 'status': False, 'description': '新用户注册功能'},
                {'name': '密码重置', 'status': False, 'description': '忘记密码后的重置功能'},
                {'name': '个人中心', 'status': False, 'description': '用户个人信息管理'}
            ],
            '高级功能': [
                {'name': '案例分析', 'status': False, 'description': '数据分析和可视化'},
                {'name': '报告生成', 'status': False, 'description': '自动生成分析报告'},
                {'name': '预警系统', 'status': False, 'description': '风险预警功能'}
            ]
        }
    }
    
    return render_template('feature_list.html', features=features)

# 新增功能
@app.route('/features/add', methods=['POST'])
def add_feature():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    data = request.json
    category = data.get('category')
    feature = {
        'name': data.get('name'),
        'description': data.get('description'),
        'status': data.get('status', False)
    }
    
    # 在实际应用中，这里应该将数据存储到数据库
    if feature['status']:
        features['implemented'].setdefault(category, []).append(feature)
    else:
        features['planned'].setdefault(category, []).append(feature)
    
    return jsonify({'success': True})

# 编辑功能
@app.route('/features/edit', methods=['POST'])
def edit_feature():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    data = request.json
    # 在实际应用中，这里应该更新数据库中的数据
    return jsonify({'success': True})

@app.route('/api/case/<case_id>')
def get_case_detail(case_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # 获取案例基本信息
        cursor.execute('SELECT * FROM cases WHERE case_id = ?', (case_id,))
        case = cursor.fetchone()
        print(f"Debug - Case data: {case}")
        
        if not case:
            print(f"No case found for ID: {case_id}")
            return jsonify({'error': 'Case not found'}), 404
            
        # 获取证据列表
        cursor.execute('SELECT * FROM evidence WHERE case_id = ?', (case_id,))
        evidence = cursor.fetchall()
        print(f"Debug - Evidence data: {evidence}")
        
        # 获取案件进展
        cursor.execute('SELECT * FROM case_progress WHERE case_id = ? ORDER BY date ASC', (case_id,))
        progress = cursor.fetchall()
        print(f"Debug - Progress data: {progress}")
        
        conn.close()
        
        # 转换为字典格式
        case_dict = {
            'case_id': case[0],
            'title': case[1],
            'type': case[2],
            'platform': case[3],
            'amount': case[4],
            'victim_count': case[5],
            'status': case[6],
            'created_at': case[7],
            'updated_at': case[8]
        }
        
        evidence_list = [{
            'id': e[0],
            'type': e[2],
            'file_path': e[3],
            'file_hash': e[4],
            'upload_time': e[5],
            'description': e[6]
        } for e in evidence]
        
        progress_list = [{
            'stage': p[2],
            'description': p[3],
            'date': p[4],
            'operator': p[5]
        } for p in progress]
        
        return jsonify({
            'case': case_dict,
            'evidence': evidence_list,
            'progress': progress_list
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 