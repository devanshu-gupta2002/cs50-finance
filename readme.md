# CS-50 Finance Problem Set

![CS-50 Finance](https://example.com/cs-50-finance-screenshot.png)

## Table of Contents

- [Introduction](#introduction)
- [Problem Description](#problem-description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

Welcome to the CS-50 Finance Problem Set! This problem set is part of CS-50, a popular introductory computer science course offered at Harvard University. In this problem set, you will build a web application that allows users to manage their own stock portfolios.

## Problem Description

In this problem set, you are tasked with implementing a web application that simulates a stock trading platform. Users can register accounts, look up stock prices, buy and sell stocks, and view their transaction history. The application uses real stock data to provide a realistic trading experience.

You will need to implement various functionalities, such as validating user input, querying stock data from a third-party API, updating user balances, and recording transaction history. The problem set will also challenge you to design the front-end interface and handle user authentication securely.

The problem set is divided into multiple tasks, each building upon the previous one. You are expected to follow the instructions provided in the CS-50 Finance problem set specification.

## Installation

To get started with the CS-50 Finance problem set, follow these steps:

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

The CS-50 Finance problem set is built using the following technologies:

- Python: The back-end of the application is written in Python.
- Flask: A micro web framework is used for building the web application.
- SQLite: The database system used for storing user information and transactions.
- HTML/CSS: The front-end of the application is built using HTML and CSS.

## Contributing

This problem set is meant for educational purposes and is not actively maintained. Therefore, we do not accept direct contributions to this repository. However, you are encouraged to fork the repository and make your modifications for learning and personal use.

## License

The CS-50 Finance problem set is provided under the [MIT License](https://opensource.org/licenses/MIT).

## Contact

If you have any questions or need further assistance, please feel free to contact the CS-50 teaching staff at Harvard University or create an issue in this repository. Happy coding!