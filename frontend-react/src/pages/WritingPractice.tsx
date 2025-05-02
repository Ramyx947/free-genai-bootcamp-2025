import { useEffect } from 'react';

export const WritingPractice = () => {
  useEffect(() => {
    // Redirect to the Streamlit app
    window.location.href = 'http://localhost:7860';
  }, []);

  return (
    <div className="flex items-center justify-center h-screen">
      <p>Redirecting to Writing Practice...</p>
    </div>
  );
}; 