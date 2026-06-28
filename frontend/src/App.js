import React, { useState } from 'react';
import axios from 'axios';
import { Toaster, toast } from 'react-hot-toast';
import './App.css';

const SKILLS_LIST = [
  'python', 'java', 'javascript', 'react', 'node', 'sql', 'machine learning',
  'deep learning', 'django', 'flask', 'fastapi', 'spring', 'spring boot',
  'aws', 'docker', 'kubernetes', 'git', 'mongodb', 'postgresql', 'mysql',
  'html', 'css', 'typescript', 'angular', 'vue', 'tensorflow', 'pytorch',
  'pandas', 'numpy', 'scikit-learn', 'tableau', 'power bi', 'excel',
  'c++', 'c#', 'php', 'ruby', 'swift', 'kotlin', 'flutter', 'android',
  'linux', 'bash', 'jenkins', 'ci/cd', 'microservices', 'rest api'
];

function extractSkills(text) {
  const lower = text.toLowerCase();
  return SKILLS_LIST.filter(skill => lower.includes(skill));
}

function calculateScore(text, skills) {
  let score = 0;
  if (text.length > 500) score += 20;
  if (text.length > 1000) score += 10;
  if (skills.length > 5) score += 20;
  if (skills.length > 10) score += 10;
  if (text.toLowerCase().includes('experience')) score += 10;
  if (text.toLowerCase().includes('project')) score += 10;
  if (text.toLowerCase().includes('education')) score += 10;
  if (text.toLowerCase().includes('certification')) score += 10;
  return Math.min(score, 100);
}

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [skills, setSkills] = useState([]);
  const [score, setScore] = useState(0);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
    setSkills([]);
    setScore(0);
  };

  const handleSubmit = async () => {
    if (!file) {
      toast.error('Please upload a resume first!');
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await axios.post('https://resume-screener-tf1e.onrender.com/predict', formData);
      const data = response.data;
      const extractedSkills = extractSkills(data.full_text || data.text_preview);
      const resumeScore = calculateScore(data.full_text || data.text_preview, extractedSkills);
      setResult(data);
      setSkills(extractedSkills);
      setScore(resumeScore);
      toast.success('Resume analyzed successfully!');
    } catch (error) {
      console.log('Full error:', error);
      if (error.response && error.response.data && error.response.data.detail) {
        toast.error(error.response.data.detail);
      } else if (error.response) {
        toast.error('Server error: ' + error.response.status);
      } else {
        toast.error('Cannot connect to server!');
      }
    }
    setLoading(false);
  };

  return (
    <div className="app">
      <Toaster position="top-right" />

      <nav className="navbar">
        <div className="navbar-logo">Resume<span>Screener</span></div>
        <div className="navbar-tag">⚡ Powered by ML</div>
      </nav>

      <div className="hero">
        <h1>Screen Resumes with <span>AI</span></h1>
        <p>Upload your resume and instantly discover which job role you are best suited for using Machine Learning</p>
        <div className="hero-stats">
          <div className="stat">
            <div className="stat-number">2484+</div>
            <div className="stat-label">Resumes Trained On</div>
          </div>
          <div className="stat">
            <div className="stat-number">81%</div>
            <div className="stat-label">Model Accuracy</div>
          </div>
          <div className="stat">
            <div className="stat-number">6</div>
            <div className="stat-label">Job Categories</div>
          </div>
        </div>
      </div>

      <div className="main">
        <div className="upload-card">
          <h2>Upload Your Resume</h2>
          <p>Supported formats: PDF, TXT</p>
          <div className="upload-area">
            <div className="upload-icon">📄</div>
            <h3>Drag & Drop your resume here</h3>
            <p>or click to browse files</p>
            <label className="upload-label">
              Choose File
              <input type="file" accept=".pdf,.txt" onChange={handleFileChange} />
            </label>
            {file && <div className="file-selected">✅ {file.name} selected</div>}
          </div>
          <button className="analyze-btn" onClick={handleSubmit} disabled={loading}>
            {loading ? '🔍 Analyzing your resume...' : '🚀 Analyze Resume'}
          </button>
        </div>

        {result && (
          <div className="results">
            <div className="prediction-card">
              <h2>Best Job Match</h2>
              <div className="predicted-role">{result.predicted_category}</div>
              <div className="confidence-badge">🎯 {result.confidence}% Confidence</div>
            </div>

            <div style={{display:'grid', gridTemplateColumns:'1fr 1fr 1fr', gap:'16px'}}>
              <div className="result-card" style={{textAlign:'center'}}>
                <div style={{fontSize:'40px', fontWeight:'800', color:'#4f46e5'}}>{score}</div>
                <div style={{color:'#6b7280', marginTop:'4px'}}>Resume Score</div>
              </div>
              <div className="result-card" style={{textAlign:'center'}}>
                <div style={{fontSize:'40px', fontWeight:'800', color:'#4f46e5'}}>{skills.length}</div>
                <div style={{color:'#6b7280', marginTop:'4px'}}>Skills Found</div>
              </div>
              <div className="result-card" style={{textAlign:'center'}}>
                <div style={{fontSize:'40px', fontWeight:'800', color:'#4f46e5'}}>{result.confidence}%</div>
                <div style={{color:'#6b7280', marginTop:'4px'}}>Match Score</div>
              </div>
            </div>

            <div className="result-card">
              <div className="section-title">📊 Top 5 Job Matches</div>
              {result.top_5_matches.map((match, i) => (
                <div key={i} className="match-item">
                  <div className="match-rank">{i + 1}</div>
                  <span className="match-name">{match.category}</span>
                  <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${match.score}%` }}></div>
                  </div>
                  <span className="match-score">{match.score}%</span>
                </div>
              ))}
            </div>

            {skills.length > 0 && (
              <div className="result-card">
                <div className="section-title">🛠️ Skills Detected</div>
                <div className="skills-grid">
                  {skills.map((skill, i) => (
                    <span key={i} className="skill-tag">{skill}</span>
                  ))}
                </div>
              </div>
            )}

            <div className="result-card">
              <div className="section-title">📝 Resume Preview</div>
              <div className="preview-text">{result.text_preview}</div>
            </div>
          </div>
        )}
      </div>

      <div className="how-it-works">
        <h2>How It Works</h2>
        <div className="steps">
          <div className="step">
            <div className="step-icon">📤</div>
            <h3>Upload Resume</h3>
            <p>Upload your PDF or TXT resume file</p>
          </div>
          <div className="step">
            <div className="step-icon">🤖</div>
            <h3>ML Analysis</h3>
            <p>Our Random Forest model analyzes your resume</p>
          </div>
          <div className="step">
            <div className="step-icon">🎯</div>
            <h3>Get Results</h3>
            <p>See your best job match with confidence score</p>
          </div>
          <div className="step">
            <div className="step-icon">🚀</div>
            <h3>Apply Smart</h3>
            <p>Apply to roles that match your profile</p>
          </div>
        </div>
      </div>

      <div className="footer">
        Built with ❤️ by <span>Aaruhya Reddy</span> · Powered by Machine Learning
      </div>
    </div>
  );
}

export default App;