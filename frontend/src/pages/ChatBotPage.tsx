import { FormEvent, useState } from 'react';

const suggestions = [
  'Which crop should I grow?',
  'Should I irrigate my tomato crop today?',
  'Is my crop at risk of disease?',
  'Will rain affect my crop?',
  'How can I improve my yield?',
  'What fertilizer should I use?',
];

const ChatBotPage = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Hello! I can help with crop selection, irrigation timing, disease risk, and field decisions.' },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async (prompt: string) => {
    const userMessage = { role: 'user', text: prompt };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: prompt }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { role: 'assistant', text: data.reply }]);
    } catch {
      setMessages((prev) => [...prev, { role: 'assistant', text: 'I am having trouble connecting to the AI service right now. Please try again in a moment.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    const prompt = input.trim();
    setInput('');
    sendMessage(prompt);
  };

  return (
    <div className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">AgriMitra Assistant</p>
          <h2>Ask about your field and crop decisions.</h2>
        </div>
      </div>
      <div className="chat-shell panel">
        <div className="suggestion-row">
          {suggestions.map((item) => (
            <button key={item} className="secondary" onClick={() => sendMessage(item)}>{item}</button>
          ))}
        </div>
        <div className="chat-window">
          {messages.map((msg, idx) => (
            <div key={`${msg.role}-${idx}`} className={`chat-bubble ${msg.role}`}>
              {msg.text}
            </div>
          ))}
          {loading && (
            <div className="chat-bubble assistant typing-bubble">
              <span className="typing-dot" />
              <span className="typing-dot" />
              <span className="typing-dot" />
            </div>
          )}
        </div>
        <form onSubmit={handleSubmit} className="chat-form">
          <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask AgriMitra about your farm..." />
          <button className="primary" type="submit" disabled={loading}>{loading ? 'Thinking...' : 'Send'}</button>
        </form>
      </div>
    </div>
  );
};

export default ChatBotPage;
