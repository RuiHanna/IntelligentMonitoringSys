# backend/app.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pymysql
import os, datetime
from detector import process_video

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

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT detection_thresh, max_targets FROM system_settings WHERE id = 1")
        row = cur.fetchone()
    conn.close()

    detection_thresh = row[0] if row else 0.5
    max_targets = row[1] if row else 20

    # 调用检测器
    results = process_video(save_path, detection_thresh, max_targets)

    # 存入数据库
    conn = get_db_connection()
    cur = conn.cursor()
    for r in results:
        track_id = r["track_id"]
        x, y, w, h = r["bbox"]
        timestamp = r["timestamp"]

        cur.execute("""
            INSERT INTO target_summary (video_id, track_id, x, y, w, h, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (filename, track_id, x, y, w, h, timestamp))

    conn.commit()
    conn.close()

    log('INFO', f"{filename} 上传并处理，检测结果数量: {len(results)}")

    return jsonify({
        "message": "处理完成",
        "result_count": len(results),
        "results": results[:10]
    })


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

    cur.execute("""
        SELECT 
            track_id,
            MIN(timestamp) AS enter_time,
            MAX(timestamp) AS exit_time,
            COUNT(*) AS track_length
        FROM target_summary
        GROUP BY track_id
        ORDER BY track_id DESC
        LIMIT 100
    """)
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        row["object_id"] = row["track_id"]
        row["class_name"] = "person"  # 可根据后续检测结果分类替换
        # 时间格式化可选
        row["enter_time"] = datetime.datetime.fromtimestamp(row["enter_time"]).strftime("%Y-%m-%d %H:%M:%S")
        row["exit_time"] = datetime.datetime.fromtimestamp(row["exit_time"]).strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(rows)


@app.route('/api/heatmap')
def heatmap_data():
    conn = get_db_connection()
    cur = conn.cursor()

    # 示例：将 x 分成 10 格，y 分成 10 格，统计每个区域的目标数
    x_bins = 10
    y_bins = 10

    cur.execute("SELECT x, y FROM target_summary")
    rows = cur.fetchall()
    conn.close()

    heat_counts = [[0 for _ in range(x_bins)] for _ in range(y_bins)]
    for row in rows:
        x = row['x']
        y = row['y']
        if x is not None and y is not None:
            x_idx = min(int(x / 100), x_bins - 1)
            y_idx = min(int(y / 100), y_bins - 1)
            heat_counts[y_idx][x_idx] += 1

    data = []
    for y in range(y_bins):
        for x in range(x_bins):
            data.append([x, y, heat_counts[y][x]])

    return jsonify({
        "tooltip": {},
        "grid": {"height": "50%", "top": "10%"},
        "xAxis": {
            "type": "category",
            "data": [str(i) for i in range(x_bins)],
            "splitArea": {"show": True}
        },
        "yAxis": {
            "type": "category",
            "data": [str(i) for i in range(y_bins)],
            "splitArea": {"show": True}
        },
        "visualMap": {
            "min": 0,
            "max": max(map(lambda d: d[2], data)) if data else 10,
            "calculable": True,
            "orient": "horizontal",
            "left": "center",
            "bottom": "15%"
        },
        "series": [{
            "name": "热力图",
            "type": "heatmap",
            "data": data,
            "label": {"show": True},
            "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(0, 0, 0, 0.5)"}}
        }]
    })


@app.route('/api/stats')
def bar_data():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT track_id FROM target_summary")
    rows = cur.fetchall()
    conn.close()

    total = len(rows)
    unique = len(set(r['track_id'] for r in rows if r['track_id'] is not None))

    return jsonify({
        "xAxis": {"type": "category", "data": ["总轨迹数", "唯一目标数"]},
        "yAxis": {"type": "value"},
        "series": [{
            "data": [total, unique],
            "type": "bar"
        }]
    })


def log(level, msg):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO system_logs (log_time, level, message) VALUES (%s, %s, %s)",
        (datetime.datetime.now(), level, msg))
    conn.commit()
    conn.close()


@app.route('/output/<filename>')
def serve_output_video(filename):
    return send_file(f'output/{filename}', mimetype='video/mp4')


@app.route('/api/output_videos')
def list_output_videos():
    output_dir = 'output'
    videos = [f for f in os.listdir(output_dir) if f.endswith('.mp4')]
    return jsonify(videos)


if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    app.run(debug=True)
