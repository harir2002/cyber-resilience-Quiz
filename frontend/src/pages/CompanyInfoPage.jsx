import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../config';

const CompanyInfoPage = ({ config, assessmentData, setAssessmentData }) => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        company_name: '',
        industry: '',
        company_size: '',
        region: '',
        contact_email: '',
        contact_name: '',
        additional_notes: ''
    });
    const [errors, setErrors] = useState({});

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        // Clear error when user types
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: null
            }));
        }
    };

    const validateForm = () => {
        const newErrors = {};
        if (!formData.company_name.trim()) newErrors.company_name = 'Company Name is required';
        if (!formData.industry) newErrors.industry = 'Industry is required';
        if (!formData.company_size) newErrors.company_size = 'Company Size is required';
        if (!formData.region) newErrors.region = 'Region is required';
        if (!formData.contact_email.trim()) {
            newErrors.contact_email = 'Contact Email is required';
        } else if (!/\S+@\S+\.\S+/.test(formData.contact_email)) {
            newErrors.contact_email = 'Invalid email format';
        }
        return newErrors;
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        const newErrors = validateForm();

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }

        try {
            // Call backend API to create company
            const response = await fetch(`${API_BASE_URL}/api/company/create`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.success) {
                setAssessmentData({
                    companyInfo: formData,
                    assessmentId: data.assessment_id,
                    responses: {}
                });
                navigate('/questionnaire');
            }
        } catch (error) {
            console.error('Error creating company:', error);
            alert('Error starting assessment. Please try again.');
        }
    };

    return (
        <div className="container fade-in">
            <h1>Company Information</h1>

            <div className="alert alert-info mb-4">
                <p>Please provide your organization's details to begin the assessment.</p>
            </div>

            <div className="card">
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">
                            Company Name <span className="required-marker">*</span>
                        </label>
                        <input
                            type="text"
                            name="company_name"
                            className="form-control"
                            value={formData.company_name}
                            onChange={handleChange}
                            placeholder="Enter your company name"
                        />
                        {errors.company_name && <div className="text-error mt-1">{errors.company_name}</div>}
                    </div>

                    <div className="form-group">
                        <label className="form-label">
                            Industry <span className="required-marker">*</span>
                        </label>
                        <select
                            name="industry"
                            className="form-select"
                            value={formData.industry}
                            onChange={handleChange}
                        >
                            <option value="">Select Industry</option>
                            {config?.industries?.map(ind => (
                                <option key={ind} value={ind}>{ind}</option>
                            ))}
                        </select>
                        {errors.industry && <div className="text-error mt-1">{errors.industry}</div>}
                    </div>

                    <div className="form-group">
                        <label className="form-label">
                            Company Size <span className="required-marker">*</span>
                        </label>
                        <select
                            name="company_size"
                            className="form-select"
                            value={formData.company_size}
                            onChange={handleChange}
                        >
                            <option value="">Select Company Size</option>
                            {config?.company_sizes?.map(size => (
                                <option key={size} value={size}>{size}</option>
                            ))}
                        </select>
                        {errors.company_size && <div className="text-error mt-1">{errors.company_size}</div>}
                    </div>

                    <div className="form-group">
                        <label className="form-label">
                            Region <span className="required-marker">*</span>
                        </label>
                        <select
                            name="region"
                            className="form-select"
                            value={formData.region}
                            onChange={handleChange}
                        >
                            <option value="">Select Region</option>
                            {config?.regions?.map(region => (
                                <option key={region} value={region}>{region}</option>
                            ))}
                        </select>
                        {errors.region && <div className="text-error mt-1">{errors.region}</div>}
                    </div>

                    <div className="form-group">
                        <label className="form-label">
                            Contact Email <span className="required-marker">*</span>
                        </label>
                        <input
                            type="email"
                            name="contact_email"
                            className="form-control"
                            value={formData.contact_email}
                            onChange={handleChange}
                            placeholder="contact@company.com"
                        />
                        {errors.contact_email && <div className="text-error mt-1">{errors.contact_email}</div>}
                    </div>

                    <div className="form-group">
                        <label className="form-label">Contact Name (Optional)</label>
                        <input
                            type="text"
                            name="contact_name"
                            className="form-control"
                            value={formData.contact_name}
                            onChange={handleChange}
                            placeholder="Your name"
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Additional Notes (Optional)</label>
                        <textarea
                            name="additional_notes"
                            className="form-textarea"
                            value={formData.additional_notes}
                            onChange={handleChange}
                            placeholder="Any additional information..."
                        />
                    </div>

                    <div className="d-flex gap-2">
                        <button type="button" className="btn btn-outline" onClick={() => navigate('/')}>
                            ← Back
                        </button>
                        <button type="submit" className="btn">
                            Continue to Assessment →
                        </button>
                    </div>
                </form>
            </div>

            <div className="text-center mt-4" style={{ opacity: 0.7, fontSize: '0.9em' }}>
                <p>© 2026 {config?.company_name} - Enterprise Cybersecurity Solutions</p>
            </div>
        </div>
    );
};

export default CompanyInfoPage;
