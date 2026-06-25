# AI Gym & Fitness Assistant 💪

An AI-powered fitness ecosystem that combines computer vision, NLP, IoT simulation, behavioural AI, and conversational chatbots into a single unified application.

---

## ✨ Features

| Module | Description |
|---|---|
| 🤸 **AI Gym Trainer** | MediaPipe pose detection, rep counting, posture feedback |
| 🥗 **AI Dietician** | Personalised meal plans, calorie & macro targets, diet logging |
| 📡 **IoT Monitor** | Simulated heart-rate, calorie, and equipment-load sensors |
| 🧠 **Habit Tracker** | ML-based workout-skip prediction with motivational nudges |
| 🤖 **Virtual Gym Buddy** | Rule-based + LLM chatbot with sentiment-aware responses |
| 📊 **Performance Analyzer** | Session scoring (0–100), weekly progress charts |
| 🏋️ **Gym Recommender** | Content-based filtering for workouts & gym recommendations |

---

## 🗂️ Project Structure

```
AI-Gym-Fitness-Assistant/
├── main.py                  # Unified launcher
├── requirements.txt
├── frontend/
│   └── app.py               # Streamlit UI (all 8 tabs)
├── backend/
│   ├── main.py              # FastAPI application
│   ├── schemas.py           # Pydantic request/response models
│   └── routers/
│       ├── users.py
│       ├── workout.py
│       ├── diet.py
│       ├── iot.py
│       ├── tracker.py
│       ├── chatbot.py
│       └── recommender.py
├── models/
│   ├── pose_detector.py     # MediaPipe pose analysis
│   ├── diet_planner.py      # Meal plan generation
│   ├── iot_simulator.py     # Sensor simulation
│   ├── habit_tracker.py     # Gradient Boosting skip predictor
│   ├── gym_buddy.py         # Conversational chatbot
│   ├── performance_analyzer.py
│   └── gym_recommender.py
├── utils/
│   ├── bmi_calculator.py
│   ├── calorie_tracker.py
│   └── helpers.py
├── database/
│   ├── db.py                # SQLAlchemy engine (SQLite)
│   └── models.py            # ORM table definitions
├── api/
│   └── llm_client.py        # Optional LLM API wrapper
└── data/
    ├── gyms.csv
    └── workouts.csv
```

---

## 🚀 Quick Start

### 1. Clone & create a virtual environment

```bash
git clone https://github.com/Prashant-kamagond/AI-Gym-Fitness-Assistant.git
cd AI-Gym-Fitness-Assistant
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure LLM API

Create a `.env` file in the project root to enable the LLM-powered chatbot:

```env
LLM_API_KEY=your_api_key_here
LLM_PROVIDER=openai          # or: gemini
LLM_MODEL=gpt-3.5-turbo      # or: gemini-pro
LLM_API_URL=https://api.openai.com/v1/chat/completions
```

Without this, the chatbot falls back to a fully functional rule-based engine.

### 4. Run the Streamlit frontend

```bash
python main.py --mode frontend
# or directly:
streamlit run frontend/app.py
```

Open **http://localhost:8501** in your browser.

### 5. (Optional) Run the FastAPI backend separately

```bash
python main.py --mode backend
# or:
uvicorn backend.main:app --reload --port 8000
```

API docs available at **http://localhost:8000/docs**

### 6. Run both together

```bash
python main.py --mode both
```

---

## 🖥️ UI Tabs

1. **Dashboard** – BMI gauge, macro pie chart, weekly calorie bar
2. **Workout Trainer** – Simulated rep counter, posture tips, workout logger
3. **Diet Planner** – Daily meal plan, calorie progress, meal logger
4. **Performance** – Score timeline, reps by exercise, session log table
5. **Gym Buddy** – Real-time chat with sentiment-aware AI assistant
6. **IoT Monitor** – Live heart-rate and load charts from simulated sensors
7. **Habit Tracker** – Daily check-in, skip prediction, weekly summary
8. **Recommender** – Personalised workout & gym recommendations

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| Computer Vision | OpenCV + MediaPipe |
| Machine Learning | scikit-learn (Gradient Boosting) |
| Database | SQLite via SQLAlchemy |
| Visualisation | Plotly |
| Optional LLM | OpenAI / Google Gemini |

---

## 📝 Notes

- The **pose detection** module (`models/pose_detector.py`) is fully implemented and works with a live webcam in a local environment. The Streamlit tab uses a simulation mode for cloud/demo deployments where camera access may be restricted.
- The **SQLite database** (`fitness_assistant.db`) is created automatically on first run in the project root.
- All modules work **offline** without any API key.



cd /d "c:\Users\prash\OneDrive\Desktop\AI-Gym-Fitness-Assistant\AI-Gym-Fitness-Assistant"
.\.venv\Scripts\activate.bat
python -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501


>> If stuck:
netstat -ano | findstr :8501
taskkill /PID <that_pid> /F


#Optional backend (API):
netstat -ano | findstr :8501
taskkill /PID <that_pid> /F


python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
