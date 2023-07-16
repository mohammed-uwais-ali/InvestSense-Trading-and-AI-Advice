import robin_stocks_api as api
import robin_stocks.robinhood as r
username = "xavierdlopez@gmail.com"
password = "TestForApp123"
mfa = "011756"
str(username)
str(password)
str(mfa)
api.login_to_robinhood(username, password, mfa)

list = api.getStockOrders()

for order in list:
        #transaction = ""
        stockName = api.getStockName(order["instrument"])
        print(f"Symbol: " + stockName + " \n")
        print(f"Quantity: {order['quantity']}\n")
        print(f"Price: {order['price']}\n")
        print(f"Timestamp: {order['created_at']}\n")
#print(list[0]['quantity'])
#print(list[0]['price'])
#print(list[0]['created_at'])
#str = list[0]['instrument']
#print(r.get_symbol_by_url(str))
#x = "https://api.robinhood.com/instruments/abcdef12-3456-7890-abcd-ef1234567890/"+str
#print(r.get_symbol_by_url(x))
#for key in list[0]:
    #print(key)
    #print("--------------")
    #print(value)
#print(api.get_holdings())
#print(api.getStockOrders())