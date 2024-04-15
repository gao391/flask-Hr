from exts import db
from werkzeug.security import generate_password_hash, check_password_hash

# 用户账号密码
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 员工考勤表
class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 名字
    name = db.Column(db.String(255), nullable=False)
    # 职位
    position = db.Column(db.String(255), nullable=False)
    # 入职日期
    start_date = db.Column(db.Date, nullable=False)
    # 离职日期
    end_date = db.Column(db.Date, default=None)
    # 员工状态
    status = db.Column(db.String(255), nullable=False)
    # 是否在岗位
    on_duty = db.Column(db.String(255), nullable=False)
    # 是否离职
    is_delete = db.Column(db.Boolean, default=False, nullable=False)
    # 离职原因
    reason_for_leaving = db.Column(db.String(512), nullable=True)
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'status': self.status,
            'on_duty': self.on_duty,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'reason_for_leaving': self.reason_for_leaving,
        }
    
# 用户管理表
class User_add(db.Model):
    __tablename__ = 'User_add'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户登录名字
    login_name = db.Column(db.String(255), nullable=False)
    # 用户姓名
    users_name = db.Column(db.String(255), nullable=False)
    # 用户类型
    customer_type = db.Column(db.String(255), nullable=False)
    # 角色 
    role = db.Column(db.String(255), nullable=False)
    # 电话号码
    phone = db.Column(db.Integer(), nullable=False)
    # 状态
    status = db.Column(db.String(255), nullable=False)
    # 密码
    password = db.Column(db.String(255), nullable=False)
    def Users_add(self):
        return{
            'id': self.id,
            'login_name': self.login_name,
            'user_name': self.users_name,
            'customer_type': self.customer_type,
            'role': self.role,
            'phone': self.phone,
            'status': self.status,
            'password': self.password
        }

# 房地产订单管理
class Purchasing(db.Model):
    __tablename__ = 'Purchasing'
    id = db.Column(db.Integer, primary_key=True)
    billNumber = db.Column(db.String(255), nullable=False)
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    productInfo = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    purchasingagent = db.Column(db.String(255), nullable=False)
    money = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"RealEstateOrder(id={self.id}, billNumber='{self.billNumber}', startDate='{self.startDate}', endDate='{self.endDate}', productInfo='{self.productInfo}', state='{self.state}', number={self.number}, purchasingagent='{self.purchasingagent}', money={self.money})"
    
# 商品订单
class Commodity(db.Model):
    __tablename__ = 'Commodity'
# ID自增
    id = db.Column(db.Integer, primary_key=True)
    # 订单编号
    billNumber = db.Column(db.String(255), nullable=False)
    # 起始日期
    startDate = db.Column(db.Date, nullable=False)
    # 结束日期
    endDate = db.Column(db.Date, nullable=False)
    # 商品信息
    productInfo = db.Column(db.String(255), nullable=False)
    # 审核状态
    state = db.Column(db.Enum('通过', '未通过'), nullable=False, default='通过')
    # 客户
    customer = db.Column(db.String(255), nullable=False)
    # 金额
    money = db.Column(db.Numeric(10, 2), nullable=False)
    
