from flask import Flask, jsonify
import os
from flask_cors import CORS
import config
from exts import db
from flask_migrate import Migrate
from buleprints.views.auth.auth import bp as qa_auth
from buleprints.views.auth.qa import bp as qa
from buleprints.views.employee.employee import bp as employee_bp
from buleprints.views.department.department import bp as department_bp
from buleprints.views.purchasing.purchasing import bp as purchasing_bp
from buleprints.views.commodity.commodity import bp as commodity_bp

app = Flask(__name__)
# 跨域
CORS(app)
app.secret_key = os.urandom(24)
# 绑定数据库配置文件
app.config.from_object(config)
app.secret_key = 'KisDgtDfgFGuf14352hio45'
db.init_app(app)

migrate = Migrate(app, db)
app.register_blueprint(qa_auth)
app.register_blueprint(qa)
app.register_blueprint(employee_bp)
app.register_blueprint(department_bp)
app.register_blueprint(purchasing_bp)
app.register_blueprint(commodity_bp)
if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
