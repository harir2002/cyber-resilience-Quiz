import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import './index.css';

import { API_BASE_URL } from './config';

// Import pages (we'll create these)
import LandingPage from './pages/LandingPage';
import CompanyInfoPage from './pages/CompanyInfoPage';
import QuestionnairePage from './pages/QuestionnairePage';
import ReviewPage from './pages/ReviewPage';
import ResultsPage from './pages/ResultsPage';

function App() {
  const [config, setConfig] = useState(null);
  const [assessmentData, setAssessmentData] = useState({
    companyInfo: null,
    assessmentId: null,
    responses: {},
  });

  // Fetch application config from API
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/config`)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then(data => {
        if (data.app_title) {
          setConfig(data);
        } else {
          console.error('Invalid config data:', data);
        }
      })
      .catch(err => console.error('Error loading config:', err));
  }, []);

  if (!config) {
    return (
      <div className="container text-center" style={{ marginTop: '100px' }}>
        <div className="spinner"></div>
        <p>Loading Cyber Resilience Assessment...</p>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route
            path="/"
            element={<LandingPage config={config} />}
          />
          <Route
            path="/company-info"
            element={
              <CompanyInfoPage
                config={config}
                assessmentData={assessmentData}
                setAssessmentData={setAssessmentData}
              />
            }
          />
          <Route
            path="/questionnaire"
            element={
              <QuestionnairePage
                config={config}
                assessmentData={assessmentData}
                setAssessmentData={setAssessmentData}
              />
            }
          />
          <Route
            path="/review"
            element={
              <ReviewPage
                config={config}
                assessmentData={assessmentData}
              />
            }
          />
          <Route
            path="/results"
            element={
              <ResultsPage
                config={config}
                assessmentData={assessmentData}
              />
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
