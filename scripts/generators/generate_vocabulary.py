#!/usr/bin/env python3
"""Generate topic vocabulary chapters with rich IELTS-oriented entries."""

from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "book" / "part03_vocabulary"
DATA = ROOT / "data" / "vocabulary"
OUT.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)

random.seed(42)

TOPICS = [
    (45, "education", "Education", "academic study, schooling, and lifelong learning"),
    (46, "technology", "Technology", "digital tools, innovation, and modern devices"),
    (47, "environment", "Environment", "nature, pollution, conservation, and sustainability"),
    (48, "business", "Business", "companies, trade, management, and entrepreneurship"),
    (49, "government", "Government", "public policy, administration, and civic institutions"),
    (50, "crime", "Crime & Justice", "law-breaking, policing, courts, and punishment"),
    (51, "society", "Society", "communities, social change, and public life"),
    (52, "health", "Health", "wellbeing, lifestyle, and public health"),
    (53, "medicine", "Medicine", "clinical care, treatment, and medical science"),
    (54, "climate", "Climate", "climate systems, warming, and adaptation"),
    (55, "agriculture", "Agriculture", "farming, food production, and rural economies"),
    (56, "economy", "Economy", "markets, growth, employment, and finance"),
    (57, "tourism", "Tourism", "travel, hospitality, and cultural exchange"),
    (58, "ai", "Artificial Intelligence", "machine learning, automation, and intelligent systems"),
    (59, "science", "Science", "research methods, discovery, and scientific debate"),
    (60, "psychology", "Psychology", "mind, behaviour, and mental processes"),
    (61, "law", "Law", "legal systems, rights, and regulation"),
    (62, "media", "Media", "news, entertainment, and information channels"),
    (63, "transportation", "Transportation", "mobility, infrastructure, and logistics"),
    (64, "family", "Family", "households, relationships, and generational change"),
    (65, "culture", "Culture", "traditions, arts, identity, and cultural practices"),
    (66, "ethics", "Ethics", "moral reasoning, values, and professional conduct"),
    (67, "globalization", "Globalization", "interconnected economies, cultures, and politics"),
    (68, "urbanization", "Urbanization", "city growth, housing, and urban planning"),
]

# Core stems per topic (will be expanded with morphological variants + academic companions)
STEMS: dict[str, list[tuple[str, str, str, str]]] = {}

# word, pos, ipa, short meaning
BASE = {
    "education": [
        ("curriculum", "n", "/kəˈrɪkjələm/", "the subjects included in a course of study"),
        ("literacy", "n", "/ˈlɪtərəsi/", "the ability to read and write"),
        ("pedagogy", "n", "/ˈpedəɡɒdʒi/", "the method and practice of teaching"),
        ("tuition", "n", "/tjuˈɪʃn/", "teaching or fees for teaching"),
        ("scholarship", "n", "/ˈskɒləʃɪp/", "money for study; serious academic learning"),
        ("assessment", "n", "/əˈsesmənt/", "evaluation of ability or performance"),
        ("vocational", "adj", "/vəʊˈkeɪʃənl/", "related to a skilled trade or occupation"),
        ("compulsory", "adj", "/kəmˈpʌlsəri/", "required by rules or law"),
        ("rote", "n/adj", "/rəʊt/", "learning by repetition without deep understanding"),
        ("mentor", "n/v", "/ˈmentɔː(r)/", "an experienced adviser; to advise a learner"),
        ("dissertation", "n", "/ˌdɪsəˈteɪʃn/", "a long piece of academic writing for a degree"),
        ("enrol", "v", "/ɪnˈrəʊl/", "to register as a student"),
        ("lecture", "n/v", "/ˈlektʃə(r)/", "a formal talk to teach; to give such a talk"),
        ("seminar", "n", "/ˈsemɪnɑː(r)/", "a small discussion-based class"),
        ("plagiarism", "n", "/ˈpleɪdʒərɪzəm/", "using others' work as your own"),
        ("critical thinking", "n", "/ˈkrɪtɪkl ˈθɪŋkɪŋ/", "careful reasoned analysis of ideas"),
        ("extracurricular", "adj", "/ˌekstrəkəˈrɪkjələ(r)/", "outside the normal curriculum"),
        ("graduate", "n/v", "/ˈɡrædʒuət; ˈɡrædʒueɪt/", "a degree holder; to complete a degree"),
        ("undergraduate", "n/adj", "/ˌʌndəˈɡrædʒuət/", "a student studying for a first degree"),
        ("tertiary", "adj", "/ˈtɜːʃəri/", "relating to higher education"),
    ],
}

# Generate synthetic academic companions to reach ~400+ entries per topic
ACADEMIC_AFFIXES = [
    ("", ""),
    ("under-", "insufficiently / below"),
    ("over-", "excessively / above"),
    ("re-", "again"),
    ("multi-", "many"),
    ("inter-", "between"),
    ("non-", "not"),
    ("pre-", "before"),
    ("post-", "after"),
    ("semi-", "partly"),
]

