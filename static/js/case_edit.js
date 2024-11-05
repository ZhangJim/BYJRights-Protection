function openEditModal(caseId) {
    // 获取案例数据
    fetch(`/api/cases/${caseId}/detail`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                fillEditForm(data.data);
                document.getElementById('caseEditModal').style.display = 'block';
            }
        });
}

function closeEditModal() {
    document.getElementById('caseEditModal').style.display = 'none';
}

function fillEditForm(data) {
    const form = document.getElementById('caseEditForm');
    
    // 填充基本信息
    form.case_id.value = data.case.case_id;
    form.title.value = data.case.title;
    form.type.value = data.case.type;
    form.platform.value = data.case.platform;
    form.amount.value = data.case.amount;
    form.victim_count.value = data.case.victim_count;
    form.status.value = data.case.status;
    form.punishment_result.value = data.case.punishment_result || '';

    // 填充案件进展，保持与详情页一致的格式
    const progressList = document.getElementById('progressList');
    progressList.innerHTML = data.progress.map((item, index) => `
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <input type="hidden" name="progress[${index}].id" value="${item.progress_id}">
            <div class="timeline-content">
                <div class="timeline-header">
                    <div class="form-group">
                        <label>阶段</label>
                        <input type="text" name="progress[${index}].stage" value="${item.stage}" class="form-control">
                    </div>
                    <div class="form-group">
                        <label>时间</label>
                        <input type="datetime-local" name="progress[${index}].date" 
                               value="${formatDateForInput(item.date)}" class="form-control">
                    </div>
                </div>
                <div class="form-group">
                    <label>描述</label>
                    <textarea name="progress[${index}].description" 
                              class="form-control">${item.description}</textarea>
                </div>
                <div class="form-group">
                    <label>处理结果</label>
                    <textarea name="progress[${index}].result" 
                              class="form-control">${item.result || ''}</textarea>
                </div>
                <div class="form-group">
                    <label>操作人</label>
                    <input type="text" name="progress[${index}].operator" 
                           value="${item.operator}" class="form-control">
                </div>
                <button type="button" class="btn-remove" onclick="removeProgress(this)">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');

    // 修改证据材料的展示部分
    const evidenceList = document.getElementById('evidenceList');
    evidenceList.innerHTML = data.evidence.map((item, index) => `
        <div class="evidence-item">
            <input type="hidden" name="evidence[${index}].id" value="${item.evidence_id}">
            <div class="evidence-info">
                <div class="evidence-title">
                    <div class="form-group">
                        <label>描述</label>
                        <input type="text" name="evidence[${index}].description" 
                               value="${item.description}" class="form-control">
                    </div>
                </div>
                <div class="evidence-meta">
                    <div class="form-group">
                        <label>类型</label>
                        <select name="evidence[${index}].type" class="form-control">
                            <option value="视频" ${item.type === '视频' ? 'selected' : ''}>视频</option>
                            <option value="图片" ${item.type === '图片' ? 'selected' : ''}>图片</option>
                            <option value="文档" ${item.type === '文档' ? 'selected' : ''}>文档</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>上传时间</label>
                        <input type="datetime-local" name="evidence[${index}].upload_time" 
                               value="${formatDateForInput(item.upload_time)}" class="form-control">
                    </div>
                </div>
            </div>
            <button type="button" class="btn-remove" onclick="removeEvidence(this)">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `).join('');

    // 添加焦点新闻的展示部分
    const newsList = document.getElementById('newsList');
    newsList.innerHTML = data.news.map((item, index) => `
        <div class="news-item">
            <input type="hidden" name="news[${index}].id" value="${item.news_id}">
            <div class="form-group">
                <label>标题</label>
                <input type="text" name="news[${index}].title" 
                       value="${item.title}" class="form-control" required>
            </div>
            <div class="news-meta">
                <div class="form-group">
                    <label>来源</label>
                    <input type="text" name="news[${index}].source" 
                           value="${item.source}" class="form-control" required>
                </div>
                <div class="form-group">
                    <label>发布时间</label>
                    <input type="datetime-local" name="news[${index}].publish_date" 
                           value="${formatDateForInput(item.publish_date)}" class="form-control">
                </div>
            </div>
            <div class="form-group">
                <label>链接</label>
                <input type="url" name="news[${index}].url" 
                       value="${item.url}" class="form-control" required>
            </div>
            <div class="form-group">
                <label>摘要</label>
                <textarea name="news[${index}].summary" 
                          class="form-control" rows="2">${item.summary}</textarea>
            </div>
            <div class="form-group">
                <label>重要程度</label>
                <select name="news[${index}].importance" class="form-control">
                    <option value="1" ${item.importance === 1 ? 'selected' : ''}>普通</option>
                    <option value="2" ${item.importance === 2 ? 'selected' : ''}>重要</option>
                    <option value="3" ${item.importance === 3 ? 'selected' : ''}>非常重要</option>
                </select>
            </div>
            <button type="button" class="btn-remove" onclick="removeNews(this)">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `).join('');
}

// 格式化日期为 input datetime-local 所需的格式
function formatDateForInput(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toISOString().slice(0, 16); // 格式: YYYY-MM-DDTHH:mm
}

// 添加新的进展记录
function addProgress() {
    const progressList = document.getElementById('progressList');
    const index = progressList.children.length;
    const newProgress = document.createElement('div');
    newProgress.className = 'timeline-item';
    newProgress.innerHTML = `
        <div class="timeline-dot"></div>
        <div class="timeline-content">
            <div class="timeline-header">
                <div class="form-group">
                    <label>阶段</label>
                    <input type="text" name="progress[${index}].stage" class="form-control" required>
                </div>
                <div class="form-group">
                    <label>时间</label>
                    <input type="datetime-local" name="progress[${index}].date" 
                           class="form-control" required>
                </div>
            </div>
            <div class="form-group">
                <label>描述</label>
                <textarea name="progress[${index}].description" 
                          class="form-control" required></textarea>
            </div>
            <div class="form-group">
                <label>处理结果</label>
                <textarea name="progress[${index}].result" class="form-control"></textarea>
            </div>
            <div class="form-group">
                <label>操作人</label>
                <input type="text" name="progress[${index}].operator" 
                       class="form-control" required>
            </div>
            <button type="button" class="btn-remove" onclick="removeProgress(this)">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    progressList.appendChild(newProgress);
}

// 添加 Toast 提示函数
function showToast(message, type = 'success') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    // 3秒后移除
    setTimeout(() => {
        toast.remove();
        // 如果没有其他 toast，移除容器
        if (toastContainer.children.length === 0) {
            toastContainer.remove();
        }
    }, 3000);
}

