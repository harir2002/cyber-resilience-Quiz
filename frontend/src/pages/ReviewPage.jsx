import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../config';

const ReviewPage = ({ config, assessmentData, setAssessmentData }) => {
    const navigate = useNavigate();
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async () => {
        setSubmitting(true);
        setError(null);

        try {
            // Prepare submission payload matching backend expectation (AssessmentSubmit model)
            const payload = {
                company_info: assessmentData.companyInfo,
                assessment_id: assessmentData.assessmentId,
                responses: assessmentData.responses || {}
            };

            const response = await fetch(`${API_BASE_URL}/api/assessment/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Submission failed');
            }

            const data = await response.json();

            // Navigate to results with the calculated data
            navigate('/results', {
                state: {
                    results: data.results,
                    companyInfo: assessmentData.companyInfo
                }
            });

        } catch (err) {
            console.error("Submission Error:", err);
            setError(err.message);
            setSubmitting(false);
        }
    };

    // Calculate completion status
    const totalQuestions = 12; // Hardcoded for now based on known schema
    let answeredCount = 0;
    if (assessmentData.responses) {
        Object.values(assessmentData.responses).forEach(section => {
            answeredCount += Object.keys(section).length;
        });
    }
    const isComplete = answeredCount >= totalQuestions;

    return (
        <div className="container" style={{ maxWidth: '800px', margin: '0 auto', paddingTop: '40px' }}>
            <h1 style={{ textAlign: 'center', marginBottom: '30px' }}>Ready to Submit?</h1>

            <div className="card" style={{ padding: '30px', background: '#1a1a1a', border: '1px solid #333', borderRadius: '12px' }}>
                <div style={{ textAlign: 'center', marginBottom: '30px' }}>
                    <div style={{ fontSize: '4rem', marginBottom: '10px' }}>📝</div>
                    <h3>Assessment Summary</h3>
                    <p style={{ opacity: 0.7 }}>
                        You have answered <strong>{answeredCount}</strong> out of <strong>{totalQuestions}</strong> questions.
                    </p>
                </div>

                {!isComplete && (
                    <div className="alert alert-warning" style={{ marginBottom: '20px', background: '#332b00', border: '1px solid #665500', color: '#ffcc00', padding: '15px', borderRadius: '8px' }}>
                        ⚠️ You haven't answered all questions yet. Your score may be lower than expected.
                    </div>
                )}

                {error && (
                    <div className="alert alert-error" style={{ marginBottom: '20px', background: '#330000', border: '1px solid #660000', color: '#ff4444', padding: '15px', borderRadius: '8px' }}>
                        Error: {error}
                    </div>
                )}

                <div style={{ display: 'flex', gap: '15px', justifyContent: 'center' }}>
                    <button
                        className="btn btn-outline"
                        onClick={() => navigate('/questionnaire')}
                        style={{ padding: '12px 24px', border: '1px solid #666', background: 'transparent', color: 'white', borderRadius: '6px', cursor: 'pointer' }}
                        disabled={submitting}
                    >
                        ← Go Back & Edit
                    </button>
                    <button
                        className="btn btn-primary"
                        onClick={handleSubmit}
                        disabled={submitting}
                        style={{
                            padding: '12px 24px',
                            background: submitting ? '#666' : '#e7000b',
                            border: 'none',
                            color: 'white',
                            borderRadius: '6px',
                            cursor: submitting ? 'not-allowed' : 'pointer',
                            fontWeight: 'bold'
                        }}
                    >
                        {submitting ? 'Generating Report...' : 'Generate Scorecard 🚀'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ReviewPage;
