const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Case = sequelize.define('Case', {
  caseNumber: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  title: {
    type: DataTypes.STRING,
    allowNull: false
  },
  type: DataTypes.STRING,
  platform: DataTypes.STRING,
  amount: DataTypes.DECIMAL(10, 2),
  victimCount: DataTypes.INTEGER,
  status: DataTypes.STRING,
  description: DataTypes.TEXT
});

module.exports = Case; 