from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def init_db(app):
    # MySQL配置 (根据实际修改)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/monitor_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # 初始化迁移
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()