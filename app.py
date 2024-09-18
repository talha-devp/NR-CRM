from flask import render_template, request, redirect, send_from_directory, url_for
from app import get_app
from api.admin import api_admin
from api.index import api_index
from app.initialize_db import create_db

app = get_app()
create_db(app)

app.secret_key = 'frC7DNd2T485'
app.register_blueprint(api_admin)
app.register_blueprint(api_index)


@app.route('/robots.txt')
def robots_txt():
    return send_from_directory('static', 'app/static/robots.txt')


@app.errorhandler(404)
def page_not_found(e):
    if request.path.startswith('/admin'):
        return redirect(url_for('api_admin.login')), 302
    else:
        return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
