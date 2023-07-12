## 安装
pip install "uvicorn[standard]"  

pip install fastapi  

pip install gunicorn

## 启动
gunicorn main:app -c gunicorn.py

## websocket
ws://0.0.0.0:8000/ws/123