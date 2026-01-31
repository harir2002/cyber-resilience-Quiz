"""
ChromaDB Manager - Handles all database operations for the questionnaire
Implements collections for companies, questions, responses, and assessments
"""

import chromadb
from chromadb.config import Settings
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config import CHROMADB_PATH, COLLECTIONS


class ChromaDBManager:
    """
    Manages all ChromaDB operations for the Cyber Resilience Assessment application
    """
    
    def __init__(self):
        """Initialize ChromaDB client and create necessary collections"""
        self.client = chromadb.PersistentClient(
            path=str(CHROMADB_PATH),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        self._initialize_collections()
    
    def _initialize_collections(self):
        """Create or get existing collections"""
        # Companies collection
        self.companies = self.client.get_or_create_collection(
            name=COLLECTIONS["companies"],
            metadata={"description": "Stores company information"}
        )
        
        # Questions collection
        self.questions = self.client.get_or_create_collection(
            name=COLLECTIONS["questions"],
            metadata={"description": "Stores questionnaire questions"}
        )
        
        # Responses collection
        self.responses = self.client.get_or_create_collection(
            name=COLLECTIONS["responses"],
            metadata={"description": "Stores user responses"}
        )
        
        # Assessments collection
        self.assessments = self.client.get_or_create_collection(
            name=COLLECTIONS["assessments"],
            metadata={"description": "Stores complete assessments"}
        )
    
    # ==============================
    # COMPANY OPERATIONS
    # ==============================
    
    def add_company(self, company_data: Dict) -> str:
        """
        Add a new company to the database
        
        Args:
            company_data: Dictionary containing company information
            
        Returns:
            company_id: Unique identifier for the company
        """
        company_id = str(uuid.uuid4())
        
        self.companies.add(
            ids=[company_id],
            documents=[json.dumps(company_data)],
            metadatas=[{
                "company_name": company_data.get("company_name", ""),
                "industry": company_data.get("industry", ""),
                "company_size": company_data.get("company_size", ""),
                "region": company_data.get("region", ""),
                "created_at": datetime.now().isoformat()
            }]
        )
        
        return company_id
    
    def get_company(self, company_id: str) -> Optional[Dict]:
        """Retrieve company information by ID"""
        try:
            result = self.companies.get(ids=[company_id])
            if result and result['documents']:
                return json.loads(result['documents'][0])
            return None
        except Exception as e:
            print(f"Error retrieving company: {e}")
            return None
    
    def search_companies(self, company_name: str = None, industry: str = None) -> List[Dict]:
        """Search companies by name or industry"""
        where_filter = {}
        
        if company_name:
            where_filter["company_name"] = company_name
        if industry:
            where_filter["industry"] = industry
        
        try:
            if where_filter:
                results = self.companies.get(where=where_filter)
            else:
                results = self.companies.get()
            
            companies = []
            if results and results['documents']:
                for doc in results['documents']:
                    companies.append(json.loads(doc))
            
            return companies
        except Exception as e:
            print(f"Error searching companies: {e}")
            return []
    
    # ==============================
    # QUESTION OPERATIONS
    # ==============================
    
    def add_question(self, question_data: Dict) -> str:
        """Add a new question to the database"""
        question_id = str(uuid.uuid4())
        
        self.questions.add(
            ids=[question_id],
            documents=[question_data.get("question_text", "")],
            metadatas=[{
                "section": question_data.get("section", ""),
                "question_type": question_data.get("question_type", ""),
                "order": str(question_data.get("order", 0)),
                "required": str(question_data.get("required", True))
            }]
        )
        
        return question_id
    
    def get_questions_by_section(self, section: str) -> List[Dict]:
        """Get all questions for a specific section"""
        try:
            results = self.questions.get(
                where={"section": section}
            )
            
            questions = []
            if results and results['ids']:
                for i, qid in enumerate(results['ids']):
                    questions.append({
                        "id": qid,
                        "text": results['documents'][i],
                        "metadata": results['metadatas'][i]
                    })
            
            # Sort by order
            questions.sort(key=lambda x: int(x['metadata'].get('order', 0)))
            return questions
            
        except Exception as e:
            print(f"Error retrieving questions: {e}")
            return []
    
    def get_all_questions(self) -> List[Dict]:
        """Get all questions from all sections"""
        try:
            results = self.questions.get()
            
            questions = []
            if results and results['ids']:
                for i, qid in enumerate(results['ids']):
                    questions.append({
                        "id": qid,
                        "text": results['documents'][i],
                        "metadata": results['metadatas'][i]
                    })
            
            return questions
            
        except Exception as e:
            print(f"Error retrieving all questions: {e}")
            return []
    
    # ==============================
    # RESPONSE OPERATIONS
    # ==============================
    
    def add_response(self, response_data: Dict) -> str:
        """Add a user response to a question"""
        response_id = str(uuid.uuid4())
        
        self.responses.add(
            ids=[response_id],
            documents=[json.dumps(response_data)],
            metadatas=[{
                "assessment_id": response_data.get("assessment_id", ""),
                "question_id": response_data.get("question_id", ""),
                "section": response_data.get("section", ""),
                "answer": str(response_data.get("answer", "")),
                "timestamp": datetime.now().isoformat()
            }]
        )
        
        return response_id
    
    def get_responses_by_assessment(self, assessment_id: str) -> List[Dict]:
        """Get all responses for a specific assessment"""
        try:
            results = self.responses.get(
                where={"assessment_id": assessment_id}
            )
            
            responses = []
            if results and results['documents']:
                for doc in results['documents']:
                    responses.append(json.loads(doc))
            
            return responses
            
        except Exception as e:
            print(f"Error retrieving responses: {e}")
            return []
    
    # ==============================
    # ASSESSMENT OPERATIONS
    # ==============================
    
    def create_assessment(self, company_id: str) -> str:
        """Create a new assessment for a company"""
        assessment_id = str(uuid.uuid4())
        
        assessment_data = {
            "assessment_id": assessment_id,
            "company_id": company_id,
            "created_at": datetime.now().isoformat(),
            "status": "in_progress",
            "completed_sections": []
        }
        
        self.assessments.add(
            ids=[assessment_id],
            documents=[json.dumps(assessment_data)],
            metadatas=[{
                "company_id": company_id,
                "status": "in_progress",
                "created_at": datetime.now().isoformat()
            }]
        )
        
        return assessment_id
    
    def update_assessment_status(self, assessment_id: str, status: str, completed_sections: List[str] = None):
        """Update assessment status and completed sections"""
        try:
            # Get current assessment
            result = self.assessments.get(ids=[assessment_id])
            
            if result and result['documents']:
                assessment_data = json.loads(result['documents'][0])
                assessment_data['status'] = status
                assessment_data['updated_at'] = datetime.now().isoformat()
                
                if completed_sections:
                    assessment_data['completed_sections'] = completed_sections
                
                if status == "completed":
                    assessment_data['completed_at'] = datetime.now().isoformat()
                
                # Update the assessment
                self.assessments.update(
                    ids=[assessment_id],
                    documents=[json.dumps(assessment_data)],
                    metadatas=[{
                        "company_id": assessment_data.get("company_id", ""),
                        "status": status,
                        "updated_at": datetime.now().isoformat()
                    }]
                )
                
        except Exception as e:
            print(f"Error updating assessment: {e}")
    
    def get_assessment(self, assessment_id: str) -> Optional[Dict]:
        """Retrieve assessment by ID"""
        try:
            result = self.assessments.get(ids=[assessment_id])
            if result and result['documents']:
                return json.loads(result['documents'][0])
            return None
        except Exception as e:
            print(f"Error retrieving assessment: {e}")
            return None
    
    def get_company_assessments(self, company_id: str) -> List[Dict]:
        """Get all assessments for a company"""
        try:
            results = self.assessments.get(
                where={"company_id": company_id}
            )
            
            assessments = []
            if results and results['documents']:
                for doc in results['documents']:
                    assessments.append(json.loads(doc))
            
            return assessments
            
        except Exception as e:
            print(f"Error retrieving company assessments: {e}")
            return []
    
    # ==============================
    # UTILITY OPERATIONS
    # ==============================
    
    def clear_questions(self):
        """Clear all questions from the questions collection"""
        try:
            # Delete the collection
            self.client.delete_collection(name=COLLECTIONS["questions"])
            # Recreate it
            self.questions = self.client.create_collection(
                name=COLLECTIONS["questions"],
                metadata={"description": "Assessment questions"}
            )
            print("[✓] Questions collection cleared and recreated")
        except Exception as e:
            print(f"[!] Error clearing questions: {e}")
            # Try to recreate if delete failed (maybe didn't exist)
            try:
                self.questions = self.client.get_or_create_collection(
                    name=COLLECTIONS["questions"],
                    metadata={"description": "Assessment questions"}
                )
                print("[✓] Questions collection recreated after error")
            except Exception as e2:
                print(f"[!] Critical error recreating questions: {e2}")
    
    def reset_database(self):
        """Reset all collections (USE WITH CAUTION)"""
        self.client.reset()
        self._initialize_collections()
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        return {
            "total_companies": self.companies.count(),
            "total_questions": self.questions.count(),
            "total_responses": self.responses.count(),
            "total_assessments": self.assessments.count()
        }
