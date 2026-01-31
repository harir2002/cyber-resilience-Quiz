"""
Database Initialization Script
Populates ChromaDB with questionnaire schema on first run
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from database.chromadb_manager import ChromaDBManager
from questionnaire.questionnaire_schema import get_questionnaire_schema


def initialize_database():
    """Initialize ChromaDB with questionnaire questions"""
    
    print("[*] Initializing ChromaDB...")
    
    db = ChromaDBManager()
    
    # Check if questions already exist
    existing_questions = db.get_all_questions()
    
    if existing_questions:
        print(f"[OK] Database already initialized with {len(existing_questions)} questions")
        return
    
    # Get questionnaire schema
    schema = get_questionnaire_schema()
    
    print("[*] Adding questionnaire questions to database...")
    
    question_count = 0
    
    for section_name, questions in schema.items():
        print(f"  Adding section: {section_name}")
        
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
    
    print(f"[OK] Successfully added {question_count} questions across {len(schema)} sections")
    
    # Display statistics
    stats = db.get_statistics()
    print("\n[Stats] Database Statistics:")
    print(f"  - Total Questions: {stats['total_questions']}")
    print(f"  - Total Companies: {stats['total_companies']}")
    print(f"  - Total Assessments: {stats['total_assessments']}")
    print(f"  - Total Responses: {stats['total_responses']}")
    
    print("\n[DONE] Database initialization complete!")


if __name__ == "__main__":
    initialize_database()
