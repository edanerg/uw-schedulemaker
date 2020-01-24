import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  // Testing connection with backend
  const [backendMessage, setBackendMessage] = useState('');

  useEffect(() => {
    fetch('/courses').then(response => {
      response.json().then(data => {
        const { courses } = data;
        setBackendMessage(courses);
      });
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        {/* ADD stuff here */}
        {`Backend Message: ${backendMessage}`}
      </header>
    </div>
  );
}

export default App;
