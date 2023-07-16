import robin_stocks.robinhood as r
import pyotp
def login_to_robinhood(username, password, otp):
    """
    Logs in to Robinhood with the given username and password.
    """
    # code = pyotp.TOTP(otp).now()
    login = r.login(username, password,  mfa_code = otp)
    #if otp:
        # code = pyotp.TOTP(otp).now()
    #    login = r.login(username, password,  mfa_code = otp)
    #else:
    #    login = r.login(username, password)
    return login
    

def get_holdings():
    """
    Fetches and returns the account information.
    If an account_number is provided, fetches information for that account.
    """
    return r.build_holdings()

def get_portfolio_total_value():
    """
    Retrieves account portfolio's total equity value
    """
    profile = r.build_user_profile()
    total_value = profile['total_equity']
    return total_value

def execute_trade(symbol, action, quantity):
    """
    Executes a trade.
    Args:
        symbol (str): The symbol of the stock to trade.
        action (str): The action to take ("buy" or "sell").
        quantity (int): The number of shares to trade.
    """
    if action == "buy":
        r.orders.order_buy_market(symbol, quantity)
    elif action == "sell":
        r.orders.order_sell_market(symbol, quantity)
    else:
        raise ValueError("Invalid action. Must be 'buy' or 'sell'.")

def getStockOrders():
    """Get all stock orders """
    return r.get_all_stock_orders()

def getStockName(instrument):
    return r.get_symbol_by_url(instrument)
def logout_from_robinhood():
    """
    Logs out from Robinhood.
    """
    r.logout()

def getAccountInfo():
    """Get the all account of the user"""
    return r.get_account_info()