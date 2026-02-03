import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../config';

const ResultsPage = () => {
    const location = useLocation();
    const navigate = useNavigate();

    // 1. ALL HOOKS MUST BE AT THE TOP LEVEL
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(true);

    // Email specific hooks
    const [email, setEmail] = useState('');
    const [sending, setSending] = useState(false);
    const [emailStatus, setEmailStatus] = useState(null);

    // Effect for loading results
    useEffect(() => {
        if (location.state?.results) {
            setResults(location.state.results);
            setLoading(false);
        } else {
            console.warn("No results found in navigation state");
            setLoading(false);
        }
    }, [location.state]);

    // Effect for pre-filling email
    useEffect(() => {
        if (location.state?.companyInfo?.contact_email) {
            setEmail(location.state.companyInfo.contact_email);
        }
    }, [location.state]);

    // Styles - Defined at the top to be available for all returns
    const pageStyle = {
        minHeight: '100vh',
        backgroundColor: '#000',
        color: '#fff',
        padding: '40px',
        fontFamily: 'sans-serif'
    };

    const containerStyle = {
        maxWidth: '1000px',
        margin: '0 auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '40px'
    };

    const headerStyle = {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-end',
        borderBottom: '1px solid #e7000b',
        paddingBottom: '20px'
    };

    const sectionHeaderStyle = {
        borderLeft: '4px solid #e7000b',
        paddingLeft: '15px',
        fontSize: '1.4rem',
        fontWeight: 'bold',
        marginBottom: '20px',
        color: '#fff'
    };

    const tableStyle = {
        width: '100%',
        borderCollapse: 'collapse',
        marginBottom: '20px'
    };

    const thStyle = {
        border: '1px solid #444',
        padding: '10px',
        background: '#1a1a1a',
        textAlign: 'left',
        fontWeight: 'bold',
        fontSize: '0.9rem'
    };

    const tdStyle = {
        border: '1px solid #444',
        padding: '10px',
        fontSize: '0.9rem'
    };

    const cellCenter = { ...tdStyle, textAlign: 'center' };

    // 2. NOW WE CAN DO CONDITIONAL RENDERING (Early Returns)
    if (loading) return (
        <div style={pageStyle}>
            <div style={{ ...containerStyle, alignItems: 'center', justifyContent: 'center', minHeight: '80vh' }}>
                <div className="spinner"></div>
                <p style={{ marginTop: '20px' }}>Generating Scorecard...</p>
            </div>
        </div>
    );

    if (!results) {
        return (
            <div style={pageStyle}>
                <div style={{ ...containerStyle, alignItems: 'center', justifyContent: 'center', minHeight: '80vh' }}>
                    <h2 style={{ color: '#e7000b', marginBottom: '20px' }}>No Assessment Results Found</h2>
                    <p style={{ marginBottom: '30px', opacity: 0.8 }}>It looks like you haven't completed an assessment yet, or the data was lost.</p>
                    <button
                        onClick={() => navigate('/')}
                        style={{
                            padding: '12px 24px',
                            background: 'transparent',
                            border: '1px solid #e7000b',
                            color: '#e7000b',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontWeight: 'bold'
                        }}
                    >
                        Start New Assessment
                    </button>
                </div>
            </div>
        )
    }

    const safeResults = results || {};

    const total_score = safeResults.total_score || 0;
    const average_score = safeResults.average_score || 0;
    const maturity_label = safeResults.maturity_label || "N/A";
    const characteristics = safeResults.characteristics || "Not available";
    const recommended_next_step = safeResults.recommended_next_step || "Contact administrator";
    const question_scores = safeResults.question_scores || [];
    const maturity_level = safeResults.maturity_level || 0;

    const max_score = safeResults.max_score || 44;

    // Safety check for gap_analysis specifically
    const gap_analysis = safeResults.gap_analysis || {
        gap_points: 0,
        estimated_effort: "N/A"
    };

    console.log("Rendering Results with:", safeResults);

    // Styles were here previously, but are now moved to the top.



    const handleSendEmail = async () => {
        if (!email) return;
        setSending(true);
        setEmailStatus(null);

        try {
            const response = await fetch(`${API_BASE_URL}/api/assessment/send-email`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: email,
                    company_name: location.state?.companyInfo?.company_name || "Client",
                    results: results
                })
            });

            const data = await response.json();
            if (response.ok) {
                setEmailStatus('success');
                alert('Report sent successfully!');
            } else {
                throw new Error(data.detail || 'Failed to send');
            }
        } catch (err) {
            console.error(err);
            setEmailStatus('error');
            alert('Failed to send email: ' + err.message);
        } finally {
            setSending(false);
        }
    };

    return (
        <div style={pageStyle}>
            <div style={containerStyle}>

                {/* HEADER */}
                <div style={headerStyle}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                        {/* SBA INFO SOLUTIONS LOGO */}
                        <img src="/sba_logo.png" alt="SBA Info Solutions" style={{ height: '60px', objectFit: 'contain' }} />

                        <div>
                            <h1 style={{ fontSize: '1.8rem', fontWeight: 'bold', margin: '0 0 5px 0', color: '#e7000b', textTransform: 'uppercase', letterSpacing: '1px' }}>
                                Assessment Summary
                            </h1>
                            <p style={{ opacity: 0.7, margin: 0, fontSize: '0.9rem', fontWeight: 'bold' }}>
                                POWERED BY SBA INFO SOLUTIONS
                            </p>
                        </div>
                    </div>

                    <div style={{ textAlign: 'right', fontSize: '0.9rem', opacity: 0.8 }}>
                        <p style={{ margin: '2px 0' }}><strong>Client:</strong> {location.state?.companyInfo?.company_name || "Unknown"}</p>
                        <p style={{ margin: '2px 0' }}><strong>Date:</strong> {new Date().toLocaleDateString()}</p>
                    </div>
                </div>

                {/* QUESTIONS & ANSWERS LIST */}
                <section>
                    <h2 style={{ borderLeft: '4px solid #e7000b', paddingLeft: '15px', color: '#fff', marginBottom: '20px' }}>
                        Your Responses
                    </h2>

                    <div style={{ display: 'grid', gap: '20px' }}>
                        {question_scores.map((q, idx) => {
                            if (!q) return null;

                            // Visualize answers: check if array (multi-select) or string
                            const answerDisplay = Array.isArray(q.user_answer)
                                ? q.user_answer.join(', ')
                                : (q.user_answer || 'No answer provided');

                            return (
                                <div key={idx} style={{ background: '#1a1a1a', padding: '20px', borderRadius: '8px', border: '1px solid #333' }}>
                                    <div style={{ display: 'flex', gap: '15px' }}>
                                        <div style={{
                                            background: '#e7000b', color: 'white', fontWeight: 'bold',
                                            width: '30px', height: '30px', borderRadius: '50%',
                                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                                            flexShrink: 0
                                        }}>
                                            {idx + 1}
                                        </div>
                                        <div style={{ flex: 1 }}>
                                            <h3 style={{ margin: '0 0 10px 0', fontSize: '1.1rem', color: '#ddd' }}>
                                                {q.question_text}
                                            </h3>
                                            <div style={{
                                                background: '#000', padding: '15px', borderRadius: '6px',
                                                borderLeft: '3px solid #4CAF50', color: '#fff', fontWeight: '500',
                                                whiteSpace: 'pre-wrap'
                                            }}>
                                                {answerDisplay}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </section>

                {/* ACTIONS */}
                <div className="no-print" style={{ background: '#111', padding: '20px', marginTop: '20px', borderRadius: '8px', border: '1px solid #333' }}>
                    <h3 style={{ marginTop: 0, color: 'white', fontSize: '1.2rem', marginBottom: '15px' }}>📩 Email Report</h3>
                    <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Email address for report"
                            style={{ padding: '12px', borderRadius: '4px', border: '1px solid #444', background: '#222', color: 'white', flex: 1 }}
                        />
                        <button
                            onClick={handleSendEmail}
                            disabled={sending}
                            style={{
                                padding: '12px 24px',
                                background: sending ? '#666' : '#e7000b',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: sending ? 'not-allowed' : 'pointer',
                                fontWeight: 'bold'
                            }}
                        >
                            {sending ? 'Sending...' : 'Send to Email 📧'}
                        </button>
                    </div>
                </div>

                <div className="no-print" style={{ display: 'flex', justifyContent: 'center', gap: '20px', paddingTop: '20px' }}>
                    <button
                        onClick={() => window.print()}
                        style={{ padding: '12px 25px', background: '#222', border: '1px solid #444', color: 'white', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '10px' }}
                    >
                        <span>🖨️</span> Print PDF
                    </button>
                    <button
                        onClick={() => navigate('/')}
                        style={{ padding: '12px 25px', background: '#e7000b', border: 'none', color: 'white', fontWeight: 'bold', borderRadius: '6px', cursor: 'pointer' }}
                    >
                        Start New
                    </button>
                </div>
            </div>

            <style>
                {`
                    @media print {
                        .no-print { display: none !important; }
                        body { background-color: #fff !important; color: #000 !important; }
                        div[style*="background: #1a1a1a"] { background: #fff !important; border: 1px solid #ddd !important; color: #000 !important; }
                        div[style*="background: #000"] { background: #f5f5f5 !important; color: #000 !important; border: 1px solid #ccc !important; }
                        h3 { color: #000 !important; }
                    }
                `}
            </style>
        </div>
    );
};
export default ResultsPage;

