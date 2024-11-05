import { useNavigate } from 'react-router-dom';

function List() {
  const navigate = useNavigate();

  // 现有代码...

  return (
    <div className="list-container">
      {items.map(item => (
        <div 
          key={item.id} 
          className="list-item"
          onClick={() => handleItemClick(item)}  // 添加点击事件
        >
          {/* 现有的列表项内容 */}
          <div className="item-basic-info">
            <h3>{item.title}</h3>
            <p>{item.description}</p>
          </div>
          
          {/* 添加查看详情按钮 */}
          <button 
            className="detail-btn"
            onClick={(e) => {
              e.stopPropagation();  // 防止触发父元素的点击事件
              handleViewDetail(item);
            }}
          >
            查看详情
          </button>
        </div>
      ))}
    </div>
  );
} 

// 在列表项中添加跳转
const handleViewDetail = (item) => {
  navigate(`/cases/${item.caseNumber}`);  // 使用案例编号作为路由参数
};