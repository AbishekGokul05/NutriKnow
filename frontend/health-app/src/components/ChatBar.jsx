import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const ChatBar = ({ inlineMode = false }) => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([
    { type: 'system', text: 'Hello! I\'m your NutriKnow assistant. Ask me anything about nutrition or scan a product to get started.' }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [showCameraOptions, setShowCameraOptions] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  
  const fileInputRef = useRef(null);
  const chatContainerRef = useRef(null);
  const navigate = useNavigate();

  // Set initial expanded state when in inline mode
  useEffect(() => {
    if (inlineMode) {
      setIsExpanded(true);
    }
  }, [inlineMode]);

  // Auto-scroll to bottom when chat history changes
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory, isLoading]);

  // Get the setShowCamera function from the app context
  const setShowCamera = () => {
    // This is a temporary approach. In a full implementation, you would use React Context
    // or pass this function as a prop.
    if (window.setAppShowCamera) {
      window.setAppShowCamera(true);
    } else {
      // Fallback: store this function in the global scope
      window.setAppShowCamera = (val) => {
        // Find the App component's setState in the DOM
        const appElement = document.getElementById('root');
        if (appElement && appElement.__reactFiber$) {
          // This is a React internal API and might break in future versions
          const appInstance = appElement.__reactFiber$;
          if (appInstance && appInstance.setShowCamera) {
            appInstance.setShowCamera(val);
          }
        }
      };
      window.setAppShowCamera(true);
    }
    setShowCameraOptions(false);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!message.trim()) return;
    
    // Add user message to chat
    const userMessage = { type: 'user', text: message };
    setChatHistory(prev => [...prev, userMessage]);
    
    // Clear input field
    const sentMessage = message;
    setMessage('');
    
    // Show loading state
    setIsLoading(true);
    
    try {
      // For messages without an image, create a text-only response
      setTimeout(() => {
        const responseText = getAutoResponse(sentMessage);
        const botResponse = { 
          type: 'system', 
          text: responseText
        };
        setChatHistory(prev => [...prev, botResponse]);
        setIsLoading(false);
      }, 1000);
      
    } catch (error) {
      console.error('Error sending message:', error);
      // Fallback response if API fails
      setTimeout(() => {
        const botResponse = { 
          type: 'system', 
          text: 'Sorry, I\'m having trouble connecting to the server. Please try again later or check your connection.'
        };
        setChatHistory(prev => [...prev, botResponse]);
        setIsLoading(false);
      }, 500);
    }
  };

  const getAutoResponse = (query) => {
    const lowerQuery = query.toLowerCase();
    
    if (lowerQuery.includes('hello') || lowerQuery.includes('hi') || lowerQuery.includes('hey')) {
      return "Hello! How can I help you with your nutrition questions today?";
    } else if (lowerQuery.includes('thank') || lowerQuery.includes('thanks')) {
      return "You're welcome! Feel free to ask if you have more questions.";
    } else if (lowerQuery.includes('keto') || lowerQuery.includes('ketogenic')) {
      return "The ketogenic diet is a high-fat, low-carb diet that can help with weight loss and may provide health benefits for certain conditions. It typically limits carbs to 20-50g per day and focuses on fats from sources like oils, fatty fish, and nuts.";
    } else if (lowerQuery.includes('gluten')) {
      return "Gluten is a group of proteins found in grains like wheat, barley, and rye. People with celiac disease, gluten sensitivity, or wheat allergy should avoid it. Gluten-free alternatives include rice, corn, quinoa, and buckwheat.";
    } else if (lowerQuery.includes('protein') || lowerQuery.includes('proteins')) {
      return "Proteins are essential nutrients for muscle building and repair. Good sources include lean meats, fish, eggs, dairy, legumes, nuts, and seeds. For most adults, the recommended daily intake is about 0.8g per kg of body weight.";
    } else if (lowerQuery.includes('vitamin') || lowerQuery.includes('vitamins')) {
      return "Vitamins are essential micronutrients needed for various bodily functions. They're classified as water-soluble (B, C) or fat-soluble (A, D, E, K). A balanced diet with plenty of fruits and vegetables usually provides adequate vitamins.";
    } else if (lowerQuery.includes('sugar') || lowerQuery.includes('sugars')) {
      return "Added sugars should be limited in a healthy diet. The WHO recommends limiting added sugars to less than 10% of daily calories. Sugar can be hidden in many processed foods, so it's important to read ingredient labels carefully.";
    } else if (lowerQuery.includes('carb') || lowerQuery.includes('carbohydrate')) {
      return "Carbohydrates are a major source of energy. Complex carbs like whole grains, fruits, and vegetables are generally healthier than simple carbs like sugar. They provide fiber and nutrients and cause a more gradual rise in blood sugar.";
    } else if (lowerQuery.includes('fat') || lowerQuery.includes('fats')) {
      return "Not all fats are unhealthy. Unsaturated fats from foods like olive oil, avocados, and nuts are beneficial. Trans fats should be avoided, while saturated fats should be limited. Fat is essential for absorbing certain vitamins and providing energy.";
    } else if (lowerQuery.includes('scan') || lowerQuery.includes('picture') || lowerQuery.includes('photo')) {
      return "To scan a product, click the camera icon in the chat input area. You can take a photo or upload an image of the product's ingredient list or nutrition label.";
    } else {
      return "That's an interesting question about nutrition. While I don't have specific information on that, I recommend looking for foods with minimal processing and a variety of nutrients. Is there something more specific you'd like to know?";
    }
  };

  const toggleChat = () => {
    setIsExpanded(!isExpanded);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    // Store the selected image in sessionStorage
    const reader = new FileReader();
    reader.onload = (event) => {
      sessionStorage.setItem('scannedImage', event.target.result);
      navigate('/scanner');
    };
    reader.readAsDataURL(file);
  };

  const handleFileUpload = () => {
    fileInputRef.current?.click();
  };

  const handleScanClick = () => {
    setShowCameraOptions(!showCameraOptions);
  };

  const handleCameraCapture = () => {
    setShowCamera();
  };

  // If in inline mode, render the chat without the popup container
  if (inlineMode) {
    return (
      <div className="flex flex-col h-full rounded-lg overflow-hidden border border-gray-200">
        <div 
          ref={chatContainerRef}
          className="flex-grow h-96 p-4 overflow-y-auto bg-gray-50"
        >
          {chatHistory.map((msg, index) => (
            <div 
              key={index} 
              className={`mb-3 ${msg.type === 'user' ? 'text-right' : ''}`}
            >
              <div 
                className={`inline-block p-3 rounded-lg max-w-xs sm:max-w-sm md:max-w-md ${
                  msg.type === 'user' 
                    ? 'bg-green-600 text-white rounded-br-none' 
                    : 'bg-gray-200 text-gray-800 rounded-bl-none'
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex items-center justify-start mb-3">
              <div className="bg-gray-200 rounded-lg p-3">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
        </div>
        
        {/* Camera options dropdown */}
        {showCameraOptions && (
          <div className="absolute bottom-16 left-4 bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden z-10">
            <button 
              onClick={handleCameraCapture}
              className="w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Take a Photo
            </button>
            <button 
              onClick={handleFileUpload}
              className="w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              Upload Image
            </button>
          </div>
        )}
        
        <input
          type="file"
          accept="image/*"
          className="hidden"
          ref={fileInputRef}
          onChange={handleFileChange}
        />
        
        <form onSubmit={handleSendMessage} className="border-t border-gray-200 p-3 flex items-center bg-white">
          <button 
            type="button" 
            onClick={handleScanClick}
            className="p-2 text-gray-500 hover:text-green-600 focus:outline-none"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </button>
          <input
            type="text"
            placeholder="Type your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="flex-1 mx-3 py-2 px-3 rounded-full focus:outline-none bg-gray-100 focus:bg-white"
          />
          <button 
            type="submit" 
            className="p-2 text-white bg-green-600 rounded-full hover:bg-green-700 focus:outline-none"
            disabled={isLoading || !message.trim()}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </form>
      </div>
    );
  }

  // Regular floating chat box
  return (
    <div className={`fixed bottom-6 right-6 z-40 transition-all duration-300 ease-in-out ${isExpanded ? 'w-96' : 'w-56'}`}>
      {/* Chat header/toggle button */}
      <div 
        className="bg-green-600 text-white p-3 rounded-t-xl flex justify-between items-center cursor-pointer shadow-lg"
        onClick={toggleChat}
      >
        <div className="flex items-center">
          <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center mr-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-green-600" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
            </svg>
          </div>
          <h3 className="font-medium">Nutrition Assistant</h3>
        </div>
        <div>
          {isExpanded ? (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z" clipRule="evenodd" />
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
          )}
        </div>
      </div>
      
      {/* Expanded chat content */}
      {isExpanded && (
        <div className="bg-white rounded-b-xl shadow-lg overflow-hidden">
          <div 
            ref={chatContainerRef}
            className="h-80 p-4 overflow-y-auto bg-gray-50"
          >
            {chatHistory.map((msg, index) => (
              <div 
                key={index} 
                className={`mb-3 ${msg.type === 'user' ? 'text-right' : ''}`}
              >
                <div 
                  className={`inline-block p-3 rounded-lg max-w-xs ${
                    msg.type === 'user' 
                      ? 'bg-green-600 text-white rounded-br-none' 
                      : 'bg-gray-200 text-gray-800 rounded-bl-none'
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex items-center justify-start mb-3">
                <div className="bg-gray-200 rounded-lg p-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          {/* Camera options dropdown */}
          {showCameraOptions && (
            <div className="absolute bottom-16 left-4 bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden z-10">
              <button 
                onClick={handleCameraCapture}
                className="w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Take a Photo
              </button>
              <button 
                onClick={handleFileUpload}
                className="w-full text-left px-4 py-2 hover:bg-gray-100 flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                Upload Image
              </button>
            </div>
          )}
          
          <input
            type="file"
            accept="image/*"
            className="hidden"
            ref={fileInputRef}
            onChange={handleFileChange}
          />
          
          <form onSubmit={handleSendMessage} className="border-t border-gray-200 p-3 flex items-center">
            <button 
              type="button" 
              onClick={handleScanClick}
              className="p-2 text-gray-500 hover:text-green-600 focus:outline-none"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
            <input
              type="text"
              placeholder="Type your message..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="flex-1 mx-3 py-2 px-3 rounded-full focus:outline-none bg-gray-100 focus:bg-white"
            />
            <button 
              type="submit" 
              className="p-2 text-white bg-green-600 rounded-full hover:bg-green-700 focus:outline-none"
              disabled={isLoading || !message.trim()}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </form>
        </div>
      )}
      
      {/* Collapsed quick actions (visible when chat is collapsed) */}
      {!isExpanded && (
        <div className="flex justify-center space-x-2 bg-white p-2 rounded-b-xl shadow-lg">
          <button 
            onClick={() => {
              setIsExpanded(true);
              setTimeout(() => {
                if (chatContainerRef.current) {
                  chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
                }
              }, 100);
            }}
            className="p-2 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors"
            title="Ask a question"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </button>
          <button 
            onClick={handleCameraCapture}
            className="p-2 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors"
            title="Take a photo"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </button>
          <button 
            onClick={handleFileUpload}
            className="p-2 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors"
            title="Upload an image"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
          </button>
        </div>
      )}
    </div>
  );
};

export default ChatBar; 