// 创建 Toast 容器
function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

// 修改保存函数中的提示逻辑
function handleSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {
        case_id: formData.get('case_id'),
        title: formData.get('title'),
        type: formData.get('type'),
        platform: formData.get('platform'),
        amount: parseFloat(formData.get('amount')),
        victim_count: parseInt(formData.get('victim_count')),
        status: formData.get('status'),
        punishment_result: formData.get('punishment_result'),
        evidence: collectArrayData(formData, 'evidence'),
        progress: collectArrayData(formData, 'progress'),
        news: collectArrayData(formData, 'news')
    };

    fetch(`/api/cases/${data.case_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showToast('保存成功');  // 使用 Toast 提示
            closeEditModal();
            refreshCaseList();
        } else {
            showToast(result.error || '保存失败', 'error');  // 错误提示
        }
    })
    .catch(error => {
        showToast(error.message || '保存失败', 'error');  // 错误提示
    });
}

// 辅助函数：收集数组类型的表单数据
function collectArrayData(formData, prefix) {
    const data = [];
    const entries = Array.from(formData.entries());
    
    // 找到所有属于该前缀的字段
    const fields = entries.filter(([key]) => key.startsWith(`${prefix}[`));
    
    // 根据索引分组
    const groups = fields.reduce((acc, [key, value]) => {
        const match = key.match(new RegExp(`${prefix}\\[(\\d+)\\]\\.(.+)`));
        if (match) {
            const [, index, field] = match;
            if (!acc[index]) acc[index] = {};
            acc[index][field] = value;
        }
        return acc;
    }, {});
    
    // 转换为数组
    return Object.values(groups);
}

// 添加刷新列表的函数
function refreshCaseList() {
    fetch('/cases/data')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('.case-table tbody');
            tbody.innerHTML = data.cases.map((item, index) => `
                <tr>
                    <td>${index + 1}</td>
                    <td>${item.case_id}</td>
                    <td>
                        <a href="#" class="case-title" onclick="showCaseDetail('${item.case_id}')">${item.title}</a>
                    </td>
                    <td>
                        <span class="tag">${item.type}</span>
                    </td>
                    <td>${item.platform}</td>
                    <td>¥${Number(item.amount).toLocaleString()}</td>
                    <td>${item.victim_count}人</td>
                    <td>
                        <span class="status-badge ${item.status}">${item.status}</span>
                    </td>
                    <td>
                        <div class="action-buttons">
                            <button class="btn-view" onclick="showCaseDetail('${item.case_id}')">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button class="btn-edit" onclick="openEditModal('${item.case_id}')">
                                <i class="fas fa-edit"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `).join('');
        });
} 