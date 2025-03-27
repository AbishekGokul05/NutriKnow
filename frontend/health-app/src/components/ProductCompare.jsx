import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const ProductCompare = () => {
  const [product1, setProduct1] = useState(null);
  const [product2, setProduct2] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [comparison, setComparison] = useState(null);
  
  const fileInputRef = useRef(null);
  const navigate = useNavigate();
  const location = useLocation();
  
  useEffect(() => {
    // Load first product from session storage if available
    const storedProduct = sessionStorage.getItem('product_to_compare');
    if (storedProduct) {
      try {
        const parsedProduct = JSON.parse(storedProduct);
        setProduct1(parsedProduct);
      } catch (err) {
        console.error('Error parsing stored product:', err);
        setError('Failed to load product data for comparison.');
      }
    }
    
    // If there's a second product in query params or state, load it
    const queryParams = new URLSearchParams(location.search);
    const secondProductId = queryParams.get('product2');
    
    if (secondProductId) {
      // Fetch second product data
      fetchProductData(secondProductId);
    }
  }, [location]);

  const compareProducts = async (product1Data, product2Data) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/compare/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          product1: product1Data.ingredients,
          product2: product2Data.ingredients,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to compare products');
      }

      const comparisonData = await response.json();
      setComparison(comparisonData);
    } catch (err) {
      console.error('Error comparing products:', err);
      setError('Failed to compare products. Please try again.');
    }
  };
  
  const fetchProductData = async (productId) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`http://localhost:8000/api/v1/products/${productId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch product data');
      }
      
      const productData = await response.json();
      setProduct2(productData);
      
      if (product1) {
        await compareProducts(product1, productData);
      }
    } catch (err) {
      console.error('Error fetching product data:', err);
      setError('Failed to load comparison product data.');
    } finally {
      setLoading(false);
    }
  };
  
  const handleAddSecondProduct = () => {
    fileInputRef.current.click();
  };
  
  const handleFileSelect = async (event) => {
    const file = event.target.files[0];
    setError(null);
    
    if (file) {
      if (!file.type.startsWith('image/')) {
        setError('Please select an image file.');
        return;
      }
      
      setLoading(true);
      
      try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('http://localhost:8000/api/v1/analyze/', {
          method: 'POST',
          body: formData,
        });
        
        if (!response.ok) {
          throw new Error('Failed to analyze product');
        }
        
        const productData = await response.json();
        setProduct2(productData);
        
        if (product1) {
          await compareProducts(product1, productData);
        }
      } catch (err) {
        console.error('Error analyzing product:', err);
        setError('Failed to analyze product. Please try again.');
      } finally {
        setLoading(false);
      }
    }
  };
  
  if (!product1) {
    return (
      <div className="max-w-4xl mx-auto p-4">
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Product Comparison</h2>
          <div className="text-center py-8">
            <p className="text-gray-500 text-lg mb-4">No product selected for comparison.</p>
            <button
              onClick={() => navigate('/scan')}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Scan a Product First
            </button>
          </div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="max-w-7xl mx-auto p-4">
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Product Comparison</h2>
        
        <input
          type="file"
          accept="image/*"
          className="hidden"
          ref={fileInputRef}
          onChange={handleFileSelect}
        />
        
        {error && (
          <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <p>{error}</p>
          </div>
        )}
        
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-500"></div>
          </div>
        ) : (
          <div>
            {/* Comparison Header */}
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="text-xl font-semibold text-gray-800">{product1.productName}</h3>
                <p className="text-sm text-gray-500 mt-1 line-clamp-2">{product1.ingredients}</p>
              </div>
              
              {product2 ? (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h3 className="text-xl font-semibold text-gray-800">{product2.productName}</h3>
                  <p className="text-sm text-gray-500 mt-1 line-clamp-2">{product2.ingredients}</p>
                </div>
              ) : (
                <div 
                  className="bg-gray-50 p-4 rounded-lg border-2 border-dashed border-gray-300 flex flex-col items-center justify-center cursor-pointer hover:bg-gray-100"
                  onClick={handleAddSecondProduct}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  <p className="text-gray-500">Add second product for comparison</p>
                </div>
              )}
            </div>
            
            {/* Tab Navigation */}
            <div className="flex overflow-x-auto border-b border-gray-200 bg-white mb-4 scrollbar-hide">
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
            </div>
            
            {/* Comparison Content */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Product 1 */}
              <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                {activeTab === 'overview' && (
                  <div className="p-4">
                    <p className="text-gray-700 mb-4">{product1.analysis?.overview || 'No overview available.'}</p>
                    <div className="bg-green-50 p-3 rounded-lg">
                      <h4 className="text-sm font-medium text-green-700 mb-2">Benefits</h4>
                      <ul className="text-sm text-gray-600 list-disc list-inside">
                        {product1.analysis?.healthBenefits?.map((benefit, index) => (
                          <li key={index}>{benefit}</li>
                        )) || <li>No benefits information available.</li>}
                      </ul>
                    </div>
                  </div>
                )}
                
                {activeTab === 'nutrition' && (
                  <div className="p-4">
                    <div className="grid grid-cols-2 gap-2">
                      {product1.analysis?.nutritionOverview ? (
                        Object.entries(product1.analysis.nutritionOverview).map(([key, value]) => (
                          <div key={key} className="bg-blue-50 p-2 rounded-lg">
                            <h4 className="text-xs font-medium text-blue-700 capitalize">{key}</h4>
                            <p className="text-sm font-semibold text-gray-800">{value}</p>
                          </div>
                        ))
                      ) : (
                        <p className="text-gray-700 col-span-2">No nutritional information available.</p>
                      )}
                    </div>
                  </div>
                )}
                
                {activeTab === 'allergens' && (
                  <div className="p-4">
                    {product1.analysis?.allergenAlerts?.length > 0 ? (
                      <div className="bg-red-50 p-3 rounded-lg">
                        <h4 className="text-sm font-medium text-red-700 mb-2">Allergen Alerts</h4>
                        <ul className="text-sm text-gray-700">
                          {product1.analysis.allergenAlerts.map((allergen, index) => (
                            <li key={index} className="py-1 flex items-center">
                              <span className="h-2 w-2 bg-red-500 rounded-full mr-2"></span>
                              {allergen}
                            </li>
                          ))}
                        </ul>
                      </div>
                    ) : (
                      <p className="text-gray-700">No allergen alerts detected.</p>
                    )}
                  </div>
                )}
                
                {activeTab === 'ingredients' && (
                  <div className="p-4">
                    <div className="space-y-3">
                      <div>
                        <h4 className="text-sm font-medium text-green-700 mb-1">Good Ingredients</h4>
                        <p className="text-sm text-gray-700">
                          {product1.analysis?.goodIngredients?.join(', ') || 'No good ingredients identified.'}
                        </p>
                      </div>
                      <div>
                        <h4 className="text-sm font-medium text-yellow-700 mb-1">Cautions</h4>
                        <p className="text-sm text-gray-700">
                          {product1.analysis?.cautionaryNotes?.join(', ') || 'No cautionary notes.'}
                        </p>
                      </div>
                      <div>
                        <h4 className="text-sm font-medium text-red-700 mb-1">Problematic</h4>
                        <p className="text-sm text-gray-700">
                          {product1.analysis?.problematicIngredients?.length > 0 
                            ? product1.analysis.problematicIngredients.join(', ') 
                            : 'None detected'}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
              
              {/* Product 2 */}
              {product2 ? (
                <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                  {activeTab === 'overview' && (
                    <div className="p-4">
                      <p className="text-gray-700 mb-4">{product2.analysis?.overview || 'No overview available.'}</p>
                      <div className="bg-green-50 p-3 rounded-lg">
                        <h4 className="text-sm font-medium text-green-700 mb-2">Benefits</h4>
                        <ul className="text-sm text-gray-600 list-disc list-inside">
                          {product2.analysis?.healthBenefits?.map((benefit, index) => (
                            <li key={index}>{benefit}</li>
                          )) || <li>No benefits information available.</li>}
                        </ul>
                      </div>
                    </div>
                  )}
                  
                  {activeTab === 'nutrition' && (
                    <div className="p-4">
                      <div className="grid grid-cols-2 gap-2">
                        {product2.analysis?.nutritionOverview ? (
                          Object.entries(product2.analysis.nutritionOverview).map(([key, value]) => (
                            <div key={key} className="bg-blue-50 p-2 rounded-lg">
                              <h4 className="text-xs font-medium text-blue-700 capitalize">{key}</h4>
                              <p className="text-sm font-semibold text-gray-800">{value}</p>
                            </div>
                          ))
                        ) : (
                          <p className="text-gray-700 col-span-2">No nutritional information available.</p>
                        )}
                      </div>
                    </div>
                  )}
                  
                  {activeTab === 'allergens' && (
                    <div className="p-4">
                      {product2.analysis?.allergenAlerts?.length > 0 ? (
                        <div className="bg-red-50 p-3 rounded-lg">
                          <h4 className="text-sm font-medium text-red-700 mb-2">Allergen Alerts</h4>
                          <ul className="text-sm text-gray-700">
                            {product2.analysis.allergenAlerts.map((allergen, index) => (
                              <li key={index} className="py-1 flex items-center">
                                <span className="h-2 w-2 bg-red-500 rounded-full mr-2"></span>
                                {allergen}
                              </li>
                            ))}
                          </ul>
                        </div>
                      ) : (
                        <p className="text-gray-700">No allergen alerts detected.</p>
                      )}
                    </div>
                  )}
                  
                  {activeTab === 'ingredients' && (
                    <div className="p-4">
                      <div className="space-y-3">
                        <div>
                          <h4 className="text-sm font-medium text-green-700 mb-1">Good Ingredients</h4>
                          <p className="text-sm text-gray-700">
                            {product2.analysis?.goodIngredients?.join(', ') || 'No good ingredients identified.'}
                          </p>
                        </div>
                        <div>
                          <h4 className="text-sm font-medium text-yellow-700 mb-1">Cautions</h4>
                          <p className="text-sm text-gray-700">
                            {product2.analysis?.cautionaryNotes?.join(', ') || 'No cautionary notes.'}
                          </p>
                        </div>
                        <div>
                          <h4 className="text-sm font-medium text-red-700 mb-1">Problematic</h4>
                          <p className="text-sm text-gray-700">
                            {product2.analysis?.problematicIngredients?.length > 0 
                              ? product2.analysis.problematicIngredients.join(', ') 
                              : 'None detected'}
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div 
                  className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center cursor-pointer hover:bg-gray-50"
                  onClick={handleAddSecondProduct}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  <p className="text-gray-600 mb-2">Add Second Product</p>
                  <p className="text-gray-400 text-sm">Take a photo or upload image to compare</p>
                </div>
              )}
            </div>
            
            {/* Summary and Recommendation (when two products are compared) */}
            {product1 && product2 && comparison && (
              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <h3 className="text-lg font-semibold text-blue-800 mb-2">Comparison Summary</h3>
                <p className="text-gray-700 mb-3">{comparison.insights}</p>
                <div className="space-y-4">
                  <div>
                    <h4 className="text-sm font-medium text-blue-700">Better Product</h4>
                    <p className="text-gray-700">{comparison.better_product}</p>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-yellow-700">Product 1 Considerations</h4>
                    <ul className="list-disc list-inside text-gray-700 text-sm">
                      {comparison.drawbacks_1?.map((drawback, index) => (
                        <li key={index}>{drawback}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-yellow-700">Product 2 Considerations</h4>
                    <ul className="list-disc list-inside text-gray-700 text-sm">
                      {comparison.drawbacks_2?.map((drawback, index) => (
                        <li key={index}>{drawback}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}
            
            {/* Actions */}
            <div className="mt-6 flex justify-between">
              <button
                onClick={() => navigate('/home')}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
              >
                Back to Home
              </button>
              
              {!product2 && (
                <button
                  onClick={handleAddSecondProduct}
                  className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700"
                >
                  Add Second Product
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductCompare; 