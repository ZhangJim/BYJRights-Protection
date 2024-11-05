const express = require('express');
const sequelize = require('./config/database');
const casesRouter = require('./routes/cases');

const app = express();

app.use(express.json());
app.use('/api', casesRouter);

// 同步数据库模型
sequelize.sync({ alter: true })
  .then(() => {
    console.log('数据库模型同步完成');
  })
  .catch(err => {
    console.error('数据库模型同步失败:', err);
  });

const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
}); 