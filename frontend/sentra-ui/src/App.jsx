import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [showResult, setShowResult] = useState(false);
  const resultRef = useRef(null);

  const handleEvaluate = () => {
    if (input.trim()) {
      setShowResult(true);
      setTimeout(() => {
        resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    }
  };

  return (
    <div className="sentra-layout">
      {/* Full-width Top Bar */}
      <nav className="top-bar">
        <div className="container-wide">
          <div className="brand">SENTRA</div>
          <div className="nav-menu">
            <span>Governance</span>
            <span>Compliance</span>
            <span>API</span>
          </div>
        </div>
      </nav>

      {/* Centered Page Content */}
      <main className="main-content">
        <section className="hero-section">
          <div className="badge">v1.0 Decision Intelligence</div>
          <h1 className="hero-title">AI Policy Governance</h1>
          <p className="hero-subtitle">
            Automate policy enforcement and decision intelligence with Sentra's 
            enterprise-grade evaluation engine.
          </p>
        </section>

        <section className="page-block">
          <div className="upload-box">
            <div className="glow-icon">✦</div>
            <h3>Contextualize Documentation</h3>
            <p>Drop your internal policy PDFs or compliance JSONs here</p>
            <button className="btn-secondary">Upload Files</button>
          </div>
        </section>

        <section className="page-block">
          <h2 className="section-heading">Decision Input</h2>
          <div className="input-card-bg">
            <textarea
              className="decision-textarea"
              placeholder="Example: Can an intern work remotely using a personal laptop?"
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button className="btn-primary" onClick={handleEvaluate}>
              Evaluate Decision
            </button>
          </div>
        </section>

        {showResult && (
          <section className="results-container fade-in" ref={resultRef}>
            <div className="res-card">
              <span className="res-label">Evaluation Result</span>
              <div className="res-row"><strong>Risk Level:</strong> <span className="risk-tag">High</span></div>
              <div className="res-row"><strong>Policy Evidence:</strong> <span>Section 4.1.2</span></div>
              <div className="res-row"><strong>Recommendation:</strong> <span>Deny Access</span></div>
            </div>

            <div className="res-card">
              <span className="res-label">Reasoning</span>
              <p className="res-text">Using personal hardware for internal tasks violates the managed device policy.</p>
            </div>

            <div className="res-card accent-left">
              <span className="res-label">Safer Alternative</span>
              <p className="res-text">Issue a corporate-managed device with pre-configured security protocols.</p>
            </div>
          </section>
        )}
      </main>

      <footer className="page-footer">
        © 2026 SENTRA AI
      </footer>
    </div>
  );
}

export default App;