import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const ResultsPage = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(true);

    // In a real app, we might fetch results from backend ID passing via location state
    // For now, let's look for "assessmentData" or "results" in location.state 
    // OR we simulate the calculation if we have the raw responses.

    useEffect(() => {
        // If we have results passed directly (e.g. from ReviewPage submission)
        if (location.state?.results) {
            setResults(location.state.results);
            setLoading(false);
        } else {
            // Redirect or show error if no data
            // For demo purposes, if no data, we might want to redirect back
            // console.log("No results found in state");
            setLoading(false);
        }
    }, [location.state]);

    if (loading) return <div className="p-10 text-white">Generating Scorecard...</div>;

    if (!results) {
        return (
            <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-4">
                <h2 className="text-xl text-red-500 mb-4">No Assessment Results Found</h2>
                <button onClick={() => navigate('/')} className="px-4 py-2 border border-red-500 rounded text-red-500 hover:bg-red-500 hover:text-white transition">
                    Start New Assessment
                </button>
            </div>
        )
    }

    const { total_score, average_score, maturity_label, characteristics, recommended_next_step, question_scores, gap_analysis } = results;

    // Styles
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

    return (
        <div style={pageStyle}>
            <div style={containerStyle}>

                {/* HEADER */}
                <div style={headerStyle}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                        {/* SBA INFO SOLUTIONS LOGO */}
                        <img src="/sba_logo.png" alt="SBA Info Solutions" style={{ height: '60px', objectFit: 'contain' }} />

                        <div>
                            <h1 style={{ fontSize: '2rem', fontWeight: 'bold', margin: '0 0 5px 0', color: '#e7000b', textTransform: 'uppercase', letterSpacing: '1px' }}>
                                Cyber Resilience Maturity Scorecard
                            </h1>
                            <p style={{ opacity: 0.7, margin: 0, fontSize: '1rem', letterSpacing: '2px', fontWeight: 'bold' }}>
                                POWERED BY SBA INFO SOLUTIONS
                            </p>
                        </div>
                    </div>

                    <div style={{ textAlign: 'right', fontSize: '0.9rem', opacity: 0.8 }}>
                        <p style={{ margin: '2px 0' }}><strong>Client Organization:</strong> {location.state?.companyInfo?.company_name || "Demo Corp"}</p>
                        <p style={{ margin: '2px 0' }}><strong>Assessment Date:</strong> {new Date().toLocaleDateString()}</p>
                    </div>
                </div>

                {/* 1. ASSESSMENT RESULTS TABLE */}
                <section>
                    <h2 style={sectionHeaderStyle}>1. Assessment Results</h2>
                    <table style={tableStyle}>
                        <thead>
                            <tr>
                                <th style={{ ...thStyle, width: '50px', textAlign: 'center' }}>#</th>
                                <th style={thStyle}>Domain</th>
                                <th style={{ ...thStyle, width: '100px', textAlign: 'center' }}>Score (0-4)</th>
                                <th style={{ ...thStyle, width: '200px', textAlign: 'center' }}>Maturity Level</th>
                            </tr>
                        </thead>
                        <tbody>
                            {question_scores.map((q, idx) => (
                                <tr key={q.question_id} style={{ background: idx % 2 === 0 ? '#000' : '#111' }}>
                                    <td style={{ ...cellCenter, color: '#888' }}>{idx + 1}</td>
                                    <td style={tdStyle}>{q.domain}</td>
                                    <td style={{ ...cellCenter, fontWeight: 'bold', color: q.score >= 3 ? '#4caf50' : q.score >= 2 ? '#ffeb3b' : '#ff5252' }}>
                                        {q.score}
                                    </td>
                                    <td style={cellCenter}>Level {q.maturity_indicated}</td>
                                </tr>
                            ))}
                            {/* Total Row */}
                            <tr style={{ background: '#222', borderTop: '2px solid #555' }}>
                                <td colSpan={2} style={{ ...tdStyle, textAlign: 'right', fontWeight: 'bold' }}>TOTAL SCORE</td>
                                <td style={{ ...cellCenter, fontSize: '1.2rem', color: '#e7000b', fontWeight: 'bold' }}>{total_score}</td>
                                <td style={tdStyle}></td>
                            </tr>
                        </tbody>
                    </table>
                </section>

                {/* 2. AGGREGATE SCORE SUMMARY */}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px' }}>
                    <section>
                        <h2 style={sectionHeaderStyle}>2. Aggregate Score Summary</h2>
                        <table style={tableStyle}>
                            <tbody>
                                <tr>
                                    <td style={{ ...tdStyle, background: '#1a1a1a', width: '60%' }}>Total Points Achieved</td>
                                    <td style={{ ...tdStyle, fontSize: '1.1rem', fontWeight: 'bold' }}>{total_score} <span style={{ fontSize: '0.8rem', color: '#888', fontWeight: 'normal' }}>/ 48</span></td>
                                </tr>
                                <tr>
                                    <td style={{ ...tdStyle, background: '#1a1a1a' }}>Average Maturity Score</td>
                                    <td style={{ ...tdStyle, fontSize: '1.1rem', fontWeight: 'bold' }}>{average_score} <span style={{ fontSize: '0.8rem', color: '#888', fontWeight: 'normal' }}>/ 4.0</span></td>
                                </tr>
                                <tr>
                                    <td style={{ ...tdStyle, background: '#1a1a1a' }}>Current Maturity Level</td>
                                    <td style={{ ...tdStyle, fontSize: '1.1rem', fontWeight: 'bold', color: '#e7000b', textTransform: 'uppercase' }}>{maturity_label}</td>
                                </tr>
                            </tbody>
                        </table>
                    </section>

                    <section>
                        <h2 style={sectionHeaderStyle}>Gap Analysis</h2>
                        <table style={tableStyle}>
                            <tbody>
                                <tr>
                                    <td style={{ ...tdStyle, background: '#1a1a1a', width: '60%' }}>Target Level (Adaptive)</td>
                                    <td style={tdStyle}>48 Points</td>
                                </tr>
                                <tr>
                                    <td style={{ ...tdStyle, background: '#1a1a1a' }}>Gap (Points)</td>
                                    <td style={{ ...tdStyle, color: '#ff5252', fontWeight: 'bold' }}>{gap_analysis.gap_points} Pts</td>
                                </tr>
                                <tr>
                                    <td style={{ ...tdStyle, background: '#1a1a1a' }}>Estimated Effort</td>
                                    <td style={tdStyle}>{gap_analysis.estimated_effort}</td>
                                </tr>
                            </tbody>
                        </table>
                    </section>
                </div>

                {/* 3. MATURITY LEVEL INDICATION */}
                <section>
                    <h2 style={sectionHeaderStyle}>3. Maturity Level Assessment</h2>
                    <div style={{ background: '#111', border: '1px solid #333', padding: '30px', borderRadius: '8px', display: 'flex', gap: '40px', alignItems: 'center' }}>
                        <div style={{ textAlign: 'center', minWidth: '200px' }}>
                            <div style={{ fontSize: '0.8rem', color: '#888', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '10px' }}>Current Status</div>
                            <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#e7000b', marginBottom: '10px' }}>{maturity_label}</div>
                            <div style={{ fontSize: '0.8rem', background: '#222', padding: '5px 15px', borderRadius: '4px', display: 'inline-block' }}>Level {results.maturity_level}</div>
                        </div>

                        <div style={{ borderLeft: '1px solid #333', paddingLeft: '40px', flex: 1 }}>
                            <div style={{ marginBottom: '20px' }}>
                                <span style={{ color: '#ff8a80', fontWeight: 'bold', display: 'block', marginBottom: '5px' }}>Key Characteristics:</span>
                                <p style={{ color: '#ccc', margin: 0, lineHeight: 1.5 }}>{characteristics}</p>
                            </div>
                            <div>
                                <span style={{ color: '#69f0ae', fontWeight: 'bold', display: 'block', marginBottom: '5px' }}>Recommended Next Step:</span>
                                <div style={{ background: 'rgba(0, 255, 0, 0.1)', border: '1px solid rgba(0, 255, 0, 0.3)', padding: '10px', borderRadius: '4px', color: '#fff' }}>
                                    {recommended_next_step}
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* 4. INVESTMENT ROADMAP (Preview) */}
                <section>
                    <h2 style={sectionHeaderStyle}>4. Strategic Roadmap Preview</h2>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
                        {/* Phase 1 */}
                        <div style={{ background: '#111', padding: '20px', borderRadius: '8px', borderTop: '3px solid #448aff' }}>
                            <h3 style={{ color: '#448aff', marginTop: 0 }}>Phase 1: Quick Wins</h3>
                            <div style={{ fontSize: '0.8rem', color: '#888', marginBottom: '15px' }}>0-30 Days</div>
                            <ul style={{ paddingLeft: '20px', margin: 0, color: '#ccc', lineHeight: 1.6 }}>
                                <li>Implement Immutable Backups</li>
                                <li>Audit Privileged Access</li>
                                <li>Activate MFA Everywhere</li>
                            </ul>
                        </div>

                        {/* Phase 2 */}
                        <div style={{ background: '#111', padding: '20px', borderRadius: '8px', borderTop: '3px solid #ffeb3b' }}>
                            <h3 style={{ color: '#ffeb3b', marginTop: 0 }}>Phase 2: Hardening</h3>
                            <div style={{ fontSize: '0.8rem', color: '#888', marginBottom: '15px' }}>30-60 Days</div>
                            <ul style={{ paddingLeft: '20px', margin: 0, color: '#ccc', lineHeight: 1.6 }}>
                                <li>Deploy Threat Detection</li>
                                <li>Air-Gap Critical Assets</li>
                                <li>Conduct Tabletop Exercise</li>
                            </ul>
                        </div>

                        {/* Phase 3 */}
                        <div style={{ background: '#111', padding: '20px', borderRadius: '8px', borderTop: '3px solid #00e676' }}>
                            <h3 style={{ color: '#00e676', marginTop: 0 }}>Phase 3: Strategic</h3>
                            <div style={{ fontSize: '0.8rem', color: '#888', marginBottom: '15px' }}>60-90 Days</div>
                            <ul style={{ paddingLeft: '20px', margin: 0, color: '#ccc', lineHeight: 1.6 }}>
                                <li>Automate Recovery Runbooks</li>
                                <li>AI-Driven Resilience</li>
                                <li>Continuous Validation</li>
                            </ul>
                        </div>
                    </div>
                </section>

                {/* ACTIONS */}
                <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', paddingTop: '40px', borderTop: '1px solid #333' }}>
                    <button
                        onClick={() => window.print()}
                        style={{ padding: '15px 30px', background: '#222', border: '1px solid #444', color: 'white', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '10px' }}
                    >
                        <span>🖨️</span> Print Scorecard
                    </button>
                    <button
                        onClick={() => navigate('/')}
                        style={{ padding: '15px 30px', background: '#e7000b', border: 'none', color: 'white', fontWeight: 'bold', borderRadius: '6px', cursor: 'pointer', boxShadow: '0 4px 15px rgba(231, 0, 11, 0.3)' }}
                    >
                        Start New Assessment
                    </button>
                </div>

            </div>
        </div>
    );
};
export default ResultsPage;

