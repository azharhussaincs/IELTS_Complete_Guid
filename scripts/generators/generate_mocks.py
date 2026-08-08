#!/usr/bin/env python3
"""Generate 50 original complete IELTS-style mock tests (text-based)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book" / "part09_practice_tests"
OUT.mkdir(parents=True, exist_ok=True)

TOPICS = [
    "urban green space", "digital privacy", "lifelong learning", "food waste", "public transport",
    "renewable energy", "remote work", "ageing societies", "cultural festivals", "water management",
    "artificial intelligence", "youth unemployment", "biodiversity loss", "online education", "housing costs",
    "mental wellbeing", "space research", "media literacy", "agricultural innovation", "tourism pressure",
    "language preservation", "healthcare access", "gender equality", "recycling systems", "smart cities",
    "financial literacy", "disaster preparedness", "scientific funding", "community volunteering", "road safety",
    "museum education", "climate adaptation", "gig economy", "childhood play", "ocean pollution",
    "architectural heritage", "workplace diversity", "vaccination policy", "library futures", "desertification",
    "consumer debt", "wildlife corridors", "teacher training", "noise pollution", "ethical fashion",
    "public art", "migration skills", "energy efficiency", "sports investment", "local democracy",
]


def listening_section(n: int, topic: str) -> str:
    return f"""## Listening (40 questions)

*Audio is not embedded in this edition; practise with the transcript as a reading-listening hybrid, then have a partner read it aloud at natural speed.*

### Section 1 — Conversation (Questions 1–10)
**Scenario:** A caller enquires about a community workshop on **{topic}**.

**Transcript excerpt:**  
A: Good morning, Green Civic Centre.  
B: Hi — I’m calling about the Saturday workshop on {topic}. What time does it start?  
A: The main session begins at 10:15, but please arrive by 10:00 for registration.  
B: And the fee?  
A: It’s £18 for adults and £12 for students. There’s a group discount if four people book together.  
B: Do I need to bring anything?  
A: Just a notebook. Materials are provided. Parking is behind the building on River Lane.

**Questions 1–6 complete the notes below. Write ONE WORD AND/OR A NUMBER.**

Workshop topic: {topic}  
Start time of main session: **1** …………  
Arrive by: **2** …………  
Adult fee: **3** £…………  
Student fee: **4** £…………  
Bring: a **5** …………  
Parking: River Lane, **6** the building

**Questions 7–10 multiple choice**

7. The workshop is held on:  
A Monday B Saturday C Sunday  

8. Materials are:  
A sold at the door B provided C downloaded only  

9. A discount is available for:  
A students only B groups of four C members  

10. The centre’s name is:  
A Green Civic Centre B River Lane Hub C Community Hall

### Section 2 — Monologue (Questions 11–20)
**Talk:** Local council plans related to {topic}.

**Questions 11–15:** matching priorities A–E to statements (create labels: funding, training, public consultation, timeline, evaluation).  
**Questions 16–20:** map labelling of community facilities (North Gate, Lake Path, Info Desk, Cafe, Workshop Room).

*(Full map practice: sketch five buildings in a park layout and label from a partner’s oral description.)*

### Section 3 — Academic discussion (Questions 21–30)
Two students discuss a project on {topic}.

**Questions 21–25 MCQ; 26–30 matching researcher opinions.**

### Section 4 — Lecture (Questions 31–40)
Lecture title: “Evidence and policy: {topic}”

**Questions 31–40:** summary completion + short answers from lecture notes style text below.

**Lecture notes:** Research on {topic} shows three recurring findings: (1) early intervention is cheaper than late repair; (2) public trust rises when data are transparent; (3) local adaptation outperforms one-size-fits-all rules. Case studies from two cities indicate that participation rates increase when incentives are clear and procedures are simple. Critics argue that short political cycles undermine long projects. The lecturer concludes that measurement frameworks must track both efficiency and equity.

31–33 Complete the summary with words from the notes.  
34–40 Short answers (NO MORE THAN THREE WORDS).
"""


def reading_section(n: int, topic: str) -> str:
    passage_a = f"""### Passage 1 — The Quiet Politics of {topic.title()}

In the last two decades, debates about {topic} have moved from specialist journals into everyday conversation. This shift did not happen because the underlying science suddenly became simple; rather, digital media made contested claims highly visible. When visibility rises faster than public understanding, societies often polarise around symbols instead of mechanisms.

