from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import uuid
import threading
from models.db import db, init_db
from models.task import Task
from models.alert import Alert
from utils.video_processor import process_video
from utils.tracker import DeepSORTTracker

app = Flask(__name__)
CORS(app)

# 配置
app.config.from_pyfile('config.py')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化数据库
init_db(app)


@app.route('/api/upload', methods=['POST'])
def upload_video():
    """处理视频上传"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    # 生成唯一文件名
    ext = file.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # 创建数据库任务记录
    task_id = str(uuid.uuid4())
    new_task = Task(
        id=task_id,
        filename=filename,
        status='queued'
    )
    db.session.add(new_task)
    db.session.commit()

    # 启动后台处理
    thread = threading.Thread(
        target=process_video_task,
        args=(task_id, filepath)
    )
    thread.start()

    return jsonify(new_task.to_dict())


def process_video_task(task_id, filepath):
    """后台视频处理任务"""
    with app.app_context():
        task = Task.query.get(task_id)
        try:
            task.status = 'processing'
            db.session.commit()

            # 初始化跟踪器
            tracker = DeepSORTTracker(
                model_path='models/yolov8n.pt',
                max_age=30
            )

            # 处理视频
            results = process_video(filepath, tracker)

            # 更新任务状态
            task.status = 'completed'
            task.completed_at = datetime.utcnow()
            task.object_count = len(results['tracks'])
            task.processing_time = results['processing_time']
            db.session.commit()

            # 生成报警
            generate_alerts(task_id, results['tracks'])

        except Exception as e:
            task.status = 'failed'
            task.error = str(e)
            db.session.commit()


@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    """获取所有任务"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    tasks = Task.query.order_by(Task.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    return jsonify({
        'items': [task.to_dict() for task in tasks.items],
        'total': tasks.total,
        'pages': tasks.pages,
        'current_page': tasks.page
    })


@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """获取单个任务详情"""
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)