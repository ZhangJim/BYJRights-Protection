import { Routes, Route } from 'react-router-dom';
import CaseDetail from './pages/CaseDetail';

function App() {
  return (
    <div className="App">
      <Routes>
        {/* 保留原有路由 */}
        <Route path="/" element={<CaseList />} />
        {/* 添加新的详情页路由 */}
        <Route path="/cases/:id" element={<CaseDetail />} />
      </Routes>
    </div>
  );
}

export default App;