from flask import Blueprint,request, jsonify, session
from exts import db
from Models.models import Users, User_add
from datetime import datetime
bp = Blueprint('department', __name__, url_prefix="/department")

# 添加用户
@bp.route("/add_user", methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request data"}), 400

        login_name = data.get("login_name")
        users_name = data.get("users_name")
        customer_type = data.get("customer_type")
        role = data.get("role")
        phone = data.get("phone")
        status = data.get("status")
        password = "123456"  # 默认密码

        if not all([login_name, users_name, customer_type, role, phone, status]):
            return jsonify({"error": "Missing required fields"}), 400

        new_user = User_add(login_name=login_name, users_name=users_name, customer_type=customer_type,
                            role=role, phone=phone, status=status, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"success": "添加用户成功"})
    except Exception as e:
        print(f"Error during adding user: {str(e)}")
        return jsonify({"error": "添加用户失败，请重试。"}), 500

# 添加注册用户信息
@bp.route("/register_login_user", methods=['POST'])
def register_login_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request data"}), 400

        username = data.get("username")
        password = data.get("password")

        if not all([username, password]):
            return jsonify({"error": "Missing required fields"}), 400

        new_login_user = Users(username=username)
        new_login_user.set_password(password)
        db.session.add(new_login_user)
        db.session.commit()

        return jsonify({"success": "注册登录账号成功"})
    except Exception as e:
        print(f"Error during registering login user: {str(e)}")
        return jsonify({"error": "注册登录账号失败，请重试。"}), 500

# 将数据库中所有的数据传递给前端
@bp.route("/all", methods=['GET'])
def get_users():
    try:
        users = User_add.query.all()
        users_list = []
        for user in users:
            users_list.append({
                "login_name": user.login_name,
                "users_name": user.users_name,
                "customer_type": user.customer_type,
                "role": user.role,
                "phone": user.phone,
                "status": user.status
            })
        return jsonify({"success": True, "data": users_list})
    except Exception as e:
        print(f"Error during getting users: {str(e)}")
        return jsonify({"success": False, "error": "获取用户信息失败"}), 500

# 删除账号
@bp.route("/delete_user", methods=['DELETE'])
def delete_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request data"}), 400

        login_name = data.get("login_name")

        if not login_name:
            return jsonify({"error": "Missing required fields"}), 400

        user = User_add.query.filter_by(login_name=login_name).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"success": True, "message": "用户删除成功"})
    except Exception as e:
        print(f"Error during deleting user: {str(e)}")
        return jsonify({"error": "删除用户失败，请重试。"}), 500

# 禁用、启用
@bp.route("/update_user", methods=['PUT', 'OPTIONS'])
def update_user():
    if request.method == 'OPTIONS':
        return jsonify({"success": True}), 200
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request data"}), 400

        login_name = data.get("login_name")

        if not login_name:
            return jsonify({"error": "Missing required fields"}), 400

        user = User_add.query.filter_by(login_name=login_name).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.status = data.get("status")
        db.session.commit()

        return jsonify({"success": True, "message": "用户禁用成功"})
    except Exception as e:
        print(f"Error during updating user: {str(e)}")
        return jsonify({"error": "禁用用户失败，请重试。"}), 500

# 重置密码
@bp.route("/reset_password", methods=['PUT', 'OPTIONS'])
def reset_password():
    if request.method == 'OPTIONS':
        return jsonify({"success": True}), 200
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request data"}), 400

        login_name = data.get("login_name")
        new_password = data.get("newPassword")

        if not all([login_name, new_password]):
            return jsonify({"error": "Missing required fields"}), 400

        # 查询user_add表中的用户
        user_add = User_add.query.filter_by(login_name=login_name).first()
        if not user_add:
            return jsonify({"error": "User not found in User_add table"}), 404

        # 更新user_add表中的密码
        user_add.password = new_password

        # 查询users表中的用户
        user = Users.query.filter_by(username=login_name).first()
        if not user:
            return jsonify({"error": "User not found in Users table"}), 404

        # 更新users表中的密码
        user.set_password(new_password)

        # 提交事务保存更改
        db.session.commit()

        return jsonify({"success": True, "message": "密码修改成功"})
    except Exception as e:
        print(f"Error during resetting password: {str(e)}")
        return jsonify({"error": "密码修改失败，请重试。"}), 500


# 更新密码
@bp.route("/update_password", methods=['PUT'])
def update_password():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request data"}), 400

        login_name = data.get("login_name")
        new_password = data.get("password")

        if not all([login_name, new_password]):
            return jsonify({"error": "Missing required fields"}), 400

        user = User_add.query.filter_by(login_name=login_name).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # 更新密码
        user.password = new_password
        db.session.commit()

        return jsonify({"success": True, "message": "密码修改成功"})
    except Exception as e:
        print(f"Error during updating password: {str(e)}")
        return jsonify({"error": "密码修改失败，请重试。"}), 500


