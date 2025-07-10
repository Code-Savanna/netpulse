import React from 'react';
import './App.css';
import DeviceList from './components/DeviceList';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>NetPulse</h1>
      </header>
      <main>
        <DeviceList />
      </main>
    </div>
  );
}

export default App;
