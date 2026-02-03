import { useNavigate } from 'react-router-dom';
import { Shield, FileCheck, Clock, TrendingUp, Building2, Lock, Users, Network } from 'lucide-react';

const LandingPage = ({ config }) => {
    const navigate = useNavigate();
    const { app_title, app_subtitle, company_name, company_tagline, colors } = config;

    const domains = [
        { icon: Building2, title: "Governance & Risk Management", desc: "Strategy, policies, and risk assessment processes" },
        { icon: FileCheck, title: "Asset Management", desc: "Inventory and classification of IT assets" },
        { icon: Lock, title: "Access Control & Identity Management", desc: "Authentication, authorization, and access controls" },
        { icon: Shield, title: "Security Operations & Monitoring", desc: "Threat detection, monitoring, and vulnerability management" },
        { icon: TrendingUp, title: "Incident Response & Recovery", desc: "Incident handling and business continuity" },
        { icon: Lock, title: "Data Protection & Privacy", desc: "Encryption, privacy controls, and data governance" },
        { icon: Network, title: "Third-Party Risk Management", desc: "Vendor security and supply chain risk" },
        { icon: Users, title: "Security Awareness & Training", desc: "Employee education and security culture" },
    ];

    return (
        <div className="container fade-in">
            {/* Header with Logo */}
            <div className="text-center mb-4">
                <img
                    src="/sba_logo.png"
                    alt="SBA Info Solutions"
                    style={{ width: '200px', margin: '40px auto 20px' }}
                />
                <h1>{app_title}</h1>
                <h3 style={{ color: colors.secondary }}>{app_subtitle}</h3>
                <p style={{ fontSize: '1.1em', marginTop: '15px', opacity: 0.8 }}>
                    {company_tagline}
                </p>
            </div>

            {/* Introduction */}
            <div className="card mb-4" style={{ textAlign: 'center', padding: '40px 20px' }}>
                <h2 style={{ marginBottom: '20px', color: '#e7000b' }}>Welcome to Your Cyber Resilience Assessment</h2>
                <p style={{ fontSize: '1.2em', lineHeight: 1.6, maxWidth: '800px', margin: '0 auto' }}>
                    Understanding your organization's cyber resilience posture is critical.
                    This assessment evaluates your maturity across key security domains, providing actionable insights.
                </p>

                <div style={{ marginTop: '40px' }}>
                    <button
                        className="btn btn-large"
                        onClick={() => navigate('/company-info')}
                        style={{ fontSize: '1.2rem', padding: '15px 40px', boxShadow: '0 4px 15px rgba(231, 0, 11, 0.4)' }}
                    >
                        Start Assessment 🚀
                    </button>
                </div>
            </div>

            {/* Assessment Domains (Simplified) */}
            <div className="mb-4">
                <h3 className="text-center mb-3" style={{ opacity: 0.8 }}>Key Assessment Areas</h3>
                <div className="row" style={{ justifyContent: 'center' }}>
                    {domains.map((domain, idx) => {
                        const Icon = domain.icon;
                        return (
                            <div key={idx} className="col-3" style={{ marginBottom: '20px' }}>
                                <div style={{
                                    padding: '15px',
                                    border: '1px solid #333',
                                    borderRadius: '8px',
                                    textAlign: 'center',
                                    background: '#111',
                                    height: '100%'
                                }}>
                                    <div style={{ marginBottom: '10px' }}>
                                        <Icon size={24} color={colors.secondary} />
                                    </div>
                                    <h5 style={{ margin: 0, fontSize: '0.9rem', color: '#ddd' }}>{domain.title}</h5>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>



            {/* Footer */}
            <div className="text-center mb-4" style={{ opacity: 0.7, fontSize: '0.9em' }}>
                <p>🔒 All responses are stored securely and confidentially</p>
                <p>© 2026 {company_name} - Enterprise Cybersecurity Solutions</p>
                <p style={{ fontSize: '0.85em' }}>
                    🌐 https://www.sbainfo.in
                </p>
            </div>
        </div>
    );
};

export default LandingPage;
