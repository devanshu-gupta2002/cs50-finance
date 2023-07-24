## Table of Contents

- [Introduction](#introduction)
- [Problem Description](#problem-description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Technologies Used](#technologies-used)


## Installation

To get started with the CS-50 Finance, follow these steps:

1. Clone the repository to your local machine:

```
git clone https://github.com/your-username/cs-50-finance.git
```

2. Change into the project directory:

```
cd cs-50-finance
```

3. Install the necessary dependencies:

```
pip install -r requirements.txt
```

4. Set up the database by running:

```
flask db init
flask db migrate
flask db upgrade
```

## Usage

To run the CS-50 Finance application, execute the following command in your terminal:

```
flask run
```

The application will be accessible at `http://localhost:5000` in your web browser.

## Features

The CS-50 Finance application comes with the following features:

- User registration and authentication.
- Stock symbol lookup to get real-time stock prices.
- Buying and selling stocks.
- Display of user portfolio with current stock holdings.
- Transaction history showing past buys and sells.
- Real-time balance updates upon stock transactions.

## Technologies Used

The CS-50 Finance is built using the following technologies:

- Python: The back-end of the application is written in Python.
- Flask: A micro web framework is used for building the web application.
- SQLite: The database system used for storing user information and transactions.
- HTML/CSS: The front-end of the application is built using HTML and CSS.
