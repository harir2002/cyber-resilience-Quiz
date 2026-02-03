"""
Scoring and Analytics Module
Calculates cyber resilience maturity scores based on the questionnaire
Matches the specific Scorecard format and logic provided
"""

from typing import Dict, List, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
# We import get_max_score from schema, assuming it's available or we hardcode it
from questionnaire.questionnaire_schema import get_questionnaire_schema, get_max_score


class ResilienceScorer:
    """
    Calculates cyber resilience scores and provides insights
    Based on Strategic Questions (0-4 points each)
    """
    
    def __init__(self):
        self.questionnaire = get_questionnaire_schema()
        self.max_score = get_max_score()
    
    def calculate_score(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate the full assessment score from responses
        
        Args:
            responses: Dictionary of user responses
                      Format could be flat {q_id: answer} or nested by section
        
        Returns:
            Dictionary containing:
            - total_score
            - average_score (0-4.0)
            - maturity_level (1-5)
            - maturity_label (BASIC, etc.)
            - next_steps
            - question_details (list of question scores)
        """
        
        total_score = 0
        question_details = []
        
        # Get all questions from schema (flattened)
        all_questions = []
        for section, questions in self.questionnaire.items():
            all_questions.extend(questions)
            
        # Calculate score per question
        for q in all_questions:
            q_id = q["question_id"]
            user_answer = self._get_answer(responses, q_id)
            
            # Default to 0 points if not answered
            points = 0
            
            # Special handling for text questions or unexpected types
            if q["question_type"] == "text":
                # For Q8 (System Coverage Gaps), logic could be complex
                # But typically we might score based on "None" = 4, or manual review
                # For now, if "None" or "0" -> 4 points, else 0-3 based on content length?
                # The prompt earlier suggested specific logic, let's try to infer
                if str(user_answer).lower() in ["none", "n/a", "0", "no", ""]:
                    points = 4
                else:
                    # Assume having gaps reduces score. 
                    # If answer is present (listing systems), give 1 point or 0
                    points = 1 
            
            elif q.get("scoring"):
                if isinstance(user_answer, list):
                    # Multi-select: take the max score of selected options
                    option_scores = [q["scoring"].get(ans, 0) for ans in user_answer]
                    points = max(option_scores) if option_scores else 0
                else:
                    points = q["scoring"].get(user_answer, 0)
            
            total_score += points
            
            # Calculate max points for this specific question for normalization
            q_max = 4
            if q.get("scoring"):
                scores = list(q["scoring"].values())
                if scores:
                    q_max = max(scores)
            
            question_details.append({
                "question_id": q_id,
                "domain": q["domain"],
                "question_text": q["question_text"],
                "score": points,
                "user_answer": user_answer,  # Include the actual answer
                "max_points": q_max,
                "maturity_indicated": self._points_to_maturity_level_single(points)
            })
            
        # Calculate Average (0-4.0)
        # Normalize: (Total Score / Max Score) * 4
        if self.max_score > 0:
            avg_score = (total_score / self.max_score) * 4
        else:
            avg_score = 0
        
        # Determine Aggregate Maturity Level
        maturity_info = self._get_maturity_level_info(total_score)
        
        return {
            "total_score": total_score,
            "max_score": self.max_score,
            "average_score": round(avg_score, 1),
            "maturity_level": maturity_info["level"],
            "maturity_label": maturity_info["label"],
            "characteristics": maturity_info["characteristics"],
            "recommended_next_step": maturity_info["next_step"],
            "question_scores": question_details,
            "gap_analysis": self._calculate_gap(total_score)
        }
    
    def _get_answer(self, responses: Dict, q_id: str) -> str:
        """Helper to find answer in potentially nested response dict"""
        # Check if flat key exists
        if q_id in responses:
            return responses[q_id]
            
        # Check if hidden inside objects (like {q_id: {answer: "..."}})
        if q_id in responses and isinstance(responses[q_id], dict):
            return responses[q_id].get("answer", "")

        # Check nested sections
        for key, val in responses.items():
            if isinstance(val, dict):
                if q_id in val:
                    if isinstance(val[q_id], dict):
                        return val[q_id].get("answer", "")
                    return val[q_id]
        return ""

    def _points_to_maturity_level_single(self, points: int) -> int:
        """Map single question points (0-4) to a maturity level (1-5) approximation"""
        # Simple 1-to-1 mapping for display purposes if needed
        # 0->1, 1->2, 2->3, 3->4, 4->5
        return points + 1

    def _get_maturity_level_info(self, total_score: int) -> Dict:
        """Map total score to Maturity Level Info based on percentage of max score"""
        
        if self.max_score == 0:
             return {"level": 0, "label": "N/A", "characteristics": "", "next_step": ""}
             
        percent = (total_score / self.max_score) * 100
        
        if percent <= 25:
            return {
                "level": 1,
                "label": "BASIC",
                "characteristics": "Traditional backup; manual recovery; days/weeks RTO",
                "next_step": "Activate immutability & air-gapping"
            }
        elif percent <= 50:
            return {
                "level": 2,
                "label": "RISK-INFORMED",
                "characteristics": "Backup hardening; reactive response; aware of threats",
                "next_step": "Establish recovery playbooks & testing"
            }
        elif percent <= 75:
            return {
                "level": 3,
                "label": "REPEATABLE",
                "characteristics": "Air-gapped; documented playbooks; 24-48hr recovery",
                "next_step": "Deploy detection & monitoring capabilities"
            }
        elif percent <= 90:
            return {
                "level": 4,
                "label": "MANAGED",
                "characteristics": "Proactive detection; anomaly alerts; hours-level recovery",
                "next_step": "Automate orchestration & clean-room setup"
            }
        else: # 91-100
            return {
                "level": 5,
                "label": "ADAPTIVE",
                "characteristics": "Fully automated; AI-driven; minutes-level recovery; zero-lat",
                "next_step": "Continuous optimization & innovation"
            }

    def _calculate_gap(self, current_score: int) -> Dict:
        """Calculate gap against an ideal target (Level 5 = Max points)"""
        target_score = self.max_score
        gap = target_score - current_score
        
        # Estimate effort based on gap size (percentage based)
        gap_percent = (gap / target_score) * 100 if target_score > 0 else 0
        
        if gap_percent <= 10:
            effort = "Low - Tuning required"
        elif gap_percent <= 30:
            effort = "Medium - Dedicated project required"
        else:
            effort = "High - Strategic transformation required"
            
        return {
            "current_points": current_score,
            "target_points": target_score,
            "gap_points": gap,
            "estimated_effort": effort
        }
