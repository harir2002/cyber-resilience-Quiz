import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../config';

const CompanyInfoPage = ({ config, assessmentData, setAssessmentData }) => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        contact_name: '',
        contact_email: '',
        designation: '',
        company_name: '',
        current_backup_solution: '',
        // Hidden fields for backward compatibility
        industry: 'Other',
        company_size: 'Other',
        state: 'Other'
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
        if (!formData.contact_name.trim()) newErrors.contact_name = 'Name is required';
        if (!formData.contact_email.trim()) {
            newErrors.contact_email = 'Email ID is required';
        } else if (!/\S+@\S+\.\S+/.test(formData.contact_email)) {
            newErrors.contact_email = 'Invalid email format';
        }
        if (!formData.designation.trim()) newErrors.designation = 'Designation is required';
        if (!formData.company_name.trim()) newErrors.company_name = 'Company Name is required';

        return newErrors;
    };

    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const newErrors = validateForm();

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }

        setIsSubmitting(true);

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
            } else {
                alert('Server returned an error: ' + (data.message || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error creating company:', error);
            alert('Error starting assessment. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="container fade-in">
            <h1>Company Information</h1>

            <div className="alert alert-info mb-4">
                <p>Please provide your details to begin the assessment.</p>
            </div>

            <div className="card">
                <form onSubmit={handleSubmit}>

                    {/* Name */}
                    <div className="form-group">
                        <label className="form-label">
                            Name <span className="required-marker">*</span>
                        </label>
                        <input
                            type="text"
                            name="contact_name"
                            className="form-control"
                            value={formData.contact_name}
                            onChange={handleChange}
                            placeholder="Your Name"
                            disabled={isSubmitting}
                        />
                        {errors.contact_name && <div className="text-error mt-1">{errors.contact_name}</div>}
                    </div>

                    {/* Email ID */}
                    <div className="form-group">
                        <label className="form-label">
                            Email ID <span className="required-marker">*</span>
                        </label>
                        <input
                            type="email"
                            name="contact_email"
                            className="form-control"
                            value={formData.contact_email}
                            onChange={handleChange}
                            placeholder="name@company.com"
                            disabled={isSubmitting}
                        />
                        {errors.contact_email && <div className="text-error mt-1">{errors.contact_email}</div>}
                    </div>

                    {/* Designation */}
                    <div className="form-group">
                        <label className="form-label">
                            Designation <span className="required-marker">*</span>
                        </label>
                        <input
                            type="text"
                            name="designation"
                            className="form-control"
                            value={formData.designation}
                            onChange={handleChange}
                            placeholder="Your Designation (e.g. CISO, IT Manager)"
                            disabled={isSubmitting}
                        />
                        {errors.designation && <div className="text-error mt-1">{errors.designation}</div>}
                    </div>

                    {/* Company Name */}
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
                            disabled={isSubmitting}
                        />
                        {errors.company_name && <div className="text-error mt-1">{errors.company_name}</div>}
                    </div>

                    {/* Current Backup Solution */}
                    <div className="form-group">
                        <label className="form-label">
                            Current Backup Solution
                        </label>
                        <input
                            type="text"
                            name="current_backup_solution"
                            className="form-control"
                            value={formData.current_backup_solution}
                            onChange={handleChange}
                            placeholder="e.g. Veeam, Commvault, Rubrik..."
                            disabled={isSubmitting}
                        />
                    </div>

                    <div className="d-flex gap-2">
                        <button
                            type="button"
                            className="btn btn-outline"
                            onClick={() => navigate('/')}
                            disabled={isSubmitting}
                        >
                            ← Back
                        </button>
                        <button
                            type="submit"
                            className="btn"
                            disabled={isSubmitting}
                            style={{
                                cursor: isSubmitting ? 'not-allowed' : 'pointer',
                                opacity: isSubmitting ? 0.7 : 1,
                                minWidth: '200px'
                            }}
                        >
                            {isSubmitting ? (
                                <span style={{ display: 'flex', alignItems: 'center', gap: '8px', justifyContent: 'center' }}>
                                    <span>⏳</span> Starting...
                                </span>
                            ) : (
                                'Continue to Assessment →'
                            )}
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
