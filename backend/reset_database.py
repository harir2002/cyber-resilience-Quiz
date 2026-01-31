"""
Reset ChromaDB and reload questionnaire with 12 questions from Excel
Run this to clear old data and load fresh questions
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from database.chromadb_manager import ChromaDBManager
from questionnaire.questionnaire_schema import get_questionnaire_schema, get_question_count
import shutil

def reset_database():
    print("=" * 60)
    print("  RESETTING CYBER RESILIENCE ASSESSMENT DATABASE")
    print("=" * 60)
    print()
    
    # Path to ChromaDB data
    chromadb_path = Path(__file__).parent / "data" / "chromadb"
    
    # Step 1: Delete old database
    if chromadb_path.exists():
        print(f"[*] Deleting old database at: {chromadb_path}")
        shutil.rmtree(chromadb_path)
        print("[✓] Old database deleted")
    else:
        print("[*] No existing database found")
    
    print()
    
    # Step 2: Initialize new database
    print("[*] Initializing fresh ChromaDB...")
    db = ChromaDBManager()
    print("[✓] ChromaDB initialized")
    print()
    
    # Step 3: Load new questionnaire schema
    print("[*] Loading questionnaire schema from Excel...")
    schema = get_questionnaire_schema()
    total_questions = get_question_count()
    
    print(f"[*] Found {total_questions} questions in schema")
    print(f"[*] Sections: {list(schema.keys())}")
    print()
    
    # Step 4: Populate database
    print("[*] Populating database with questions...")
    question_count = 0
    
    for section_name, questions in schema.items():
        print(f"\n  Section: {section_name}")
        for idx, question in enumerate(questions):
            question_data = {
                "section": section_name,
                "question_text": question["question_text"],
                "question_type": question["question_type"],
                "order": idx,
                "required": question.get("required", True)
            }
            db.add_question(question_data)
            question_count += 1
            print(f"    [{question_count}] {question['question_text'][:60]}...")
    
    print()
    print(f"[✓] Added {question_count} questions to database")
    print()
    
    # Step 5: Verify
    stats = db.get_statistics()
    print("=" * 60)
    print("  DATABASE RESET COMPLETE")
    print("=" * 60)
    print(f"  Total Questions: {stats['total_questions']}")
    print(f"  Total Companies: {stats['total_companies']}")
    print(f"  Total Assessments: {stats['total_assessments']}")
    print("=" * 60)
    print()
    print("[✓] Database is ready!")
    print()
    print("Next steps:")
    print("  1. Restart the backend: python main.py")
    print("  2. Refresh your browser")
    print("  3. You should now see 12 questions!")
    print()

if __name__ == "__main__":
    try:
        reset_database()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
