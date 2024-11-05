const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');
const Case = require('./Case');

const ProcessLog = sequelize.define('ProcessLog', {
  date: {
    type: DataTypes.DATE,
    defaultValue: DataTypes.NOW
  },
  content: {
    type: DataTypes.TEXT,
    allowNull: false
  }
});

// 建立模型关联
ProcessLog.belongsTo(Case);
Case.hasMany(ProcessLog);

module.exports = ProcessLog; 