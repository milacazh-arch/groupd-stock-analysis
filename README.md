# GroupD - 股票智能分析平台

GroupD是一个专业的股票智能分析平台，基于Flask和Tushare API构建，提供全面的股票数据分析、趋势预测和投资决策支持。

## 🚀 主要功能

### 📈 核心分析功能
- **股票概述**：获取股票基本信息（代码、名称、行业、市场等）
- **盈利分析**：查看近3年的营业收入、营业利润、净利润等数据
- **市场估值**：显示市盈率(PE)、市净率(PB)、市销率(PS)等估值指标
- **股权收益**：分析总资产、总负债、股东权益和净资产收益率(ROE)

### 🎯 智能预测功能
- **股价走势图**：交互式历史价格和成交量图表
- **业绩趋势分析**：收入增长、利润趋势可视化分析
- **未来趋势预测**：基于业绩和价格趋势的智能预测
- **投资建议**：看涨/看跌/中性趋势判断及置信度

## 🛠 快速开始

### 方法一：传统部署

#### 1. 安装依赖
```bash
cd stock_analysis_app
pip install -r requirements.txt
```

#### 2. 配置环境
复制环境配置文件并设置Tushare Token：
```bash
cp .env.example .env
# 编辑 .env 文件，设置你的 TUSHARE_TOKEN
```

#### 3. 运行应用
```bash
python app.py
```

#### 4. 访问应用
打开浏览器访问：http://localhost:5001

### 方法二：Docker部署

#### 1. 构建镜像
```bash
docker build -t groupd-stock-analysis .
```

#### 2. 运行容器
```bash
docker run -d -p 5001:5001 -e TUSHARE_TOKEN=your_token_here groupd-stock-analysis
```

### 方法三：Docker Compose部署

#### 1. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，设置 TUSHARE_TOKEN
```

#### 2. 启动服务
```bash
docker-compose up -d
```

## 📊 支持的股票代码格式

- **深圳股票**：000001.SZ
- **上海股票**：600000.SH  
- **创业板**：300001.SZ
- **科创板**：688001.SH

## 🏗 项目结构

```
stock_analysis_app/
├── app.py                 # 主应用文件
├── config.py             # 配置文件
├── requirements.txt      # Python依赖
├── Dockerfile           # Docker构建文件
├── docker-compose.yml   # Docker编排配置
├── .env.example         # 环境变量示例
├── templates/
│   └── index.html       # 网页模板
├── static/
│   └── style.css        # 样式文件
└── README.md            # 说明文档
```

## 🔧 技术栈

### 后端技术
- **框架**：Flask
- **数据处理**：Pandas, NumPy
- **API集成**：Tushare金融数据接口
- **图表渲染**：Chart.js

### 前端技术
- **界面**：HTML5, CSS3, JavaScript
- **图表**：Chart.js
- **响应式设计**：CSS Grid & Flexbox

### 部署技术
- **容器化**：Docker, Docker Compose
- **生产环境**：Gunicorn (可扩展)

## 🌐 生产部署

### 云服务器部署
```bash
# 1. 上传代码到服务器
# 2. 安装Docker
curl -fsSL https://get.docker.com | sh
# 3. 使用Docker Compose部署
docker-compose up -d
```

### 环境变量配置
```bash
# .env 文件配置示例
TUSHARE_TOKEN=your_actual_token_here
FLASK_ENV=production
HOST=0.0.0.0
PORT=5001
```

## 📈 预测算法

GroupD采用智能预测算法，基于以下指标进行趋势判断：

1. **收入增长率**：计算最新季度收入同比增长
2. **价格趋势**：分析最近30个交易日的价格变化
3. **业绩稳定性**：评估盈利能力的连续性

**趋势分类**：
- 🟢 强烈看涨：收入增长>20%且价格趋势>10%
- 🟡 看涨：收入增长>10%且价格趋势为正
- 🔴 看跌：收入增长<-10%且价格趋势<-5%
- ⚪ 中性：其他情况

## ⚠️ 注意事项

- **API限制**：请确保已注册Tushare账号并获取有效的API Token
- **数据延迟**：部分数据可能存在T+1的更新延迟
- **投资风险**：本平台提供分析参考，不构成投资建议
- **网络要求**：应用需要稳定的网络连接以调用Tushare API

## 🔄 更新日志

### v2.0 (当前版本)
- ✅ 品牌升级为GroupD
- ✅ 新增智能趋势预测功能
- ✅ 添加交互式价格图表
- ✅ 支持Docker容器化部署
- ✅ 优化移动端响应式设计

### v1.0 (初始版本)
- ✅ 基础股票数据分析功能
- ✅ 财务数据展示
- ✅ 估值指标计算

## 📞 技术支持

如遇问题，请检查：
1. Tushare Token是否正确配置
2. 网络连接是否正常
3. 股票代码格式是否正确

---

**GroupD - 让投资决策更智能** 🚀
