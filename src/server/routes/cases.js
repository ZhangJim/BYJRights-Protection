const express = require('express');
const Case = require('../models/Case');
const ProcessLog = require('../models/ProcessLog');

const router = express.Router();

router.get('/api/cases/:id', async (req, res) => {
  try {
    const caseId = req.params.id;
    const caseDetail = await Case.findOne({
      where: { id: caseId },
      include: [{
        model: ProcessLog,
        as: 'processLogs',
        order: [['createdAt', 'DESC']]
      }]
    });
    
    if (!caseDetail) {
      return res.status(404).json({ message: '未找到案例' });
    }
    
    res.json(caseDetail);
  } catch (error) {
    console.error('获取案例详情失败:', error);
    res.status(500).json({ message: '服务器错误' });
  }
});

module.exports = router; 