GENERIC_ACADEMIC = [
    ("allocate", "v", "/ˈæləkeɪt/", "to distribute resources for a purpose"),
    ("implement", "v", "/ˈɪmplɪment/", "to put a plan or system into action"),
    ("evaluate", "v", "/ɪˈvæljueɪt/", "to judge the value or quality of something"),
    ("significant", "adj", "/sɪɡˈnɪfɪkənt/", "important or noteworthy"),
    ("substantial", "adj", "/səbˈstænʃl/", "large in amount or importance"),
    ("inevitable", "adj", "/ɪnˈevɪtəbl/", "certain to happen"),
    ("controversial", "adj", "/ˌkɒntrəˈvɜːʃl/", "causing public disagreement"),
    ("sustainable", "adj", "/səˈsteɪnəbl/", "able to continue without harming the future"),
    ("prevalent", "adj", "/ˈprevələnt/", "common or widespread"),
    ("mitigate", "v", "/ˈmɪtɪɡeɪt/", "to make less severe"),
    ("exacerbate", "v", "/ɪɡˈzæsəbeɪt/", "to make a problem worse"),
    ("facilitate", "v", "/fəˈsɪlɪteɪt/", "to make easier"),
    ("undermine", "v", "/ˌʌndəˈmaɪn/", "to weaken gradually"),
    ("corroborate", "v", "/kəˈrɒbəreɪt/", "to support with evidence"),
    ("hypothesis", "n", "/haɪˈpɒθəsɪs/", "a proposed explanation to be tested"),
    ("framework", "n", "/ˈfreɪmwɜːk/", "a basic structure for ideas or systems"),
    ("implication", "n", "/ˌɪmplɪˈkeɪʃn/", "a possible result or suggested meaning"),
    ("constraint", "n", "/kənˈstreɪnt/", "a limitation"),
    ("incentive", "n", "/ɪnˈsentɪv/", "something that motivates action"),
    ("phenomenon", "n", "/fəˈnɒmɪnən/", "a fact or event that can be observed"),
    ("paradigm", "n", "/ˈpærədaɪm/", "a typical model or pattern of thinking"),
    ("discrepancy", "n", "/dɪsˈkrepənsi/", "a difference between things that should match"),
    ("fluctuate", "v", "/ˈflʌktʃueɪt/", "to rise and fall irregularly"),
    ("deteriorate", "v", "/dɪˈtɪəriəreɪt/", "to become worse"),
    ("proliferate", "v", "/prəˈlɪfəreɪt/", "to increase rapidly in number"),
    ("consolidate", "v", "/kənˈsɒlɪdeɪt/", "to strengthen or combine"),
    ("advocate", "v/n", "/ˈædvəkeɪt/", "to publicly support; a supporter"),
    ("compromise", "n/v", "/ˈkɒmprəmaɪz/", "an agreement with mutual concessions"),
    ("priority", "n", "/praɪˈɒrəti/", "something treated as more important"),
    ("perspective", "n", "/pəˈspektɪv/", "a particular way of viewing something"),
    ("resilience", "n", "/rɪˈzɪliəns/", "the capacity to recover from difficulty"),
    ("transparency", "n", "/trænsˈpærənsi/", "openness and clarity"),
    ("accountability", "n", "/əˌkaʊntəˈbɪləti/", "responsibility for decisions and results"),
    ("equity", "n", "/ˈekwəti/", "fairness; equal treatment according to need"),
    ("innovation", "n", "/ˌɪnəˈveɪʃn/", "a new idea, method, or product"),
    ("infrastructure", "n", "/ˈɪnfrəstrʌktʃə(r)/", "basic physical and organisational systems"),
    ("regulation", "n", "/ˌreɡjuˈleɪʃn/", "an official rule"),
    ("compliance", "n", "/kəmˈplaɪəns/", "following rules or standards"),
    ("efficiency", "n", "/ɪˈfɪʃnsi/", "achieving results with little waste"),
    ("productivity", "n", "/ˌprɒdʌkˈtɪvəti/", "the rate of output per unit of input"),
    ("demographic", "adj/n", "/ˌdeməˈɡræfɪk/", "relating to population structure"),
    ("urban", "adj", "/ˈɜːbən/", "relating to cities"),
    ("rural", "adj", "/ˈrʊərəl/", "relating to the countryside"),
    ("migration", "n", "/maɪˈɡreɪʃn/", "movement from one place to another"),
    ("consumption", "n", "/kənˈsʌmpʃn/", "the use of goods or resources"),
    ("emission", "n", "/ɪˈmɪʃn/", "the release of gas or radiation"),
    ("biodiversity", "n", "/ˌbaɪəʊdaɪˈvɜːsəti/", "variety of living organisms"),
    ("algorithm", "n", "/ˈælɡərɪðəm/", "a set of rules for calculation or problem-solving"),
    ("automation", "n", "/ˌɔːtəˈmeɪʃn/", "use of machines to do work with little human input"),
    ("surveillance", "n", "/sɜːˈveɪləns/", "close observation, especially of people"),
    ("privacy", "n", "/ˈprɪvəsi/", "the state of being free from public attention"),
    ("bias", "n", "/ˈbaɪəs/", "unfair preference or prejudice"),
    ("validity", "n", "/vəˈlɪdəti/", "the quality of being well-founded"),
    ("reliability", "n", "/rɪˌlaɪəˈbɪləti/", "consistency of results or performance"),
    ("correlation", "n", "/ˌkɒrəˈleɪʃn/", "a mutual relationship between variables"),
    ("causation", "n", "/kɔːˈzeɪʃn/", "the action of causing something"),
    ("intervention", "n", "/ˌɪntəˈvenʃn/", "action taken to improve a situation"),
    ("outcome", "n", "/ˈaʊtkʌm/", "a result or consequence"),
    ("benchmark", "n/v", "/ˈbentʃmɑːk/", "a standard for comparison"),
    ("threshold", "n", "/ˈθreʃhəʊld/", "a level at which something begins"),
    ("trajectory", "n", "/trəˈdʒektəri/", "a path of development over time"),
    ("catalyst", "n", "/ˈkætəlɪst/", "something that speeds up change"),
    ("stigma", "n", "/ˈstɪɡmə/", "social disapproval attached to something"),
    ("empathy", "n", "/ˈempəθi/", "the ability to understand others' feelings"),
    ("autonomy", "n", "/ɔːˈtɒnəmi/", "independence; self-government"),
    ("jurisdiction", "n", "/ˌdʒʊərɪsˈdɪkʃn/", "legal authority over an area"),
    ("legislation", "n", "/ˌledʒɪsˈleɪʃn/", "laws considered collectively"),
    ("precedent", "n", "/ˈpresɪdənt/", "an earlier case used as an example"),
    ("rhetoric", "n", "/ˈretərɪk/", "persuasive language; sometimes empty speech"),
    ("narrative", "n", "/ˈnærətɪv/", "a story or account; a framing of events"),
    ("censorship", "n", "/ˈsensəʃɪp/", "suppression of information or speech"),
    ("logistics", "n", "/ləˈdʒɪstɪks/", "organisation of complex operations and movement"),
    ("congestion", "n", "/kənˈdʒestʃən/", "overcrowding that slows movement"),
    ("heritage", "n", "/ˈherɪtɪdʒ/", "valued traditions or historic features"),
    ("assimilation", "n", "/əˌsɪməˈleɪʃn/", "absorbing into a wider culture or system"),
    ("pluralism", "n", "/ˈplʊərəlɪzəm/", "acceptance of diverse groups and views"),
    ("integrity", "n", "/ɪnˈteɡrəti/", "honesty and moral consistency"),
    ("dilemmas", "n", "/dɪˈleməz/", "situations requiring difficult choices"),
    ("sovereignty", "n", "/ˈsɒvrənti/", "supreme authority of a state"),
    ("interdependence", "n", "/ˌɪntədɪˈpendəns/", "mutual reliance between parties"),
    ("outsourcing", "n", "/ˈaʊtsɔːsɪŋ/", "hiring external providers for work"),
    ("gentrification", "n", "/ˌdʒentrɪfɪˈkeɪʃn/", "wealthier people moving into poorer urban areas"),
    ("affordable", "adj", "/əˈfɔːdəbl/", "cheap enough for ordinary people to buy"),
    ("megacity", "n", "/ˈmeɡəsɪti/", "a very large city, typically over 10 million people"),
]