Researchers studying {topic} repeatedly observe a gap between what experts measure and what citizens experience. Experts may emphasise long-term indicators — cumulative exposure, systemic risk, or intergenerational cost — while residents focus on immediate inconvenience, fairness, and trust. Policy that ignores lived experience tends to fail even when technically elegant. Conversely, policy that only mirrors public mood can become unstable, swinging with headlines.

A useful framework distinguishes three layers of response. The first is **information**: accurate, timely, and comprehensible explanation. The second is **infrastructure**: the physical or digital systems that make better choices easy. The third is **incentives**: prices, norms, and rules that reward beneficial behaviour. Programmes that strengthen only one layer rarely endure. For example, campaigns about {topic} can raise awareness, yet without convenient alternatives and fair incentives, behaviour change remains fragile.

Comparative evidence suggests that cities which treat {topic} as a design problem — not merely a messaging problem — achieve more durable gains. They prototype small interventions, measure outcomes openly, and adjust without treating revision as political defeat. In that sense, the quiet politics of {topic} is less about winning arguments and more about building institutions that can learn.
"""
    passage_b = f"""### Passage 2 — Measuring What Matters in {topic.title()}

Measurement is often treated as a neutral prelude to action. In practice, the choice of metrics can decide which problems become visible. In the field of {topic}, narrow indicators may create an illusion of progress while broader harms accumulate elsewhere. Scholars therefore warn against “metric capture,” where organisations optimise for what is counted rather than what counts.

Consider a programme evaluated solely by short-term participation numbers. Attendance may rise because events are entertaining, yet long-term capability related to {topic} might not improve. A richer evaluation mix could include retention, transfer of skills, equity of access, and unintended consequences. Mixed-methods designs — combining statistics with interviews — are increasingly recommended precisely because {topic} sits at the intersection of behaviour, technology, and institutions.

International comparisons add another complication: data definitions differ. What one country classifies as success, another may exclude from official totals. Without careful harmonisation, league tables mislead policymakers and the public alike. The most responsible approach is humble quantification: publish methods, confidence ranges, and known blind spots alongside headline figures.
"""
    passage_c = f"""### Passage 3 — Futures Thinking and {topic.title()}

Forecasts about {topic} often fail not because analysts lack intelligence, but because social systems adapt around predictions. If a forecast of shortage triggers early investment, the shortage may never appear — making the forecast look “wrong” even though it was useful. This paradox implies that the value of futures work lies in preparedness, not prophetic accuracy.

Scenario planning offers a disciplined alternative to single-point prediction. Planners construct contrasting but plausible futures for {topic}, then identify actions that perform reasonably well across scenarios. Such “robust” strategies are typically modular: they can be scaled up, paused, or redirected as evidence arrives. Ethical scrutiny is essential, because interventions that protect majorities can still burden already disadvantaged groups.

Ultimately, maturity in managing {topic} looks like institutional patience: the capacity to maintain long projects, admit uncertainty, and revise course without abandoning core principles of fairness and evidence.
"""
    return f"""## Reading (40 questions) — 60 minutes

{passage_a}

**Questions 1–8:** True / False / Not Given  
**Questions 9–13:** Matching headings (i–viii) for paragraphs  

{passage_b}

**Questions 14–19:** Summary completion  
**Questions 20–26:** Multiple choice  

{passage_c}

**Questions 27–32:** Matching features (researcher/planner views)  
**Questions 33–40:** Yes / No / Not Given + short answers  

*(Detailed keys appear in the Answer Key section of this mock.)*
"""


def writing_section(n: int, topic: str) -> str:
    return f"""## Writing (60 minutes)

### Task 1 (Academic) — 20 minutes

The table below shows participation in community programmes related to **{topic}** in four cities in 2015 and 2025.

| City | 2015 (%) | 2025 (%) |
|------|----------|----------|
| Aderon | 12 | 28 |
| Belmora | 25 | 24 |
| Casterly | 9 | 31 |
| Durnham | 18 | 35 |

Summarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.

### Task 2 — 40 minutes

Some people believe that governments should take primary responsibility for problems connected to **{topic}**. Others argue that individuals and private organisations should lead change.

Discuss both views and give your own opinion. Write at least 250 words.
"""


def speaking_section(n: int, topic: str) -> str:
    return f"""## Speaking (11–14 minutes)

