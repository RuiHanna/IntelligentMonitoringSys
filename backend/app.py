# backend/app.py
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
import pymysql
import os, datetime, threading
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2

app = Flask(__name__)
CORS(app)

# MySQL 配置（使用 PyMySQL）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',  # 替换为真实密码
    'database': 'monitor_db',
    'cursorclass': pymysql.cursors.DictCursor
}


def get_db_connection():
    return pymysql.connect(**DB_CONFIG)


@app.route('/upload', methods=['POST'])
def upload_video():
    file = request.files['file']
    filename = file.filename
    save_path = os.path.join('uploads', filename)
    file.save(save_path)
    log('INFO', f'视频上传: {filename}')
    return jsonify({"message": "视频上传成功"})


@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'GET':
        cur.execute("SELECT * FROM system_settings WHERE id=1")
        result = cur.fetchone()
        conn.close()
        return jsonify(result)
    else:
        data = request.json
        cur.execute("""
            UPDATE system_settings
            SET retain_days=%s, max_targets=%s, detection_thresh=%s
            WHERE id=1
        """, (data['retain_days'], data['max_targets'], data['detection_thresh']))
        conn.commit()
        log('INFO', '系统设置已更新')
        conn.close()
        return jsonify({"status": "success"})


@app.route('/api/logs')
def get_logs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM system_logs ORDER BY log_time DESC LIMIT 100")
    logs = cur.fetchall()
    conn.close()
    return jsonify(logs)


@app.route('/api/targets')
def get_targets():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM target_summary ORDER BY id DESC LIMIT 100")
    targets = cur.fetchall()
    conn.close()
    return jsonify(targets)


@app.route('/api/heatmap')
def heatmap_data():
    return jsonify({
        "tooltip": {},
        "grid": {"height": "50%", "top": "10%"},
        "xAxis": {
            "type": "category",
            "data": ["0", "1", "2", "3", "4", "5"],  # 示例 x 坐标
            "splitArea": {"show": True}
        },
        "yAxis": {
            "type": "category",
            "data": ["A", "B", "C", "D"],  # 示例 y 坐标
            "splitArea": {"show": True}
        },
        "visualMap": {
            "min": 0,
            "max": 10,
            "calculable": True,
            "orient": "horizontal",
            "left": "center",
            "bottom": "15%"
        },
        "series": [{
            "name": "热力图",
            "type": "heatmap",
            "data": [
                [0, 0, 5], [1, 0, 1], [2, 0, 0],
                [0, 1, 7], [1, 1, 3], [2, 1, 6]
            ],
            "label": {"show": True},
            "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(0, 0, 0, 0.5)"}}
        }]
    })



@app.route('/api/stats')
def bar_data():
    return jsonify({
        "xAxis": {"type": "category", "data": ["person", "car"]},
        "yAxis": {"type": "value"},
        "series": [{"data": [20, 5], "type": "bar"}]
    })


def log(level, msg):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO system_logs (log_time, level, message) VALUES (%s, %s, %s)",
        (datetime.datetime.now(), level, msg))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
