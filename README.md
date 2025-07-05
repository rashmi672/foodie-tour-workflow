# 🍽️ AI‑Powered Foodie Tour Generator

Turn any city into a delicious one‑day foodie adventure! This project combines real‑time weather, iconic local dishes, top‑rated restaurants, and AI‑driven narrative (with optional TTS) into a single, Dockerized workflow.

---

## 🔍 Features

- **Weather‑aware**: Indoor/Outdoor dining decisions (OpenWeatherMap)
- **3 Iconic dishes**: Per city (Mixtral via Together.ai)
- **Top‑rated restaurant**: Lookup (Mixtral “best restaurant” prompt fallback)
- **One‑day foodie tour**: Narrative (<100 words with emojis) via Mixtral
- **Task queue**: With Celery + RabbitMQ + Redis
- **Minimal frontend**: HTML to interact end‑to‑end
- **Optional audiobook**: Text‑to‑speech (TTS) via Groq PlayAI TTS
- **Optional History**: List of history via MongoDb


---

## 🏗️ Architecture & Tech Stack

| Component              | Technology                         |
|------------------------|------------------------------------|
| **API Server**         | FastAPI                            |
| **Background Worker**  | Celery                             |
| **Message Broker**     | RabbitMQ                           |
| **Result Backend**     | Redis                              |
| **History Storage**    | MongoDB                            |
| **LLM & Prompts**      | Together.ai v1 (Mixtral‑8x7B)      |
| **TTS (Audio)**        | Groq PlayAI                        |
| **Frontend**           | HTML JavaScript                    |
| **Deployment**         | Docker & Docker Compose            |

---

## 📂 Repository Layout

```
.
├── docker-compose.yml              # Orchestrates backend, RabbitMQ, Redis, MongoDB, frontend
├── backend/
│   ├── Dockerfile                  # Builds FastAPI + Celery worker image
│   ├── requirements.txt            # Python dependencies
│   └── app/
│       ├── .env                    # API keys & secrets 
│       ├── api.py                  # FastAPI endpoints
│       ├── itinery_stack/
│       │   ├── database/           # MongoDB & Redis helpers
│       │   ├── message_queue/      # Rabbit Config for message broker
│       │   ├── services/           # Weather condition, Dining (Indoor/Outdorr), Iconic dishes, Restaurants details, TTS logic
│       │   └── task_queue/         # Celery config & tasks
│       └── output/                 # Generated audio files 
└── frontend/
    ├── Dockerfile                  # Static‑server image
    └── index.html                  # Single‑page UI to drive the workflow
```

---

## 🛠 System Requirements

### ✅ Supported OS

- *Linux* (Ubuntu/Debian preferred)
- *Windows* with *WSL2* (Windows Subsystem for Linux)

> 💡 Recommended WSL Distro: Ubuntu

---

### ✅ Required Tools

- *Docker* 
- *Docker Compose* 

Install Docker and Docker Compose:

```bash
sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
```

## 🚀 Quickstart (Local)

1. **Clone** this repository  
   ```bash
   git clone https://github.com/rashmi672/foodie-tour-workflow.git
   cd foodie-tour-workflow
   ```

2. **Add your `.env`** in `backend/app/`:
   ```dotenv
   OPENWEATHER_API_KEY  = <your_openweather_api_key>
   TOGETHER_API_KEY     = <your_togetherai_api_key>
   GROQ_API_KEY         = <your_groq_api_key>
   ```

3. **Build & Launch** all services  
   a. Docker compose build
   ```bash
   sudo docker-compose up -d --build
   ```
   **Access Web app** → http://localhost:8080

   b. Check the running container
   ```bash
   sudo docker ps -a
   ```
   c. Check the docker log file with container ID
   ```bash
   sudo docker logs -f <first 3 digit of container id>
   ```
   d. Docker compose down
   ```bash
   sudo docker-compose down
   ```
   e. Cleaning the docker images, networks & volumes, etc
   ```bash
   sudo docker system prune -a --volumes -f
   ```

---

## 💡 Next Steps / Future Scope

- 🎨 **React**: Frontend for a richer UI.
- 🌐 **Map integration**: Google Maps links for restaurants.
- 🏷 **User preferences**: Dietary restrictions, budget friendly.  
- 🌎 **Localization**: Auto‑translate narratives for local language.
- ⏰ **Scheduling**:  For weekend‑long tours.

---

## 🤝 Contributing & License

Feel free to open issues or PRs!  
This project is MIT‑licensed.  

---

> Happy eating! 🍴😋  
