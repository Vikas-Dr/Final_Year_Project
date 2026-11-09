import { useEffect, useRef, useState } from "react";
import api from "../api";
import { BrainCircuitIcon, SparklesIcon } from "./Icons";

const SUGGESTIONS = [
  "How can I improve my resume for a software role?",
  "What should I expect in a technical interview?",
  "Help me explain a project clearly.",
];

export default function AIChatAgentWidget() {
  const [inputMsg, setInputMsg] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      sender: "agent",
      text: "Hi, I’m your career assistant. I can help you strengthen a resume, prepare for an interview, or make sense of your evaluation.",
      provider: "AI Career Assistant",
    },
  ]);
  const messagesPanelRef = useRef(null);

  useEffect(() => {
    if (messages.length > 1) {
      const panel = messagesPanelRef.current;
      panel?.scrollTo({ top: panel.scrollHeight, behavior: "smooth" });
    }
  }, [messages]);

  const handleSend = async (event) => {
    event.preventDefault();
    if (!inputMsg.trim() || loading) return;

    const userText = inputMsg.trim();
    const assistantId = `${Date.now()}-${Math.random()}`;
    setInputMsg("");
    setMessages((prev) => [
      ...prev,
      { sender: "user", text: userText },
      {
        id: assistantId,
        sender: "agent",
        text: "",
        provider: "Llama 3 · preparing",
        streaming: true,
      },
    ]);
    setLoading(true);

    try {
      const token = localStorage.getItem("ai_eval_token");
      const response = await fetch(`${api.defaults.baseURL}/agent-chat/stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ message: userText }),
      });
      if (!response.ok) {
        throw new Error(`Chat request failed with status ${response.status}.`);
      }
      if (!response.body) {
        throw new Error("Streaming responses are not supported by this browser.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let completed = false;
      const updateAgent = (update) => {
        setMessages((prev) => prev.map((message) =>
          message.id === assistantId ? { ...message, ...update } : message
        ));
      };
      const processEvent = (line) => {
        if (!line.trim()) return;
        const event = JSON.parse(line);
        if (event.token) {
          setMessages((prev) => prev.map((message) =>
            message.id === assistantId
              ? { ...message, text: message.text + event.token, provider: "Llama 3 · replying" }
              : message
          ));
        }
        if (event.reply) updateAgent({ text: event.reply });
        if (event.provider) updateAgent({ provider: event.provider });
        if (event.error) updateAgent({ text: event.error, provider: "System notice" });
        if (event.done) {
          completed = true;
          updateAgent({ streaming: false });
        }
      };

      while (true) {
        const { value, done } = await reader.read();
        buffer += decoder.decode(value || new Uint8Array(), { stream: !done });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";
        lines.forEach(processEvent);
        if (done) break;
      }
      if (buffer.trim()) processEvent(buffer);
      if (!completed) throw new Error("The AI response ended before it was complete.");
    } catch (error) {
      setMessages((prev) => prev.map((message) =>
        message.id === assistantId
          ? {
              ...message,
              text: message.text || `${error.message} Check that the AI server is running, then try again.`,
              provider: message.text ? "Response interrupted" : "System notice",
              streaming: false,
            }
          : message
      ));
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="assistant-page">
      <div className="assistant-page-heading">
        <div className="assistant-page-title">
          <span className="assistant-eyebrow"><SparklesIcon size={15} /> YOUR CAREER WORKSPACE</span>
          <h1>AI career assistant</h1>
          <p>Get practical help with resumes, interviews, and your next career move.</p>
        </div>
        <div className="assistant-model-status">
          <span className="assistant-status-dot" />
          Local AI · llama3
        </div>
      </div>

      <div className="assistant-workspace">
        <aside className="assistant-context-panel">
          <div className="assistant-mark"><BrainCircuitIcon size={23} /></div>
          <span className="assistant-eyebrow">A CLEARER NEXT STEP</span>
          <h2>Work through the hard parts.</h2>
          <p>Use this space to turn a question into an action you can take.</p>
          <div className="assistant-topic-list" aria-label="Ways the assistant can help">
            <span><i>01</i> Improve a resume</span>
            <span><i>02</i> Practice an interview</span>
            <span><i>03</i> Understand your results</span>
          </div>
          <div className="assistant-context-note">
            <span className="assistant-status-dot" />
            Your conversation is handled by the local AI model.
          </div>
        </aside>

        <div className="assistant-chat-panel">
          <div className="assistant-chat-heading">
            <div className="assistant-avatar"><BrainCircuitIcon size={19} /></div>
            <div>
              <strong>Career assistant</strong>
              <span>Ask a question to get started</span>
            </div>
          </div>
          <div ref={messagesPanelRef} className="assistant-messages" aria-live="polite" aria-relevant="additions text">
            {messages.map((message, index) => (
              <div
                key={message.id || `${message.sender}-${index}`}
                className={`assistant-message-row ${message.sender === "user" ? "from-user" : "from-agent"}`}
              >
                {message.sender === "agent" && (
                  <span className="assistant-message-avatar"><BrainCircuitIcon size={15} /></span>
                )}
                <div className="assistant-message-content">
                  <div className={`assistant-message-bubble ${message.sender === "user" ? "user-bubble" : "agent-bubble"}`}>
                    {message.text || (message.streaming ? "Thinking…" : "")}
                    {message.streaming && message.text && <span className="chat-stream-cursor" aria-hidden="true" />}
                  </div>
                  {message.provider && <span className="assistant-message-meta">{message.provider}</span>}
                </div>
              </div>
            ))}
            {messages.length === 1 && (
              <div className="assistant-suggestions">
                <span>Try asking</span>
                {SUGGESTIONS.map((suggestion) => (
                  <button type="button" key={suggestion} onClick={() => setInputMsg(suggestion)}>
                    {suggestion}
                  </button>
                ))}
              </div>
            )}
          </div>

          <form onSubmit={handleSend} className="assistant-composer">
            <input
              type="text"
              value={inputMsg}
              onChange={(event) => setInputMsg(event.target.value)}
              placeholder="Ask about your resume, interview, or results…"
              aria-label="Message the career assistant"
              disabled={loading}
            />
            <button type="submit" disabled={loading || !inputMsg.trim()}>
              <span>{loading ? "Replying" : "Send"}</span>
              <span aria-hidden="true">↗</span>
            </button>
          </form>
          <p className="assistant-disclaimer">AI responses can be imperfect. Use them as a starting point.</p>
        </div>
      </div>
    </section>
  );
}
