import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { getWatchlists, removeSymbolFromWatchlist } from '../../redux/watchlist';
import { FaTrash } from 'react-icons/fa';
import OpenModalButton from '../OpenModalButton/OpenModalButton';
import ConfirmModal from '../Modals/ConfirmModal';
import './Watchlists.css';

function Watchlists({ onSelectStock }) {
  const dispatch = useDispatch();
  const watchlists = useSelector(state => state.watchlist.watchlists);
  const [isLoading, setIsLoading] = useState(true);
  const [activeWatchlist, setActiveWatchlist] = useState(null);
  const [showMenu, setShowMenu] = useState(false);

  useEffect(() => {
    const loadWatchlists = async () => {
      try {
        await dispatch(getWatchlists());
        setIsLoading(false);
      } catch (error) {
        console.error('Error loading watchlists:', error);
        setIsLoading(false);
      }
    };

    loadWatchlists();
  }, [dispatch]);

  useEffect(() => {
    if (watchlists.length > 0 && !activeWatchlist) {
      setActiveWatchlist(watchlists[0].id);
    }
  }, [watchlists, activeWatchlist]);

  const closeMenu = () => setShowMenu(false);

  const handleRemoveSymbol = async (watchlistId, symbol) => {
    try {
      const success = await dispatch(removeSymbolFromWatchlist(watchlistId, symbol));
      
      if (success) {
        // Refresh watchlists after successful removal
        await dispatch(getWatchlists());
      } else {
        console.error('Failed to remove symbol from watchlist');
        // You could add a toast notification here
      }
    } catch (error) {
      console.error('Error removing symbol:', error);
      // You could add a toast notification here
    }
    closeMenu();
  };

  if (isLoading) return <div className="loading">Loading watchlists...</div>;

  const activeList = watchlists.find(list => list.id === activeWatchlist);

  return (
    <div className="watchlists-container">
      <div className="watchlists-header">
        <h2>Watchlists</h2>
      </div>

      {watchlists.length === 0 ? (
        <div className="no-watchlists">
          <p>No watchlists yet.</p>
          <button className="create-watchlist-btn">Create Watchlist</button>
        </div>
      ) : (
        <>
          <div className="watchlist-tabs">
            {watchlists.map(list => (
              <button
                key={list.id}
                className={`watchlist-tab ${activeWatchlist === list.id ? 'active' : ''}`}
                onClick={() => setActiveWatchlist(list.id)}
              >
                {list.name}
                <span className="symbol-count">({list.symbols.length})</span>
              </button>
            ))}
          </div>

          <div className="watchlist-content">
            {activeList?.symbols.map(symbol => (
              <div 
                key={symbol.id} 
                className="stock-item"
              >
                <div 
                  className="stock-info"
                  onClick={() => onSelectStock(symbol)}
                >
                  <div className="company-name">{symbol.company_name}</div>
                  <div className="stock-symbol">{symbol.symbol}</div>
                  
                </div>
                <div className="stock-actions">
                  <div className="stock-price">
                    <div className="current-price">${symbol.current_price?.toFixed(2) || 'N/A'}</div>
                    {symbol.price_change && (
                      <div className={`price-change ${symbol.price_change >= 0 ? 'gain' : 'loss'}`}>
                        {symbol.price_change >= 0 ? '+' : ''}{symbol.price_change.toFixed(2)}%
                      </div>
                    )}
                  </div>
                  <OpenModalButton
                    buttonText={<FaTrash />}
                    className="remove-symbol-btn"
                    modalComponent={
                      <ConfirmModal
                        message={`Remove ${symbol.symbol} from watchlist?`}
                        onConfirm={() => handleRemoveSymbol(activeWatchlist, symbol.symbol)}
                      />
                    }
                  />
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default Watchlists; 