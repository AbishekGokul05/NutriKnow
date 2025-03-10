import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { FiSend } from 'react-icons/fi';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github-dark.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { text: userMessage, isUser: true }]);
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/api/chat', {
        message: userMessage
      });
      
      setMessages(prev => [...prev, { text: response.data.response, isUser: false }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        text: 'Sorry, I encountered an error. Please try again.',
        isUser: false 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="chat-container pb-24">
        <h1 className="text-3xl font-bold text-center text-gray-800 py-6">
          Gemini Chat
        </h1>
        
        <div className="message-container">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.isUser ? 'user-message' : 'bot-message'}`}
            >
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeHighlight]}
                components={{
                  code({ node, inline, className, children, ...props }) {
                    return !inline ? (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    ) : (
                      <code className="bg-gray-100 px-1 rounded" {...props}>
                        {children}
                      </code>
                    );
                  }
                }}
              >
                {message.text}
              </ReactMarkdown>
            </div>
          ))}
          {isLoading && (
            <div className="bot-message message">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <form onSubmit={handleSubmit} className="input-container">
        <div className="max-w-4xl mx-auto flex gap-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 rounded-lg border-gray-300 focus:ring-2 focus:ring-primary focus:border-transparent"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-primary hover:bg-secondary text-white px-4 py-2 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <FiSend className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
}

export default App; 