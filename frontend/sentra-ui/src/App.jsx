import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [showResult, setShowResult] = useState(false);
  const resultRef = useRef(null);

  // --- NEW STATE FOR FILE UPLOAD ---
  const [isDragging, setIsDragging] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(''); // 'idle', 'uploading', 'success', 'error'
  const fileInputRef = useRef(null);

  const handleEvaluate = () => {
    if (input.trim()) {
      setShowResult(true);
      setTimeout(() => {
        resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    }
  };

  // --- NEW DRAG AND DROP HANDLERS ---
  const onDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    if (droppedFiles.length > 0) {
      uploadFiles(droppedFiles);
    }
  };

  const onFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    if (selectedFiles.length > 0) {
      uploadFiles(selectedFiles);
    }
  };

  // --- API CALL TO YOUR PYTHON BACKEND ---
  const uploadFiles = async (files) => {
    setUploadStatus('uploading');
    
    // Create FormData object to send files correctly
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file); // 'files' must match the Python backend parameter
    });

    try {
      // Sending to the local FastAPI server we just started
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setUploadStatus('success');
        // Reset back to idle after 3 seconds
        setTimeout(() => setUploadStatus(''), 3000); 
      } else {
        setUploadStatus('error');
      }
    } catch (error) {
      console.error("Upload failed:", error);
      setUploadStatus('error');
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
          {/* UPDATED UPLOAD BOX */}
          <div 
            className={`upload-box ${isDragging ? 'drag-active' : ''}`}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            style={{ 
              border: isDragging ? '2px dashed #4ade80' : '2px dashed #333',
              transition: 'all 0.3s ease'
            }}
          >
            <div className="glow-icon">✦</div>
            <h3>Contextualize Documentation</h3>
            
            {uploadStatus === 'uploading' ? (
              <p style={{ color: '#60a5fa' }}>Uploading and indexing into Pinecone...</p>
            ) : uploadStatus === 'success' ? (
              <p style={{ color: '#4ade80' }}>✅ Files successfully ingested!</p>
            ) : uploadStatus === 'error' ? (
              <p style={{ color: '#f87171' }}>❌ Upload failed. Is the backend running?</p>
            ) : (
              <p>Drop your internal policy PDFs or compliance JSONs here</p>
            )}

            {/* Hidden File Input */}
            <input 
              type="file" 
              multiple 
              ref={fileInputRef} 
              onChange={onFileSelect} 
              style={{ display: 'none' }} 
              accept=".pdf,.txt,.json"
            />
            
            <button 
              className="btn-secondary" 
              onClick={() => fileInputRef.current.click()}
              disabled={uploadStatus === 'uploading'}
            >
              {uploadStatus === 'uploading' ? 'Processing...' : 'Upload Files'}
            </button>
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