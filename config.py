# import pymysql
# 配置数据库信息
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'hr'
USERNAME = "root"
PASSWORD = '123456'
DB_URI = \
    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
# DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf-8".format(HOSTNAME, PORT, DATABASE, USERNAME, PASSWORD)
SQLALCHEMY_DATABASE_URI = DB_URI
# conn = pymysql.connect(
#     host='127.0.0.1',
#     user='root',
#     password='123456',
#     db='student',
#     charset='utf8mb4'
# )












# # 启用用户
# @bp.route("/enable_users", methods=['PUT'])
# def enable_users():
#     try:
#         data = request.get_json()
#         if not data or not data.get("userIds"):
#             return jsonify({"error": "Invalid request data"}), 400

#         user_ids = data.get("userIds")
#         print("Received User IDs to disable:", user_ids)  # 添加这行打印语句
#         users_to_enable = User_add.query.filter(User_add.id.in_(user_ids)).all()
#         for user in users_to_enable:
#             user.status = '启用'
#         db.session.commit()  # 保存更改到数据库

#         return jsonify({"success": True})
#     except Exception as e:
#         print(f"Error during enabling users: {str(e)}")
#         return jsonify({"success": False, "error": "启用用户失败，请重试。"}), 500

# # 禁用用户
# @bp.route("/disable_users", methods=['PUT'])
# def disable_users():
#     try:
#         data = request.get_json()
#         if not data or not data.get("userIds"):
#             return jsonify({"error": "Invalid request data"}), 400

#         user_ids = data.get("userIds")
#         print("Received User IDs to disable:", user_ids)  # 添加这行打印语句
#         users_to_disable = User_add.query.filter(User_add.id.in_(user_ids)).all()
#         for user in users_to_disable:
#             user.status = '禁用'
#         db.session.commit()  # 保存更改到数据库

#         return jsonify({"success": True})
#     except Exception as e:
#         print(f"Error during disabling users: {str(e)}")
#         db.session.rollback()  # 回滚更改
#         return jsonify({"success": False, "error": "禁用用户失败，请重试。"}), 500

# #  删除用户
# @bp.route("/delete_user/<int:user_id>", methods=['DELETE'])
# def delete_user(user_id):
#     try:
#         user_to_delete = User_add.query.get(user_id)
#         if not user_to_delete:
#             return jsonify({"error": "用户不存在"}), 404

#         db.session.delete(user_to_delete)
#         db.session.commit()

#         return jsonify({"success": True})
#     except Exception as e:
#         print(f"Error during deleting user: {str(e)}")
#         db.session.rollback()
#         return jsonify({"success": False, "error": "删除用户失败，请重试。"}), 500
