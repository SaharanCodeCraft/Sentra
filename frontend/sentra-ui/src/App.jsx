import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  // --- UI State ---
  const [input, setInput] = useState('');
  const [showResult, setShowResult] = useState(false);
  const resultRef = useRef(null);

  // --- Upload State ---
  const [isDragging, setIsDragging] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(''); // 'idle', 'uploading', 'success', 'error'
  const fileInputRef = useRef(null);

  // --- Analysis State ---
  const [analysis, setAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // ==========================================
  // 1. DRAG AND DROP HANDLERS
  // ==========================================
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

  // ==========================================
  // 2. BACKEND API: UPLOAD (Ingestion)
  // ==========================================
  const uploadFiles = async (files) => {
    setUploadStatus('uploading');
    
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setUploadStatus('success');
        setTimeout(() => setUploadStatus(''), 3000); 
      } else {
        setUploadStatus('error');
      }
    } catch (error) {
      console.error("Upload failed:", error);
      setUploadStatus('error');
    }
  };

  // ==========================================
  // 3. BACKEND API: EVALUATE (RAG Retrieval)
  // ==========================================
  const handleEvaluate = async () => {
    if (!input.trim()) return;

    setIsAnalyzing(true);
    setShowResult(true); 
    setAnalysis(null);

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: input }), 
      });

      const data = await response.json();
      setAnalysis(data);

      setTimeout(() => {
        resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
      
    } catch (error) {
      console.error("Analysis failed:", error);
      setAnalysis({ 
        riskLevel: "Error", 
        evidence: "Connection failed", 
        recommendation: "Check backend", 
        reasoning: "Could not connect to localhost:8000", 
        alternatives: "Make sure uvicorn is running." 
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  // ==========================================
  // 4. UI RENDER
  // ==========================================
  return (
    <div className="sentra-layout">
      {/* Navigation */}
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

      <main className="main-content">
        {/* Hero Section */}
        <section className="hero-section">
          <div className="badge">v1.0 Decision Intelligence</div>
          <h1 className="hero-title">AI Policy Governance</h1>
          <p className="hero-subtitle">
            Automate policy enforcement and decision intelligence with Sentra's 
            enterprise-grade evaluation engine.
          </p>
        </section>

        {/* Upload Section */}
        <section className="page-block">
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

        {/* Input Section */}
        <section className="page-block">
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

        {/* Results Section */}
        {showResult && (
          <section className="results-container fade-in" ref={resultRef}>
            {isAnalyzing ? (
              <div className="res-card" style={{ textAlign: 'center', padding: '2rem' }}>
                <p className="res-text">Consulting Policy Knowledge Base...</p>
              </div>
            ) : analysis ? (
              <>
                <div className="res-card">
                  <span className="res-label">Evaluation Result</span>
                  <div className="res-row">
                    <strong>Risk Level:</strong> 
                    <span className={`risk-tag ${analysis.riskLevel === 'High' ? 'high' : analysis.riskLevel === 'Low' ? 'low' : 'medium'}`}>
                      {analysis.riskLevel}
                    </span>
                  </div>
                  <div className="res-row"><strong>Policy Evidence:</strong> <span>{analysis.evidence}</span></div>
                  <div className="res-row"><strong>Recommendation:</strong> <span>{analysis.recommendation}</span></div>
                </div>

                <div className="res-card">
                  <span className="res-label">Reasoning / Policy Extract</span>
                  <p className="res-text">{analysis.reasoning}</p>
                </div>

                <div className="res-card accent-left">
                  <span className="res-label">Safer Alternative</span>
                  <p className="res-text">{analysis.alternatives}</p>
                </div>
              </>
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