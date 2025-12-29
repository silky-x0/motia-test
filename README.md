# Polyglot + AI Username Generator

A Motia project demonstrating a **multi-language** unified backend (TypeScript + Python) with **AI integration**.

## Why Motia?

I was exploring the ways where I can use Multiple languages like TS, Python, JS, etc. in a single project. And that's where I found Motia. It is language agnostic and can be used to build a unified backend. Its core Idea is treat different services as steps and connect them using events, hence event driven architecture. I'll be using/exporing it more in coming days.

## Features

### 1. Instagram Username Generator (New!)
A complete AI-driven workflow that generates creative Instagram usernames using Google's Gemini AI.

- **TypeScript**: API endpoint (`generate-username.step.ts`) - Accepts user preferences
- **Python**: AI Processor (`generate_username_ai_step.py`) - Uses Gemini API to generate creative names
- **TypeScript**: Logger (`log-usernames.step.ts`) - Logs and stores the results

### 2. Polyglot "Hello World"
The starter template demonstrating cross-language communication.

- **TypeScript**: API endpoint (`hello-api.step.ts`)
- **Python**: Event processor (`process_greeting_step.py`)
- **JavaScript**: Logger (`log-greeting.step.js`)

## Quick Start

### 1. Prerequisites
- Node.js and Python 3.10+ installed
- A Google Gemini API key (Get one [here](https://aistudio.google.com/apikey))

### 2. Setup

```bash
# Install dependencies
npm install

# Configure Environment
echo "GEMINI_API_KEY=your_gemini_key_here" > .env
```

### 3. Run

```bash
# Start the development server
npm run dev
```

The server will start at `http://localhost:3000`.

## Testing

### Generate Usernames
Generate creative usernames based on a theme and keywords:

```bash
curl -X POST http://localhost:3000/api/generate-username \
  -H "Content-Type: application/json" \
  -d '{"theme": "gaming", "keywords": ["ninja", "pro"], "count": 5}'
```

### Hello World Demo
```bash
curl http://localhost:3000/hello
```

## How It Works (Username Generator)

1. **API Step (TS)**: Receives a POST request with `theme`, `keywords`, and `count`. It emits a `username.requested` event.
2. **AI Step (Python)**: Subscribes to `username.requested`. It constructs a prompt and calls the **Gemini API** using the `google-genai` SDK to generate unique usernames. It then emits `username.generated`.
3. **Logger Step (TS)**: Subscribes to `username.generated`. It logs the usernames to the console and stores them in the Motia state for persistence.

## Project Structure

```
src/
├── hello/                      # Hello World Demo
│   ├── hello-api.step.ts
│   ├── process_greeting_step.py
│   └── log-greeting.step.js
│
└── username-generator/         # AI Username Generator
    ├── generate-username.step.ts    # TS: API Endpoint
    ├── generate_username_ai_step.py # Python: AI Logic
    └── log-usernames.step.ts        # TS: Logging
```

## Learn More

- [Motia Documentation](https://motia.dev/docs)
- [Google Gemini API](https://ai.google.dev/)
