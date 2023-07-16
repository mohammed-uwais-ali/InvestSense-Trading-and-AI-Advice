from flask import Blueprint,render_template, request, jsonify
from flask_login import login_required, current_user
from modules.models import User, Portfolio
#from modules.databaseModel import User, Portfolio
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
from modules import gpt_api as gpt, db
import base64
import modules.robin_stocks_api as api
##this file is the blueprint of our app

views = Blueprint('views',__name__) #set up blueprint for our application
user = current_user

@views.route('/')
def homePage():
    list = ['aaaaaaaaaaaaaa','bbbbbbbbbbbbbb','bbbbbbbfb','fdddg','fdgdgdfgdf','dfgdfgdf','dfgdf','dfgdfgdf']
    return render_template('homePage.html', list= list)

@views.route('/myHome', methods=['GET', 'POST'])
@login_required
def home():
    """
    brokerageUserName = Brokerage.username
    brokeragePassWord = Brokerage.password"""
    my_stocks = api.get_holdings()
    holdings=[]
    #need to add to storage all the stock holdings
    for stock, data in my_stocks.items():
        holding = stock + "\n"

        holding+=f"price: {data['price']}\n"
        holding+=f"Quantity: {data['quantity']}\n"
        holding+=f"Average Buy Price: {data['average_buy_price']}\n"
        holding+=f"Equity Value: {data['equity']}\n"
        
        holdings.append(holding)
    
    #storing to database 
    account_stock_info = api.get_holdings()
    for ticker, holding in account_stock_info.items():
        stock_info = Portfolio(
            symbol=ticker,
            quantity=holding['quantity'],
            value=holding['equity'],
            percent_change=holding['percent_change'],
            equity_change=holding['equity_change'],
            type=holding['type'],
            name=holding['name'],
            id=holding['id'],
            pe_ratio=holding['pe_ratio'],
            portfolio_percentage=holding['percentage'],
            average_buy_price=holding['average_buy_price'],
            #user_id = current_user.id
        )
        db.session.add(stock_info)
    db.session.commit()
    
    #transactions
    transactions= []
    orders = api.getStockOrders()
    
    for order in orders:
        transaction = ""
        stockName = api.getStockName(order["instrument"])
        transaction+=f"Symbol: " + stockName + " \n"
        transaction+=f"Quantity: {order['quantity']}\n"
        transaction+=f"Price: {order['price']}\n"
        transaction+=f"Timestamp: {order['created_at']}\n"

        transactions.append(transaction)
        
    #redirect(url_for('views.ai_analysis'))
    #redirect(url_for('views.ai_advice'))
    return render_template('home.html', user = current_user,   holdings = holdings, transactions = transactions) #user = current_user,   ...   , transactions = transactions)

def retrieve_initial_context_from_database():
    # Query the database to retrieve stock context
    user = User.query.first() 
    # Retrieve the user's portfolio information from the database
    portfolio_entries = Portfolio.query.filter_by(user=user).order_by(Portfolio.id.desc()).all()
    initial_context = "You are a financial advisor AI, a helpful AI tool that provides financial investment advice to users after analyzing their stock portfolio. Below you will be provide you with the details of their current holdings, and you should be able to analyze them and provide recommendations based on the user's portfolio. The details will include current holdings, with each stock's details such as Symbol, Quantity, Value, Percent Change, Equity Change, Name, Portfolio Percentage, Average Buy Price. Below are the details\n"

    # Iterate over the retrieved portfolio entries and include relevant information in the initial context string
    for stock_info in portfolio:
        initial_context += f"Symbol: {stock_info.symbol}\n"
        initial_context += f"Quantity: {stock_info.quantity}\n"
        initial_context += f"Value: {stock_info.value}\n"
        initial_context += f"Percent Change: {stock_info.percent_change}\n"
        initial_context += f"Equity Change: {stock_info.equity_change}\n"
        initial_context += f"Name: {stock_info.name}\n"
        initial_context += f"Portfolio Percentage: {stock_info.portfolio_percentage}\n"
        initial_context += f"Average Buy Price: {stock_info.average_buy_price}\n\n"

    # Include additional information or instructions for the user
    initial_context += "You as a financial advisor will provide the user with advice when the user asks follow up questions and asks for strategy. You will provide financial investment-related answers or provide further details for analysis of the user's portfolio. Make sure you are conversing"

    return initial_context

@views.route('/ai_advice_page', methods=['GET'])
@login_required
def ai_advice_page():
    initial_context = retrieve_initial_context_from_database()
    initial_prompt = f"{initial_context}\n\nAI: "
    initial_ai_message = gpt.call_api(initial_prompt, '')
    return render_template('ai_advice.html', initial_ai_message=initial_ai_message)


@views.route('/ai_advice', methods=['POST'])
@login_required
def ai_advice():
    user_message = request.form.get('message')
    chat_history = request.form.get('chat_history', '')
    prompt = "Act as InvestSense, an AI Investment Advisor with the mission of demystifying financial securities. Here's the chat history:\n{chat_history}\nUser: {}"
    ai_message = gpt.call_api(prompt, user_message)
    return jsonify(ai_message=ai_message)


def retrieve_initial_context_from_database_for_analysis():
    # Query the database to retrieve stock context
    user = User.query.first() 
    # Retrieve the user's portfolio information from the database
    portfolio_entries = Portfolio.query.filter_by(user=user).order_by(Portfolio.id.desc()).all()
    initial_context = "You are a financial analyzer AI, a helpful AI tool that provides financial analsis to users about their stock holdings analyzing their stock portfolio. User will provide you with the details of their current holdings, and you should be able to analyze them and provide recommendations based on the user's portfolio. The details will include current holdings, with each stock's details such as Symbol, Quantity, Value, Percent Change, Equity Change, Name, Portfolio Percentage, Average Buy Price. Below are the details\n"

    # Iterate over the retrieved portfolio entries and include relevant information in the initial context string
    for stock_info in portfolio:
        initial_context += f"Symbol: {stock_info.symbol}\n"
        initial_context += f"Quantity: {stock_info.quantity}\n"
        initial_context += f"Value: {stock_info.value}\n"
        initial_context += f"Percent Change: {stock_info.percent_change}\n"
        initial_context += f"Equity Change: {stock_info.equity_change}\n"
        initial_context += f"Name: {stock_info.name}\n"
        initial_context += f"Portfolio Percentage: {stock_info.portfolio_percentage}\n"
        initial_context += f"Average Buy Price: {stock_info.average_buy_price}\n\n"

    # Include additional information or instructions for the user
    initial_context += "You as a financial analyzer AI will provide a breakdown of each stock (keep it only one line), and then analyze everything"

    return initial_context

#TODO:: create a def method for /ai-analysis

