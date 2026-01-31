import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const QuestionnairePage = ({ config, assessmentData, setAssessmentData }) => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [questionnaire, setQuestionnaire] = useState(null);
    const [responses, setResponses] = useState({});

    // Fetch questionnaire schema from backend
    useEffect(() => {
        console.log('=== QUESTIONNAIRE PAGE LOADED ===');
        console.log('Fetching from: http://localhost:8000/api/questionnaire/schema');

        fetch('http://localhost:8000/api/questionnaire/schema')
            .then(res => {
                console.log('Response received, status:', res.status);
                if (!res.ok) {
                    throw new Error(`HTTP error! status: ${res.status}`);
                }
                return res.json();
            })
            .then(data => {
                console.log('Data received:', data);
                setQuestionnaire(data);
                setLoading(false);
            })
            .catch(err => {
                console.error('FETCH ERROR:', err);
                setError(err.message);
                setLoading(false);
            });
    }, []);

    const handleAnswerChange = (questionId, answer) => {
        console.log('Answer changed:', questionId, answer);
        setResponses(prev => ({
            ...prev,
            [questionId]: answer
        }));
    };

    // Loading state
    if (loading) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                background: '#000'
            }}>
                <div style={{ fontSize: '2rem', marginBottom: '20px' }}>⏳</div>
                <h2>Loading Questionnaire...</h2>
                <p style={{ opacity: 0.7, marginTop: '10px' }}>Connecting to backend API...</p>
            </div>
        );
    }

    // Error state
    if (error) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                background: '#000',
                padding: '20px'
            }}>
                <div style={{ fontSize: '3rem', marginBottom: '20px' }}>❌</div>
                <h2 style={{ color: '#e7000b' }}>Error Loading Questionnaire</h2>
                <p style={{ opacity: 0.7, marginTop: '10px', maxWidth: '600px', textAlign: 'center' }}>
                    {error}
                </p>
                <div style={{ marginTop: '30px', padding: '20px', background: '#1a1a1a', borderRadius: '8px', maxWidth: '600px' }}>
                    <h3>Troubleshooting:</h3>
                    <ul style={{ textAlign: 'left', lineHeight: '1.8' }}>
                        <li>Check if backend is running: <code>python main.py</code></li>
                        <li>Test API: <a href="http://localhost:8000/api/questionnaire/schema" target="_blank" style={{ color: '#e7000b' }}>http://localhost:8000/api/questionnaire/schema</a></li>
                        <li>Check browser console (F12) for errors</li>
                    </ul>
                </div>
                <button
                    onClick={() => window.location.reload()}
                    style={{
                        marginTop: '20px',
                        padding: '12px 24px',
                        background: '#e7000b',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontSize: '1rem'
                    }}
                >
                    Retry
                </button>
            </div>
        );
    }

    // No data state
    if (!questionnaire || !questionnaire.schema) {
        return (
            <div style={{
                minHeight: '100vh',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                background: '#000'
            }}>
                <h2>No questionnaire data available</h2>
                <button onClick={() => navigate('/company-info')} style={{
                    marginTop: '20px',
                    padding: '12px 24px',
                    background: '#e7000b',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer'
                }}>
                    ← Back
                </button>
            </div>
        );
    }

    // Get all questions from the schema
    const allQuestions = [];
    Object.entries(questionnaire.schema).forEach(([sectionName, questions]) => {
        questions.forEach((q, idx) => {
            allQuestions.push({
                ...q,
                sectionName,
                displayIndex: allQuestions.length + 1
            });
        });
    });

    const answeredCount = Object.keys(responses).length;
    const totalCount = allQuestions.length;
    const progress = totalCount > 0 ? Math.round((answeredCount / totalCount) * 100) : 0;

    return (
        <div style={{
            minHeight: '100vh',
            background: '#000',
            color: 'white',
            padding: '40px 20px'
        }}>
            <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
                {/* Header */}
                <div style={{ textAlign: 'center', marginBottom: '40px' }}>
                    <h1 style={{ fontSize: '2.5rem', marginBottom: '10px' }}>
                        Cyber Resilience Questionnaire
                    </h1>
                    <p style={{ fontSize: '1.1rem', opacity: 0.8 }}>
                        Assessing <strong>{assessmentData?.companyInfo?.company_name || 'your organization'}</strong>
                    </p>
                </div>

                {/* Progress Bar */}
                <div style={{
                    background: '#1a1a1a',
                    padding: '30px',
                    borderRadius: '12px',
                    marginBottom: '40px',
                    border: '2px solid #e7000b'
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '30px' }}>
                        <div style={{ textAlign: 'center', minWidth: '120px' }}>
                            <div style={{ fontSize: '3rem', fontWeight: 'bold', color: progress === 100 ? '#00ff00' : '#e7000b' }}>
                                {progress}%
                            </div>
                            <div style={{ opacity: 0.8 }}>Progress</div>
                        </div>
                        <div style={{ flex: 1 }}>
                            <div style={{
                                height: '40px',
                                background: '#333',
                                borderRadius: '20px',
                                overflow: 'hidden',
                                position: 'relative'
                            }}>
                                <div style={{
                                    height: '100%',
                                    width: `${progress}%`,
                                    background: progress === 100 ? 'linear-gradient(90deg, #00ff00, #00cc00)' : 'linear-gradient(90deg, #e7000b, #ff4444)',
                                    transition: 'width 0.3s ease',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontWeight: 'bold'
                                }}>
                                    {progress > 10 && `${answeredCount} / ${totalCount} answered`}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Questions */}
                <div style={{ display: 'grid', gap: '30px' }}>
                    {allQuestions.map((q) => {
                        const currentAnswer = responses[q.question_id];
                        const isAnswered = currentAnswer !== undefined && currentAnswer !== '';

                        return (
                            <div
                                key={q.question_id}
                                style={{
                                    background: isAnswered ? 'rgba(0, 255, 0, 0.05)' : '#1a1a1a',
                                    border: `2px solid ${isAnswered ? '#00ff00' : '#e7000b'}`,
                                    borderRadius: '12px',
                                    padding: '30px',
                                    transition: 'all 0.3s ease'
                                }}
                            >
                                {/* Question Header */}
                                <div style={{ marginBottom: '20px' }}>
                                    <div style={{
                                        display: 'flex',
                                        alignItems: 'flex-start',
                                        gap: '15px',
                                        marginBottom: '10px'
                                    }}>
                                        <div style={{
                                            background: isAnswered ? '#00ff00' : '#e7000b',
                                            color: '#000',
                                            fontWeight: 'bold',
                                            padding: '8px 16px',
                                            borderRadius: '8px',
                                            minWidth: '50px',
                                            textAlign: 'center'
                                        }}>
                                            {q.displayIndex}
                                        </div>
                                        <div style={{ flex: 1 }}>
                                            <h3 style={{ fontSize: '1.3rem', marginBottom: '8px', lineHeight: '1.4' }}>
                                                {q.question_text}
                                            </h3>
                                            {q.domain && (
                                                <div style={{
                                                    display: 'inline-block',
                                                    background: '#e7000b',
                                                    color: 'white',
                                                    padding: '4px 12px',
                                                    borderRadius: '4px',
                                                    fontSize: '0.85rem',
                                                    fontWeight: 'bold'
                                                }}>
                                                    {q.domain}
                                                </div>
                                            )}
                                        </div>
                                    </div>

                                    {q.help_text && (
                                        <div style={{
                                            background: '#2a2a2a',
                                            padding: '12px',
                                            borderRadius: '8px',
                                            fontSize: '0.9rem',
                                            opacity: 0.8,
                                            fontStyle: 'italic',
                                            marginTop: '10px'
                                        }}>
                                            💡 {q.help_text}
                                        </div>
                                    )}
                                </div>

                                {/* Answer Options */}
                                <div style={{ display: 'grid', gap: '12px' }}>
                                    {q.question_type === 'text' ? (
                                        <textarea
                                            value={currentAnswer || ''}
                                            onChange={(e) => handleAnswerChange(q.question_id, e.target.value)}
                                            placeholder="Enter your answer..."
                                            style={{
                                                width: '100%',
                                                minHeight: '100px',
                                                padding: '15px',
                                                background: '#2a2a2a',
                                                border: '2px solid #444',
                                                borderRadius: '8px',
                                                color: 'white',
                                                fontSize: '1rem',
                                                fontFamily: 'inherit',
                                                resize: 'vertical'
                                            }}
                                        />
                                    ) : (
                                        (q.options || []).map((option) => (
                                            <label
                                                key={option}
                                                style={{
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    gap: '15px',
                                                    padding: '15px 20px',
                                                    background: currentAnswer === option ? '#e7000b' : '#2a2a2a',
                                                    border: `2px solid ${currentAnswer === option ? '#e7000b' : '#444'}`,
                                                    borderRadius: '8px',
                                                    cursor: 'pointer',
                                                    transition: 'all 0.2s ease',
                                                    fontSize: '1.05rem'
                                                }}
                                                onMouseEnter={(e) => {
                                                    if (currentAnswer !== option) {
                                                        e.currentTarget.style.borderColor = '#e7000b';
                                                        e.currentTarget.style.background = '#333';
                                                    }
                                                }}
                                                onMouseLeave={(e) => {
                                                    if (currentAnswer !== option) {
                                                        e.currentTarget.style.borderColor = '#444';
                                                        e.currentTarget.style.background = '#2a2a2a';
                                                    }
                                                }}
                                            >
                                                <input
                                                    type="radio"
                                                    name={q.question_id}
                                                    value={option}
                                                    checked={currentAnswer === option}
                                                    onChange={(e) => handleAnswerChange(q.question_id, e.target.value)}
                                                    style={{
                                                        width: '20px',
                                                        height: '20px',
                                                        cursor: 'pointer',
                                                        accentColor: '#e7000b'
                                                    }}
                                                />
                                                <span style={{ fontWeight: currentAnswer === option ? 'bold' : 'normal' }}>
                                                    {option}
                                                </span>
                                            </label>
                                        ))
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>

                {/* Navigation Buttons */}
                <div style={{
                    marginTop: '50px',
                    padding: '30px',
                    background: '#1a1a1a',
                    borderRadius: '12px',
                    border: '2px solid #e7000b',
                    display: 'flex',
                    gap: '20px',
                    justifyContent: 'center',
                    alignItems: 'center',
                    flexWrap: 'wrap'
                }}>
                    <button
                        onClick={() => navigate('/company-info')}
                        style={{
                            padding: '15px 30px',
                            background: 'transparent',
                            color: 'white',
                            border: '2px solid #e7000b',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            fontSize: '1.1rem',
                            fontWeight: 'bold',
                            transition: 'all 0.2s'
                        }}
                        onMouseEnter={(e) => {
                            e.target.style.background = '#e7000b';
                        }}
                        onMouseLeave={(e) => {
                            e.target.style.background = 'transparent';
                        }}
                    >
                        ← Back to Company Info
                    </button>

                    <button
                        onClick={() => {
                            if (progress === 100) {
                                navigate('/review');
                            } else {
                                alert(`Please answer all ${totalCount} questions. You've answered ${answeredCount}.`);
                            }
                        }}
                        disabled={progress !== 100}
                        style={{
                            padding: '15px 40px',
                            background: progress === 100 ? '#00ff00' : '#666',
                            color: progress === 100 ? '#000' : '#999',
                            border: 'none',
                            borderRadius: '8px',
                            cursor: progress === 100 ? 'pointer' : 'not-allowed',
                            fontSize: '1.1rem',
                            fontWeight: 'bold',
                            transition: 'all 0.2s'
                        }}
                    >
                        {progress === 100 ? '✅ Continue to Review →' : `⏳ ${answeredCount}/${totalCount} Answered`}
                    </button>
                </div>

                {/* Footer */}
                <div style={{ textAlign: 'center', marginTop: '40px', opacity: 0.7, fontSize: '0.9rem' }}>
                    <p>💾 Responses are saved automatically • 🔒 Secure and confidential</p>
                    <p>© 2026 SBA Info Solutions</p>
                </div>
            </div>
        </div>
    );
};

export default QuestionnairePage;
