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
                    style={{ width: '300px', margin: '50px auto 30px' }}
                />
                <h1>{app_title}</h1>
                <h3 style={{ color: colors.secondary }}>{app_subtitle}</h3>
                <p style={{ fontSize: '1.1em', marginTop: '15px', opacity: 0.8 }}>
                    {company_tagline}
                </p>
            </div>

            {/* Introduction */}
            <div className="card mb-4">
                <div className="card-body">
                    <h2 className="text-center">Welcome to Your Cyber Resilience Assessment</h2>
                    <p style={{ fontSize: '1.1em', lineHeight: 1.8, textAlign: 'justify' }}>
                        In today's digital landscape, cyber threats are constantly evolving. Understanding your organization's
                        cyber resilience posture is critical to protecting your assets, reputation, and stakeholders.
                    </p>
                    <p style={{ fontSize: '1.1em', lineHeight: 1.8, textAlign: 'justify' }}>
                        This comprehensive assessment evaluates your cybersecurity maturity across <strong>8 critical security domains</strong>,
                        providing you with actionable insights and recommendations to strengthen your defenses.
                    </p>
                </div>
            </div>

            {/* What to Expect */}
            <div className="mb-4">
                <h2 className="text-center mb-3">What to Expect</h2>
                <div className="row">
                    <div className="col-3">
                        <div className="metric-card">
                            <div style={{ fontSize: '50px', marginBottom: '15px' }}>📋</div>
                            <div className="metric-label"><strong>8 Security Domains</strong></div>
                            <p style={{ marginTop: '10px', fontSize: '0.9em' }}>Comprehensive coverage of cybersecurity controls</p>
                        </div>
                    </div>
                    <div className="col-3">
                        <div className="metric-card">
                            <div style={{ fontSize: '50px', marginBottom: '15px' }}>⏱️</div>
                            <div className="metric-label"><strong>20-30 Minutes</strong></div>
                            <p style={{ marginTop: '10px', fontSize: '0.9em' }}>Expected completion time</p>
                        </div>
                    </div>
                    <div className="col-3">
                        <div className="metric-card">
                            <div style={{ fontSize: '50px', marginBottom: '15px' }}>📊</div>
                            <div className="metric-label"><strong>Detailed Insights</strong></div>
                            <p style={{ marginTop: '10px', fontSize: '0.9em' }}>Actionable recommendations and scoring</p>
                        </div>
                    </div>
                    <div className="col-3">
                        <div className="metric-card">
                            <div style={{ fontSize: '50px', marginBottom: '15px' }}>🎯</div>
                            <div className="metric-label"><strong>Maturity Scoring</strong></div>
                            <p style={{ marginTop: '10px', fontSize: '0.9em' }}>Industry-standard maturity levels</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Assessment Domains */}
            <div className="mb-4">
                <h2 className="text-center mb-3">Assessment Domains</h2>
                <div className="row">
                    {domains.map((domain, idx) => {
                        const Icon = domain.icon;
                        return (
                            <div key={idx} className="col-2">
                                <div className="card">
                                    <div style={{ fontSize: '30px', marginBottom: '10px' }}>
                                        <Icon size={32} color={colors.secondary} />
                                    </div>
                                    <h4 style={{ color: colors.secondary, fontSize: '1rem' }}>{domain.title}</h4>
                                    <p style={{ fontSize: '0.9em', opacity: 0.8 }}>{domain.desc}</p>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Call to Action */}
            <div className="text-center mb-4">
                <button
                    className="btn btn-large"
                    onClick={() => navigate('/company-info')}
                >
                    🚀 Start Assessment
                </button>
            </div>

            {/* Footer */}
            <div className="text-center mb-4" style={{ opacity: 0.7, fontSize: '0.9em' }}>
                <p>🔒 All responses are stored securely and confidentially</p>
                <p>© 2026 {company_name} - Enterprise Cybersecurity Solutions</p>
                <p style={{ fontSize: '0.85em' }}>
                    📧 Contact: info@sbainfosolutions.com | 🌐 www.sbainfosolutions.com
                </p>
            </div>
        </div>
    );
};

export default LandingPage;
