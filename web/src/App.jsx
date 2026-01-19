import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, Bot, User, Cpu, Code, ClipboardList, PenTool } from 'lucide-react';
import './App.css';

const API_URL = 'http://localhost:8000/api';

const AGENTS = [
  { id: 'coordinator', name: 'Coordinator Agent', icon: ClipboardList, desc: 'Project management & orchestration' },
  { id: 'researcher', name: 'Researcher Agent', icon: PenTool, desc: 'Deep analysis & reasoning (DeepSeek-R1)' },
  { id: 'coder', name: 'Coder Agent', icon: Code, desc: 'Software development (Qwen 2.5)' },
];

function App() {
  const [activeAgent, setActiveAgent] = useState(AGENTS[0]);
  const [messages, setMessages] = useState([
    { role: 'assistant', content: `Hello! I'm the ${AGENTS[0].name}. How can I help you today?` }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleAgentChange = (agent) => {
    setActiveAgent(agent);
    setMessages([
      { role: 'assistant', content: `Switched to ${agent.name}. Ready for tasks.` }
    ]);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          agent_id: activeAgent.id,
          message: userMsg.content
        }),
      });

      if (!res.ok) throw new Error('API Error');

      const data = await res.json();
      const aiMsg = { role: 'assistant', content: data.response };
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      const errorMsg = { role: 'assistant', content: "⚠️ Error communicating with the agent. Please make sure the backend server is running." };
      setMessages(prev => [...prev, errorMsg]);
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <Cpu size={24} />
          <span>Antigravity AI</span>
        </div>
        
        <div className="agent-list">
          {AGENTS.map(agent => (
            <div 
              key={agent.id}
              className={`agent-item ${activeAgent.id === agent.id ? 'active' : ''}`}
              onClick={() => handleAgentChange(agent)}
            >
              <agent.icon size={20} />
              <div>
                <div style={{ fontWeight: 500 }}>{agent.name}</div>
                <div style={{ fontSize: '0.75rem', opacity: 0.7 }}>{agent.desc.split(' ')[0]}...</div>
              </div>
              {activeAgent.id === agent.id && <div className="status-indicator" />}
            </div>
          ))}
        </div>
      </aside>

      {/* Main Chat */}
      <main className="chat-area">
        <header className="chat-header">
          <div className="header-title">
            <h2>{activeAgent.name}</h2>
            <div className="header-subtitle">{activeAgent.desc}</div>
          </div>
          {/* Status badge or other header items could go here */}
        </header>

        <div className="messages-container">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className={`avatar ${msg.role === 'user' ? 'user' : 'ai'}`}>
                {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
              </div>
              <div className="message-content">
                <ReactMarkdown>{msg.content}</ReactMarkdown>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className={`message assistant`}>
              <div className="avatar ai"><Bot size={20} /></div>
              <div className="message-content">
                <span className="thinking-dots">Thinking...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <div className="input-container">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={`Message ${activeAgent.name}...`}
            />
            <button className="send-btn" onClick={sendMessage} disabled={isLoading || !input.trim()}>
              <Send size={20} />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