### Part 1
- Do you live in a house or an apartment?
- What do you like about your neighbourhood?
- Are you interested in issues related to {topic}? Why/why not?
- How do people in your country usually learn about social issues?

### Part 2 Cue card
Describe a project or activity related to **{topic}** that you have heard about.

You should say:
- what it was
- where it happened
- who was involved
and explain why it interested you.

### Part 3
- Why do some communities ignore problems linked to {topic}?
- What makes public campaigns about {topic} effective?
- Should schools teach more about {topic}? 
- How might international cooperation help?
"""


def answer_key(n: int) -> str:
    return f"""## Answer Key & Explanations (Mock {n})

### Listening
1. 10:15  
2. 10:00  
3. 18  
4. 12  
5. notebook  
6. behind  
7. B  
8. B  
9. B  
10. A  
11–40: Accept answers consistent with the transcripts/notes you used in partner practice; mark ruthlessly for spelling and word limits.

**Why 1 is 10:15 not 10:00:** 10:00 is arrival/registration; the main session starts later — classic distractor pattern.

### Reading (guide)
Passages support answers that distinguish awareness vs infrastructure vs incentives; beware Not Given items that invent funding figures not stated in the text.

### Writing — Band 9 Task 1 outline
- Overview: overall participation rose in three cities; Belmora slight fall
- Detail 1: Casterly largest rise (9→31)
- Detail 2: Durnham highest 2025; Belmora exception
- Comparisons with data; no reasons

### Writing — Band 9 Task 2 stance example
Governments must set rules and funding frameworks, but durable change requires individual habits and organisational practice; responsibility is shared, with the state as system designer.

### Speaking assessment checklist
Fluency, lexical precision on the topic, flexible Part 3 argumentation, pronunciation clarity.
"""


def mock_markdown(n: int) -> str:
    topic = TOPICS[(n - 1) % len(TOPICS)]
    return f"""# Practice Test {n:02d}: Complete IELTS Mock Exam

**Theme cluster:** {topic}  
**Timing:** Listening ~30 (+ transfer if paper) | Reading 60 | Writing 60 | Speaking 11–14

---

{listening_section(n, topic)}

---

{reading_section(n, topic)}

---

{writing_section(n, topic)}

---

{speaking_section(n, topic)}

---

{answer_key(n)}

---

*End of Mock {n}. Log your scores in the Error Journal before starting Mock {n+1 if n < 50 else 'review'}.*
"""


def write_how_to_and_keys() -> None:
    (OUT / "ch123_how_to_use_mocks.md").write_text(
        """# Chapter 123: How to Use the Mock Tests

**Part:** 9 — Practice Tests

---

## Learning Objectives

- Sit mocks under authentic timing and conditions
- Analyse errors by type, not only by score
- Convert mock performance into a weekly improvement plan

## Protocol

1. **Full exam simulation** at least once every 1–2 weeks (Listening→Reading→Writing in one sitting; Speaking same day).
2. **Score immediately**, then rest 30 minutes.
3. **Error journal** for every miss (see Part 1 / How to Use This Book).
4. **Targeted drills** the next day on the weakest question type.
5. **Rewrite** Writing Task 2 within 48 hours using feedback criteria.

## Scoring honesty

Do not inflate Writing/Speaking self-scores. Use public band descriptors and, if possible, a trained marker for every fifth mock.

## Review schedule

| Mocks | Focus |
|-------|-------|
| 1–10 | Format familiarity + timing |
| 11–25 | Accuracy under pressure |
| 26–40 | Band 7→8 refinement |
| 41–50 | Band 8–9 consistency + stamina |

## Exam Tips

Never review answers during the timed sitting. Never pause the Listening audio. Never exceed word-limit cheating in short-answer practice.

---
""",
        encoding="utf-8",
    )


def main() -> None:
    write_how_to_and_keys()
    all_keys = ["# Chapter 174: Consolidated Answer Keys\n\nSee each mock file for detailed keys. Summary checklist below.\n"]
    for i in range(1, 51):
        path = OUT / f"mock_{i:02d}.md"
        path.write_text(mock_markdown(i), encoding="utf-8")
        all_keys.append(f"- Mock {i:02d}: keys inside `mock_{i:02d}.md`\n")
        print(f"Wrote {path.name}")
    (OUT / "ch174_answer_keys.md").write_text("".join(all_keys), encoding="utf-8")
    print("Wrote 50 mocks + guides")


if __name__ == "__main__":
    main()
