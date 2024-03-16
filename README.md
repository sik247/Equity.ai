# Equity.AI: Empowering Retail Investors with AI

## Overview

ModelPy leverages advanced machine learning techniques, including Recurrent Neural Networks (RNN) and Long Short-Term Memory (LSTM) networks, to offer retail investors predictive insights into stock market trends. By analyzing historical data, these models can uncover patterns and predict future price movements, providing users with a competitive edge in investment decisions.

## Key Features

- **Predictive Analytics:** Use LSTM models for accurate stock price forecasts.
- **Portfolio Optimization:** Employ machine learning to suggest optimal investment strategies.
- **User-Friendly Interface:** Easy-to-use web application to access financial insights.

## Technology Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=Keras&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=TensorFlow&logoColor=white)
![CUDA](https://img.shields.io/badge/CUDA-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8 or higher
- MongoDB
- Flask

### Installation

Clone the repository and install the required Python packages:

```bash
git clone https://github.com/sik247/ModelPy.git
cd ModelPy
pip install -r requirements.txt
```

For Conda Users:
If you are using Conda, you can create an environment using the environment.yml file:

```bash
conda env create -f environment.yml
conda activate ModelPyEnv

``` 
### Usage

1. Start the Flask application: `python app.py`.
2. Access the web interface on `localhost:5000`.

## Deep Dive into LSTM and Stock Prediction

LSTMs are a type of RNN capable of learning order dependence in sequence prediction problems. Unlike traditional RNNs, LSTMs can remember information for long periods, making them ideal for analyzing stock prices, which are sequential data prone to long-term dependencies and volatility.

### Why LSTMs for Stock Prediction?

- **Memory Advantage:** LSTMs remember key patterns over long periods, essential for capturing the financial market's temporal dynamics.
- **Mitigating Gradient Vanishing:** LSTMs overcome the vanishing gradient problem, enabling more effective learning of complex patterns.
- **Adaptability:** Capable of adapting to new trends without forgetting previous learning, crucial in the ever-evolving stock market.

## Application's Goal

ModelPy is designed to democratize access to sophisticated financial analytics, providing retail investors with tools previously available only to professionals. By integrating cutting-edge AI models, ModelPy levels the playing field, allowing users to make informed investment decisions based on robust data analysis.



## Home Interface 
Upon launching the web application, users are greeted with the home screen, which displays the top 5 stocks and their predictions. This screen is designed to provide quick insights and easy navigation to detailed analyses.


![Example Image](static/display/homescreen.png "This is an example image")

## Prediction Interface 

The prediction section of the application showcases the output of LSTM models for selected stocks. Users can view detailed forecasts, historical trends, and make informed decisions based on the AI-driven predictions.
![Example Image](images/model.png "This is an example image")

## Contributing

We welcome contributions! If you have suggestions for improvements, please fork the repo and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
