from . import main
from flask import (
    render_template,
    request,
)
from utils import process_instructions


@main.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@main.route('/submit', methods=['POST'])
def submit():
    print(request.form["code"])
    return render_template('result.html')