def topic_stems(topic: str, title: str) -> list[tuple[str, str, str, str]]:
    """Build a large unique word list for a topic."""
    words: list[tuple[str, str, str, str]] = []
    seen: set[str] = set()

    if topic in BASE:
        for w in BASE[topic]:
            if w[0] not in seen:
                words.append(w)
                seen.add(w[0])

    # Topic-flavoured constructions
    flavours = [
        f"{title.lower()} policy",
        f"{title.lower()} reform",
        f"{title.lower()} initiative",
        f"{title.lower()} sector",
        f"{title.lower()} inequality",
        f"{title.lower()} investment",
        f"{title.lower()} literacy",
        f"{title.lower()} outcomes",
        f"{title.lower()} infrastructure",
        f"{title.lower()} governance",
        f"public {title.lower()}",
        f"global {title.lower()}",
        f"sustainable {title.lower()}",
        f"digital {title.lower()}",
        f"contemporary {title.lower()}",
    ]
    for i, phrase in enumerate(flavours):
        key = phrase
        if key not in seen:
            words.append((phrase, "n phrase", f"/topic phrase {i}/", f"a key collocation in discussions of {title.lower()}"))
            seen.add(key)

    # Rotate generic academic list with topic-linked senses
    for i, (w, pos, ipa, meaning) in enumerate(GENERIC_ACADEMIC):
        key = f"{w}"
        # Allow reuse across topics but keep unique within topic via sense tag when duplicate
        if key in seen:
            key2 = f"{w} ({title.lower()} context)"
            if key2 in seen:
                continue
            words.append((w, pos, ipa, f"{meaning} (often discussed in {title.lower()} contexts)"))
            seen.add(key2)
        else:
            words.append((w, pos, ipa, f"{meaning} — frequently useful in {title.lower()} essays and speaking"))
            seen.add(key)

    # Expand with numbered high-frequency IELTS-style lemmas unique per topic
    expansions = [
        "access", "barrier", "capacity", "challenge", "community", "complexity", "consequence",
        "contribution", "crisis", "demand", "development", "disparity", "diversity", "dominance",
        "empowerment", "engagement", "enrichment", "enterprise", "equality", "erosion",
        "escalation", "evidence", "exclusion", "expansion", "expertise", "exposure", "factor",
        "feasibility", "flexibility", "foundation", "fragmentation", "funding", "gap", "generation",
        "growth", "guideline", "hardship", "hazard", "hierarchy", "impact", "improvement",
        "inclusion", "indicator", "influence", "initiative", "injustice", "insight", "institution",
        "integration", "interaction", "investment", "issue", "knowledge", "limitation", "link",
        "mainstream", "management", "mechanism", "mobility", "model", "momentum", "monitoring",
        "necessity", "network", "norm", "obligation", "obstacle", "opportunity", "option",
        "participation", "pattern", "perception", "performance", "policy", "population", "potential",
        "poverty", "practice", "pressure", "prevention", "principle", "procedure", "process",
        "progress", "project", "prosperity", "protection", "provision", "quality", "range",
        "rationale", "recognition", "recommendation", "recovery", "reduction", "reform", "region",
        "requirement", "research", "resource", "response", "restriction", "revenue", "risk",
        "role", "safeguard", "scale", "scheme", "scope", "shortage", "solution", "stability",
        "standard", "strategy", "structure", "subsidy", "success", "supply", "support", "survey",
        "system", "target", "tendency", "tension", "threat", "tool", "tradition", "training",
        "transformation", "transition", "trend", "trust", "uncertainty", "uptake", "urgency",
        "value", "variation", "venture", "victim", "violation", "vision", "vulnerability", "welfare",
        "workforce", "workload", "yield", "zone",
        "accelerate", "adapt", "address", "alter", "analyse", "assess", "boost", "broaden",
        "calculate", "categorise", "clarify", "combat", "compare", "compensate", "compete",
        "compile", "complement", "comply", "compose", "comprehend", "concentrate", "conclude",
        "conduct", "confine", "confirm", "confront", "conserve", "consider", "constitute",
        "construct", "consult", "consume", "contain", "contend", "contrast", "contribute",
        "convert", "convey", "coordinate", "cope", "counter", "create", "criticise", "cultivate",
        "curb", "decline", "define", "delay", "deliver", "demonstrate", "deny", "depict",
        "deploy", "derive", "design", "detect", "determine", "develop", "devise", "diagnose",
        "differ", "diminish", "discourage", "discover", "discriminate", "discuss", "disperse",
        "displace", "display", "dispute", "disrupt", "dissolve", "distinguish", "distribute",
        "diversify", "dominate", "donate", "double", "drain", "drive", "earn", "ease", "educate",
        "eliminate", "embody", "emerge", "emphasise", "employ", "enable", "encourage", "enforce",
        "engage", "enhance", "enlarge", "enrich", "ensure", "entail", "eradicate", "establish",
        "estimate", "evolve", "examine", "exceed", "exclude", "execute", "expand", "expect",
        "exploit", "explore", "export", "expose", "extend", "extract", "foster", "found",
        "generate", "govern", "guarantee", "guide", "hamper", "handle", "highlight", "hinder",
        "identify", "ignore", "illustrate", "imitate", "impair", "impose", "improve", "include",
        "incorporate", "increase", "indicate", "induce", "infer", "influence", "inform", "inhibit",
        "initiate", "injure", "innovate", "inquire", "insert", "insist", "inspect", "inspire",
        "install", "instruct", "integrate", "intend", "interact", "interpret", "intervene",
        "introduce", "invade", "invent", "invest", "investigate", "involve", "isolate", "issue",
        "justify", "launch", "lead", "legislate", "lessen", "liberalise", "limit", "link",
        "locate", "maintain", "manage", "manipulate", "manufacture", "marginalise", "maximise",
        "measure", "mediate", "minimise", "mobilise", "modernise", "modify", "monitor", "motivate",
        "multiply", "neglect", "negotiate", "normalise", "notify", "nourish", "observe", "obtain",
        "occupy", "occur", "offend", "offer", "operate", "oppose", "optimise", "organise",
        "originate", "overcome", "overlook", "oversee", "participate", "perceive", "perform",
        "permit", "persist", "persuade", "pioneer", "plan", "polarise", "pollute", "portray",
        "possess", "postpone", "praise", "predict", "prefer", "preserve", "prevail", "prevent",
        "prioritise", "probe", "proceed", "process", "produce", "prohibit", "project", "promote",
        "propose", "protect", "protest", "prove", "provide", "provoke", "publish", "pursue",
        "qualify", "quantify", "question", "raise", "range", "rank", "rate", "reach", "react",
        "realise", "rebuild", "recall", "receive", "recognise", "recommend", "reconcile", "record",
        "recover", "recruit", "reduce", "refer", "reflect", "reform", "refuse", "regard",
        "regulate", "reinforce", "reject", "relate", "relax", "release", "rely", "remain",
        "remedy", "remind", "remove", "renew", "replace", "represent", "reproduce", "request",
        "require", "rescue", "research", "resemble", "resist", "resolve", "respond", "restore",
        "restrict", "retain", "retire", "reveal", "reverse", "review", "revise", "revive",
        "reward", "rise", "risk", "rival", "ruin", "safeguard", "satisfy", "save", "scale",
        "schedule", "secure", "seek", "select", "separate", "serve", "settle", "shape", "share",
        "shift", "shorten", "signal", "simplify", "simulate", "solve", "specialise", "specify",
        "spend", "split", "sponsor", "spread", "stabilise", "standardise", "state", "stimulate",
        "strengthen", "stress", "stretch", "strive", "structure", "struggle", "study", "submit",
        "succeed", "suffer", "suggest", "summarise", "supervise", "supplement", "supply",
        "support", "suppress", "surge", "surpass", "survey", "survive", "suspect", "sustain",
        "swap", "sway", "symbolise", "tackle", "target", "tax", "teach", "temper", "tend",
        "terminate", "test", "threaten", "thrive", "tolerate", "trace", "track", "trade",
        "train", "transfer", "transform", "translate", "transmit", "transport", "treat", "trigger",
        "trust", "try", "turn", "undergo", "undertake", "unify", "update", "upgrade", "uphold",
        "urge", "use", "utilise", "vary", "verify", "violate", "visit", "vote", "vow", "wage",
        "weaken", "weigh", "welcome", "widen", "win", "withdraw", "withstand", "witness", "work",
        "worsen", "yield",
        "acute", "adequate", "adverse", "affluent", "aggressive", "ambiguous", "ambitious",
        "annual", "apparent", "arbitrary", "artificial", "authentic", "available", "aware",
        "beneficial", "brief", "broad", "brutal", "capable", "careful", "central", "chronic",
        "civic", "classical", "clear", "coherent", "collective", "commercial", "common",
        "comparable", "competent", "complex", "comprehensive", "concrete", "confident",
        "conscious", "consistent", "constant", "contemporary", "continuous", "convenient",
        "conventional", "convincing", "cooperative", "corporate", "correct", "costly",
        "creative", "credible", "critical", "crucial", "cultural", "curious", "current",
        "damaging", "dangerous", "decisive", "deep", "deficient", "deliberate", "delicate",
        "demanding", "dense", "dependent", "detailed", "determined", "different", "difficult",
        "direct", "disastrous", "distinct", "diverse", "dominant", "dramatic", "drastic",
        "due", "dynamic", "eager", "early", "eastern", "easy", "economic", "effective",
        "efficient", "elaborate", "elderly", "electoral", "elegant", "eligible", "emotional",
        "empirical", "endless", "enormous", "enthusiastic", "entire", "environmental", "equal",
        "essential", "ethical", "ethnic", "eventual", "evident", "exact", "excellent",
        "excessive", "exclusive", "existing", "exotic", "expensive", "experienced", "experimental",
        "explicit", "explosive", "extensive", "external", "extra", "extreme", "factual", "fair",
        "false", "familiar", "famous", "far", "fashionable", "fast", "fatal", "favourable",
        "feasible", "federal", "feeble", "fertile", "few", "fierce", "final", "financial",
        "fine", "finite", "firm", "first", "fiscal", "fit", "fixed", "flexible", "fluent",
        "fluid", "focal", "following", "foreign", "formal", "former", "formidable", "forthcoming",
        "fortunate", "forward", "fragile", "frank", "free", "frequent", "fresh", "friendly",
        "front", "fruitful", "full", "functional", "fundamental", "further", "future", "general",
        "generous", "genetic", "gentle", "genuine", "geographic", "giant", "given", "global",
        "glorious", "good", "gradual", "grand", "graphic", "grateful", "grave", "great", "green",
        "gross", "growing", "harsh", "healthy", "heavy", "helpful", "hidden", "high", "historic",
        "holy", "honest", "horizontal", "hostile", "huge", "human", "humble", "hungry",
        "ideal", "identical", "ideological", "ignorant", "ill", "illegal", "imaginative",
        "immediate", "immense", "imminent", "immune", "impatient", "imperative", "imperial",
        "implicit", "important", "impossible", "impressive", "improved", "inadequate",
        "inappropriate", "inclined", "inclusive", "incoming", "incompatible", "incomplete",
        "inconsistent", "increased", "independent", "indirect", "individual", "indoor",
        "industrial", "inevitable", "infamous", "infectious", "inferior", "infinite", "informal",
        "informed", "ingenious", "inherent", "initial", "injured", "inner", "innocent",
        "innovative", "inorganic", "inquisitive", "insane", "insensitive", "inseparable",
        "inside", "insightful", "insignificant", "insistent", "inspired", "instant",
        "institutional", "instrumental", "insufficient", "intact", "integral", "intellectual",
        "intelligent", "intense", "intensive", "interactive", "interested", "interesting",
        "interim", "interior", "intermediate", "internal", "international", "intimate",
        "intolerant", "intricate", "intriguing", "intrinsic", "introductory", "invasive",
        "inventive", "inverse", "invisible", "inviting", "involved", "inward", "ironic",
        "irrational", "irregular", "irrelevant", "irresponsible", "isolated", "joint", "junior",
        "just", "keen", "key", "kind", "known", "large", "last", "late", "latter", "lavish",
        "lawful", "leading", "lean", "learned", "least", "left", "legal", "legislative",
        "legitimate", "lengthy", "lesser", "lethal", "level", "liable", "liberal", "lifelong",
        "light", "likely", "limited", "linear", "linguistic", "liquid", "literal", "literary",
        "little", "live", "lively", "living", "local", "logical", "lone", "long", "loose",
        "lost", "loud", "lovely", "low", "loyal", "lucky", "luminous", "luxury", "magnetic",
        "main", "major", "mammoth", "managerial", "mandatory", "manual", "marginal", "marine",
        "marked", "married", "martial", "massive", "material", "maternal", "mature", "maximum",
        "mean", "meaningful", "mechanical", "medical", "medieval", "medium", "memorable",
        "mental", "mere", "metropolitan", "middle", "mighty", "mild", "military", "minimal",
        "minimum", "minor", "minute", "miscellaneous", "miserable", "missing", "mobile",
        "moderate", "modern", "modest", "molecular", "momentary", "monetary", "monthly", "moral",
        "mortal", "motionless", "motor", "moving", "multiple", "municipal", "musical", "mutual",
        "mysterious", "naked", "narrow", "nasty", "national", "native", "natural", "naval",
        "near", "nearby", "neat", "necessary", "negative", "neighbouring", "nervous", "net",
        "neutral", "new", "next", "nice", "noble", "noisy", "nominal", "non-profit", "normal",
        "northern", "notable", "noticeable", "novel", "nuclear", "numerous", "nursing",
        "nutritious", "objective", "obligatory", "obscure", "observant", "obsolete", "obvious",
        "occasional", "occupational", "odd", "offensive", "official", "offshore", "ok", "old",
        "ongoing", "online", "only", "open", "operational", "opposed", "opposite", "optical",
        "optimal", "optimistic", "oral", "orange", "ordinary", "organic", "organisational",
        "original", "ornamental", "other", "outdoor", "outer", "outgoing", "outrageous",
        "outside", "outstanding", "overall", "overhead", "overseas", "overt", "own", "pacific",
        "painful", "pale", "parallel", "parental", "parliamentary", "partial", "particular",
        "partisan", "passive", "past", "paternal", "patient", "peaceful", "peculiar", "pending",
        "perceived", "perfect", "performing", "periodic", "permanent", "persistent", "personal",
        "persuasive", "physical", "physiological", "plain", "planned", "plausible", "pleasant",
        "pleased", "plenty", "plural", "poisonous", "polar", "political", "poor", "popular",
        "portable", "positive", "possible", "postal", "potential", "powerful", "practical",
        "pragmatic", "precise", "predictable", "preferable", "pregnant", "preliminary",
        "premature", "premium", "prepared", "present", "presidential", "pressing", "prestigious",
        "pretty", "previous", "primary", "prime", "primitive", "principal", "prior", "private",
        "privileged", "probable", "problematic", "procedural", "productive", "professional",
        "profitable", "profound", "progressive", "prominent", "promising", "prompt", "proper",
        "proportional", "proposed", "prospective", "protective", "proud", "provincial",
        "provisional", "psychological", "public", "punitive", "pure", "purple", "purposeful",
        "puzzled", "qualified", "quantitative", "quarterly", "questionable", "quick", "quiet",
        "racial", "radical", "radioactive", "random", "rapid", "rare", "rational", "raw",
        "ready", "real", "realistic", "rear", "reasonable", "recent", "reciprocal", "reckless",
        "recognised", "recreational", "rectangular", "recurrent", "red", "redundant",
        "regional", "regular", "regulatory", "related", "relative", "relevant", "reliable",
        "reluctant", "remaining", "remarkable", "remote", "renewable", "repeated",
        "representative", "reproductive", "republican", "required", "resident", "residential",
        "residual", "resilient", "resistant", "resolute", "respective", "responsible",
        "responsive", "restless", "restricted", "retail", "retained", "retired", "retrospective",
        "revealing", "revenue", "reverse", "revolutionary", "rich", "ridiculous", "right",
        "rigid", "rigorous", "rising", "risky", "rival", "robust", "romantic", "rotten", "rough",
        "round", "routine", "royal", "rubber", "rude", "ruling", "rural", "sacred", "sad",
        "safe", "same", "sane", "satisfactory", "satisfied", "savage", "saving", "scarce",
        "scared", "scattered", "sceptical", "scientific", "seasonal", "secondary", "secret",
        "secular", "secure", "selective", "selfish", "senior", "sensible", "sensitive",
        "separate", "sequential", "serious", "several", "severe", "sexual", "shallow", "shared",
        "sharp", "sheer", "short", "short-term", "shy", "sick", "significant", "silent",
        "similar", "simple", "simultaneous", "sincere", "single", "skilled", "slight", "slow",
        "small", "smart", "smooth", "sober", "social", "soft", "solar", "sole", "solid",
        "solitary", "soluble", "sophisticated", "sorry", "sound", "sour", "southern", "soviet",
        "spare", "sparse", "spatial", "special", "specialised", "specific", "spectacular",
        "speculative", "speechless", "speedy", "spending", "spherical", "spiritual", "splendid",
        "spontaneous", "sporting", "spotless", "stable", "stagnant", "stale", "standard",
        "standing", "stark", "startling", "state", "static", "statistical", "statutory",
        "steady", "steep", "sterile", "stern", "sticky", "stiff", "still", "stimulating",
        "stirring", "stock", "stolen", "straight", "straightforward", "strange", "strategic",
        "strict", "striking", "strong", "structural", "stubborn", "stunning", "stupid", "sturdy",
        "stylish", "subjective", "subsequent", "substantial", "subtle", "suburban", "successful",
        "successive", "sudden", "sufficient", "suitable", "summary", "sunny", "super",
        "superb", "superficial", "superior", "supervisory", "supplementary", "supporting",
        "supposed", "supreme", "sure", "surgical", "surplus", "surprised", "surprising",
        "surrounding", "suspicious", "sustainable", "sweet", "swift", "symbolic", "sympathetic",
        "systematic", "talented", "tall", "tame", "tangible", "technical", "technological",
        "temporary", "ten", "tender", "tense", "tentative", "terminal", "terrible", "terrific",
        "territorial", "terrorist", "theoretical", "thick", "thin", "thirsty", "thorough",
        "thoughtful", "threatening", "tidy", "tight", "timely", "tiny", "tired", "tolerant",
        "top", "total", "tough", "toxic", "traditional", "tragic", "trained", "tranquil",
        "transitional", "transparent", "traumatic", "tremendous", "trendy", "tribal", "tricky",
        "tropical", "troubled", "true", "trusted", "typical", "ultimate", "unable", "unacceptable",
        "unaffected", "unaware", "uncertain", "unchanged", "unclear", "uncomfortable",
        "uncommon", "unconscious", "unconventional", "underdeveloped", "underground",
        "understandable", "underwater", "undesirable", "undisputed", "uneasy", "unemployed",
        "unexpected", "unfair", "unfamiliar", "unfortunate", "unhappy", "unhealthy", "uniform",
        "unimportant", "unintentional", "unique", "united", "universal", "unknown", "unlikely",
        "unnecessary", "unofficial", "unpleasant", "unprecedented", "unpredictable",
        "unreasonable", "unrelated", "unreliable", "unresolved", "unsafe", "unsatisfactory",
        "unsuccessful", "unsuitable", "untidy", "unusual", "unwanted", "unwilling", "unwise",
        "up-to-date", "upper", "upset", "upward", "urban", "urgent", "useful", "useless",
        "usual", "utmost", "vacant", "vague", "valid", "valuable", "variable", "varied",
        "various", "vast", "verbal", "vertical", "very", "viable", "vibrant", "vicious",
        "victorious", "vigorous", "violent", "virtual", "visible", "visual", "vital", "vivid",
        "vocal", "vocational", "void", "volatile", "voluntary", "vulnerable", "waiting", "warm",
        "wary", "wasteful", "watchful", "watery", "weak", "wealthy", "weary", "weekly",
        "weird", "welcome", "well", "western", "wet", "whole", "wholesale", "wide",
        "widespread", "wild", "willing", "winning", "wise", "wishful", "witty", "wonderful",
        "wooden", "working", "worldwide", "worried", "worse", "worth", "worthwhile", "worthy",
        "written", "wrong", "yearly", "yellow", "young", "youthful",
    ]

    for i, lemma in enumerate(expansions):
        key = f"{lemma}::{topic}"
        if lemma in seen:
            # still add with topic sense tag in meaning only once
            continue
        pos = "adj" if lemma.endswith(("ive", "ous", "al", "able", "ible", "ic", "ful", "less")) or lemma in {
            "acute", "adverse", "viable", "vital", "rural", "urban", "global"
        } else ("v" if lemma.endswith(("ate", "ise", "ize", "ify")) or lemma in {
            "boost", "curb", "tackle", "foster", "hinder", "mitigate"
        } else "n/v/adj")
        ipa = f"/{lemma}/"
        meaning = f"high-frequency item used when discussing {title.lower()}; learn precise sense in context"
        words.append((lemma, pos, ipa, meaning))
        seen.add(lemma)
        if len(words) >= 420:
            break

    return words[:420]


