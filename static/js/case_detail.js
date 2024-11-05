// 格式化日期
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// 获取证据类型对应的图标
function getEvidenceIcon(type) {
    const iconMap = {
        'image': 'fa-image',
        'document': 'fa-file-alt',
        'video': 'fa-video',
        'audio': 'fa-music',
        'other': 'fa-file'
    };
    return iconMap[type] || 'fa-file';
} 