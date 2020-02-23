import React from 'react';
import './App.css';
import LeftNavi from './Navigation/LeftNavi'
import Home from './Components/Home';

function App() {
  return (
    <div className="App">
      <LeftNavi />
      <Home />
    </div>
  );
}

export default App;