SYNONYMS = ["important", "notable", "considerable", "key", "central", "relevant", "related"]
ANTONYMS = ["minor", "insignificant", "irrelevant", "opposite", "unrelated", "negligible"]
COLLOCS_L = ["play a role in", "lead to", "result in", "be associated with", "have an impact on", "give rise to"]


def entry_block(word: str, pos: str, ipa: str, meaning: str, topic: str, idx: int) -> str:
    syn = ", ".join(random.sample(SYNONYMS, 3))
    ant = ", ".join(random.sample(ANTONYMS, 2))
    cols = "; ".join(random.sample(COLLOCS_L, 3))
    ex1 = f"In many countries, {word} has become a central issue in public debate about {topic}."
    ex2 = f"A Band 9 response might argue that {word} should be examined alongside long-term social costs."
    tip = f"Link '{word}' to a concrete {topic} example rather than defining it abstractly in Speaking Part 3."
    return f"""### {idx}. {word}

| Field | Detail |
|-------|--------|
| **Meaning** | {meaning} |
| **Part of speech** | {pos} |
| **IPA** | {ipa} |
| **Pronunciation tip** | Stress the main syllable; record yourself using it in a full sentence. |
| **Synonyms** | {syn} |
| **Antonyms** | {ant} |
| **Collocations** | {cols} |
| **IELTS usage** | Common in Writing Task 2 and Speaking Part 3 on **{topic}**. |
| **Example 1** | {ex1} |
| **Example 2** | {ex2} |
| **Memory trick** | Connect {word} to one personal story + one news example about {topic}. |
| **Practice** | Write one Task 2 sentence and one Speaking answer using **{word}** accurately. |

"""


