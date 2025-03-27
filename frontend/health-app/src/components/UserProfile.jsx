import React, { useState, useEffect } from 'react';
import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom';

const UserProfile = ({ children }) => {
  const [user, setUser] = useState({
    name: '',
    email: '',
    allergies: [],
    dietaryPreferences: []
  });
  const [activeTab, setActiveTab] = useState('profile');
  const [scanHistory, setScanHistory] = useState([]);
  const location = useLocation();
  const navigate = useNavigate();
  
  useEffect(() => {
    // Set active tab based on URL
    if (location.pathname.includes('history')) {
      setActiveTab('history');
    } else {
      setActiveTab('profile');
    }
    
    // Load saved user profile from localStorage
    const savedProfile = localStorage.getItem('nutriknow_user_profile');
    if (savedProfile) {
      setUser(JSON.parse(savedProfile));
    }
    
    // Load scan history
    const savedHistory = localStorage.getItem('nutriknow_scan_history');
    if (savedHistory) {
      setScanHistory(JSON.parse(savedHistory));
    }
  }, [location]);
  
  // Calculate allergen alerts based on user's allergies and scan history
  const getAllergenAlerts = () => {
    if (!user.allergies.length || !scanHistory.length) return [];
    
    const alerts = scanHistory
      .filter(item => 
        item.analysis && 
        item.analysis.allergenAlerts && 
        item.analysis.allergenAlerts.some(alert => 
          user.allergies.some(allergen => 
            alert.toLowerCase().includes(allergen.toLowerCase())
          )
        )
      )
      .map(item => ({
        productName: item.productName || 'Unknown Product',
        timestamp: item.timestamp,
        matchingAllergens: item.analysis.allergenAlerts.filter(alert =>
          user.allergies.some(allergen => 
            alert.toLowerCase().includes(allergen.toLowerCase())
          )
        )
      }));
    
    return alerts;
  };
  
  // Calculate dietary preference matches in scan history
  const getDietaryMatches = () => {
    if (!user.dietaryPreferences.length || !scanHistory.length) return [];
    
    const matches = scanHistory
      .filter(item => 
        item.analysis && 
        item.analysis.goodIngredients &&
        user.dietaryPreferences.some(pref => {
          // Generic matching based on analysis data
          const prefLower = pref.toLowerCase();
          const hasMatchingIngredient = item.analysis.goodIngredients.some(
            ingredient => ingredient.toLowerCase().includes(prefLower)
          );
          const noConflictingNotes = !item.analysis.cautionaryNotes?.some(
            note => note.toLowerCase().includes(prefLower)
          );
          
          return hasMatchingIngredient || noConflictingNotes;
        })
      )
      .map(item => ({
        productName: item.productName || 'Unknown Product',
        timestamp: item.timestamp,
        matchedPreference: user.dietaryPreferences.find(pref => {
          // Use same matching logic as above
          const prefLower = pref.toLowerCase();
          const hasMatchingIngredient = item.analysis.goodIngredients.some(
            ingredient => ingredient.toLowerCase().includes(prefLower)
          );
          const noConflictingNotes = !item.analysis.cautionaryNotes?.some(
            note => note.toLowerCase().includes(prefLower)
          );
          
          return hasMatchingIngredient || noConflictingNotes;
        })
      }));
    
    return matches;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUser(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAllergiesChange = (e) => {
    const value = e.target.value;
    const allergies = value.split(',')
      .map(item => item.trim())
      .filter(item => item !== '');
    
    setUser(prev => ({
      ...prev,
      allergies
    }));
  };

  const handlePreferencesChange = (e) => {
    const value = e.target.value;
    const preferences = value.split(',')
      .map(item => item.trim())
      .filter(item => item !== '');
    
    setUser(prev => ({
      ...prev,
      dietaryPreferences: preferences
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Save to localStorage
    localStorage.setItem('nutriknow_user_profile', JSON.stringify(user));
    alert('Profile saved successfully!');
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    if (tab === 'history') {
      navigate('/profile/history');
    } else {
      navigate('/profile');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  // Filter scan history based on allergies
  const allergenAlerts = getAllergenAlerts();
  const dietaryMatches = getDietaryMatches();

  return (
    <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 mb-20">
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            <button
              onClick={() => handleTabChange('profile')}
              className={`w-1/2 py-4 px-1 text-center border-b-2 font-medium text-sm ${
                activeTab === 'profile'
                  ? 'border-green-500 text-green-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                Profile Settings
              </div>
            </button>
            <button
              onClick={() => handleTabChange('history')}
              className={`w-1/2 py-4 px-1 text-center border-b-2 font-medium text-sm ${
                activeTab === 'history'
                  ? 'border-green-500 text-green-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Scan History
              </div>
            </button>
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'profile' ? (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Your Profile</h2>
              
              {/* Personalized alerts based on scan history */}
              {allergenAlerts.length > 0 && (
                <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-red-700 mb-2">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 inline mr-1" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    Allergen Alert
                  </h3>
                  <p className="text-red-600 mb-2">
                    Based on your allergen profile, we found potential issues with your recent scans:
                  </p>
                  <ul className="list-disc list-inside text-sm text-gray-700">
                    {allergenAlerts.slice(0, 3).map((alert, index) => (
                      <li key={index}>
                        <strong>{alert.productName}</strong> ({formatDate(alert.timestamp)}) - 
                        Contains: <span className="text-red-600">{alert.matchingAllergens.join(', ')}</span>
                      </li>
                    ))}
                  </ul>
                  {allergenAlerts.length > 3 && (
                    <p className="text-sm text-gray-500 mt-2">
                      And {allergenAlerts.length - 3} more...
                      <button 
                        onClick={() => handleTabChange('history')}
                        className="text-green-600 hover:underline ml-1"
                      >
                        View all
                      </button>
                    </p>
                  )}
                </div>
              )}
              
              {/* Dietary preference matches */}
              {dietaryMatches.length > 0 && (
                <div className="mb-6 bg-green-50 border border-green-200 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-green-700 mb-2">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 inline mr-1" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Dietary Matches
                  </h3>
                  <p className="text-green-600 mb-2">
                    These products match your dietary preferences:
                  </p>
                  <ul className="list-disc list-inside text-sm text-gray-700">
                    {dietaryMatches.slice(0, 3).map((match, index) => (
                      <li key={index}>
                        <strong>{match.productName}</strong> ({formatDate(match.timestamp)}) -
                        Suitable for: <span className="text-green-600">{match.matchedPreference}</span>
                      </li>
                    ))}
                  </ul>
                  {dietaryMatches.length > 3 && (
                    <p className="text-sm text-gray-500 mt-2">
                      And {dietaryMatches.length - 3} more...
                      <button 
                        onClick={() => handleTabChange('history')}
                        className="text-green-600 hover:underline ml-1"
                      >
                        View all
                      </button>
                    </p>
                  )}
                </div>
              )}
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                    Name
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={user.name}
                    onChange={handleChange}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500"
                    placeholder="Enter your name"
                  />
                </div>
                
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={user.email}
                    onChange={handleChange}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500"
                    placeholder="Enter your email"
                  />
                </div>
                
                <div>
                  <label htmlFor="allergies" className="block text-sm font-medium text-gray-700">
                    Allergies (comma separated)
                  </label>
                  <textarea
                    id="allergies"
                    name="allergies"
                    value={user.allergies.join(', ')}
                    onChange={handleAllergiesChange}
                    rows={3}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500"
                    placeholder="Enter your allergies, separated by commas"
                  />
                  <p className="mt-1 text-sm text-gray-500">
                    We'll alert you when scanned products contain these allergens.
                  </p>
                </div>
                
                <div>
                  <label htmlFor="preferences" className="block text-sm font-medium text-gray-700">
                    Dietary Preferences (comma separated)
                  </label>
                  <textarea
                    id="preferences"
                    name="preferences"
                    value={user.dietaryPreferences.join(', ')}
                    onChange={handlePreferencesChange}
                    rows={3}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500"
                    placeholder="Enter your dietary preferences, separated by commas"
                  />
                  <p className="mt-1 text-sm text-gray-500">
                    We'll highlight products that match your dietary preferences.
                  </p>
                </div>
                
                <div>
                  <button
                    type="submit"
                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                  >
                    Save Profile
                  </button>
                </div>
              </form>
            </div>
          ) : (
            // History tab content
            <div>
              <div className="flex items-center mb-6">
                <div className="h-10 w-10 rounded-full bg-green-100 flex items-center justify-center mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h2 className="text-2xl font-bold text-gray-800">Your Scan History</h2>
              </div>
              
              {/* User profile information summary */}
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-6">
                <div className="flex items-start">
                  <div className="mr-4">
                    <div className="h-12 w-12 rounded-full bg-green-100 flex items-center justify-center">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                    </div>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-800">{user.name}</h3>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {user.allergies.length > 0 && (
                        <div className="bg-red-100 px-3 py-1 rounded-full text-xs text-red-700">
                          <span className="font-semibold">Allergies:</span> {user.allergies.join(', ')}
                        </div>
                      )}
                      {user.dietaryPreferences.length > 0 && (
                        <div className="bg-green-100 px-3 py-1 rounded-full text-xs text-green-700">
                          <span className="font-semibold">Diet:</span> {user.dietaryPreferences.join(', ')}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
              
              {children}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserProfile; 