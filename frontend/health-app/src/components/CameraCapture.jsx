import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const CameraCapture = ({ setShowCamera }) => {
  const [stream, setStream] = useState(null);
  const [error, setError] = useState(null);
  const [facingMode, setFacingMode] = useState('environment'); // 'environment' is rear camera, 'user' is front camera
  const [isCapturing, setIsCapturing] = useState(false);
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    startCamera();
    
    return () => {
      // Clean up by stopping all tracks when component unmounts
      if (stream) {
        stream.getTracks().forEach(track => {
          track.stop();
        });
      }
    };
  }, [facingMode]);

  const startCamera = async () => {
    setError(null);
    try {
      const constraints = {
        audio: false,
        video: {
          facingMode: facingMode,
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        }
      };
      
      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      setStream(mediaStream);
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      console.error("Error accessing camera:", err);
      setError(`Error accessing camera: ${err.message}`);
    }
  };

  const switchCamera = () => {
    // First stop all tracks
    if (stream) {
      stream.getTracks().forEach(track => {
        track.stop();
      });
    }
    
    // Then toggle the facing mode
    setFacingMode(prevMode => prevMode === 'environment' ? 'user' : 'environment');
  };

  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) return;
    
    setIsCapturing(true);
    
    const video = videoRef.current;
    const canvas = canvasRef.current;
    
    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw the video frame to the canvas
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert canvas to data URL
    const imageDataUrl = canvas.toDataURL('image/jpeg');
    
    // Save to session storage for the Scanner component to use
    sessionStorage.setItem('scannedImage', imageDataUrl);
    
    // Stop all tracks
    if (stream) {
      stream.getTracks().forEach(track => {
        track.stop();
      });
    }
    
    // Hide camera component and navigate to scanner
    setShowCamera(false);
    navigate('/scan');
    
    setIsCapturing(false);
  };

  const handleCancel = () => {
    // Stop all tracks
    if (stream) {
      stream.getTracks().forEach(track => {
        track.stop();
      });
    }
    
    setShowCamera(false);
    navigate('/home');
  };

  return (
    <div className="fixed inset-0 bg-black z-50 flex flex-col">
      <div className="relative flex-grow overflow-hidden">
        {error && (
          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-80 p-4">
            <div className="bg-white p-4 rounded-lg max-w-md">
              <h3 className="text-red-600 font-semibold mb-2">Camera Error</h3>
              <p className="text-gray-800">{error}</p>
              <button 
                onClick={handleCancel}
                className="mt-4 w-full px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
              >
                Close
              </button>
            </div>
          </div>
        )}
        
        <video
          ref={videoRef}
          autoPlay
          playsInline
          className="h-full w-full object-cover"
        />
        
        <canvas ref={canvasRef} className="hidden" />
        
        {/* Capture UI Overlay */}
        <div className="absolute bottom-0 inset-x-0 p-4 bg-gradient-to-t from-black to-transparent">
          <div className="flex items-center justify-between">
            <button
              onClick={handleCancel}
              className="p-2 bg-white bg-opacity-20 rounded-full text-white hover:bg-opacity-30 transition-all"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            
            <button
              onClick={capturePhoto}
              disabled={isCapturing || error}
              className={`p-1 bg-white rounded-full ${isCapturing ? 'opacity-50' : 'hover:opacity-80'} transition-all`}
            >
              <div className="h-16 w-16 border-4 border-gray-800 rounded-full"></div>
            </button>
            
            <button
              onClick={switchCamera}
              disabled={isCapturing || error}
              className="p-2 bg-white bg-opacity-20 rounded-full text-white hover:bg-opacity-30 transition-all"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
          </div>
        </div>
        
        {/* Camera Frame Guide */}
        <div className="absolute inset-0 border-[40px] border-black border-opacity-50 pointer-events-none">
          <div className="h-full w-full border-2 border-white border-opacity-70 rounded-lg"></div>
        </div>
        
        {/* Header Instructions */}
        <div className="absolute top-0 inset-x-0 p-4 bg-gradient-to-b from-black to-transparent">
          <h2 className="text-white text-center text-lg font-semibold">
            Position product label in frame
          </h2>
          <p className="text-white text-center text-sm opacity-80">
            Make sure text is clearly visible
          </p>
        </div>
      </div>
    </div>
  );
};

export default CameraCapture; 