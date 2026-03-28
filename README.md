# 🖐 Real-Time Hand Gesture Recognition Web Application

A real-time hand gesture recognition system built using **MediaPipe, OpenCV, and Flask**.
This application detects hand gestures through a webcam and displays results in a web interface.

---

## 🚀 Features

* 🎥 Real-time webcam streaming using Flask
* 🧠 Hand landmark detection using MediaPipe
* ✋ Gesture recognition:

  * 👍 Thumbs Up
  * ✌️ Peace
  * 🖐 Palm
  * ✊ Fist
* 🔢 Gesture counting system
* 🌐 Web-based interface (HTML + Flask)
* ⚡ Lightweight and beginner-friendly implementation

---

## 🛠️ Tech Stack

* **Python**
* **OpenCV**
* **MediaPipe**
* **Flask**
* **HTML / CSS**

---

## 📂 Project Structure

```
cv-task/
│
├── main.py             # Flask app
├── camera.py            # Gesture detection logic
├── templates/
│   └── index.html       # Frontend UI
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/your-username/hand-gesture-recognition.git
cd hand-gesture-recognition
```

### 2. Create virtual environment (recommended)

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

If requirements file is not available:

```
pip install opencv-python mediapipe flask
```

---

## ▶️ Run the Application

```
python main.py
```

Open your browser and go to:

```
http://127.0.0.1:5000
```

---

## 🧠 How It Works

1. Webcam captures live video
2. MediaPipe detects 21 hand landmarks
3. Gesture logic identifies finger positions
4. Flask streams processed frames to browser
5. UI displays detected gesture and counts

---

## 🔮 Future Improvements

* Add more gestures
* Gesture-based control (volume, mouse, etc.)
* Store gesture data (CSV / database)
* Improve UI with dashboard
* Deploy using cloud (Heroku / Render)

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo and improve the project.

---

## 📄 License

This project is open-source and available under the **MIT License**.

---

## 🙋‍♂️ Author

**Your Name**

* GitHub: https://github.com/salvashirinpp

---

⭐ If you like this project, give it a star!
