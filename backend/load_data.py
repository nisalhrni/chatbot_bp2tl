import pandas as pd
import os
from pathlib import Path
from embedding_service import embedding_service
from vector_store import vector_store
from database import supabase
import numpy as np

def load_faq_from_csv(csv_path: str):
    print(f"Loading FAQ from {csv_path}...")

    if not os.path.exists(csv_path):
        print(f"FAQ file not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)

    if 'question' not in df.columns or 'answer' not in df.columns:
        print("CSV must have 'question' and 'answer' columns")
        return

    print(f"Found {len(df)} FAQ entries")

    supabase.table("faq").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()

    for idx, row in df.iterrows():
        question = str(row['question']).strip()
        answer = str(row['answer']).strip()

        if not question or not answer:
            continue

        text_for_embedding = f"{question} {answer}"
        embedding = embedding_service.encode_single_passage(text_for_embedding)

        embedding_list = embedding.tolist()

        supabase.table("faq").insert({
            "question": question,
            "answer": answer,
            "embedding": embedding_list
        }).execute()

        documents = [f"FAQ: {question}\nJawaban: {answer}"]
        metadata = [{"type": "faq", "question": question, "answer": answer}]
        vector_store.add_documents(
            np.array([embedding]),
            documents,
            metadata
        )

        print(f"Loaded FAQ {idx + 1}/{len(df)}")

    print("FAQ data loaded successfully")

def load_knowledge_from_txt(knowledge_dir: str):
    print(f"Loading knowledge from {knowledge_dir}...")

    if not os.path.exists(knowledge_dir):
        print(f"Knowledge directory not found: {knowledge_dir}")
        return

    txt_files = list(Path(knowledge_dir).glob("*.txt"))

    if not txt_files:
        print("No .txt files found in knowledge directory")
        return

    print(f"Found {len(txt_files)} knowledge files")

    supabase.table("knowledge").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()

    for idx, txt_file in enumerate(txt_files):
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        if not content:
            continue

        embedding = embedding_service.encode_single_passage(content)
        embedding_list = embedding.tolist()

        supabase.table("knowledge").insert({
            "content": content,
            "source_file": txt_file.name,
            "embedding": embedding_list
        }).execute()

        documents = [f"Knowledge ({txt_file.name}): {content}"]
        metadata = [{"type": "knowledge", "source": txt_file.name, "content": content}]
        vector_store.add_documents(
            np.array([embedding]),
            documents,
            metadata
        )

        print(f"Loaded knowledge {idx + 1}/{len(txt_files)}: {txt_file.name}")

    print("Knowledge data loaded successfully")

def initialize_data():
    print("=" * 60)
    print("Initializing BP2TL Chatbot Data")
    print("=" * 60)

    data_dir = Path(__file__).parent.parent / "data"
    faq_path = data_dir / "faq1.csv"
    knowledge_dir = data_dir / "knowledge"

    load_faq_from_csv(str(faq_path))
    load_knowledge_from_txt(str(knowledge_dir))

    vector_store.save("./faiss_index/bp2tl")
    print("\nFAISS index saved successfully")

    print("=" * 60)
    print("Data initialization completed!")
    print("=" * 60)

if __name__ == "__main__":
    initialize_data()
