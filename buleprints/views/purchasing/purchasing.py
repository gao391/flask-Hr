from flask import Blueprint,request, jsonify, session
from exts import db
from Models.models import Purchasing
from datetime import datetime
bp = Blueprint('purchasing', __name__, url_prefix="/purchasing")


# 添加数据路由
@bp.route('/add', methods=['POST'])
def add_purchasing():
    data = request.json
    billNumber = data.get('billNumber')
    startDate = data.get('startDate')
    endDate = data.get('endDate')
    productInfo = data.get('productInfo')
    state = data.get('state')
    number = data.get('number')
    purchasingagent = data.get('purchasingagent')
    money = data.get('money')

    purchasing = Purchasing(
        billNumber=billNumber,
        startDate=startDate,
        endDate=endDate,
        productInfo=productInfo,
        state=state,
        number=number,
        purchasingagent=purchasingagent,
        money=money
    )
    db.session.add(purchasing)
    db.session.commit()

    return jsonify({'message': '购买信息添加成功'})


# 获取所有购买信息
@bp.route('/all', methods=["GET", "POST"])
def get_all_purchasing():
    purchasings = Purchasing.query.all()
    purchasing_list = []
    for purchasing in purchasings:
        purchasing_dict = {
            'billNumber': purchasing.billNumber,
            'startDate': purchasing.startDate,
            'endDate': purchasing.endDate,
            'productInfo': purchasing.productInfo,
            'state': purchasing.state,
            'number': purchasing.number,
            'purchasingagent': purchasing.purchasingagent,
            'money': purchasing.money
        }
        purchasing_list.append(purchasing_dict)
    return jsonify(purchasing_list)


# 删除数据路由
@bp.route('/delete', methods=["GET", "POST"])
def delete_purchasing():
    data = request.json
    selected_rows = data.get('selectedRows')
    # 将数据库中的信息删除
    for bill_number in selected_rows:
        purchasing = Purchasing.query.filter_by(billNumber=bill_number).first()
        if purchasing:
            db.session.delete(purchasing)
    db.session.commit()
    return jsonify({'message': '购买信息删除成功'})


# 审核数据路由
@bp.route('/updateState', methods=["GET", "POST"])
def update_state():
  data = request.json
  selected_rows = data.get('selectedRows')

  for row in selected_rows:
    purchasing = Purchasing.query.filter_by(billNumber=row['billNumber']).first()
    if purchasing:
      purchasing.state = row['state']
      db.session.commit()

  return jsonify({'message': '状态更新成功'})

