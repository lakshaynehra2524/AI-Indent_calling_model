# AI Intent Calling Assistant

An AI-powered Streamlit application that identifies a user's intent from natural language text and routes them to the appropriate action page.

The project uses Machine Learning with TF-IDF Vectorization and a Linear Support Vector Classifier (LinearSVC) to classify user commands into predefined intents such as calling, emailing, alarms, music, calculator, camera, flashlight, and 

---

## Features

- Intent Detection using Machine Learning
- Real-time Prediction
- Interactive Streamlit Interface
- Multiple Action Categories
- Fast and Lightweight Model
- User-Friendly Navigation

---

## Supported Intents

- Call
- Email
- Camera
- Music
- Alarm
- Calculator
- Water Reminder
- Sleep Reminder
- Flashlight
- Running Assistant

---

## Project Structure

```text
AI-Intent-Calling/
│
├── app.py
│
├── sections/
│   ├── alarm.py
│   ├── calculator.py
│   ├── call.py
│   ├── camera.py
│   ├── flashlight.py
│   ├── home.py
│   ├── mail.py
│   ├── music.py
│   ├── running.py
│   ├── sleep.py
│   └── water.py
│
├── utils/
│   ├── predictor.py
│   └── router.py
│
├── Model_Training/
│   ├── linear_svc_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── requirements.txt
└── README.md
```

---

## Machine Learning Pipeline

### Text Preprocessing
User commands are cleaned and prepared for feature extraction.

### Feature Extraction
TF-IDF Vectorization converts text into numerical vectors.

### Model Training
A Linear Support Vector Classifier (LinearSVC) is trained on intent-labelled commands.

### Prediction
The trained model predicts the most probable intent from user input.

### Routing
The predicted intent is mapped to the corresponding application section.

---

## Technologies Used

- Python
- Streamlit
- Scikit-Learn
- Joblib
- TF-IDF Vectorizer
- LinearSVC

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/AI-Intent-Calling.git
cd AI-Intent-Calling
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
streamlit run app.py
```

The application will open in your browser automatically.

---

## Example Commands

```text
Call John
Open camera
Play music
Set an alarm for 6 AM
Turn on flashlight
I need a calculator
Remind me to drink water
Track my running activity
```

---

## Future Improvements

- Voice Command Support
- Deep Learning-Based Intent Detection
- Mobile-Friendly Interface
- Multi-Language Support
- Smart Action Automation
- Integration with External APIs

---

## Author

Lakshay

B.Tech Computer Science Engineering

Machine Learning and AI Enthusiast

---

## License

This project is developed for educational and portfolio purposes.
