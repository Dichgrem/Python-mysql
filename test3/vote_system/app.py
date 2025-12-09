from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from database import connect_db, close_db, db
from models import User, Option, UserVote
from controllers.vote_controller import register, login, vote, cancel

app = Flask(__name__, template_folder='templates')

@app.before_request
def _before():
    connect_db()

@app.teardown_request
def _teardown(exc):
    close_db()

def init_data():
    db.connect(reuse_if_open=True)
    db.create_tables([User, Option, UserVote])
    if Option.select().count() == 0:
        for i in range(1, 11):
            Option.create(title=f"选项{i}")
    if User.select().count() == 0:
        register("user1", "pass1")
        register("user2", "pass2")
        register("user3", "pass3")
    db.close()

@app.route('/register', methods=['POST'])
def api_register():
    data = request.get_json(force=True)
    uid = register(data.get('username', ''), data.get('password', ''))
    if uid:
        return jsonify({'ok': True, 'user_id': uid})
    return jsonify({'ok': False}), 400

@app.route('/login', methods=['POST'])
def api_login():
    data = request.get_json(force=True)
    uid = login(data.get('username', ''), data.get('password', ''))
    if uid:
        return jsonify({'ok': True, 'user_id': uid})
    return jsonify({'ok': False}), 401

@app.route('/options', methods=['GET'])
def api_options():
    items = [{'id': o.id, 'title': o.title, 'count': o.vote_count} for o in Option.select().order_by(Option.id)]
    return jsonify(items)

@app.route('/vote', methods=['POST'])
def api_vote():
    data = request.get_json(force=True)
    ok = vote(int(data.get('user_id')), int(data.get('option_id')))
    return jsonify({'ok': ok}), (200 if ok else 409)

@app.route('/cancel', methods=['POST'])
def api_cancel():
    data = request.get_json(force=True)
    ok = cancel(int(data.get('user_id')))
    return jsonify({'ok': ok}), (200 if ok else 409)

# UI routes
@app.route('/', methods=['GET'])
def page_index():
    uid = request.cookies.get('user_id')
    if not uid:
        return render_template('login.html')
    u = User.get_or_none(User.id == int(uid))
    opts = list(Option.select().order_by(Option.id))
    uv = UserVote.select().where(UserVote.user == u).order_by(UserVote.created_at.desc()).first() if u else None
    msg = request.args.get('msg')
    err = request.args.get('err')
    return render_template('options.html', user=u, options=opts, current_option_id=(uv.option_id if uv else None), msg=msg, err=err)

@app.route('/web/register', methods=['POST'])
def web_register():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    uid = register(username, password)
    if not uid:
        return redirect(url_for('page_index'))
    resp = make_response(redirect(url_for('page_index')))
    resp.set_cookie('user_id', str(uid))
    return resp

@app.route('/web/login', methods=['POST'])
def web_login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    uid = login(username, password)
    if not uid:
        return redirect(url_for('page_index'))
    resp = make_response(redirect(url_for('page_index')))
    resp.set_cookie('user_id', str(uid))
    return resp

@app.route('/web/logout', methods=['POST'])
def web_logout():
    resp = make_response(redirect(url_for('page_index'))) 
    resp.delete_cookie('user_id')
    return resp

@app.route('/web/vote', methods=['POST'])
def web_vote():
    uid = request.cookies.get('user_id')
    option_id = request.form.get('option_id')
    if not uid or not option_id:
        return redirect(url_for('page_index', err='提交无效'))
    ok = vote(int(uid), int(option_id))
    if ok:
        return redirect(url_for('page_index', msg='投票成功'))
    return redirect(url_for('page_index', err='投票失败：可能已投票或选项不存在'))

@app.route('/web/cancel', methods=['POST'])
def web_cancel():
    uid = request.cookies.get('user_id')
    if not uid:
        return redirect(url_for('page_index', err='未登录'))
    ok = cancel(int(uid))
    if ok:
        return redirect(url_for('page_index', msg='取消成功'))
    return redirect(url_for('page_index', err='取消失败：未找到投票'))

if __name__ == '__main__':
    init_data()
    app.run(host='0.0.0.0', port=5001, threaded=True)