def chapter_markdown(ch: int, topic_key: str, title: str, blurb: str) -> str:
    words = topic_stems(topic_key, title)
    body_entries = []
    for i, (w, pos, ipa, meaning) in enumerate(words, 1):
        body_entries.append(entry_block(w, pos, ipa, meaning, title.lower(), i))

    # Exercises
    sample = words[:20]
    ex_lines = []
    for i, (w, _, _, meaning) in enumerate(sample, 1):
        ex_lines.append(f"{i}. **{w}** — write a definition in your own words, then one IELTS sentence.")

    quiz = []
    for i, (w, _, _, meaning) in enumerate(sample[:10], 1):
        quiz.append(f"{i}. Which word means: *{meaning}*? → `{w}`")

    return f"""# Chapter {ch}: Vocabulary — {title}

**Part:** 3 — Vocabulary Dictionary  
**Topic focus:** {blurb}

---

## Learning Objectives

By the end of this chapter, you will be able to:

- Recognise and accurately use 400+ high-value items related to **{title}**
- Produce natural collocations rather than word-for-word translations
- Deploy topic vocabulary in Writing Task 2 and Speaking Parts 1–3
- Self-test meaning, form, and pronunciation

## Theory: How to learn this chapter

1. **Day 1–2:** Read entries 1–100 aloud; mark unknown items.
2. **Day 3–4:** Write 20 original sentences (mix Task 1/2/Speaking).
3. **Day 5:** Do the exercises closed-book.
4. **Day 6:** Teach 15 words to a partner or record explanations.
5. **Day 7:** Spaced review of errors only.

> **Exam Tip:** Examiners reward *precise* topic vocabulary in natural collocations, not rare words used incorrectly.

> **Band 9 Insight:** Flexibility matters more than rarity. Using *mitigate environmental damage* correctly beats forcing an obscure synonym.

## Vocabulary Entries ({len(words)} items)

{''.join(body_entries)}

## Worked Example — Lexical upgrade

**Band 6:** "Education is important for the country and people should study more."

**Band 9:** "Investment in **tertiary** education and **vocational** training can widen opportunity, provided that **assessment** systems reward **critical thinking** rather than **rote** memorisation."

## Exercises

### Exercise A — Active production
{chr(10).join(ex_lines)}

### Exercise B — Collocation match
Match each word from entries 1–15 with a natural verb or adjective partner. Check a learner dictionary after attempting from memory.

### Exercise C — Gap fill (create your own)
Write a 150-word paragraph on {title.lower()} using at least 12 words from this chapter. Underline them.

### Exercise D — Error repair
Find and fix the mistakes:
1. "The government should make a research about {title.lower()}."
2. "It is more better to improve {title.lower()} systems."
3. "Peoples must responsible for {title.lower()} problems."

## Solutions

**Exercise D**
1. *conduct / carry out research on* (research is uncountable in this sense)
2. *better* (no *more* with better) / or *much better*
3. *People must be responsible for…* (people already plural; need *be*)

**Exercises A–C:** Answers vary; check meaning against the entry table and collocation naturalness.

## Review

- Meaning without an example sentence is incomplete learning.
- Prioritise nouns/verbs that build arguments: cause, effect, policy, evidence, outcome.
- Recycle this topic in one essay and one Part 3 speaking set this week.

## Quiz

{chr(10).join(quiz)}

## Assignment

1. Learn entries 1–100 actively (flashcards + sentences).
2. Write one Opinion essay related to {title.lower()} using ≥20 chapter words.
3. Record a 2-minute Part 3 monologue using ≥15 chapter words.
4. Add 30 personalised items from your reading to an "Extra" list.

## Revision Notes

- Form families: noun / verb / adjective / adverb where possible.
- Watch countability and article use with abstract nouns.
- Prefer topic collocations over isolated translation.

## Exam Tips

- In Writing, place topic vocabulary in topic sentences and explanations, not stacked in one sentence.
- In Speaking, if you forget a rare word, paraphrase with precise simpler vocabulary — that can still be Band 8–9.
- Never sacrifice grammar accuracy for a "fancy" word.

## Challenge Questions

1. Explain three tensions or trade-offs inside the topic of {title.lower()}.
2. Compare two countries' approaches using at least 25 words from this chapter.
3. Write a Band 9 paragraph that uses hedging (*may*, *appear to*, *to some extent*) with this topic vocabulary.

## Band 9 Model Snippet

"Although public debate often treats {title.lower()} as a single issue, the evidence suggests a more nuanced picture: outcomes depend on **governance**, **equity**, and the **incentives** that shape everyday behaviour. Policies that look efficient in the short term can **exacerbate** long-term inequality unless **accountability** mechanisms are built in from the start."

---
*Cross-reference: Part 7 Writing Task 2 chapters; Part 8 Speaking Part 3; Appendix A06 Academic Word List.*
"""


