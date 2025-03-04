# Multimodal Doctor Pre-screening App in Next.js

S/O to Yeyulabs (original code)

## Features

- Realtime audio/video(image) interaction with Gemini 2.0 Multimodal Live API
- Live transcription by Gemini 1.5/2.0 GenerativeAI API
- Built with Next.js for optimal performance

## Architecture


## Prerequisites

- Node.js 18+ installed
- API key for Gemini 2.0 Model

## Getting Started

1. Install dependencies
```bash
npm install
# or
yarn install
```

2. Set up environment variables
```bash
cp .env.example .env.local
```
Add your Gemini API key to `.env.local`:
```
GEMINI_API_KEY=your_api_key_here
```

3. Run the development server
```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.


