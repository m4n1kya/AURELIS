# AURELIS: Financial Affordability Intelligence

AURELIS is an advanced, privacy-first AI financial agent that deterministically evaluates your affordability and builds optimized payment plans based on your true cash flow, upcoming liabilities, and required minimum reserves.

Unlike static budgeting apps, AURELIS analyzes your 90-day cash flow projection (inclusive of expected bills, currency conversions, and LLM-extracted unstructured evidence) to tell you exactly how much you can afford *right now* and how to finance the rest safely.

## Features

- **Deterministic Financial Engine**: Built on a highly strict cash-flow simulation engine that guarantees you never drop below your absolute minimum reserve.
- **Multimodal Evidence Processing**: Uses Google Gemini to extract verifiable financial constraints from unstructured messages and receipts, falling back to safe defaults if limits are hit.
- **Dynamic Payment Planning**: Autonomously ranks and schedules payment plans if an item isn't affordable upfront.
- **Premium Fintech Dashboard**: A high-end Next.js UI for interacting with your financial intelligence command center in real time.

## Architecture

AURELIS is built with a strictly separated architecture:

- **`engine/`**: The core deterministic Python financial engine. Operates entirely independently without any web server dependencies.
- **`api/`**: A lightweight FastAPI bridge that securely wraps the deterministic engine to serve JSON payloads.
- **`frontend/`**: An ultra-premium React (Next.js) dashboard built with Tailwind CSS and Recharts for visualizing your 90-day financial forecast.
- **`dataset/`**: Local CSV-based data lake acting as your private financial history and requests ledger.

## Setup & Installation

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ (for the dashboard)
- Google Gemini API Key

### 2. Environment Variables
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_key_here
```

### 3. Backend Setup (Engine & API)
Install Python dependencies:
```bash
pip install -r requirements.txt
```

Launch the API Server:
```bash
python -m uvicorn api.main:app --port 8000
```

*(Alternatively, you can run the engine purely in the CLI by executing `python engine/main.py`)*

### 4. Frontend Setup
In a new terminal window, initialize the Next.js application:
```bash
cd frontend
npm install
npm run dev
```

Navigate to `http://localhost:3000` to access the AURELIS Dashboard.

## License
MIT License