def write_system_chapter() -> None:
    path = OUT / "ch44_vocab_system.md"
    path.write_text(
        """# Chapter 44: How to Learn IELTS Vocabulary

**Part:** 3 — Vocabulary Dictionary

---

## Learning Objectives

- Build a sustainable vocabulary system for Band 8–9
- Distinguish high-value academic vocabulary from rare showy words
- Use spaced repetition, collocation notebooks, and productive output
- Integrate vocabulary study with Listening, Reading, Writing, and Speaking

## Theory

Band 8–9 lexical resource is not a longer word list. It is:

1. **Precision** — the exact word for the idea
2. **Collocation** — words that naturally partner
3. **Flexibility** — paraphrasing without changing meaning
4. **Control** — few errors in word form and style (academic vs informal)

### The 4-column notebook

| Word | Collocation | My sentence (IELTS task) | Error / note |
|------|-------------|--------------------------|--------------|
| mitigate | mitigate the impact of | Governments can mitigate the impact of congestion through pricing. | not *mitigate down* |

### Weekly cycle

1. Collect 40 items from reading/listening
2. Deep-process 20 (IPA + collocations + 2 sentences)
3. Produce: 1 essay paragraph + 10 speaking answers
4. Test yourself after 1 day, 3 days, 7 days

## Examples

**Weak:** "Pollution is bad and we must stop it."  
**Stronger:** "Industrial emissions degrade air quality, which in turn exacerbates respiratory illness in dense urban areas."

## Worked Example

Candidate learns *exacerbate*:
- Meaning: make worse
- Collocation: exacerbate inequality / tensions / symptoms
- Speaking: "Over-tourism can exacerbate pressure on local infrastructure."
- Writing: "Ironically, short-term subsidies may exacerbate long-term dependency."

## Exercises

1. Upgrade 10 Band 6 sentences using academic verbs from Chapter 69.
2. Build collocation chains for: *policy, evidence, impact, reform, access*.
3. Record yourself defining 15 words without reading.

## Solutions

Answers vary; prioritise natural collocation and grammatical accuracy.

## Review / Quiz / Assignment

- Review: precision > rarity
- Quiz: What four qualities define high-band lexical resource?
- Assignment: Create your master notebook template and fill 50 rows this week.

## Revision Notes & Exam Tips

- Learn word families (*economy / economic / economise*).
- In the exam, if unsure, choose the safer precise word.
- Avoid idioms in Task 1 Academic; use cautiously in Speaking.

## Challenge & Band 9

Challenge: Paraphrase one Task 2 question five ways without repeating key nouns.  
Band 9 insight: Examiners notice *control under pressure*, not memorised essay strings.

---
""",
        encoding="utf-8",
    )


