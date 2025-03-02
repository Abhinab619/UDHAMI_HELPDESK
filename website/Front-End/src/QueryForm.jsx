import { useState } from "react";
import axios from "axios";

function QueryForm() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/process-query", {
        query,
      });
      setResult(response.data);
    } catch (error) {
      console.error("Error processing query:", error);
    }
  };

  return (
    <div style={styles.pageContainer}>
      <div style={styles.contentWrapper}>
        <header style={styles.header}>
          <h1 style={styles.headerTitle}>Udhami Yojna Query Helpdesk</h1>
          <p style={styles.headerSubtitle}>
            Submit your query below, and we’ll help you find the right answer or the right officer.
          </p>
        </header>
        <main style={styles.mainContent}>
          <form onSubmit={handleSubmit} style={styles.form}>
            <textarea
              style={styles.textarea}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Describe your issue or ask your query here..."
              required
            />
            <button type="submit" style={styles.submitButton}>
              Submit Query
            </button>
          </form>

          {result && (
            <div style={styles.resultBox}>
              <h2 style={styles.resultTitle}>Response Details</h2>
              <p>
                <strong>Type:</strong> {result.type}
              </p>
              <p>
                <strong>Response:</strong> {result.response}
              </p>
              <p>
                <strong>Similarity Score:</strong> {result.score.toFixed(4)}
              </p>
            </div>
          )}
        </main>
        <footer style={styles.footer}>
          <p>© 2025 Udhami Yojna Helpdesk. All rights reserved.</p>
        </footer>
      </div>
    </div>
  );
}

const styles = {
  pageContainer: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    minHeight: "100vh",
    backgroundColor: "#f0f4f8",
    margin: 0,
    padding: 0,
  },
  contentWrapper: {
    width: "100%",
    maxWidth: "800px",
    backgroundColor: "#ffffff",
    borderRadius: "12px",
    boxShadow: "0 8px 16px rgba(0, 0, 0, 0.1)",
    padding: "20px",
    textAlign: "center",
  },
  header: {
    marginBottom: "20px",
  },
  headerTitle: {
    fontSize: "24px",
    fontWeight: "bold",
    color: "#333333",
  },
  headerSubtitle: {
    fontSize: "16px",
    color: "#666666",
  },
  mainContent: {
    marginTop: "20px",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },
  textarea: {
    width: "100%",
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #cccccc",
    fontSize: "16px",
    resize: "vertical",
    minHeight: "100px",
  },
  submitButton: {
    padding: "12px",
    backgroundColor: "#007bff",
    color: "#ffffff",
    border: "none",
    borderRadius: "8px",
    fontSize: "16px",
    cursor: "pointer",
  },
  resultBox: {
    marginTop: "20px",
    padding: "16px",
    backgroundColor: "#f9f9f9",
    borderRadius: "8px",
    border: "1px solid #dddddd",
  },
  resultTitle: {
    fontSize: "18px",
    fontWeight: "bold",
    color: "#333333",
    marginBottom: "10px",
  },
  footer: {
    marginTop: "20px",
    fontSize: "14px",
    color: "#888888",
  },
};

export default QueryForm;
