from flask import Blueprint,request, jsonify
from exts import db
from Models.models import Commodity
from datetime import datetime
bp = Blueprint('commodity', __name__, url_prefix="/commodity")

# 添加数据路由
@bp.route('/add', methods=['GET', 'POST'])
def add_commodity():
    data = request.json
    billNumber = data.get('billNumber')
    startDate = data.get('startDate')
    endDate = data.get('endDate')
    productInfo = data.get('productInfo')
    state = data.get('state')
    money = data.get('money')
    customer = data.get('customer')

    commodity = Commodity(
        billNumber=billNumber,
        startDate=startDate,
        endDate=endDate,
        productInfo=productInfo,
        state=state,
        money=money,
        customer=customer
    )
    db.session.add(commodity)
    db.session.commit()

    return jsonify({'message': '订单信息添加成功'})

# 获取所有订单信息
@bp.route('/all', methods=["GET", "POST"])
def get_all_commodity():
    commodity = Commodity.query.all()
    commodity_list = []
    for commodity in commodity:
        commodity_dict = {
            'billNumber': commodity.billNumber,
            'startDate': commodity.startDate,
            'endDate': commodity.endDate,
            'productInfo':commodity.productInfo,
            'state': commodity.state,
            'money': commodity.money,
            'customer':commodity.customer
        }
        commodity_list.append(commodity_dict)
    return jsonify(commodity_list)

# 审核数据路由
@bp.route('/updateState', methods=["GET", "POST"])
def update_state():
    data = request.json
    selected_rows = data.get('selectedRows')
    
    for row in selected_rows:
        commodity = Commodity.query.filter_by(billNumber=row['billNumber']).first()
        if commodity:
            commodity.state = row['state']
            db.session.commit()
    return jsonify({'message': '状态更新成功'})


# 删除数据路由
@bp.route('/delete', methods=["GET", "POST"])
def delete_commodity():
    data = request.json
    selected_rows = data.get('selectedRows')
    # 将数据库中的信息删除
    for billNumber in selected_rows:
        commodity = Commodity.query.filter_by(billNumber=billNumber).first()
        if commodity:
            db.session.delete(commodity)
        db.session.commit()
        return jsonify({'message': '商品性信息删除成功'})