from flask import Blueprint, redirect, session, request, jsonify
from exts import db
from Models.models import Users

bp = Blueprint('auth', __name__, url_prefix="/auth")


# 登录路由
@bp.route("/login", methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return jsonify({"error": "用户已登录"}), 403
    if request.method == "POST":
        try:
            data = request.get_json()
            print("Received data:", data)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return jsonify({"error": "用户名和密码不能为空"}), 400

            user = Users.query.filter_by(username=username).first()

            if user and user.check_password(password):
                session['user_id'] = user.id
                return jsonify({"success": "登录成功"})
            else:
                return jsonify({"error": "用户名或密码错误"}), 401

        except Exception as e:
            print(f"Error during login: {str(e)}")
            return jsonify({"error": "登录失败，请重试。"}), 500



# 注册路由
@bp.route("/register", methods=["GET", "POST"])
def register():
    if 'user_id' in session:
        return redirect("/")
    if request.method == "POST":
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            if username is None or password is None:
                return jsonify({"error": "Invalid registration data."}), 400

            existing_user = Users.query.filter_by(username=username).first()
            if existing_user:
                return jsonify({"error": "用户名已被注册，请选择一个不同的用户名。"}), 400

            new_user = Users(username=username)

            if password is not None:
                new_user.set_password(password)
            else:
                return jsonify({"error": "密码格式不正确"}), 400

            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            return jsonify({"success": "注册成功"})

        except Exception as e:
            print(f"Error during registration: {str(e)}")
            return jsonify({"error": "注册失败，请重试。"}), 500

    return jsonify({"error": "请求无效"}), 400



