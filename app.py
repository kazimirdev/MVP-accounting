from flask import Flask, render_template

from src.controllers.account import account_bp
from src.controllers.transaction import transaction_bp


app = Flask(__name__)
app.register_blueprint(account_bp, url_prefix="/account")
app.register_blueprint(transaction_bp, url_prefix="/transaction")


# Route to display home page
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
