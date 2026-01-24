function App() {
  return (
    /* Page background */
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#0b0e14",
        display: "flex",
        justifyContent: "center",
        padding: "32px",
        boxSizing: "border-box",
        fontFamily: "Inter, Arial, sans-serif",
        color: "#e6e6e6",
      }}
    >
      {/* App Canvas */}
      <div
        style={{
          width: "100%",
        }}
      >
        {/* Header */}
        <header
          style={{
            marginBottom: "24px",
            paddingBottom: "16px",
            borderBottom: "1px solid #1f2430",
          }}
        >
          <h1 style={{ marginBottom: "6px" }}>SENTRA</h1>
          <p style={{ margin: 0, color: "#9aa0aa" }}>
            AI Policy Governance & Decision Intelligence Platform
          </p>
        </header>

        {/* Main Console */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "420px 1fr",
            gap: "24px",
          }}
        >
          {/* Decision Input */}
          <section
            style={{
              backgroundColor: "#121826",
              borderRadius: "10px",
              padding: "20px",
              border: "1px solid #1f2430",
            }}
          >
            <h3 style={{ marginTop: 0 }}>Decision Input</h3>

            <textarea
              rows="8"
              placeholder="Example: Can an intern work remotely using a personal laptop?"
              style={{
                width: "100%",
                padding: "12px",
                fontSize: "14px",
                backgroundColor: "#0b0e14",
                color: "#e6e6e6",
                border: "1px solid #1f2430",
                borderRadius: "6px",
                boxSizing: "border-box",
              }}
            />

            <div style={{ marginTop: "16px" }}>
              <button
                style={{
                  width: "100%",
                  padding: "12px",
                  fontSize: "14px",
                  backgroundColor: "#2f6feb",
                  color: "#ffffff",
                  border: "none",
                  borderRadius: "6px",
                  cursor: "pointer",
                }}
              >
                Evaluate Decision
              </button>
            </div>
          </section>

          {/* Evaluation Result */}
          <section
            style={{
              backgroundColor: "#121826",
              borderRadius: "10px",
              padding: "20px",
              border: "1px solid #1f2430",
              minHeight: "320px",
            }}
          >
            <h3 style={{ marginTop: 0 }}>Evaluation Result</h3>

            <p><strong>Risk Level:</strong> —</p>
            <p><strong>Policy Evidence:</strong> —</p>
            <p><strong>Recommendation:</strong> —</p>

            <hr style={{ borderColor: "#1f2430", margin: "16px 0" }} />

            <h4>Reasoning</h4>
            <p>Explanation will appear here.</p>

            <h4>Safer Alternative</h4>
            <p>Suggested alternatives will appear here.</p>
          </section>
        </div>
      </div>
    </div>
  );
}

export default App;
