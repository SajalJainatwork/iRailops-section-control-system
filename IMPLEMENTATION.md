# Railway Operations System - Implementation Guide

## 🚂 Overview

This implementation provides a complete Railway Operations System following the simplified architecture you specified. The system includes:

- **FastAPI Backend**: Modular services for ingest, events, reasoning, and RAG
- **Streamlit UI**: Three-tab interface for dashboard, recommendations, and Q&A
- **PostgreSQL Database**: Complete schema with all required tables
- **ML Components**: Delay classifier and rule engine
- **Sample Data**: Ready-to-use test data

## 🏗️ Architecture Implementation

### Core Services (FastAPI)

1. **Ingest Service** (`src/services/ingest_service.py`)
   - Parses timetable CSV/Excel files
   - Handles topology data (stations, blocks)
   - Processes SOP documents with text chunking
   - Stores data in PostgreSQL

2. **Events Service** (`src/services/events_service.py`)
   - Accepts live train events via API
   - Calculates delays and status
   - Provides event history and analysis

3. **Reasoning Service** (`src/services/reasoning_service.py`)
   - Analyzes delay causes using ML classifier
   - Generates recovery recommendations using rule engine
   - Stores recommendations with explanations

4. **RAG Service** (`src/services/rag_service.py`)
   - Keyword search through SOP chunks (MVP)
   - Template-based responses (MVP)
   - Ready for LLM integration

### Database Schema

Complete PostgreSQL schema with:
- `timetables`: Train schedules
- `train_events`: Live events with delays
- `stations`: Station information
- `blocks`: Track segments
- `sop_documents` & `sop_chunks`: SOP storage
- `recommendations`: Recovery suggestions
- `delay_analysis`: ML predictions
- `query_logs`: RAG interactions

### UI Components (Streamlit)

1. **Delay Dashboard**
   - Real-time delay metrics
   - Visual charts and distributions
   - Detailed train status table

2. **Recovery Recommendations**
   - Train-specific recommendations
   - Apply/reject actions
   - Manual recommendation input

3. **Ops Copilot Q&A**
   - Natural language queries
   - SOP-based answers
   - Sample questions

## 🚀 Quick Start

### Option 1: Local Development

1. **Setup Environment**
   ```bash
   python setup.py
   ```

2. **Start Services**
   ```bash
   # Terminal 1: API Server
   python -m src.cli start-api
   
   # Terminal 2: UI
   python -m src.cli start-ui
   ```

3. **Access Application**
   - API: http://localhost:8000
   - UI: http://localhost:8501
   - API Docs: http://localhost:8000/docs

### Option 2: Docker Compose

1. **Start All Services**
   ```bash
   docker-compose up -d
   ```

2. **Access Application**
   - API: http://localhost:8000
   - UI: http://localhost:8501
   - PostgreSQL: localhost:5432
   - Neo4j: http://localhost:7474

## 📊 Sample Data

The system includes comprehensive sample data:

- **5 Stations**: Central, North Terminal, South Junction, East Platform, West Station
- **5 Blocks**: Main lines, loops, and sidings
- **5 Trains**: Multiple routes with realistic schedules
- **25 Events**: Mix of on-time and delayed trains
- **SOP Document**: Emergency procedures with 5 chunks

## 🔧 Configuration

### Environment Variables (`.env`)

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/irailops

# Neo4j (optional)
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# API
API_HOST=0.0.0.0
API_PORT=8000

# File Storage
UPLOAD_DIR=data/uploads
SOP_DIR=data/sops

# ML
MODEL_DIR=models
OPENAI_API_KEY=your_key_here
```

## 📈 Key Features Implemented

### ✅ Phase 0 MVP (Completed)

- [x] PostgreSQL database with complete schema
- [x] Ingest service for timetables and topology
- [x] Basic Streamlit UI showing stations and timetable
- [x] Sample data ingestion

### ✅ Phase 1 Core (Completed)

- [x] Events service API for live events
- [x] Delay classifier (Random Forest with synthetic training)
- [x] Rule engine for recovery recommendations
- [x] Streamlit tabs: Dashboard, Recovery, Q&A
- [x] Keyword search for SOP documents

### 🔄 Phase 2+ (Ready for Extension)

- [ ] Vector search with pgvector/Qdrant
- [ ] LLM integration for RAG responses
- [ ] Neo4j graph database integration
- [ ] Simulation and optimization services
- [ ] Real-time event streaming

## 🎯 API Endpoints

### Ingest Service
- `POST /api/ingest/timetable` - Upload timetable files
- `POST /api/ingest/topology` - Upload topology files
- `POST /api/ingest/sop` - Upload SOP documents

### Events Service
- `POST /api/events` - Create train event
- `GET /api/events/{train_no}` - Get train events

### Reasoning Service
- `POST /api/reasoning/analyze` - Analyze delay
- `GET /api/recommendations/{train_no}` - Get recommendations

### RAG Service
- `POST /api/rag/query` - Query SOP documents

## 🧠 ML Components

### Delay Classifier
- **Model**: Random Forest Classifier
- **Features**: Delay minutes, time, station type, weather, congestion
- **Causes**: weather, mechanical, congestion, signal_failure, passenger_delay, etc.
- **Training**: Synthetic data for MVP, ready for real data

### Rule Engine
- **Skip Halt**: Skip intermediate stations for delay recovery
- **Overtake**: Use loop lines for faster trains
- **Prioritize**: Give priority based on delay severity
- **Platform Change**: Redirect to avoid congestion

## 🔍 Testing the System

1. **View Sample Data**
   ```bash
   python -m src.cli analyze-delay --train-no 12345
   ```

2. **Test API Endpoints**
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/api/events/12345
   ```

3. **Upload Files via UI**
   - Use the upload modal in Streamlit
   - Test with CSV files containing timetable data

## 🚀 Next Steps

### Immediate Enhancements
1. **Real Data Integration**: Replace synthetic data with real railway data
2. **Weather API**: Integrate weather data for better delay prediction
3. **Real-time Updates**: WebSocket connections for live updates
4. **Advanced ML**: Deep learning models for delay prediction

### Production Considerations
1. **Authentication**: Add user authentication and authorization
2. **Monitoring**: Implement logging and monitoring
3. **Scalability**: Add caching and load balancing
4. **Security**: Input validation and rate limiting

## 📝 File Structure

```
src/
├── api/
│   └── main.py              # FastAPI application
├── services/
│   ├── ingest_service.py    # File parsing and ingestion
│   ├── events_service.py    # Live event handling
│   ├── reasoning_service.py # Delay analysis and recommendations
│   └── rag_service.py       # SOP-based Q&A
├── data/
│   ├── models.py            # SQLAlchemy models
│   └── database.py          # Database connection
├── ml/
│   └── delay_classifier.py  # ML delay prediction
├── utils/
│   └── rule_engine.py       # Business rules
├── ui/
│   └── app.py               # Streamlit interface
└── cli.py                   # Command-line interface
```

This implementation provides a solid foundation for your Railway Operations System and can be easily extended with additional features as needed.
