# RESUME RANKING - MINIMAL UPGRADE
# Drop-in replacement for your existing "Rank Resumes" node
# Adds: Tokenization, Stopwords, Cosine Similarity (NO OTHER CHANGES)

import re
from datetime import datetime
from collections import Counter
import math

# Read input
items = _input.all()

if not items:
    return [{"json": {"info": "No input items", "received_items": 0}}]

# ============================================
# SIMPLE NLP ADDITIONS (20 lines total)
# ============================================

# Basic stopwords (most common English words to ignore)
STOP = set(['the','a','an','and','or','but','in','on','at','to','for','of','with','is','are','was','were','be','have','has','had','do','does','i','you','he','she','it','we','they','my','your','this','that'])

def tokenize(text):
    """Simple tokenization: lowercase + split into words"""
    if not text:
        return []
    return re.findall(r'\b[a-z0-9]+\b', text.lower())

def remove_stopwords(tokens):
    """Remove common words"""
    return [t for t in tokens if t not in STOP and len(t) > 2]

def cosine_sim(vec1, vec2):
    """Calculate cosine similarity between two word-count dictionaries"""
    common = set(vec1.keys()) & set(vec2.keys())
    if not common:
        return 0.0
    
    dot = sum(vec1[k] * vec2[k] for k in common)
    mag1 = math.sqrt(sum(v**2 for v in vec1.values()))
    mag2 = math.sqrt(sum(v**2 for v in vec2.values()))
    
    return dot / (mag1 * mag2) if mag1 and mag2 else 0.0

# ============================================
# YOUR ORIGINAL CODE (Unchanged)
# ============================================

job_keywords = [
    'python', 'machine learning', 'ml', 'ai', 'artificial intelligence',
    'nlp', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
    'data analysis', 'eda', 'pandas', 'numpy', 'sql', 'mysql',
    'automation', 'n8n', 'make', 'api', 'git', 'github',
    'computer vision', 'neural networks', 'classification', 'regression',
    'c++', 'algorithms', 'data structures', 'opencv', 'django', 'flask'
]

TOTAL_KEYWORDS = len(job_keywords)

# Weights (unchanged)
KEYWORD_MATCH_WEIGHT = 10
MATCH_PERCENTAGE_WEIGHT = 5
EXPERIENCE_WEIGHT = 3
EDUCATION_WEIGHT = 2

def calculate_keyword_score(text, keywords):
    """Original keyword matching (unchanged)"""
    if not text:
        return 0, [], [], 0
    low = text.lower()
    matched, missing = [], []
    for kw in keywords:
        if kw.lower() in low:
            matched.append(kw)
        else:
            missing.append(kw)
    count = len(matched)
    pct = (count / len(keywords) * 100) if keywords else 0
    return count, matched, missing, pct

def extract_experience_years(text):
    """Original experience extraction (unchanged)"""
    if not text:
        return 0
    matches = re.findall(r'(\d{4})\s*[-–]\s*(\d{4}|present|current)', text.lower())
    cur = datetime.now().year
    years = 0
    for s, e in matches:
        try:
            start = int(s)
            end = cur if e in ['present', 'current'] else int(e)
            years = max(years, end - start)
        except:
            continue
    return years

def check_education(text):
    """Original education scoring (unchanged)"""
    if not text:
        return 0
    t = text.lower()
    if 'phd' in t or 'doctorate' in t:
        return 10
    if 'master' in t or 'm.s.' in t or 'ms ' in t:
        return 8
    if 'bachelor' in t or 'b.s.' in t or 'bs ' in t:
        return 6
    if 'associate' in t or 'diploma' in t:
        return 4
    if 'a level' in t or 'a-level' in t:
        return 3
    return 1

def relevance(pct):
    """Original relevance classification (unchanged)"""
    if pct >= 70:
        return "Highly Relevant"
    if pct >= 50:
        return "Relevant"
    if pct >= 30:
        return "Somewhat Relevant"
    return "Not Relevant"

# ============================================
# MAIN PROCESSING (Only 3 NEW lines added)
# ============================================

# NEW: Tokenize job description for similarity calculation
job_tokens = remove_stopwords(tokenize(' '.join(job_keywords)))
job_vec = Counter(job_tokens)

ranked = []

for idx, item in enumerate(items, start=1):
    data = item.get('json', {})
    sheet_hash = data.get('#') or data.get('ID') or f"resume-{idx}"
    name = (data.get('Name') or '').strip()
    text = (data.get('Job Description') or data.get('description') or '').strip()

    if not text or len(text) < 50:
        continue

    # Original keyword matching
    match_count, matched, missing, pct = calculate_keyword_score(text, job_keywords)
    
    # NEW: Tokenize resume and calculate cosine similarity
    resume_tokens = remove_stopwords(tokenize(text))
    resume_vec = Counter(resume_tokens)
    similarity = cosine_sim(job_vec, resume_vec)
    
    # Original scoring
    years = extract_experience_years(text)
    edu = check_education(text)

    # Original score calculation (unchanged)
    score = (match_count * KEYWORD_MATCH_WEIGHT) + (pct * MATCH_PERCENTAGE_WEIGHT) + (years * EXPERIENCE_WEIGHT) + (edu * EDUCATION_WEIGHT)

    ranked.append({
        "#": sheet_hash,
        "ID": sheet_hash,
        "Name": name,
        "Job Description": text,
        "Role": "AI/ML Developer",
        "Matched Keywords": ", ".join(matched),
        "Missing Keywords": ", ".join(missing),
        "Match Count": match_count,
        "Total Keywords": TOTAL_KEYWORDS,
        "Match %": round(pct, 2),
        "Cosine Similarity": round(similarity, 4),  # NEW: Added this field
        "Experience Years": years,
        "Education Score": edu,
        "Total Score": round(score, 2),
        "Relevance": relevance(pct)
    })

# Original sorting and ranking
ranked.sort(key=lambda x: x["Total Score"], reverse=True)
for i, r in enumerate(ranked, start=1):
    r["Rank"] = i

return [{"json": r} for r in ranked]