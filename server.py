from flask import *
from mongo import user_exist, username_taken, get_data, put_confirmation_token, get_confirmation_token, user_create
from mailer import send_join_mail


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

@app.route('/', methods=['GET', 'POST'])
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'users' not in session or len(session["users"]) == 0:
        return redirect("/login")
    return render_template("accounts-12.html", username="User 1", accounts=["ivanpush27@gmail.com", "hbr.tip@gmail.com", "admin@ya.ru"])


@app.route('/confirm', methods=['GET', 'POST'])
def confirm_join():
    token = request.args.get("token", "")
    if token:
        response, message = get_confirmation_token(token)
        print(response, message)
        if response:
            username, password = message
            response, data = user_create(username, password)
            if response:
                if "users" not in session:
                    session["users"] = {}
                session["users"][username] = data
                if "order" not in session["users"]:
                    session["users"]["order"] = []
                session["users"]["order"].append(username)
                print(session["users"])
                return redirect("/")
    return render_template("login.html")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("got it")
        username, password = request.form.get("username", ""), request.form.get("password", "")
        print(username, password)
        if username and password:
            print("there")
            if user_exist(username, password):
                if "users" not in session:
                    session["users"] = {}
                session["users"][username] = {
                    "username": username
                }
                if "order" not in session["users"]:
                    session["users"]["order"] = []
                session["users"]["order"].append(username)
                print(session["users"])
                return redirect("/")
            else:
                print("nope")
                return render_template("login.html", attempt=True)
    return render_template("login.html")


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        print("got it register")
        email, password = request.form.get("email", ""), request.form.get("password", "")
        print(email, password)
        if email and password:
            print("lol rly")
            if not username_taken(email):
                print("rendering success")
                token = put_confirmation_token(email, password)
                send_join_mail(email, token)
                return render_template("join_success.html")
            else:
                print("oops")
                return render_template("registration.html", attempt=True)
    return render_template("registration.html")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', threaded=True)
    app.app_context().push()
