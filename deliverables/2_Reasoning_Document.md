# Deliverable 2: The Lever — Strategic Intervention & Trade-off Reasoning

**Candidate Role:** AI Forward Deployed Associate (Founder's Office)  
**Company:** BrightChamps  
**Document Purpose:** Evaluation of candidate interventions, selection of the highest-leverage 2-week solution, and rigorous trade-off analysis of rejected alternatives.

---

## 1. The Decision Summary

| Dimension | Detail |
|---|---|
| **Selected Intervention** | **Autonomous WhatsApp "No-Show Concierge" & Instant Rescheduling Agent** |
| **Target Funnel Stage** | **Leak 2:** Demo Scheduled $\rightarrow$ Demo Joined (36.2% no-show rate) |
| **Financial Impact** | Recovering 20% of no-shows = **+₹12,32,557 / month** (+₹1.48 Cr annualized) |
| **Deployment Timeline** | **9 Days** (Go-live well within 2-week constraint) |
| **Engineering Requirement** | **Zero engineering sprint** (built on Wati / Gallabox + Make.com / Zapier + OpenAI API) |
| **Operating Cost** | < ₹25,000 / month (Software SaaS + WhatsApp message credits) |
| **Implied ROI** | **> 4,800%** |

---

## 2. Why Leak 2 is the Highest-Leverage Target

In sales ops, not all leaks are created equal. Sizing the opportunity requires evaluating both **monetary volume** and **intent state**:

1. **Massive Dollar Size (₹61.63L/mo):** As proven in Deliverable 1, demo no-shows represent the single largest gross revenue leak in the BrightChamps funnel.
2. **Pre-Qualified Intent:** Unlike top-of-funnel leads who merely filled out a web form, a parent who scheduled a demo has:
   - Acknowledged the need for their child's STEM/coding education.
   - Agreed to a date and time.
   - Picked a specific subject/curriculum focus.
3. **Friction, Not Rejection:** An analysis of no-shows in consumer edtech indicates that >70% of missed demos are not active rejections; they are caused by calendar conflicts, forgotten timings, child extracurricular clashes, or missing Zoom links.
4. **Immediate Latency Benefit:** The data shows scheduling within <24h maintains a **74.1% join rate**, whereas latency >48h drops attendance to **43.5%**. An automated agent that engages parents within 10 minutes of a missed demo recaptures intent while it is warm.

---

## 3. The Selected Lever: Autonomous WhatsApp "No-Show Concierge"

### How It Works (Zero Code Architecture)
```
[Demo Start Time: Rep logs "No-Show" in CRM / Google Sheet]
               │
               ▼ (Webhook trigger within 10 minutes)
   [Make.com / Zapier Orchestrator]
               │
               ▼
[WhatsApp Business API (Wati / Gallabox) + LLM Prompt Engine]
               │
               ▼
"Hi [Parent_Name]! We missed [Child_Name] at today's BrightChamps Coding Demo!
We know how busy family life gets 😊.

Would you like to re-book for tomorrow?
[Button: Tomorrow 5 PM]  [Button: Tomorrow 7 PM]  [Button: Custom Time]"
               │
               ▼
[Parent Clicks / Chats with AI Concierge in local timezone]
               │
               ▼
[Cal.com / Calendly syncs new slot & updates rep calendar automatically]
```

### Why It Solves the Core Bottlenecks:
1. **Timezone Autonomy:** The bot interacts according to the parent’s local timezone (EST, GMT, GST, SGT, ICT) 24/7, bypassing the limitation of rep shift coverage.
2. **Frictionless Rescheduling:** Re-booking takes 2 taps inside WhatsApp without needing another phone tag call.
3. **Rep Bandwidth Liberation:** Reps stop spending 3–4 manual follow-up calls dialing unanswered numbers and instead focus on conducting demos for confirmed attendees.

---

## 4. Alternatives Considered & Explicitly Rejected

To demonstrate rigorous trade-off thinking, the table below outlines the 4 major alternatives evaluated and the specific reasons for their rejection:

| Alternative Proposal | Expected Theoretical Impact | Why It Was REJECTED | Verdict |
|---|---|---|---|
| **Option A: Full CRM & Lead Routing Re-Architecture (Shift & Timezone Matching)** | High (~₹15L–20L/mo by fixing the 35% performance gap when IST reps call US parents) | **Requires an extensive engineering sprint.** Modifying CRM routing rules, integrating telephony dialers, re-negotiating rep employment contracts for night shifts, and testing load balancing requires 6–8 weeks and dedicated engineering resources. Violates the 2-week constraint. | ❌ **REJECTED** (Too slow & heavy) |
| **Option B: Aggressive Outbound Calling Campaign (Increasing Rep Call Quota from 4 to 8+)** | Low to Negative | **Counter-productive based on empirical dataset.** The data proves conversion collapses to **3.57% at 7 attempts** and **0.00% across 8–9 attempts**. Increasing call quotas causes parent irritation, brand erosion, and rep burnout without driving conversions. | ❌ **REJECTED** (Empirically invalid) |
| **Option C: Mid-Demo Interactive Gamification to Prevent Dropouts (Leak 3)** | Low (~₹5L–7L/mo) | **Total leak is only ₹16.66L/mo.** While mid-demo dropouts (274 leads) exist, curriculum redesign, teacher re-training, and interactive platform code changes take months. Sizing upside is small compared to no-shows. | ❌ **REJECTED** (Low ROI / High effort) |
| **Option D: Retargeting Ad Campaigns on Meta & Google** | Medium (~₹10L/mo) | **High incremental CAC.** BrightChamps already spends ₹900/lead. Re-bidding on paid ads adds customer acquisition cost without fixing the operational friction that caused them to miss the demo in the first place. | ❌ **REJECTED** (Wastes marketing capital) |

---

## 5. 14-Day Rapid Deployment Roadmap

Because no custom frontend or backend codebase is needed, deployment is executed via standard Founder’s Office rapid operationalization:

```
Week 1: Setup & Protocol
├── Day 1–2: Connect WhatsApp Business API via Wati/Interakt; configure webhook to CRM/Sheets.
├── Day 3–4: Draft 3 conversational re-engagement templates (A/B testing tone: Urgent vs Casual vs Empathetic).
└── Day 5: Set up Cal.com calendar integration with timezone auto-detection.

Week 2: Pilot & Full Rollout
├── Day 6–7: Run pilot across 2 sales reps (AD-01 & AD-04) on 100 historical no-shows.
├── Day 8: Review response rates, optimize prompt/timing (15-min post demo vs 2-hour post demo).
├── Day 9: Roll out across all 12 reps and all geographies.
└── Day 10–14: Monitor baseline lift, adjust messaging, track attendance rate.
```

---

## 6. Financial Sizing of Expected Net Return

- **Monthly No-Show Volume:** 584.5 leads/month
- **Conservative Recovery Rate (Rescheduled & Attended):** 20% = **116.9 recovered attendees/month**
- **Conversion Rate of Joined Attendees:** 17.57%
- **Net New Conversions:** $116.9 \times 17.57\% = \mathbf{20.54\text{ conversions/month}}$
- **Gross Monthly Revenue Added:** $20.54 \times ₹60,000 = \mathbf{₹12,32,557\text{ / month}}$
- **Tooling Costs:** ₹20,000/month (Wati Pro + WhatsApp conversation credits)
- **Net Monthly Profit Lift:** **~₹12.12 Lakhs / month**
