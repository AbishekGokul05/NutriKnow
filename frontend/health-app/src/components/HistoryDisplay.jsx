import React, { useState, useEffect } from 'react';

const STORAGE_KEY = 'nutriknow_scan_history';

const HistoryDisplay = () => {
  const [history, setHistory] = useState(() => {
    // Load history from local storage on component mount
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  });
  const [userProfile, setUserProfile] = useState({
    allergies: [],
    dietaryPreferences: []
  });
  const [activeFilter, setActiveFilter] = useState('all');
  const [filteredHistory, setFilteredHistory] = useState([]);

  // Save history to local storage whenever it changes
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
  }, [history]);
  
  // Load user profile for filtering
  useEffect(() => {
    const savedProfile = localStorage.getItem('nutriknow_user_profile');
    if (savedProfile) {
      setUserProfile(JSON.parse(savedProfile));
    }
  }, []);
  
  // Apply filters when user profile or active filter changes
  useEffect(() => {
    filterHistory(activeFilter);
  }, [activeFilter, userProfile, history]);

  const clearHistory = () => {
    setHistory([]);
    localStorage.removeItem(STORAGE_KEY);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };
  
  const filterHistory = (filter) => {
    switch(filter) {
      case 'allergens':
        if (!userProfile.allergies.length) {
          setFilteredHistory([]);
        } else {
          const allergyFiltered = history.filter(item => 
            item.analysis && 
            item.analysis.allergenAlerts && 
            item.analysis.allergenAlerts.some(alert => 
              userProfile.allergies.some(allergen => 
                alert.toLowerCase().includes(allergen.toLowerCase())
              )
            )
          );
          setFilteredHistory(allergyFiltered);
        }
        break;
        
      case 'diet':
        if (!userProfile.dietaryPreferences.length) {
          setFilteredHistory([]);
        } else {
          const dietaryFiltered = history.filter(item => 
            item.analysis && 
            item.analysis.goodIngredients &&
            userProfile.dietaryPreferences.some(pref => {
              // Simple diet matching logic
              if (pref.toLowerCase() === 'vegetarian') {
                return !item.analysis.cautionaryNotes?.some(note => 
                  note.toLowerCase().includes('meat') || 
                  note.toLowerCase().includes('animal')
                );
              }
              if (pref.toLowerCase() === 'vegan') {
                return !item.analysis.cautionaryNotes?.some(note => 
                  note.toLowerCase().includes('dairy') || 
                  note.toLowerCase().includes('animal') ||
                  note.toLowerCase().includes('egg')
                );
              }
              if (pref.toLowerCase().includes('low-carb')) {
                return item.analysis.nutritionOverview?.carbohydrates === 'low';
              }
              return false;
            })
          );
          setFilteredHistory(dietaryFiltered);
        }
        break;
        
      case 'recent':
        // Get items from the last 7 days
        const sevenDaysAgo = new Date();
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
        const recentItems = history.filter(item => 
          new Date(item.timestamp) > sevenDaysAgo
        );
        setFilteredHistory(recentItems);
        break;
        
      case 'all':
      default:
        setFilteredHistory(history);
        break;
    }
  };
  
  const displayItems = activeFilter === 'all' ? history : filteredHistory;
  
  // Calculate stats based on history
  const totalScans = history.length;
  const allergenMatches = userProfile.allergies.length ? 
    history.filter(item => 
      item.analysis && 
      item.analysis.allergenAlerts && 
      item.analysis.allergenAlerts.some(alert => 
        userProfile.allergies.some(allergen => 
          alert.toLowerCase().includes(allergen.toLowerCase())
        )
      )
    ).length : 0;
  
  const dietaryMatches = userProfile.dietaryPreferences.length ?
    history.filter(item => 
      item.analysis && 
      item.analysis.goodIngredients &&
      userProfile.dietaryPreferences.some(pref => {
        if (pref.toLowerCase() === 'vegetarian') {
          return !item.analysis.cautionaryNotes?.some(note => 
            note.toLowerCase().includes('meat') || 
            note.toLowerCase().includes('animal')
          );
        }
        if (pref.toLowerCase() === 'vegan') {
          return !item.analysis.cautionaryNotes?.some(note => 
            note.toLowerCase().includes('dairy') || 
            note.toLowerCase().includes('animal') ||
            note.toLowerCase().includes('egg')
          );
        }
        if (pref.toLowerCase().includes('low-carb')) {
          return item.analysis.nutritionOverview?.carbohydrates === 'low';
        }
        return false;
      })
    ).length : 0;

  return (
    <div className="max-w-4xl mx-auto">
      {/* Stats section */}
      {history.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-lg shadow-sm p-4 text-center border-l-4 border-blue-500">
            <p className="text-gray-500 text-sm">Total Scans</p>
            <p className="text-3xl font-bold text-blue-600">{totalScans}</p>
          </div>
          
          {userProfile.allergies.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm p-4 text-center border-l-4 border-red-500">
              <p className="text-gray-500 text-sm">Allergen Alerts</p>
              <p className="text-3xl font-bold text-red-600">{allergenMatches}</p>
            </div>
          )}
          
          {userProfile.dietaryPreferences.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm p-4 text-center border-l-4 border-green-500">
              <p className="text-gray-500 text-sm">Diet Matches</p>
              <p className="text-3xl font-bold text-green-600">{dietaryMatches}</p>
            </div>
          )}
        </div>
      )}
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex flex-col sm:flex-row justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4 sm:mb-0">Scan History</h2>
          <div className="flex flex-wrap gap-2">
            {history.length > 0 && (
              <>
                <div className="inline-flex rounded-md shadow-sm" role="group">
                  <button
                    onClick={() => setActiveFilter('all')}
                    className={`px-4 py-2 text-sm font-medium rounded-l-lg ${
                      activeFilter === 'all'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
                    }`}
                  >
                    All
                  </button>
                  <button
                    onClick={() => setActiveFilter('recent')}
                    className={`px-4 py-2 text-sm font-medium ${
                      activeFilter === 'recent'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white text-gray-700 hover:bg-gray-100 border-t border-b border-gray-300'
                    }`}
                  >
                    Recent
                  </button>
                  {userProfile.allergies.length > 0 && (
                    <button
                      onClick={() => setActiveFilter('allergens')}
                      className={`px-4 py-2 text-sm font-medium ${
                        activeFilter === 'allergens'
                          ? 'bg-red-600 text-white'
                          : 'bg-white text-gray-700 hover:bg-gray-100 border-t border-b border-gray-300'
                      }`}
                    >
                      Allergens
                    </button>
                  )}
                  {userProfile.dietaryPreferences.length > 0 && (
                    <button
                      onClick={() => setActiveFilter('diet')}
                      className={`px-4 py-2 text-sm font-medium rounded-r-lg ${
                        activeFilter === 'diet'
                          ? 'bg-green-600 text-white'
                          : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
                      }`}
                    >
                      Diet
                    </button>
                  )}
                </div>
                
                <button
                  onClick={clearHistory}
                  className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 ml-2"
                >
                  Clear
                </button>
              </>
            )}
          </div>
        </div>

        {history.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500 text-lg">No scan history yet.</p>
            <p className="text-gray-400">Your scanned products will appear here.</p>
          </div>
        ) : displayItems.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500 text-lg">No items match your selected filter.</p>
            <button 
              onClick={() => setActiveFilter('all')}
              className="mt-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Show All Items
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {displayItems.map((item, index) => (
              <div
                key={index}
                className={`border rounded-lg p-4 hover:bg-gray-50 transition-colors ${
                  userProfile.allergies.length > 0 && 
                  item.analysis?.allergenAlerts?.some(alert => 
                    userProfile.allergies.some(allergen => 
                      alert.toLowerCase().includes(allergen.toLowerCase())
                    )
                  ) ? 'border-red-300 bg-red-50 hover:bg-red-100' : 'border-gray-200'
                }`}
              >
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-semibold text-gray-800">
                    {item.productName || 'Unknown Product'}
                  </h3>
                  <span className="text-sm text-gray-500">
                    {formatDate(item.timestamp)}
                  </span>
                </div>

                {item.analysis && (
                  <div className="space-y-2">
                    {item.analysis.goodIngredients && item.analysis.goodIngredients.length > 0 && (
                      <div>
                        <p className="text-sm font-medium text-green-600">Good Ingredients:</p>
                        <p className="text-sm text-gray-600">
                          {item.analysis.goodIngredients.join(', ')}
                        </p>
                      </div>
                    )}

                    {item.analysis.cautionaryNotes && item.analysis.cautionaryNotes.length > 0 && (
                      <div>
                        <p className="text-sm font-medium text-yellow-600">Cautions:</p>
                        <p className="text-sm text-gray-600">
                          {item.analysis.cautionaryNotes.join(', ')}
                        </p>
                      </div>
                    )}

                    {item.analysis.allergenAlerts && item.analysis.allergenAlerts.length > 0 && (
                      <div>
                        <p className="text-sm font-medium text-red-600">Allergen Alerts:</p>
                        <p className="text-sm text-gray-600">
                          {userProfile.allergies.length > 0 ? (
                            <span>
                              {item.analysis.allergenAlerts.map((alert, i) => (
                                <span key={i} className={`${
                                  userProfile.allergies.some(allergen => 
                                    alert.toLowerCase().includes(allergen.toLowerCase())
                                  ) ? 'text-red-600 font-semibold' : ''
                                }`}>
                                  {alert}{i < item.analysis.allergenAlerts.length - 1 ? ', ' : ''}
                                </span>
                              ))}
                            </span>
                          ) : (
                            item.analysis.allergenAlerts.join(', ')
                          )}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryDisplay; 