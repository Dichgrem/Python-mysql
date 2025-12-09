from flask import Flask, request, jsonify, render_template, redirect, url_for
from database import connect_db, close_db, db
from models import Account, BankTransaction
from controllers.bank_controller import create_account, deposit, withdraw, transfer

app = Flask(__name__, template_folder='templates')

@app.before_request
def _before():
    connect_db()

@app.teardown_request
def _teardown(exc):
    close_db()

def init_data():
    db.connect(reuse_if_open=True)
    db.create_tables([Account, BankTransaction])
    if Account.select().count() == 0:
        create_account('Alice', 1000)
        create_account('Bob', 800)
        create_account('Charlie', 500)
    db.close()

@app.route('/accounts', methods=['GET'])
def api_accounts():
    items = [{'id': a.id, 'name': a.name, 'balance': a.balance} for a in Account.select().order_by(Account.id)]
    return jsonify(items)

@app.route('/account/create', methods=['POST'])
def api_account_create():
    data = request.get_json(force=True)
    aid = create_account(data.get('name', ''), int(data.get('balance', 0)))
    if aid:
        return jsonify({'ok': True, 'account_id': aid})
    return jsonify({'ok': False}), 400

@app.route('/deposit', methods=['POST'])
def api_deposit():
    data = request.get_json(force=True)
    ok = deposit(int(data.get('account_id')), int(data.get('amount')))
    return jsonify({'ok': ok}), (200 if ok else 400)

@app.route('/withdraw', methods=['POST'])
def api_withdraw():
    data = request.get_json(force=True)
    ok = withdraw(int(data.get('account_id')), int(data.get('amount')))
    return jsonify({'ok': ok}), (200 if ok else 400)

@app.route('/transfer', methods=['POST'])
def api_transfer():
    data = request.get_json(force=True)
    ok = transfer(int(data.get('from_id')), int(data.get('to_id')), int(data.get('amount')))
    return jsonify({'ok': ok}), (200 if ok else 400)

@app.route('/', methods=['GET'])
def page_accounts():
    items = [{'id': a.id, 'name': a.name, 'balance': a.balance} for a in Account.select().order_by(Account.id)]
    msg = request.args.get('msg')
    err = request.args.get('err')
    return render_template('accounts.html', accounts=items, msg=msg, err=err)

@app.route('/web/deposit', methods=['POST'])
def web_deposit():
    account_id = request.form.get('account_id')
    amount = request.form.get('amount')
    if account_id and amount:
        deposit(int(account_id), int(amount))
    return redirect(url_for('page_accounts'))

@app.route('/web/withdraw', methods=['POST'])
def web_withdraw():
    account_id = request.form.get('account_id')
    amount = request.form.get('amount')
    if account_id and amount:
        withdraw(int(account_id), int(amount))
    return redirect(url_for('page_accounts'))

@app.route('/web/transfer', methods=['POST'])
def web_transfer():
    from_id = request.form.get('from_id')
    to_id = request.form.get('to_id')
    amount = request.form.get('amount')
    if not (from_id and to_id and amount):
        return redirect(url_for('page_accounts', err='提交无效'))
    ok = transfer(int(from_id), int(to_id), int(amount))
    if ok:
        return redirect(url_for('page_accounts', msg='转账成功'))
    return redirect(url_for('page_accounts', err='转账失败：余额不足或账户无效或并发冲突'))


if __name__ == '__main__':
    init_data()
    app.run(host='0.0.0.0', port=5002, threaded=True)
