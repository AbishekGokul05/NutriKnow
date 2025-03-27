import React, { useState, useEffect } from 'react';

const STORAGE_KEY = 'nutriknow_health_facts_history';
const MAX_STORED_FACTS = 10;

const HealthFact = () => {
  const [currentFact, setCurrentFact] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Load previous facts from local storage
  const [previousFacts, setPreviousFacts] = useState(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  });

  // Save previous facts to local storage when they change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(previousFacts));
  }, [previousFacts]);

  const fetchNewFact = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Construct URL with query parameters for previous facts
      let url = 'http://localhost:8000/api/v1/health-facts/';
      if (previousFacts && previousFacts.length > 0) {
        const queryParams = previousFacts
          .map(fact => `previous_facts=${encodeURIComponent(fact)}`)
          .join('&');
        url = `${url}?${queryParams}`;
      }
      
      // First try the new endpoint with proper GET request
      const response = await fetch(url, {
        method: 'GET',
      });

      if (!response.ok) {
        // If new endpoint fails, try the legacy endpoint
        const legacyResponse = await fetch('http://localhost:8000/api/v1/health-fact/', {
          method: 'GET',
        });
        
        if (!legacyResponse.ok) {
          throw new Error(`Error: ${legacyResponse.status}`);
        }
        
        const data = await legacyResponse.json();
        const newFact = data.fact;
        setCurrentFact(newFact);
        
        // Add to previous facts
        setPreviousFacts(prev => {
          const updated = [newFact, ...prev].slice(0, MAX_STORED_FACTS);
          return updated;
        });
      } else {
        const data = await response.json();
        const newFact = data.fact;
        setCurrentFact(newFact);
        
        // Add to previous facts
        setPreviousFacts(prev => {
          const updated = [newFact, ...prev].slice(0, MAX_STORED_FACTS);
          return updated;
        });
      }
    } catch (err) {
      console.error('Error fetching health fact:', err);
      setError('Failed to load health fact. Please try again.');
      // Fallback facts if API fails
      const fallbackFacts = [
        "Regular exercise can improve both physical and mental health.",
        "Drinking water helps maintain body temperature and remove waste.",
        "Getting enough sleep is crucial for immune system function.",
        "Eating a balanced diet provides essential nutrients for optimal health.",
        "Stress management techniques can improve overall well-being.",
        "Fruits and vegetables provide essential vitamins, minerals, and fiber.",
        "Whole grains contain fiber, which promotes digestive health.",
        "Lean proteins help build and repair body tissues.",
        "Healthy fats support brain function and nutrient absorption.",
        "Limiting processed foods can reduce sodium, sugar, and unhealthy fat intake."
      ];
      
      // Get facts that haven't been shown recently
      const unusedFacts = fallbackFacts.filter(fact => !previousFacts.includes(fact));
      const randomFact = unusedFacts.length > 0 
        ? unusedFacts[Math.floor(Math.random() * unusedFacts.length)]
        : fallbackFacts[Math.floor(Math.random() * fallbackFacts.length)];
      
      setCurrentFact(randomFact);
      
      // Add to previous facts
      setPreviousFacts(prev => {
        const updated = [randomFact, ...prev].slice(0, MAX_STORED_FACTS);
        return updated;
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchNewFact();
  }, []);

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-800">Health Fact of the Day</h2>
          <button
            onClick={fetchNewFact}
            disabled={isLoading}
            className="text-green-600 hover:text-green-800 focus:outline-none"
            title="Get another fact"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
        
        {isLoading ? (
          <div className="flex justify-center items-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-green-500"></div>
          </div>
        ) : error ? (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <p>{error}</p>
          </div>
        ) : (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <p className="text-gray-700 text-lg italic">"{currentFact}"</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default HealthFact; 