from flask import Flask, render_template_string
import redis
import os
from socket import gethostname

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Shop visits</title>
    <style>
        body {
            background-color: #1e1e2f;
            color: #ffffff;
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 50px;
        }
        h1 {
            color: #4caf50;
        }
        .box {
            background: #2c2c3e;
            padding: 20px;
            margin: auto;
            width: 60%;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>Интернет-магазин (версия v2)</h1>
        <p><strong>Количество визитов:</strong> {{count}}</p>
        <p><strong>Обслуживающий контейнер:</strong> {{container}}</p>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    try:
        count = r.incr("hits")
    except Exception as e:
        count = f"Redis error: {e}"
    return render_template_string(
        TEMPLATE,
        count=count,
        container=gethostname()
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)