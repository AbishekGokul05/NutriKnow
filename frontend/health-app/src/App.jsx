import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import WelcomeAnimation from './components/WelcomeAnimation';
import Home from './components/Home';
import Scanner from './components/Scanner';
import HistoryDisplay from './components/HistoryDisplay';
import UserProfile from './components/UserProfile';
import HealthFact from './components/HealthFact';
import CameraCapture from './components/CameraCapture';
import ChatBar from './components/ChatBar';
import ProductCompare from './components/ProductCompare';
import './index.css';

// Home component
const HomeComponent = () => {
  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to NutriKnow
        </h1>
        <p className="text-xl text-gray-600">
          Your personal health and nutrition companion
        </p>
      </div>
      
      <HealthFact />
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Scan Products</h2>
          <p className="text-gray-600">
            Upload product images to analyze ingredients and get health insights.
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Track History</h2>
          <p className="text-gray-600">
            Keep track of your scanned products and their health information.
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Personal Profile</h2>
          <p className="text-gray-600">
            Customize your preferences and manage your health information.
          </p>
        </div>
      </div>
    </div>
  );
};

function App() {
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem('nutriknow_user_profile');
    return storedUser ? JSON.parse(storedUser) : { name: 'Guest' };
  });

  const [showNavbar, setShowNavbar] = useState(true);
  const [showCamera, setShowCamera] = useState(false);

  // Expose setShowCamera to the window object
  useEffect(() => {
    // Make the setShowCamera function available globally
    window.setAppShowCamera = (value) => {
      setShowCamera(value);
    };
    
    // Cleanup on unmount
    return () => {
      delete window.setAppShowCamera;
    };
  }, []);

  return (
    <Router>
      <div className="flex flex-col min-h-screen bg-gradient-to-b from-gray-50 to-gray-100" id="app-root">
        {/* Simplified Header */}
        <header className="bg-white shadow-md sticky top-0 z-30">
          <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <Link to="/home" className="text-2xl font-bold text-green-600 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
              </svg>
              NUTRIKNOW
            </Link>
            
            <Link to="/profile" className="flex items-center text-gray-700 hover:text-green-600">
              <span className="mr-2 hidden sm:inline">{user.name || 'Guest'}</span>
              <div className="h-10 w-10 bg-green-100 rounded-full flex items-center justify-center shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
            </Link>
          </div>
        </header>

        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<WelcomeAnimation />} />
            <Route path="/home" element={<Home />} />
            <Route path="/scan" element={<Scanner setShowNavbar={setShowNavbar} />} />
            <Route path="/compare" element={<ProductCompare />} />
            <Route path="/profile/*" element={
              <Routes>
                <Route index element={<UserProfile />} />
                <Route path="history" element={<UserProfile><HistoryDisplay /></UserProfile>} />
              </Routes>
            } />
            <Route path="*" element={<Navigate to="/home" replace />} />
          </Routes>
        </main>
        
        {/* Camera as overlay */}
        {showCamera && <CameraCapture setShowCamera={setShowCamera} />}
        
        <footer className="bg-green-600 text-white py-6 mt-auto">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div>
                <h3 className="text-lg font-semibold mb-4">NUTRIKNOW</h3>
                <p className="text-sm text-green-100">
                  Helping you make informed food choices by analyzing product ingredients
                  and providing personalized nutrition insights.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
                <ul className="space-y-2 text-sm">
                  <li><Link to="/home" className="text-green-100 hover:text-white">Home</Link></li>
                  <li><Link to="/scan" className="text-green-100 hover:text-white">Scan Product</Link></li>
                  <li><Link to="/compare" className="text-green-100 hover:text-white">Compare Products</Link></li>
                  <li><Link to="/profile/history" className="text-green-100 hover:text-white">View History</Link></li>
                  <li><Link to="/profile" className="text-green-100 hover:text-white">Profile</Link></li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-4">Contact</h3>
                <p className="text-sm text-green-100 mb-2">
                  Questions or feedback? Reach out to us!
                </p>
                <p className="text-sm text-green-100">
                  Email: support@nutriknow.com
                </p>
              </div>
            </div>
            <div className="border-t border-green-500 mt-8 pt-6 text-center text-sm text-green-100">
              © {new Date().getFullYear()} NUTRIKNOW. All rights reserved.
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App; 