# System Design for SEO Project #2

## System Architecture:

Here is a high-level system architecture design of our proposed trading application:

1. **User Interface (UI)**: This is the front-end part of the application where users interact with the system. It's designed to be intuitive and easy to navigate. It consists of elements for portfolio management, AI advisor, and trader copy settings.

2. **Backend Server**: This is where the core business logic of the application resides. It is responsible for performing operations such as executing trades, fetching user account details, and managing portfolio balances.

3. **Database**: This component stores all relevant user data, including account details, trading history, and portfolio details. We'll use an SQL database for structured, reliable, and efficient storage.

4. **OpenAI's GPT API**: This will be used to generate AI advice based on the user's current account holdings and positions. 

5. **Sec-api.io and Senator Trading APIs**: These will provide information about institutional ownership and senator trades, respectively. This data can be used to mimic successful traders or provide input for AI advice.

6. **Brokerage APIs (TD Ameritrade and Robinhood)**: These APIs will allow our application to fetch user account data and execute trades on their behalf.

Here's a simple diagram of the system:

```
                              +------------------+
                              | User Interface   |
                              +------------------+
                                        |
                                        V
                              +------------------+
                              | Backend Server   |
                              +------------------+
                                        |
                                        V
                              +------------------+
                              | Database         |
                              +------------------+
                                        |
                                        V
                  +------------------+         +------------------+
                  | Brokerage APIs   |         | Data APIs        |
                  +------------------+         +------------------+
                                        |
                                        V
                              +------------------+
                              | OpenAI's GPT API |
                              +------------------+
```

## Core Functionalities:

1. **Account Management**: Users should be able to link their brokerage account, view balances and current holdings, and unlink their account if necessary.

2. **Portfolio Management**: Users should be able to view and manage their portfolios, set rebalancing schedules, and manually rebalance if necessary.

3. **AI Advisor**: The AI advisor should provide advice based on the user's current holdings, market trends, and global news. Users should also be able to ask follow-up questions.

4. **Trader Copy**: Users should be able to follow public traders and have their portfolio mimic the trader's moves.

## Data Flow:

1. When a user links their brokerage account, the backend server uses the brokerage API to fetch account information.

2. This information is then stored in the SQL database.

3. When the user requests AI advice, the backend server fetches the necessary information from the database and sends a request to the OpenAI's GPT API.

4. When a user decides to follow a trader, the backend server uses the Sec-api.io and Senator Trading APIs to fetch the trader's data, which is then stored in the database. 

5. The backend server checks the database regularly to determine if a new trade needs to be executed to match the followed trader.

6. If a new trade is required, the backend server uses the brokerage API to execute the trade.

This system design should provide a comprehensive view of how the different components of our application interact. The modular design allows for flexibility and scalability, ensuring our application can adapt and grow as required.