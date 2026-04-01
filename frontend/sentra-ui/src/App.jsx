import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  // --- UI State ---
  const [input, setInput] = useState('');
  const [showResult, setShowResult] = useState(false);
  
  // --- New File & Warning State ---
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [showWarning, setShowWarning] = useState(false);

  // --- Refs for Auto-Scrolling ---
  const resultRef = useRef(null);
  const decisionRef = useRef(null); 
  const uploadRef = useRef(null); // New ref for the top of the page

  // --- Upload State ---
  const [isDragging, setIsDragging] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(''); 
  const fileInputRef = useRef(null);

  // --- Analysis State ---
  const [analysis, setAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // ==========================================
  // DRAG AND DROP HANDLERS
  // ==========================================
  const onDragOver = (e) => { e.preventDefault(); setIsDragging(true); };
  const onDragLeave = (e) => { e.preventDefault(); setIsDragging(false); };
  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    if (droppedFiles.length > 0) uploadFiles(droppedFiles);
  };
  const onFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    if (selectedFiles.length > 0) uploadFiles(selectedFiles);
  };

  // ==========================================
  // BACKEND API: UPLOAD & CLEAR
  // ==========================================
  const uploadFiles = async (files) => {
    setUploadStatus('uploading');
    
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setUploadStatus('success');
        
        // Save the filenames to display them in the UI
        const fileNames = files.map(f => f.name);
        setUploadedFiles(fileNames);
        setShowWarning(false); // Hide warning if it was showing
        
        setTimeout(() => {
          setUploadStatus('');
          decisionRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 1500); 

      } else {
        setUploadStatus('error');
      }
    } catch (error) {
      console.error("Upload failed:", error);
      setUploadStatus('error');
    }
  };

  const handleClearFiles = async () => {
    try {
      // Tell Python to wipe Pinecone
      await fetch('http://localhost:8000/clear', { method: 'DELETE' });
      // Clear the frontend UI
      setUploadedFiles([]);
      setAnalysis(null);
      setShowResult(false);
    } catch (error) {
      console.error("Failed to clear database:", error);
    }
  };

  // ==========================================
  // BACKEND API: EVALUATE
  // ==========================================
  const handleEvaluate = async () => {
    // SECURITY CHECK: Are there files uploaded?
    if (uploadedFiles.length === 0) {
      setShowWarning(true);
      uploadRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      
      // Hide the blinking red text after 3 seconds
      setTimeout(() => setShowWarning(false), 3000);
      return;
    }

    if (!input.trim()) return;

    setIsAnalyzing(true);
    setShowResult(true); 
    setAnalysis(null);

    setTimeout(() => {
      resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input }), 
      });

      const data = await response.json();
      setAnalysis(data);
      
    } catch (error) {
      console.error("Analysis failed:", error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="sentra-layout">
      <nav className="top-bar">
        <div className="container-wide">
          <div className="brand">SENTRA</div>
          {/* The nav-menu containing Governance, Compliance, and API has been removed */}
        </div>
      </nav>

      <main className="main-content">
        <section className="hero-section">
          <div className="badge">v1.0 Decision Intelligence</div>
          <h1 className="hero-title">AI Policy Governance</h1>
          <p className="hero-subtitle">
            Automate policy enforcement and decision intelligence with Sentra's enterprise-grade evaluation engine.
          </p>
        </section>

        {/* Added uploadRef here for scrolling to the top on error */}
        <section className="page-block" ref={uploadRef}>
          <div 
            className={`upload-box ${isDragging ? 'drag-active' : ''}`}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            style={{ border: isDragging ? '2px dashed #10b981' : '2px dashed #2b303b', transition: 'all 0.3s ease' }}
          >
            <div className="glow-icon">✦</div>
            <h3>Contextualize Documentation</h3>
            
            {uploadStatus === 'uploading' ? (
              <p style={{ color: '#60a5fa' }}>Uploading and indexing into Pinecone...</p>
            ) : uploadStatus === 'success' ? (
              <p style={{ color: '#10b981' }}>✅ Files successfully ingested!</p>
            ) : uploadStatus === 'error' ? (
              <p style={{ color: '#ef4444' }}>❌ Upload failed. Is the backend running?</p>
            ) : (
              <p>Drop your internal policy PDFs or compliance JSONs here</p>
            )}

            <input type="file" multiple ref={fileInputRef} onChange={onFileSelect} style={{ display: 'none' }} accept=".pdf,.txt,.json" />
            <button className="btn-secondary" onClick={() => fileInputRef.current.click()} disabled={uploadStatus === 'uploading'}>
              {uploadStatus === 'uploading' ? 'Processing...' : 'Upload Files'}
            </button>
          </div>

          {/* --- FILE LIST AND WARNING TEXT --- */}
          <div className="upload-footer">
            {showWarning && (
              <p className="warning-text blink">⚠️ Please add a policy file first.</p>
            )}
            
            {uploadedFiles.length > 0 && (
              <div className="file-chip-container">
                {uploadedFiles.map((fileName, index) => (
                  <div key={index} className="file-chip">
                    <span className="file-icon">📄</span>
                    <span className="file-name">{fileName}</span>
                    <button className="remove-btn" onClick={handleClearFiles} title="Remove file and clear database">
                      ✕
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

        </section>

        <section className="page-block" ref={decisionRef}>
          <h2 className="section-heading">Decision Input</h2>
          <div className="input-card-bg">
            <textarea
              className="decision-textarea"
              placeholder="Example: Can an intern work remotely using a personal laptop?"
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button className="btn-primary" onClick={handleEvaluate} disabled={isAnalyzing}>
              {isAnalyzing ? "Analyzing..." : "Evaluate Decision"}
            </button>
          </div>
        </section>

        {showResult && (
          <section className="results-container fade-in" ref={resultRef}>
            {isAnalyzing ? (
              <div className="single-res-card center-text">
                <div className="spinner"></div>
                <p className="res-text">Consulting Policy Knowledge Base...</p>
              </div>
            ) : analysis ? (
              <div className="single-res-card">
                <div className="res-header-flex">
                  <h3 className="res-card-title">Evaluation Result</h3>
                  <span className={`risk-badge ${analysis.riskLevel?.trim().toLowerCase() || 'unknown'}`}>
                    {analysis.riskLevel?.trim() || 'Unknown'} Risk
                  </span>
                </div>
                <hr className="res-divider" />
                <div className="res-grid">
                  <div className="res-block">
                    <h4>Policy Evidence</h4>
                    <p>{analysis.evidence}</p>
                  </div>
                  <div className="res-block">
                    <h4>Recommendation</h4>
                    <p>{analysis.recommendation}</p>
                  </div>
                  <div className="res-block full-width">
                    <h4>Reasoning</h4>
                    <p>{analysis.reasoning}</p>
                  </div>
                  <div className="res-block full-width highlight-block">
                    <h4>Safer Alternative</h4>
                    <p>{analysis.alternatives}</p>
                  </div>
                </div>
              </div>
            ) : null}
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