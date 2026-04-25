#  AI Spam Detector Web App

A lightweight, machine learning-powered web application built with Flask that classifies text messages as **Spam** or **Ham**. The system utilizes Natural Language Processing (TF-IDF) and a Logistic Regression model to accurately predict message categories in real-time.

##  Features

- **Real-Time Classification:** Instantly detects whether a given message is spam or ham.
- **Confidence Scoring:** Displays the model's confidence score for each prediction.
- **Prediction History:** Stores and displays a log of past predictions using an SQLite database.
- **Auto-Initialization:** Intelligently trains the machine learning model on the first run if pre-trained weights are not found.
- **CLI Testing Tool:** Includes a command-line script for quick batch testing without launching the web server.

##  Tech Stack

- **Backend Framework:** Python, Flask
- **Machine Learning:** Scikit-Learn (Logistic Regression, TF-IDF Vectorization)
- **Data Handling:** Pandas, Joblib
- **Database:** SQLite, Flask-SQLAlchemy
- **Frontend:** HTML/CSS (Jinja2 Templates)

##  Project Structure

```text
├── app.py                 # Main Flask application and route definitions
├── database.py            # SQLAlchemy database models
├── train.py               # ML script to train the model and save weights
├── predict.py             # CLI tool for quick terminal testing
├── spam.csv               # Dataset used for training the model
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore rules
└── templates/
    └── index.html         # Frontend user interface


**Follow these steps to run the project locally:**

### 1. Clone the repository
git clone https://github.com/prayas670/Ai-Spam-Detector-Project-1.git

### 2. Navigate to the project directory
cd Ai-Spam-Detector-Project-1

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the application
python app.py

### 5. Open in your browser
http://127.0.0.1:5000

