from flask import Blueprint,request, jsonify
from exts import db
from Models.models import Employee
import traceback
from datetime import datetime
bp = Blueprint('employee', __name__, url_prefix="/employee")

# 添加员工考勤员工考勤路由
@bp.route('/Attendance/add', methods=['GET' ,'POST'])
def add_attendance():
    try:
        data = request.json
        name = data.get('name')
        position = data.get('position')
        start_date_str = data.get('start_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        status = data.get('status')
        on_duty = data.get('on_duty')
        end_date = data.get('end_date') or None

        # 创建员工考勤对象
        employee = Employee(
            name=name,
            position=position,
            start_date=start_date,
            status=status,
            on_duty=on_duty,
            end_date=end_date   
        )
        # 将员工考勤对象添加到数据库
        db.session.add(employee)
        db.session.commit()

        # 返回添加的员工考勤信息
        return jsonify({
            'message': 'Employee attendance data added successfully',
            'employee': {
                'id': employee.id,
                'name': employee.name,
                'position': employee.position,
                'start_date': employee.start_date.strftime('%Y-%m-%d'),
                'status': employee.status,
                'on_duty': employee.on_duty,
                'end_date': employee.end_date.strftime('%Y-%m-%d') if employee.end_date else None
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        error_message = traceback.format_exc()
        return jsonify({'message': 'Failed to add employee attendance data', 'error': str(e), 'traceback': error_message}), 500

# 前端来获取所有员工考勤信息
@bp.route('/Attendance/all', methods=['GET', 'POST'])
def get_all_attendance():
    try:
        employees = Employee.query.all()
        employee_data = []
        for employee in employees:
            employee_data.append({
                'id': employee.id,
                'name': employee.name,
                'position': employee.position,
                'start_date': employee.start_date.strftime('%Y-%m-%d'),
                'status': employee.status,
                'on_duty': employee.on_duty,
                'end_date': employee.end_date.strftime('%Y-%m-%d') if employee.end_date else None
            })
        return jsonify(employee_data), 200
    except Exception as e:
        error_message = traceback.format_exc()
        return jsonify({'message': 'Failed to fetch employee attendance data', 'error': str(e), 'traceback': error_message}), 500

# 编辑员工路由信息将员工信息重新更新到页面上
@bp.route('/Attendance/edit', methods=['GET', 'POST'])
def edit_attendance():
    try:
        data = request.json
        employee_id = data.get('id')
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({'message': 'Employee not found'}), 404
        # 如果离职日期不是null，则禁止编辑员工信息
        if employee.end_date is not None:
            return jsonify({'message': 'Cannot edit employee information after resignation'}), 400

        employee.name = data.get('name')
        employee.position = data.get('position')
        employee.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
        employee.status = data.get('status')
        employee.on_duty = data.get('on_duty')
        employee.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d') if data.get('end_date') else None

        db.session.commit()

        return jsonify({'message': 'Employee information updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        error_message = traceback.format_exc()
        return jsonify({'message': 'Failed to update employee information', 'error': str(e), 'traceback': error_message}), 500

# 员工转正路由信息
@bp.route('/Attendance/Employee_regularization', methods=['GET' ,'POST'])
def convert_to_full_time():
    data = request.json
    employee_id = data.get('id')

    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    employee.status = '正式工'
    db.session.commit()

    return jsonify({'message': 'Employee status updated successfully', 'employee': employee.serialize()}), 200

# 在 Flask 蓝图中添加以下路由
@bp.route('/Attendance/resign', methods=['GET' ,'POST'])
def resign_employee():
    try:
        data = request.json
        employee_id = data.get('id')
        # end_date_str = data.get('end_date')
        # end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        end_date_str = data.get('end_date')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        reason = data.get('reason')
        status = data.get('status')
        on_duty = data.get('on_duty')

        # 更新员工信息，标记为离职
        employee = Employee.query.get(employee_id)
        employee.end_date = end_date
        employee.status = status
        employee.on_duty = on_duty
        employee.is_delete = True

        db.session.commit()

        return jsonify({'message': 'Employee resigned successfully'}), 200
    except Exception as e:
        db.session.rollback()
        error_message = traceback.format_exc()
        return jsonify({'message': 'Failed to resign employee', 'error': str(e), 'traceback': error_message}), 500

