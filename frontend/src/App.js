import React, { useState } from 'react';

function App() {
  const [randomNumber, setRandomNumber] = useState(null);

  const handleButtonClick = () => {
    fetch('http://127.0.0.1:8000/api/random-number')
      .then(response => response.json())
      .then(data => setRandomNumber(data.random_number));
  };

  return (
    <div>
      <button onClick={handleButtonClick}>Get Random Number</button>
      {randomNumber !== null && <p>Random Number: {randomNumber}</p>}
    </div>
  );
}

export default App;
