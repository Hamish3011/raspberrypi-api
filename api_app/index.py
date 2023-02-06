from flask import Flask, jsonify, request, render_template, url_for, flash, redirect

from api_app.model.expense import Expense, ExpenseSchema
from api_app.model.income import Income, IncomeSchema
from api_app.model.transaction_type import TransactionType

import logging

logger = logging.getLogger("test")
logger.setLevel(level=logging.DEBUG)

logFileFormatter = logging.Formatter(
	fmt=f"%(levelname)s %(asctime)s (%(relativeCreated)d) \t %(pathname)s F%(funcName)s L%(lineno)s - %(message)s",
	datefmt="%Y-%m-%d %H:%M:%S"
)
fileHandler = logging.FileHandler(filename='logs/output.log')
fileHandler.setFormatter(logFileFormatter)
fileHandler.setLevel(level=logging.INFO)

logger.addHandler(fileHandler)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some secret key'

transactions = [
	Income('Salary',5000),
	Income('Dividends',200),
	Expense('pizza',50),
	Expense('Concert',100)
]


@app.route('/')
def index():
	return render_template('index.html',messages=transactions)


@app.route('/create/', methods=('GET','POST'))
def create():
	if request.method == 'POST':
		amount = request.form['amount']
		description = request.form['description']
		if not amount:
			flash('Amount is required')
		elif not description:
			flash('Description is required')
		else:
			logger.info('create called successfully')
			return "Success"
	return render_template('create.html')


@app.route("/incomes")
def get_incomes():
	logger.info("Navigated to incomes")
	schema = IncomeSchema(many=True)
	incomes = schema.dump(
		filter(lambda t: t.type == TransactionType.INCOME, transactions)
	)
	return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
	logger.info(request.get_json())
	income = IncomeSchema().load(request.get_json())
	transactions.append(income)
	return '',204


@app.route("/expenses")
def get_expenses():
	#logger.info*("Navigated to expenses")
        schema = ExpenseSchema(many=True)
        expenses = schema.dump(
                filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
        )
        return jsonify(expenses)


@app.route('/expenses', methods=['POST'])
def add_expense():
	#logger.info("Add Expense")
        expense = ExpenseSchema().load(request.get_json())
        transactions.append(expense)
        return '',204


if __name__ == "__main__":
	app.run()
