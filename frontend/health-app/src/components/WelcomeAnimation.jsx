import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const WelcomeAnimation = () => {
  const [animationComplete, setAnimationComplete] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // After animation completes, redirect to home page
    const timer = setTimeout(() => {
      setAnimationComplete(true);
      setTimeout(() => {
        navigate('/home');
      }, 500); // Small delay after fade-out starts
    }, 2500); // Animation duration

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className={`fixed inset-0 bg-green-50 flex items-center justify-center z-50 transition-opacity duration-500 ${animationComplete ? 'opacity-0' : 'opacity-100'}`}>
      <div className="text-center transform transition-transform duration-2000 ease-in-out scale-100 animate-zoom">
        <h1 className="text-5xl font-bold text-green-600 mb-4">Welcome to NutriKnow</h1>
        <p className="text-xl text-gray-700">Your personal health partner</p>
      </div>
    </div>
  );
};

export default WelcomeAnimation; 