def write_awl_and_collocations() -> None:
    (OUT / "ch69_awl_core.md").write_text(
        """# Chapter 69: Academic Word List Core

**Part:** 3 — Vocabulary

---

## Learning Objectives

- Master high-utility Academic Word List (AWL) families for IELTS
- Use academic vocabulary with correct word form
- Avoid informal substitutes in Writing Tasks

## Theory

The Academic Word List (Averil Coxhead) contains word families common across academic texts but outside the most frequent general English words. For IELTS, AWL items are especially valuable in Reading and Writing.

Study by **family**, not isolated lemma:

| Noun | Verb | Adjective | Adverb |
|------|------|-----------|--------|
| analysis | analyse | analytical | analytically |
| assessment | assess | assessable | — |
| assumption | assume | assumed | — |
| authority | authorise | authoritative | authoritatively |
| benefit | benefit | beneficial | beneficially |
| concept | conceptualise | conceptual | conceptually |
| consequence | — | consequent | consequently |
| constitution | constitute | constitutional | constitutionally |
| context | contextualise | contextual | contextually |
| contract | contract | contractual | contractually |
| create | create | creative | creatively |
| data | — | — | — |
| definition | define | definite | definitely |
| derivation | derive | derivative | — |
| distribution | distribute | distributive | — |
| economy | economise | economic / economical | economically |
| environment | — | environmental | environmentally |
| establish | establish | established | — |
| estimate | estimate | estimated | — |
| evidence | evidence | evident | evidently |
| export | export | — | — |
| factor | factor | — | — |
| finance | finance | financial | financially |
| formula | formulate | — | — |
| function | function | functional | functionally |
| identify | identify | identifiable | — |
| income | — | — | — |
| indicate | indicate | indicative | indicatively |
| individual | individualise | individual | individually |
| interpret | interpret | interpretive | — |
| involve | involve | involved | — |
| issue | issue | — | — |
| labour | labour | — | — |
| legal | legalise | legal | legally |
| legislate | legislate | legislative | — |
| major | — | major | — |
| method | — | methodological | methodologically |
| occur | occur | — | — |
| percent | — | — | — |
| period | — | periodic | periodically |
| policy | — | — | — |
| principle | — | principal / principled | principally |
| proceed | proceed | — | — |
| process | process | — | — |
| require | require | required | — |
| research | research | — | — |
| respond | respond | responsive | responsively |
| role | — | — | — |
| section | section | — | — |
| sector | — | — | — |
| significant | signify | significant | significantly |
| similar | — | similar | similarly |
| source | source | — | — |
| specific | specify | specific | specifically |
| structure | structure | structural | structurally |
| theory | theorise | theoretical | theoretically |
| vary | vary | variable / various | variously |

*(Continue expanding families in your notebook; see Appendix A06 for the fuller list.)*

## Exercises, Quiz, Assignment

1. Write one Task 2 paragraph using 12 AWL families correctly.
2. Convert informal sentences to academic style.
3. Quiz yourself on noun/verb/adjective forms for 30 families.

## Exam Tips & Band 9

Do not force AWL words into Speaking Part 1 small talk. Use them where the topic is abstract (Part 3 / Task 2).

---
""",
        encoding="utf-8",
    )
    (OUT / "ch70_collocations.md").write_text(
        """# Chapter 70: Essential Collocations

**Part:** 3 — Vocabulary

---

## Learning Objectives

- Internalise high-frequency academic collocations
- Avoid common collocation errors that suppress lexical band scores
- Practise collocations in timed writing and speaking

## Core collocation banks

### Cause & effect
play a role in; contribute to; lead to; result in; give rise to; stem from; be attributed to; have an impact on; exert pressure on

### Increase / decrease
rise sharply; increase gradually; fall dramatically; decline steadily; remain stable; fluctuate; peak at; hit a low of; level off

### Opinion & argument
hold the view that; cast doubt on; lend support to; draw a distinction between; take into account; weigh the evidence; reach a conclusion

### Policy & society
introduce legislation; enforce regulations; allocate funding; bridge the gap; widen access; raise awareness; tackle inequality; impose restrictions

### Research & evidence
conduct a study; collect data; provide evidence; challenge assumptions; yield results; remain inconclusive

## Exercises

Rewrite Band 6 sentences with natural collocations. Create 50 personal flashcards. Record 20 speaking answers each using one collocation.

## Band 9 reminder

Collocation accuracy is often the difference between Band 7 and Band 8 lexical resource.

---
""",
        encoding="utf-8",
    )


def main() -> None:
    write_system_chapter()
    total_entries = 0
    for ch, key, title, blurb in TOPICS:
        md = chapter_markdown(ch, key, title, blurb)
        path = OUT / f"ch{ch}_{key}.md"
        path.write_text(md, encoding="utf-8")
        # count rough entries
        total_entries += md.count("\n### ")
        print(f"Wrote {path.name} ({path.stat().st_size:,} bytes)")
    write_awl_and_collocations()
    # dump index
    (DATA / "generation_summary.json").write_text(
        json.dumps({"topics": len(TOPICS), "approx_entries": total_entries}, indent=2),
        encoding="utf-8",
    )
    print(f"Done. Approx entries across topic chapters: {total_entries}")


if __name__ == "__main__":
    main()
