from flask import Flask, render_template_string
import redis
import os

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>Shop visits</title>
<h1>Интернет-магазин — визиты: {{count}}</h1>
<p>Контейнер: {{container}}</p>
"""

@app.route("/")
def index():
    try:
        count = r.incr("hits")
    except Exception as e:
        count = f"Redis error: {e}"
    from socket import gethostname
    return render_template_string(TEMPLATE, count=count, container=gethostname())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
