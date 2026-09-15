# 🚀 BrightChamps Lead Funnel AI Agent

An interactive AI-powered dashboard that analyses the BrightChamps sales funnel to identify revenue leaks, score leads by conversion probability, recommend smart follow-up actions, and track rep performance.

Built as a deliverable for the **BrightChamps AI Forward Deployed Associate** take-home case study.

---

## 🖥️ Live Demo

> **[Coming soon — Streamlit Cloud deployment link]**

---

## 📦 What's Inside

| Page | Description |
|------|-------------|
| **🏠 Home** | High-level KPIs, funnel snapshot, and ₹/month leak overview |
| **🔍 Funnel Leak Analysis** | Stage-by-stage revenue leak quantification. Segment by source, geography, scheduling delay, timezone alignment |
| **🎯 Lead Scoring** | Logistic regression model scores every lead with conversion probability. Filterable, downloadable |
| **📞 Follow-Up Engine** | Classifies leads into action categories (never scheduled, no-show, needs closing). Flags timezone mismatches and over-contacted leads |
| **👥 Rep Performance** | Compare all 12 reps on every funnel metric. Coaching insights auto-generated |

---

## 📑 Case Study Deliverables (PDFs)

All three formal case study deliverables are compiled as executive-grade PDF reports inside the [`deliverables/`](deliverables/) folder:

1. **[1_Analysis_With_Calculations.pdf](deliverables/1_Analysis_With_Calculations.pdf)** — Stage-by-stage revenue leak quantification (₹/month), opportunity-cost formulas, latency/timezone diagnostics.
2. **[2_Reasoning_Document.pdf](deliverables/2_Reasoning_Document.pdf)** — Strategic intervention selection, zero-code architecture, rejected alternatives trade-off analysis, and 9-day deployment roadmap.
3. **[3_The_Executive_Memo.pdf](deliverables/3_The_Executive_Memo.pdf)** — 1-page CEO memorandum with baselines, scorecard metrics, and rep adoption risk mitigations.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+

### Install & Run

```bash
# Clone the repo
git clone https://github.com/vaibhav2226cse-cmyk/BrightChamps-Sales-Funnel-AI-Agent.git
cd BrightChamps-Sales-Funnel-AI-Agent

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
BrightCHAMPS/
├── app.py                              # Home page
├── pages/
│   ├── 1_Funnel_Leak_Analysis.py       # Revenue leak deep-dive
│   ├── 2_Lead_Scoring.py               # ML lead scoring
│   ├── 3_Follow_Up_Engine.py           # Follow-up recommendations
│   └── 4_Rep_Performance.py            # Rep comparison dashboard
├── utils/
│   ├── __init__.py
│   ├── styles.py                       # Custom CSS & UI components
│   ├── data_loader.py                  # Data loading & preprocessing
│   ├── funnel_analyzer.py              # Funnel analysis engine
│   └── lead_scorer.py                  # ML scoring model
├── BrightChamps_FDA_Case_Dataset.csv   # Source data (5,000 leads)
├── .streamlit/config.toml              # Streamlit theme config
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | Streamlit |
| Charts | Plotly |
| ML | scikit-learn (Logistic Regression) |
| Data | Pandas, NumPy |

---

## 🤖 AI Tools Used

- **Google Antigravity (Gemini)** — Code generation, data analysis, architecture design
- **Python + scikit-learn** — Lead scoring model

---

## 📊 Key Findings

- **Biggest Leak**: Demo Scheduled → Demo Joined (no-shows) — ~₹61.7L/month in lost revenue
- **Speed Matters**: Leads scheduled within 24h convert at 12.3% vs 5.4% for 48h+ delay
- **Timezone Alignment**: Misaligned rep-parent timezone pairs convert at ~3.2% vs ~7.6% for aligned
- **Source Quality**: Referral (11%) and Organic (10%) convert 2× better than DSA (4%)

---

## 📝 License

This project was built as a take-home case study submission. Not licensed for commercial use.
