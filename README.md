# 🚀 DataOps Copilot

**Enterprise AI-Powered DataOps Platform with Multi-Model Routing**

An intelligent data operations platform that automatically profiles, cleans, and analyzes data using Claude, GPT-4, Gemini, and Azure OpenAI with smart model routing.

![DataOps Copilot](https://img.shields.io/badge/Status-Production%20Ready-green)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)

---

## ✨ Features

### 🤖 Multi-Model AI Routing
- **Claude Sonnet 4.5** for complex reasoning and data analysis
- **GPT-4o** for fast structured outputs and code generation
- **Gemini 1.5 Pro** for vision-based dashboard OCR (FREE tier!)
- **Azure OpenAI** for enterprise compliance
- Automatic fallback routing with LiteLLM

### 📊 Core Capabilities
- **Auto Data Profiling**: Upload CSV/Excel/JSON → instant quality analysis
- **LLM-Powered Insights**: AI explains your data and suggests improvements
- **Smart SQL Generation**: Natural language → production SQL (coming soon)
- **Dashboard Vision**: Upload screenshots → extract metrics (coming soon)
- **Conversational BI**: Ask questions about your data (coming soon)

### 🏗️ Architecture
- **Frontend**: Next.js 14 (TypeScript, Tailwind CSS, React Query)
- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with DuckDB for analytics
- **Deployment**: Docker + Cloud Run ready
- **Cost**: ~$15-30/month during active use

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- API Keys (at least one):
  - Anthropic (Claude)
  - OpenAI (GPT-4)
  - Google AI (Gemini) - Recommended for free tier!

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd dataops-copilot
```

### 2. Set Up Environment Variables
```bash
# Copy example env file
cp backend/.env.example backend/.env

# Edit with your API keys
nano backend/.env
```

**Minimum required in `.env`:**
```env
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
GOOGLE_API_KEY=xxxxx
```

### 3. Start with Docker Compose
```bash
# Start all services (backend, postgres, redis)
docker-compose up -d

# View logs
docker-compose logs -f backend
```

The backend will be available at: http://localhost:8000

### 4. Set Up Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at: http://localhost:3000

---

## 🎯 Usage

### Upload and Profile Data

1. Navigate to http://localhost:3000
2. Click "Launch App"
3. Upload a CSV, Excel, or JSON file
4. Toggle "Use AI insights" (recommended)
5. Click "Analyze File"
6. View comprehensive profiling results with:
   - Basic statistics (rows, columns, nulls)
   - Column-level analysis
   - Data quality issues
   - AI-generated insights and recommendations

### Example Data
Use the included `sample_data/sales_data.csv` for testing.

---

## 📁 Project Structure

```
dataops-copilot/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # FastAPI app entry
│   │   ├── core/
│   │   │   └── config.py      # Configuration
│   │   ├── routers/           # API endpoints
│   │   │   ├── data.py        # Data upload & profiling
│   │   │   └── health.py      # Health checks
│   │   ├── services/          # Business logic
│   │   │   ├── llm_router.py  # Multi-model routing (LiteLLM)
│   │   │   └── data_profiler.py # Data analysis
│   │   └── models/            # Pydantic schemas
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile
│
├── frontend/                   # Next.js Frontend
│   ├── app/                   # Next.js 14 App Router
│   │   ├── page.tsx           # Landing page
│   │   ├── dashboard/         # Main app
│   │   └── layout.tsx
│   ├── components/
│   │   └── features/          # Feature components
│   ├── lib/
│   │   └── api.ts             # API client
│   └── package.json
│
└── docker-compose.yml         # Local development
```

---

## 🛠️ Development

### Backend Development

**Run without Docker:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --port 8000
```

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build
npm start
```

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

---

## 🎨 Tech Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **LiteLLM** - Unified API for multiple LLM providers
- **Pandas/Polars** - Data manipulation
- **DuckDB** - In-memory SQL analytics
- **SQLAlchemy** - ORM
- **Redis** - Caching and task queue
- **Pydantic** - Data validation

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **React Query** - Server state management
- **Axios** - HTTP client
- **Lucide React** - Icon library

### AI Models
- **Claude Sonnet 4.5** - Complex reasoning ($3/$15 per 1M tokens)
- **GPT-4o** - Fast structured output ($2.5/$10 per 1M tokens)
- **Gemini 1.5 Pro** - Vision + FREE tier! ($1.25/$5 per 1M tokens)

---

## 🚢 Deployment

### Deploy to Railway (Free Tier)

**Backend:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

**Frontend (Vercel):**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel --prod
```

### Environment Variables for Production

**Backend (Railway):**
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
GOOGLE_API_KEY=xxxxx
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
DEBUG=False
```

**Frontend (Vercel):**
```
NEXT_PUBLIC_API_URL=https://your-railway-backend.up.railway.app
```

---

## 💰 Cost Breakdown

### Development (Testing)
- **LLM APIs**: ~$5-10/month (with smart caching)
- **Hosting**: $0 (free tiers)
- **Total**: ~$5-10/month

### Production (Active Use)
- **LLM APIs**: ~$15-30/month
- **Railway**: $5/month (500 hrs)
- **Database**: $0 (Supabase free tier)
- **Total**: ~$20-35/month

**Cost Optimization:**
- Use Gemini for vision (FREE 1500 requests/day)
- Enable prompt caching
- Use DuckDB for in-memory analytics (free)

---

## 🎯 Roadmap

### Phase 1: MVP (Week 1-2) ✅
- [x] Multi-model routing setup
- [x] Data profiling with LLM insights
- [x] Next.js frontend with file upload
- [x] Docker development environment

### Phase 2: SQL & BI (Week 3)
- [ ] Natural language to SQL generation
- [ ] Query execution with DuckDB
- [ ] Interactive chart generation

### Phase 3: Vision & Dashboards (Week 4)
- [ ] Dashboard screenshot OCR (Gemini)
- [ ] Metric extraction
- [ ] Auto-dashboard generation

### Phase 4: Advanced Features (Week 5+)
- [ ] Data cleaning workflows
- [ ] Schema mapping
- [ ] Export to Power BI/Tableau
- [ ] User authentication
- [ ] Database integration (Snowflake, BigQuery)

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - feel free to use this for your portfolio or commercial projects!

---

## 👨‍💼 Built By

**William Kim** - AI Engineer  
- 🔗 [LinkedIn](#)
- 🐙 [GitHub](#)
- 📧 williamcjk11@gmail.com

---

## ⭐ Show Your Support

If this helped you land interviews, give it a ⭐️!

---

**Note**: This is a portfolio project demonstrating full-stack AI engineering skills. For production use, add proper authentication, rate limiting, and monitoring.