import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchAllSymbols } from '../../redux/symbols';
import { useNavigate } from 'react-router-dom';
import './StockTicker.css';

function StockTicker() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const symbols = useSelector(state => state.symbols.allSymbolsList || []);
  const error = useSelector(state => state.symbols.allSymbolsError);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadSymbols = async () => {
      await dispatch(fetchAllSymbols());
      setIsLoading(false);
    };

    loadSymbols();
    
    // Refresh prices every minute
    const refreshInterval = setInterval(() => {
      dispatch(fetchAllSymbols());
    }, 60000);
    
    return () => clearInterval(refreshInterval);
  }, [dispatch]);

  const handleSymbolClick = (symbol) => {
    navigate(`/symbols/${symbol}`);
  };

  if (isLoading) return <div className="ticker-loading">Loading market data...</div>;
  if (error) return <div className="ticker-error">Error loading market data</div>;
  if (!symbols || symbols.length === 0) return <div className="ticker-empty">No market data available</div>;

  return (
    <div className="ticker-container">
      <div className="ticker-wrapper">
        <div className="ticker-track">
          {symbols.map((symbol, index) => (
            <div 
              key={`${symbol.symbol}-${index}`} 
              className="ticker-item"
              onClick={() => handleSymbolClick(symbol.symbol)}
            >
              <span className="ticker-symbol">{symbol.symbol}</span>
              <span className="ticker-price">${symbol.current_price?.toFixed(2) || 'N/A'}</span>
              {symbol.price_change_pct !== null && (
                <span className={`ticker-change ${parseFloat(symbol.price_change_pct) >= 0 ? 'gain' : 'loss'}`}>
                  {parseFloat(symbol.price_change_pct) >= 0 ? '+' : ''}{parseFloat(symbol.price_change_pct).toFixed(2)}%
                </span>
              )}
            </div>
          ))}
          {/* Duplicate items to create seamless loop */}
          {symbols.map((symbol, index) => (
            <div 
              key={`${symbol.symbol}-dup-${index}`} 
              className="ticker-item"
              onClick={() => handleSymbolClick(symbol.symbol)}
            >
              <span className="ticker-symbol">{symbol.symbol}</span>
              <span className="ticker-price">${symbol.current_price?.toFixed(2) || 'N/A'}</span>
              {symbol.price_change_pct !== null && (
                <span className={`ticker-change ${parseFloat(symbol.price_change_pct) >= 0 ? 'gain' : 'loss'}`}>
                  {parseFloat(symbol.price_change_pct) >= 0 ? '+' : ''}{parseFloat(symbol.price_change_pct).toFixed(2)}%
                </span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default StockTicker; 