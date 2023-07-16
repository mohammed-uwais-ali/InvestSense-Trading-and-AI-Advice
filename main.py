from modules import create_app

app = create_app()

if __name__=='__main__': #only works if we run main.py file directly 
    app.run(debug=True)