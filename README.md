# Othello Battle Platform 黑白棋联机对战平台
Stanford逐步求精 + CS50 工程化 Python 实现，支持网页多人实时联机对战
## 在线演示
https://你的用户名.github.io/othello-battle-platform
## 功能特性
- 双人实时联机对战（WebSocket 同步棋盘、回合、分数）
- 房间匹配机制，随机生成房间号邀请好友对战
- 完整标准黑白棋规则：合法落子提示、自动跳过无棋回合、对局结算
- 分层求精架构：规则核心Python、前端网页可视化、前后端分离
- 单机离线预览 + 联网多人双模式
## 项目结构
- docs/ GitHub Pages 静态网页对战前端
- backend/ FastAPI WebSocket Python 对战服务
- test/ CS50 单元测试用例
## 本地运行
1. 启动后端
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload