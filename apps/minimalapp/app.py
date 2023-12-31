from flask import (
    Flask, 
    render_template, 
    url_for, 
    current_app, 
    g, 
    request, 
    redirect, 
    flash,
    make_response,
    session
)
from email_validator import validate_email, EmailNotValidError
import logging
from flask_debugtoolbar import DebugToolbarExtension

# Flaskクラスをインスタンス化する
app = Flask(__name__)
# SECRET_KEYを追加する
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
# ログレベルを設定する
app.logger.setLevel(logging.DEBUG)
# リダイレクトを中断しないようにする
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# DebugToolBarExtensionにアプリケーションをセットする
toolbar = DebugToolbarExtension(app)
@app.route("/", endpoint="index")
def index():
    return "Hello, Flaskbook!"

# @app.get("/hello")
# @app.post("/hello")
@app.route("/hello/<name>",
           methods=["GET", "POST"],
           endpoint="hello-endpoint")
def hello(name):
    return f"Hello, {name}!"

@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)

# with app.test_request_context():
#     # /
#     print(url_for("index"))
#     # /hello/world
#     print(url_for("hello-endpoint", name="world"))
#     # /name/ichiro?page=1
#     print(url_for("show_name"), name="ichiro", page="1")

# アプリケーションコンテキストを取得してスタックへpushする
ctx = app.app_context()
ctx.push()

# current_appにアクセスが可能になる
print(current_app.name)

# グローバルなテンポラリ領域に値を設定する
# データベースの接続接続などに利用する
g.connection = "connection"
print(g.connection)

# リクエストコンテキスト
with app.test_request_context("/users?updated=true"):
    # trueが出力される
    print(request.args.get("updated"))

# お問い合わせページを表示する
@app.route("/contact")
def contact():
    # レスポンスオブジェクトを取得する
    response = make_response(render_template("contact.html"))

    # クッキーを設定する
    response.set_cookie("flaskbook key", "flaskbook value")

    # セッションを設定する
    session["username"] = "ichiro"
    # return render_template("contact.html")
    # レスポンスオブジェクトを返す
    return response

# お問い合わせ完了
@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # form属性を使ってフォームの値を取得する
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 入力チェック
        is_valid = True

        if not username:
            flash("ユーザー名は必須です")
            is_valid = False

        if not email:
            flash("メールアドレスは必須です")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False

        if not description:
            flash("お問い合わせ内容は必須です。")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))
        # メールを送る

        flash("お問い合わせ内容はメールにて送信しました。お問合せありがとうございます。")
        # contactエンドポイントへリダイレクトする
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")