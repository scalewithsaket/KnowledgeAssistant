import { useState } from "react";
import type { SubmitEvent } from "react";

type QueryResponse = {
  answer: string;
};

const apiUrl = import.meta.env.RAG_API_URL;

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || isLoading) return;
    if (!apiUrl) {
      setError("The API URL is not configured. Set RAG_API_URL in app/ui/.env.");
      return;
    }

    setIsLoading(true);
    setAnswer("");
    setError("");

    try {
      const response = await fetch(`${apiUrl.replace(/\/+$/, "")}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmedQuestion }),
      });

      if (!response.ok) {
        throw new Error(`The request failed (${response.status}). Please try again.`);
      }

      const result: QueryResponse = await response.json();
      if (typeof result.answer !== "string" || !result.answer.trim()) {
        throw new Error("The assistant returned an empty answer. Please try another question.");
      }

      setAnswer(result.answer);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Something went wrong while getting your answer. Please try again.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="page-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="Knowledge Assistant home">
          <span className="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 32 32" fill="none">
              <path
                d="M7.5 8.25c3.15-1.35 6.05-.8 8.5 1.2v15c-2.45-2-5.35-2.55-8.5-1.2v-15Z"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinejoin="round"
              />
              <path
                d="M24.5 8.25c-3.15-1.35-6.05-.8-8.5 1.2v15c2.45-2 5.35-2.55 8.5-1.2v-15Z"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinejoin="round"
              />
              <path d="M11 12.5c1.4-.1 2.65.25 3.7 1.05M21 12.5c-1.4-.1-2.65.25-3.7 1.05" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            </svg>
          </span>
          <span><span className="brand-light">Knowledge Assistant</span></span>
        </a>
        <div className="topbar-note">
          <span className="status-dot" />
          Grounded in your knowledge base
        </div>
      </header>

      <section className="workspace" aria-labelledby="page-title">
        <div className="intro">
          <div className="eyebrow">
            <span className="eyebrow-line" />
            YOUR KNOWLEDGE, IN CONTEXT
          </div>
          <h1>
            <span>Good questions</span>
            <br />
            <span>find their answers.</span>
          </h1>
          <p className="intro-copy">
            Ask about your documents. Get a clear answer, grounded in the information that matters.
          </p>
        </div>

        <form className="question-card" onSubmit={handleSubmit}>
          <label htmlFor="question">What would you like to know?</label>
          <textarea
            id="question"
            name="question"
            placeholder="Ask a question about your knowledge base..."
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            rows={3}
            disabled={isLoading}
          />
          <div className="form-footer">
            <span className="input-hint">Answers are generated from your connected documents.</span>
            <button type="submit" disabled={!question.trim() || isLoading}>
              {isLoading ? (
                <>
                  <span className="spinner" aria-hidden="true" />
                  Thinking
                </>
              ) : (
                <>
                  Ask assistant
                  <svg aria-hidden="true" viewBox="0 0 20 20" fill="none">
                    <path d="M4 10h11m-4-4 4 4-4 4" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </>
              )}
            </button>
          </div>
        </form>

        {error && (
          <div className="error-message" role="alert">
            <span className="error-icon" aria-hidden="true">!</span>
            {error}
          </div>
        )}

        {answer && (
          <section className="answer-card" aria-labelledby="answer-title" aria-live="polite">
            <div className="answer-heading">
              <span className="answer-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="m5 12.5 4.2 4.2L19 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </span>
              <h2 id="answer-title">Answer</h2>
            </div>
            <p className="answer-text">{answer}</p>
          </section>
        )}

        {!answer && !error && !isLoading && (
          <div className="quiet-note">
            <span className="quiet-note-icon" aria-hidden="true">↳</span>
            Your answer will appear here
          </div>
        )}
      </section>

      <footer className="page-footer">
        <span>Knowledge Assistant</span>
        <span className="footer-divider" />
        <span>Thoughtful answers, from your own sources.</span>
      </footer>
    </main>
  );
}

export default App;
