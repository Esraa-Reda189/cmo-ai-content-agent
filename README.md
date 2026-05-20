# CMO.AI — Ad & Content Generation Agent

> **Graduation Project** | Faculty of Computers and Data Science — Intelligent Systems Department

An AI-powered content generation agent that automatically produces high-quality, brand-consistent marketing materials for startups and brand-led businesses. Built as a core module within the **CMO.AI multi-agent system**, it simulates the role of a professional content marketing team using RAG, LLMs, and platform intelligence.

---

##  Features

-  **Multi-platform content generation** — Instagram, Twitter, LinkedIn, Facebook, and Email
-  **RAG-powered brand personalization** — retrieves tone, audience, products, and values from Pinecone before generating
-  **A/B variation generation** — produces multiple content variations for testing
-  **SEO integration** — extracts keywords, meta descriptions, and suggested titles from email campaigns
-  **Hashtag extraction** — automatically pulls hashtags from generated content
-  **Character limit validation** — checks all content against platform-specific limits
-  **Posting time suggestions** — recommends optimal posting times per platform

---

##  Architecture

The agent follows a 7-layer pipeline:

```
Input Layer (ContentRequest)
        ↓
RAG Retrieval Layer (Pinecone + Cohere Embeddings)
        ↓
Platform Rules Layer (PLATFORM_RULES dict)
        ↓
Prompt Engineering Layer (LangChain ChatPromptTemplate)
        ↓
LLM Generation Layer (Groq API + LLaMA 3.3 70B)
        ↓
Post-Processing Layer (Python regex + Pydantic)
        ↓
Output Layer (ContentOutput)
```

---

##  Input Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content_type` | Literal | ✅ | `social_media_post` / `email_campaign` / `promotional_message` |
| `brand_name` | str | ✅ | Name of the brand or startup |
| `industry` | str | ✅ | Industry or business sector |
| `target_audience` | str | ✅ | Description of the intended audience |
| `tone` | Literal | ❌ | `professional` / `casual` / `humorous` / `inspirational` |
| `platform` | Literal | ❌ | `instagram` / `twitter` / `linkedin` / `facebook` / `email` |
| `topic_or_offer` | str | ✅ | The main topic, product, or offer to promote |
| `cta` | str | ❌ | Call to Action text (default: "Learn more") |
| `extra_notes` | str | ❌ | Additional brand or content instructions |

---

##  Output Structure

| Field | Type | Description |
|---|---|---|
| `content_type` | str | Type of content generated |
| `platform` | str / None | Target platform |
| `generated_content` | str | The full generated content text |
| `variations` | list[ContentVariation] | Parsed A/B variations with IDs |
| `hashtags` | list[str] | Extracted hashtags (social media only) |
| `subject_line` | str / None | Email subject line (email only) |
| `seo` | SEOData / None | Keywords, meta description, title (email only) |
| `platform_rules` | dict / None | Platform rules that were applied |
| `char_count` | int | Character count of generated content |
| `within_limit` | bool | Whether content is within platform limit |

---

##  Platform Rules

| Platform | Char Limit | Best Post Time |
|---|---|---|
| Instagram | 2,200 | Tue–Fri, 9–11AM or 7–9PM |
| Twitter | 280 | Mon–Thu, 8–10AM or 6–9PM |
| LinkedIn | 3,000 | Tue–Thu, 7–9AM or 12–1PM |
| Facebook | 63,206 | Wed–Fri, 1–4PM |
| Email | 5,000 | Tue or Thu, 10–11AM |

---

##  Technologies

| Component | Technology | Purpose |
|---|---|---|
| LLM | LLaMA 3.3 70B via Groq API | Content generation |
| LLM Framework | LangChain + langchain-groq | LLM orchestration |
| Vector Database | Pinecone Serverless | Brand knowledge storage |
| Embeddings | Cohere embed-english-v3.0 | Text vectorization (1024-dim) |
| Data Validation | Pydantic | Input/output schemas |
| Environment | python-dotenv | API key management |
| Backend Ready | FastAPI + Uvicorn | API endpoint exposure |

---

##  Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Esraa-Reda189/cmo-ai-content-agent.git
cd cmo-ai-content-agent
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
COHERE_API_KEY=your_cohere_api_key
```

### 5. Seed the knowledge base
```bash
python3 knowledge_base/seed_knowledge.py
```

### 6. Run the agent
```bash
python3 run_agent.py
```

---

##  Project Structure

```
cmo_ai_content_agent/
├── agent/
│   ├── content_agent.py      # Main agent logic
│   ├── prompts.py            # Prompt templates
│   ├── schemas.py            # Pydantic input/output models
│   └── tools.py              # Helper tools + PLATFORM_RULES
├── knowledge_base/
│   ├── content_kb.py         # RAG retrieval logic
│   └── seed_knowledge.py     # Knowledge base seeding script
├── tests/                    # Test cases
├── run_agent.py              # Entry point
├── requirements.txt
└── .env                      # API keys (not committed)
```

---

##  Test Results

| Test | Content Type | Platform | Result |
|---|---|---|---|
| Test 1 | Social Media Post | Instagram | 2 variations, 10 hashtags, within 2,200 char limit ✅ |
| Test 2 | Email Campaign | Email | Subject line, full body, and SEO section generated ✅ |
| Test 3 | Promotional Message | General | 3 variations, all under 150 characters ✅ |

---

## 🔗 Role in CMO.AI System

This agent is the **Content Generation Module** within the broader CMO.AI multi-agent platform. It integrates with:

- **Brand Coaching Agent** — provides brand identity data that seeds the knowledge base
- **Marketing Planner & Scheduler Agent** — triggers content generation for automated campaigns
- **Image Generation Agent** — receives content output to generate matching visuals
- **Video Generation Agent** — uses generated copy as scripts for short-form video
- **Performance Analytics Agent** — feeds engagement data back to improve future outputs

The full system is orchestrated via **LangGraph** and **CrewAI**.

---

##  Documentation

Full project documentation is available in this repository:
- [`CMO_AI_Content_Agent.pdf`](./CMO_AI_Content_Agent.pdf)
- [`CMO_AI_Content_Agent.docx`](./CMO_AI_Content_Agent.docx)

---

##  Author

**Esraa Reda** — Faculty of Computers and Data Science, Intelligent Systems Department
