const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('cases_db', 'root', 'your_password', {
  host: 'localhost',
  dialect: 'mysql',
  logging: false
});

// 测试数据库连接
sequelize.authenticate()
  .then(() => {
    console.log('数据库连接成功');
  })
  .catch(err => {
    console.error('数据库连接失败:', err);
  });

module.exports = sequelize; 