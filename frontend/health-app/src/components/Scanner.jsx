import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Scanner = () => {
  const [imagePreview, setImagePreview] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [showCompareOptions, setShowCompareOptions] = useState(false);
  
  const fileInputRef = useRef(null);
  const navigate = useNavigate();
  
  useEffect(() => {
    const storedImage = sessionStorage.getItem('scannedImage');
    if (storedImage) {
      setImagePreview(storedImage);
      
      fetch(storedImage)
        .then(res => res.blob())
        .then(blob => {
          setImageFile(blob);
        });
      
      sessionStorage.removeItem('scannedImage');
    }
  }, []);
  
  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    setError(null);
    
    if (file) {
      if (!file.type.startsWith('image/')) {
        setError('Please select an image file.');
        return;
      }
      
      setImageFile(file);
      
      const reader = new FileReader();
      reader.onload = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };
  
  const handleCameraClick = () => {
    fileInputRef.current.click();
  };
  
  const handleAnalyze = async () => {
    if (!imagePreview || !imageFile) {
      setError('Please select or take a photo first.');
      return;
    }
    
    setIsAnalyzing(true);
    setError(null);
    
    try {
      // First, analyze the image to get ingredients
      const formData = new FormData();
      formData.append('file', imageFile);
      formData.append('message', 'Analyze these ingredients and provide detailed nutritional information.');
      
      const response = await fetch('http://localhost:8000/api/v1/chat/', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      
      const chatData = await response.json();
      
      // Now get detailed analysis
      const analysisResponse = await fetch('http://localhost:8000/api/v1/analyze/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ingredients: chatData.response,
        }),
      });
      
      if (!analysisResponse.ok) {
        throw new Error('Failed to get detailed analysis');
      }
      
      const analysisData = await analysisResponse.json();
      
      // Combine the data
      const result = {
        productName: analysisData.product_name || 'Analyzed Product',
        ingredients: chatData.response,
        analysis: {
          overview: analysisData.overview || 'No overview available',
          goodIngredients: analysisData.good_ingredients || [],
          cautionaryNotes: analysisData.cautionary_notes || [],
          problematicIngredients: analysisData.problematic_ingredients || [],
          allergenAlerts: analysisData.allergen_alerts || [],
          nutritionOverview: analysisData.nutrition_overview || {
            calories: 'Not available',
            carbohydrates: 'Not available',
            fats: 'Not available',
            proteins: 'Not available',
            sugars: 'Not available',
            sodium: 'Not available'
          },
          healthBenefits: analysisData.health_benefits || [],
          alternatives: analysisData.alternatives?.map(alt => ({
            name: alt.name,
            benefits: alt.benefits
          })) || []
        }
      };
      
      setAnalysisResult(result);
      
      // Save to history
      const historyItem = {
        ...result,
        timestamp: new Date().toISOString()
      };
      
      const existingHistory = JSON.parse(localStorage.getItem('nutriknow_scan_history') || '[]');
      localStorage.setItem('nutriknow_scan_history', JSON.stringify([historyItem, ...existingHistory]));
      
    } catch (err) {
      console.error('Error analyzing image:', err);
      setError('Failed to analyze image. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };
  
  const handleDone = () => {
    navigate('/home');
  };

  const handleCompare = () => {
    setShowCompareOptions(true);
  };
  
  const handleCaptureForComparison = () => {
    sessionStorage.setItem('product_to_compare', JSON.stringify(analysisResult));
    navigate('/scan?mode=compare');
  };
  
  const handleUploadForComparison = () => {
    sessionStorage.setItem('product_to_compare', JSON.stringify(analysisResult));
    fileInputRef.current.click();
  };
  
  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Scan Product</h2>
        
        <input
          type="file"
          accept="image/*"
          className="hidden"
          ref={fileInputRef}
          onChange={handleFileSelect}
        />
        
        {!imagePreview ? (
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center cursor-pointer hover:bg-gray-50" onClick={handleCameraClick}>
            <div className="flex justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <p className="text-gray-600 mb-2">Take a photo or upload image</p>
            <p className="text-gray-400 text-sm">Click to open camera or select file</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="relative">
              <img
                src={imagePreview}
                alt="Preview"
                className="w-full h-auto rounded-lg"
              />
              <button
                onClick={() => {
                  setImagePreview(null);
                  setImageFile(null);
                  setAnalysisResult(null);
                }}
                className="absolute top-2 right-2 bg-white rounded-full p-2 shadow-md hover:bg-gray-100"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
            
            {!analysisResult && (
              <button
                onClick={handleAnalyze}
                disabled={isAnalyzing}
                className={`w-full py-3 rounded-lg font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 ${
                  isAnalyzing
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-green-600 hover:bg-green-700 text-white'
                }`}
              >
                {isAnalyzing ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white mr-2"></div>
                    Analyzing...
                  </div>
                ) : (
                  'Analyze Product'
                )}
              </button>
            )}
          </div>
        )}
        
        {error && (
          <div className="mt-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <p>{error}</p>
          </div>
        )}
        
        {analysisResult && (
          <div className="mt-6 bg-white rounded-xl border border-gray-200 overflow-hidden">
            {/* Product Header */}
            <div className="bg-gray-50 p-4 border-b border-gray-200">
              <h3 className="text-xl font-semibold text-gray-800">{analysisResult.productName}</h3>
              <p className="text-sm text-gray-500 mt-1">{analysisResult.ingredients}</p>
            </div>
            
            {/* Tab Navigation */}
            <div className="flex overflow-x-auto border-b border-gray-200 bg-white scrollbar-hide">
              <button
                onClick={() => setActiveTab('overview')}
                className={`flex-shrink-0 px-4 py-2 text-sm font-medium ${
                  activeTab === 'overview'
                    ? 'border-b-2 border-green-500 text-green-600'
                    : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Overview
              </button>
              <button
                onClick={() => setActiveTab('nutrition')}
                className={`flex-shrink-0 px-4 py-2 text-sm font-medium ${
                  activeTab === 'nutrition'
                    ? 'border-b-2 border-green-500 text-green-600'
                    : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Nutrition
              </button>
              <button
                onClick={() => setActiveTab('allergens')}
                className={`flex-shrink-0 px-4 py-2 text-sm font-medium ${
                  activeTab === 'allergens'
                    ? 'border-b-2 border-red-500 text-red-600'
                    : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Allergens
              </button>
              <button
                onClick={() => setActiveTab('ingredients')}
                className={`flex-shrink-0 px-4 py-2 text-sm font-medium ${
                  activeTab === 'ingredients'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Ingredients
              </button>
              <button
                onClick={() => setActiveTab('alternatives')}
                className={`flex-shrink-0 px-4 py-2 text-sm font-medium ${
                  activeTab === 'alternatives'
                    ? 'border-b-2 border-purple-500 text-purple-600'
                    : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Alternatives
              </button>
            </div>
            
            {/* Tab Content */}
            <div className="p-4">
              {activeTab === 'overview' && (
                <div className="space-y-4">
                  <p className="text-gray-700">{analysisResult.analysis.overview}</p>
                  
                  <div className="grid grid-cols-2 gap-4 mt-4">
                    <div className="bg-green-50 p-3 rounded-lg">
                      <h4 className="text-sm font-medium text-green-700 mb-2">Benefits</h4>
                      <ul className="text-sm text-gray-600 list-disc list-inside">
                        {analysisResult.analysis.healthBenefits.length > 0 ? (
                          analysisResult.analysis.healthBenefits.map((benefit, index) => (
                            <li key={index}>{benefit}</li>
                          ))
                        ) : (
                          <li>No specific benefits identified</li>
                        )}
                      </ul>
                    </div>
                    
                    <div className="bg-yellow-50 p-3 rounded-lg">
                      <h4 className="text-sm font-medium text-yellow-700 mb-2">Cautions</h4>
                      <ul className="text-sm text-gray-600 list-disc list-inside">
                        {analysisResult.analysis.cautionaryNotes.length > 0 ? (
                          analysisResult.analysis.cautionaryNotes.map((note, index) => (
                            <li key={index}>{note}</li>
                          ))
                        ) : (
                          <li>No cautionary notes identified</li>
                        )}
                      </ul>
                    </div>
                  </div>
                </div>
              )}
              
              {activeTab === 'nutrition' && (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {Object.entries(analysisResult.analysis.nutritionOverview).map(([key, value]) => (
                      <div key={key} className="bg-blue-50 p-3 rounded-lg">
                        <h4 className="text-sm font-medium text-blue-700 capitalize">{key}</h4>
                        <p className="text-lg font-semibold text-gray-800">{value}</p>
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-4">
                    <h4 className="text-sm font-medium text-gray-700 mb-2">Health Benefits</h4>
                    <ul className="text-sm text-gray-600 list-disc list-inside">
                      {analysisResult.analysis.healthBenefits.length > 0 ? (
                        analysisResult.analysis.healthBenefits.map((benefit, index) => (
                          <li key={index}>{benefit}</li>
                        ))
                      ) : (
                        <li>No specific health benefits identified</li>
                      )}
                    </ul>
                  </div>
                </div>
              )}
              
              {activeTab === 'allergens' && (
                <div className="space-y-4">
                  {analysisResult.analysis.allergenAlerts.length > 0 ? (
                    <div>
                      <div className="bg-red-50 p-4 rounded-lg mb-4">
                        <div className="flex items-center mb-2">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-red-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                          </svg>
                          <h4 className="text-md font-medium text-red-700">Allergen Alerts</h4>
                        </div>
                        <ul className="text-sm text-gray-700">
                          {analysisResult.analysis.allergenAlerts.map((allergen, index) => (
                            <li key={index} className="py-1 flex items-center">
                              <span className="h-2 w-2 bg-red-500 rounded-full mr-2"></span>
                              {allergen}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <p className="text-sm text-gray-600">
                        Always check the product label for the most accurate and up-to-date allergen information.
                      </p>
                    </div>
                  ) : (
                    <p className="text-gray-700">No allergen alerts detected. However, always check the product packaging for the most accurate information.</p>
                  )}
                </div>
              )}
              
              {activeTab === 'ingredients' && (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-green-50 p-4 rounded-lg">
                      <h4 className="text-md font-medium text-green-700 mb-2">Beneficial Ingredients</h4>
                      <ul className="text-sm text-gray-700">
                        {analysisResult.analysis.goodIngredients.length > 0 ? (
                          analysisResult.analysis.goodIngredients.map((ingredient, index) => (
                            <li key={index} className="py-1 flex items-center">
                              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-green-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                              </svg>
                              {ingredient}
                            </li>
                          ))
                        ) : (
                          <li className="py-1">No beneficial ingredients identified</li>
                        )}
                      </ul>
                    </div>
                    
                    <div className="bg-red-50 p-4 rounded-lg">
                      <h4 className="text-md font-medium text-red-700 mb-2">Problematic Ingredients</h4>
                      <ul className="text-sm text-gray-700">
                        {analysisResult.analysis.problematicIngredients.length > 0 ? (
                          analysisResult.analysis.problematicIngredients.map((ingredient, index) => (
                            <li key={index} className="py-1 flex items-center">
                              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-red-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                              </svg>
                              {ingredient}
                            </li>
                          ))
                        ) : (
                          <li className="py-1">No problematic ingredients identified</li>
                        )}
                      </ul>
                    </div>
                  </div>
                </div>
              )}
              
              {activeTab === 'alternatives' && (
                <div className="space-y-4">
                  <p className="text-gray-600 mb-4">Consider these alternatives that may better match your dietary needs:</p>
                  
                  <div className="space-y-3">
                    {analysisResult.analysis.alternatives.length > 0 ? (
                      analysisResult.analysis.alternatives.map((alt, index) => (
                        <div key={index} className="bg-purple-50 p-4 rounded-lg">
                          <h4 className="text-md font-medium text-purple-700">{alt.name}</h4>
                          <p className="text-sm text-gray-700 mt-1">{alt.benefits}</p>
                        </div>
                      ))
                    ) : (
                      <p className="text-gray-700">No specific alternatives identified for this product.</p>
                    )}
                  </div>
                </div>
              )}
            </div>
            
            {/* Compare Button */}
            <div className="p-4 border-t border-gray-200 flex justify-between items-center">
              <button
                onClick={handleDone}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
              >
                Done
              </button>
              
              {!showCompareOptions ? (
                <button
                  onClick={handleCompare}
                  className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700"
                >
                  Compare with Similar
                </button>
              ) : (
                <div className="flex space-x-2">
                  <button
                    onClick={handleCaptureForComparison}
                    className="px-3 py-2 text-xs font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
                  >
                    Take Photo
                  </button>
                  <button
                    onClick={handleUploadForComparison}
                    className="px-3 py-2 text-xs font-medium text-white bg-purple-600 rounded-md hover:bg-purple-700"
                  >
                    Upload Image
                  </button>
                  <button
                    onClick={() => setShowCompareOptions(false)}
                    className="px-2 py-2 text-xs font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
                  >
                    Cancel
                  </button>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Scanner; 