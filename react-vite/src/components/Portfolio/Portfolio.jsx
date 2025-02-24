import { useState, useEffect } from 'react';
import { csrfFetch } from '../../redux/csrf';

function Portfolio() {
  const [positions, setPositions] = useState([]);
  const [totalValue, setTotalValue] = useState(0);

  useEffect(() => {
    async function fetchPortfolio() {
      const response = await csrfFetch('/api/portfolio');
      if (response.ok) {
        const data = await response.json();
        setPositions(data.positions);
        setTotalValue(data.total_value);
      }
    }
    fetchPortfolio();
  }, []);

  return (
    <div className="portfolio">
      <h2>Portfolio (${totalValue.toLocaleString()})</h2>
      <div className="positions-list">
        {positions.map(position => (
          <div key={position.symbol} className="position-item">
            <div className="position-details">
              <h3>{position.symbol}</h3>
              <p>{position.shares} shares</p>
            </div>
            <div className="position-value">
              ${(position.shares * position.current_price).toLocaleString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Portfolio; 