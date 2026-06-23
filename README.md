# FluentChat Backend

This is the backend repository for **FluentChat**, built using FastAPI, MongoDB Atlas, Motor, and WebSockets.

## Project Structure

```text
backend/
│
├── app/
│   ├── main.py          # FastAPI application entry point & routes
│   ├── database.py      # Async MongoDB Atlas connection (Motor)
│   ├── config.py        # Application configuration & env loading
│   ├── models/          # Pydantic schemas and database models
│   ├── routes/          # API endpoints
│   ├── websocket/       # WebSocket handlers and connection manager
│   └── services/        # Business logic services
│
├── .env                 # Environment variables (secret credentials)
├── requirements.txt     # Backend dependencies
└── README.md            # Project documentation
```

## Getting Started

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file (based on `.env` in this directory) and update the `MONGODB_URL` with your MongoDB Atlas URI.

3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```
