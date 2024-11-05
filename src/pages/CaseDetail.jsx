import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './CaseDetail.css';

function CaseDetail() {
  const { id } = useParams();
  const [caseDetail, setCaseDetail] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCaseDetail = async () => {
      try {
        const response = await axios.get(`/api/cases/${id}`);
        setCaseDetail(response.data);
      } catch (error) {
        console.error('获取案例详情失败:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCaseDetail();
  }, [id]);

  if (loading) return <div>加载中...</div>;
  if (!caseDetail) return <div>未找到相关案例</div>;

  return (
    <div className="case-detail-container">
      <div className="case-header">
        <h2>{caseDetail.title}</h2>
        <span className="case-status">{caseDetail.status}</span>
      </div>
      
      <div className="case-info-grid">
        <div className="info-item">
          <label>案例编号</label>
          <span>{caseDetail.caseNumber}</span>
        </div>
        <div className="info-item">
          <label>类型</label>
          <span>{caseDetail.type}</span>
        </div>
        <div className="info-item">
          <label>平台</label>
          <span>{caseDetail.platform}</span>
        </div>
        <div className="info-item">
          <label>涉案金额</label>
          <span>¥{caseDetail.amount.toLocaleString()}</span>
        </div>
        <div className="info-item">
          <label>受害人数</label>
          <span>{caseDetail.victimCount}人</span>
        </div>
      </div>

      <div className="case-detail-section">
        <h3>案例描述</h3>
        <p>{caseDetail.description}</p>
      </div>

      <div className="case-detail-section">
        <h3>处理过程</h3>
        <div className="process-timeline">
          {caseDetail.processLogs?.map((log, index) => (
            <div key={index} className="timeline-item">
              <div className="timeline-date">{log.date}</div>
              <div className="timeline-content">{log.content}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default CaseDetail; 