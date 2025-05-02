# Romanian Listening Practice Application

A microservices-based application for practicing Romanian listening comprehension through interactive exercises generated from YouTube content.

## Core Functionality

- Extract and process Romanian content from YouTube videos
- Generate multiple-choice listening comprehension questions
- Provide text-to-speech audio for questions and content
- Interactive practice interface with immediate feedback
- Progress tracking and difficulty adjustment

## Key Components

### Main Microservices

1. **Transcript Processor**
   - YouTube content extraction and processing
   - Transcript segmentation and cleaning
   - Data preparation pipeline

2. **Question Module**
   - Text embedding using TEI Embedding
   - Multiple-choice question generation via Ollama
   - Question difficulty calibration
   - Vector-based content retrieval

3. **Audio Module**
   - Text-to-speech generation for questions
   - Audio segment management
   - Speech rate and clarity optimization

### Supporting Services

- **Ollama**: Local LLM service for intelligent question generation
- **TEI Embedding**: Vector embeddings for semantic search and content organization
- **React Frontend**: Modern, responsive UI for seamless user interaction
- **Streamlit**: Local testing environment for rapid prototyping

## Data Flow

1. Content Ingestion:
   - YouTube video selection and transcript extraction
   - Text preprocessing and segmentation
   - Storage of processed transcripts

2. Question Generation:
   - Text embedding and semantic analysis
   - Multiple-choice question creation using Ollama
   - Answer validation and metadata tagging

3. Audio Processing:
   - TTS generation for questions and content
   - Audio quality optimization
   - Caching for performance

4. User Interaction:
   - Question presentation via React UI
   - Real-time feedback and scoring
   - Progress tracking and analytics

## Setup and Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Ollama installed locally
- TEI Embedding service
- YouTube API credentials

### Development Environment

1. Clone the repository:
```bash
git clone [repository-url]
cd romanian-listening-practice
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Running the Application

### Production Environment

Start each microservice:

```bash
# Transcript Processor
cd transcript-processor
python main.py

# Question Module
cd question-module
python main.py

# Audio Module
cd audio-module
python main.py

# Frontend
cd frontend
npm start
```

### Local Testing

For rapid prototyping, use Streamlit:

```bash
cd frontend
streamlit run local_test.py
```

## Configuration

Create a `.env` file with necessary credentials:

```
YOUTUBE_API_KEY=your_key
TEI_EMBEDDING_KEY=your_key
```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.