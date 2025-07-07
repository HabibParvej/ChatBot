import pandas as pd
import numpy as np
import faiss
import pickle
import os
import re
from sentence_transformers import SentenceTransformer

# -------------------------
# Configuration
# -------------------------
COLLEGE_NAME = "Siliguri Institute of Technology"
CONTACT_INFO = "+91‑9876543210 | info@sittech.edu.in"
WEBSITE = "sittech.ac.in"

# -------------------------
# Helper Functions
# -------------------------
def normalize_text(text):
    """Simplify text for embedding"""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\b(courses?|programs?|degrees?)\b', 'programs', text)
    text = re.sub(r'\b(admission|apply|application)\b', 'admission', text)
    text = re.sub(r'\b(hostel|dorm|accommodation)\b', 'hostel', text)
    text = re.sub(r'\b(placement|jobs?|recruitment)\b', 'placement', text)
    text = re.sub(r'\b(contact|phone|email|address)\b', 'contact', text)
    return re.sub(r'\s+', ' ', text).strip()

# -------------------------
# Load or Create Dataset
# -------------------------
def load_or_create_dataset():
    """Load college_knowledge.csv or create sample dataset"""
    csv_path = "data/college_knowledge.csv"
    
    # Create data directory if missing
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists(csv_path):
        print("⚠️ college_knowledge.csv not found, creating sample data...")
        sample_data = {
            "question": [
                "What are the admission requirements?",
                "Where is the campus located?",
                "What engineering programs do you offer?",
                "How do I apply for scholarships?",
                "What hostel facilities are available?",
                "Do you offer MCA?",
                "Placement statistics?",
                "Contact information?",
                ""
            ],
            "answer": [
                "Admission requires 75% in 12th with PCM. Entrance exam may apply.",
                "Our campus is at Salbari, Sukna, Siliguri, West Bengal",
                "We offer B.Tech in CSE, ECE, ME, CE, and EE",
                "Submit scholarship form by Aug 31 with income certificate",
                "AC/non-AC rooms, WiFi, mess, laundry, 24/7 security",
                "We focus on engineering programs: B.Tech & M.Tech",
                "80-85% placement rate, avg package ₹4.5L, highest ₹18L",
                f"Contact: {CONTACT_INFO} | Website: {WEBSITE}",
                "Please ask a question about our college!"
            ],
            "department": [
                "Admissions", "General", "Academics", 
                "Financial Aid", "Hostel", "Academics",
                "Placements", "General", "General"
            ],
            "keywords": [
                "admission,requirements", "location,address", "courses,programs",
                "scholarship,financial", "accommodation,stay", "mca,programs",
                "stats,numbers", "contact,info", "empty,greeting"
            ]
        }
        df = pd.DataFrame(sample_data)
        df.to_csv(csv_path, index=False)
        return df
    else:
        print("✅ Loading college_knowledge.csv")
        return pd.read_csv(csv_path)

# -------------------------
# Main Process
# -------------------------
# Load dataset
df = load_or_create_dataset()

# Clean and normalize questions
df["question"] = df["question"].fillna("")
df["normalized"] = df["question"].apply(normalize_text)

# Generate embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(df["normalized"].tolist(), show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# Create and save index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
os.makedirs("faiss_store", exist_ok=True)
faiss.write_index(index, "faiss_store/index.faiss")

# Save knowledge data
with open("faiss_store/data.pkl", "wb") as f:
    pickle.dump({
        "questions": df["question"].tolist(),
        "answers": df["answer"].tolist(),
        "departments": df["department"].tolist(),
        "keywords": df["keywords"].tolist()
    }, f)

print("✅ Vector store created successfully!")
print(f"• {len(df)} Q&A pairs indexed")
print("Next: Run 'streamlit run app.py' to start the assistant")