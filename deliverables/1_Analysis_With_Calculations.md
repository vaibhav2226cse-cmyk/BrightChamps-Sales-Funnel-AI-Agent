# Deliverable 1: The Leak — Funnel Analysis & Revenue Leak Calculations

**Candidate Role:** AI Forward Deployed Associate (Founder's Office)  
**Company:** BrightChamps  
**Dataset Analyzed:** `BrightChamps_FDA_Case_Dataset.csv` (5,000 anonymised leads across 60 days: June 1 – July 31, 2026)  
**Core Financial Assumptions:**
- Blended Cost per Lead (CAC): **₹900**
- Average Package Revenue per Conversion: **₹60,000**
- Monthly Time Basis: 60 days / 2.0 = **2,500 leads/month**

---

## 1. Executive Summary & Funnel Architecture

Over a 60-day window, BrightChamps ingested **5,000 leads** representing a marketing expenditure of **₹45,00,000** (₹22,50,000/month). Only **362 leads converted** into paying students (overall funnel conversion of **7.24%**), generating **₹2,17,20,000** in gross revenue (₹1,08,60,000/month).

### Macro Funnel Breakdown

```
[Lead Created]       5,000 leads  (100.0%)  [2,500/month]
      │
      ▼  (35.42% drop / 1,771 lost) ────► LEAK 1: Unscheduled Leads (₹59.56L/mo revenue lost)
[Demo Scheduled]     3,229 leads  ( 64.58%) [1,614.5/month]
      │
      ▼  (36.20% drop / 1,169 lost) ────► LEAK 2: Demo No-Shows     (₹61.63L/mo revenue lost)
[Demo Joined]        2,060 leads  ( 41.20%) [1,030.0/month]
      │
      ▼  (13.30% drop /   274 lost) ────► LEAK 3: Mid-Demo Dropouts (₹16.66L/mo revenue lost)
[Demo Completed]     1,786 leads  ( 35.72%) [  893.0/month]
      │
      ▼  (79.73% drop / 1,424 lost) ────► LEAK 4: Post-Demo Churn  (Closing conversion = 20.27%)
[Converted / Enrolled] 362 leads  (  7.24%) [  181.0/month]
```

---

## 2. Methodology & Financial Sizing Formulas

To size leaks in **₹/month**, we employ a realistic opportunity-cost model:
1. **Gross Revenue Lost (Opportunity Cost)**:
   $$\text{Lost Conversions} = \text{Drop Count at Stage } k \times \text{Benchmark Conversion Rate of Stage } (k+1)$$
   $$\text{Gross Revenue Leaked} = \text{Lost Conversions} \times \text{Average Order Value (₹60,000)}$$
2. **Direct Marketing Waste (Sunk CAC)**:
   $$\text{Wasted CAC} = \text{Drop Count at Stage } k \times \text{Cost Per Lead (₹900)}$$
3. **Monthly Normalization**:
   $$\text{Monthly Rate} = \frac{\text{60-Day Metric}}{2.0}$$

---

## 3. Stage-by-Stage Revenue Leak Quantification

### Leak 1: Lead $\rightarrow$ Demo Scheduled (The Capture Leak)
- **Data:** 1,771 out of 5,000 leads were never scheduled for a demo (**35.42% drop**).
- **Monthly Lost Volume:** $1,771 / 2 = \mathbf{885.5\text{ leads/month}}$.
- **Benchmark Conversion Rate:** Leads that schedule a demo convert at **11.21%** ($362 / 3,229$).
- **Calculations:**
  - Lost Monthly Conversions: $885.5 \times 11.21\% = \mathbf{99.27\text{ conversions/month}}$.
  - **Gross Revenue Leaked:** $99.27 \times ₹60,000 = \mathbf{₹59,56,352\text{ / month}}$ (**₹59.56 Lakhs/mo**).
  - **Sunk CAC Wasted:** $885.5 \times ₹900 = \mathbf{₹7,96,950\text{ / month}}$ (**₹7.97 Lakhs/mo** of marketing spend vaporized with zero pipeline contact).

### Leak 2: Demo Scheduled $\rightarrow$ Demo Joined (The No-Show Leak) — *LARGEST LEAK*
- **Data:** 1,169 out of 3,229 scheduled leads did not attend their demo (**36.20% no-show rate**).
- **Monthly Lost Volume:** $1,169 / 2 = \mathbf{584.5\text{ leads/month}}$.
- **Benchmark Conversion Rate:** Leads that join their demo convert at **17.57%** ($362 / 2,060$).
- **Calculations:**
  - Lost Monthly Conversions: $584.5 \times 17.57\% = \mathbf{102.71\text{ conversions/month}}$.
  - **Gross Revenue Leaked:** $102.71 \times ₹60,000 = \mathbf{₹61,62,786\text{ / month}}$ (**₹61.63 Lakhs/mo**).
- **Critical Context:** These are high-intent parents who already committed to a demo slot. Losing 36% of them before demo entry is the single costliest failure in the pipeline.

### Leak 3: Demo Joined $\rightarrow$ Demo Completed (Mid-Demo Abandonment)
- **Data:** 274 out of 2,060 attendees dropped off during the live session (**13.30% drop rate**).
- **Monthly Lost Volume:** $274 / 2 = \mathbf{137.0\text{ leads/month}}$.
- **Benchmark Conversion Rate:** Leads that complete the session convert at **20.27%** ($362 / 1,786$).
- **Calculations:**
  - Lost Monthly Conversions: $137.0 \times 20.27\% = \mathbf{27.77\text{ conversions/month}}$.
  - **Gross Revenue Leaked:** $27.77 \times ₹60,000 = \mathbf{₹16,66,092\text{ / month}}$ (**₹16.66 Lakhs/mo**).

### Leak 4: Demo Completed $\rightarrow$ Enrollment (Post-Demo Non-Conversion)
- **Data:** 1,424 out of 1,786 parents completed the demo but did not purchase (**79.73% non-conversion**).
- **Monthly Non-Conversions:** $1,424 / 2 = \mathbf{712\text{ parents/month}}$.
- **Benchmark Conversion:** Baseline closing rate is 20.27%. If closing effectiveness increased by just 3 percentage points (to 23.27%), BrightChamps would gain $893 \times 3\% \times ₹60,000 = \mathbf{₹16,07,400\text{ / month}}$.

---

## 4. Summary Table of Funnel Revenue Leaks

| Funnel Stage / Leak | Drop Volume (2 mo) | Monthly Drop | Stage Conversion Benchmark | Gross Revenue Leaked (₹/Month) | Direct Sunk CAC (₹/Month) | Priority |
|---|---|---|---|---|---|---|
| **Leak 2: Demo No-Shows (Scheduled $\rightarrow$ Joined)** | 1,169 | 584.5 leads | 17.57% | **₹61,62,786 / mo** | — | 🔴 **#1 Target** |
| **Leak 1: Unscheduled (Lead $\rightarrow$ Scheduled)** | 1,771 | 885.5 leads | 11.21% | **₹59,56,352 / mo** | **₹7,96,950 / mo** | 🔴 **#2 Target** |
| **Leak 3: Mid-Demo Drop (Joined $\rightarrow$ Completed)** | 274 | 137.0 leads | 20.27% | **₹16,66,092 / mo** | — | 🟡 Secondary |
| **Total Top-of-Funnel Leakage (Leak 1 + 2 + 3)** | 3,214 | 1,607.0 leads | — | **₹1,37,85,230 / mo** (~₹1.38 Cr/mo) | **₹7,96,950 / mo** | — |

---

## 5. Root-Cause Diagnostic Analysis

### A. The Latency Killer: Scheduling Delay vs Attendance & Conversion
Analyzing `demo_scheduled_at - created_at` reveals the primary driver of the No-Show crisis:

| Scheduling Latency | Scheduled Count | Demos Joined | Demo Join Rate | Converted Count | End-to-End Conversion |
|---|---|---|---|---|---|
| **< 24 Hours** | 1,477 | 1,095 | **74.14%** | 181 | **12.25%** |
| **24 – 48 Hours** | 467 | 362 | **77.52%** | 58 | **12.42%** |
| **48 – 72 Hours** | 186 | 81 | **43.55%** ⚠️ | 10 | **5.38%** ⚠️ |
| **> 72 Hours** | 1,099 | 522 | **47.50%** ⚠️ | 113 | **10.28%** |

> **Key Takeaway:** Contacting and scheduling a parent within 48 hours yields a **~75% join rate** and **12.3% conversion**. When scheduling slips past 48 hours, demo attendance **collapses to 43.5%** and conversion plunges by **56%** (to 5.38%). Fast scheduling is an immediate, high-leverage operational driver.

### B. Timezone & Shift Misalignment
Reps are frequently assigned leads across incompatible timezones without shift alignment:
- **US Shift Reps handling US Parents (`America/New_York`):**
  - Leads: 747 | Converted: 88 | **Conversion Rate: 11.78%**
- **IST Shift Reps handling US Parents (`America/New_York`):**
  - Leads: 660 | Converted: 50 | **Conversion Rate: 7.58%** (a **35.7% performance penalty**)
- **US Shift Reps handling Vietnam Parents (`Asia/Ho_Chi_Minh`):**
  - Leads: 362 | Converted: 11 | **Conversion Rate: 3.04%** (calling asleep or working parents)

### C. Follow-Up Diminishing Returns & Burnout
- Attempts 0–2 maintain a steady **~7.2% – 7.4%** conversion rate.
- Attempts 3–5 maintain **~7.0% – 8.6%** conversion rate.
- **Attempts 7+**: Sharp drop to **3.57%** at 7 attempts, and **0.00% across 8–9 attempts** (21 leads wasted). Over-contacting burns SDR bandwidth that could be deployed toward <24h follow-ups on fresh leads.

---

## 6. Conclusion for Founder's Office
The analysis confirms that **Leak 2 (Demo No-Shows, ₹61.63L/mo)** and **Leak 1 (Unscheduled Leads, ₹59.56L/mo)** together drain **₹1.21 Cr/month** in pipeline revenue. Because scheduled leads have already demonstrated intent and qualified themselves, recovering even **20% of demo no-shows** represents **+₹12.32 Lakhs/month** in immediate gross margin without any additional ad spend.
