import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { getWatchlists, removeSymbolFromWatchlist, updateWatchlistName, deleteWatchlist } from '../../redux/watchlist';
import { FaTrash, FaEdit, FaCheck, FaTimes, FaChevronDown, FaChevronUp } from 'react-icons/fa';
import OpenModalButton from '../OpenModalButton/OpenModalButton';
import ConfirmModal from '../Modals/ConfirmModal';
import './Watchlists.css';

function Watchlists({ onSelectStock: handleStockClick }) {
  const dispatch = useDispatch();
  const watchlists = useSelector(state => state.watchlist.watchlists);
  const [isLoading, setIsLoading] = useState(true);
  const [activeWatchlist, setActiveWatchlist] = useState(null);
  const [showMenu, setShowMenu] = useState(false);
  const [editingWatchlist, setEditingWatchlist] = useState(null);
  const [editName, setEditName] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [expandedWatchlists, setExpandedWatchlists] = useState({});

  useEffect(() => {
    const loadWatchlists = async () => {
        await dispatch(getWatchlists());
        setIsLoading(false);
    };

    loadWatchlists();
  }, [dispatch]);

  useEffect(() => {
    if (watchlists.length > 0 && !activeWatchlist) {
      setActiveWatchlist(watchlists[0].id);
      // Initialize expanded state for the first watchlist
      setExpandedWatchlists({ [watchlists[0].id]: true });
    }
  }, [watchlists, activeWatchlist]);

  const closeMenu = () => setShowMenu(false);

  const handleRemoveSymbol = async (watchlistId, symbol) => {
      const success = await dispatch(removeSymbolFromWatchlist(watchlistId, symbol));
      
      if (success) {
        await dispatch(getWatchlists());
      } else {
        console.error('Failed to remove symbol from watchlist');
      }
    closeMenu();
  };

  const startEditing = (watchlist) => {
    setEditingWatchlist(watchlist.id);
    setEditName(watchlist.name);
  };

  const cancelEditing = () => {
    setEditingWatchlist(null);
    setEditName('');
  };

  const handleUpdateName = async (watchlistId) => {
    if (!editName.trim()) {
      alert('Watchlist name cannot be empty');
      return;
    }

    setIsSubmitting(true);
    const result = await dispatch(updateWatchlistName(watchlistId, editName.trim()));
    setIsSubmitting(false);
    
    if (result.success) {
      setEditingWatchlist(null);
      setEditName('');
      setError('');
    } else {
      setError(result.errors || 'Failed to update watchlist name');
    }
  };

  const handleDeleteWatchlist = async (watchlistId) => {
    setIsSubmitting(true);
    try {
      const result = await dispatch(deleteWatchlist(watchlistId));
      if (result.success) {
        if (activeWatchlist === watchlistId && watchlists.length > 1) {
          // Set active watchlist to the first available one that's not being deleted
          const nextWatchlist = watchlists.find(w => w.id !== watchlistId);
          if (nextWatchlist) {
            setActiveWatchlist(nextWatchlist.id);
            setExpandedWatchlists({ [nextWatchlist.id]: true });
          }
        }
        setError('');
      } else {
        setError(result.errors || 'Failed to delete watchlist');
      }
    } catch (err) {
      setError('Failed to delete watchlist');
    } finally {
      setIsSubmitting(false);
    }
  };

  const toggleWatchlist = (watchlistId) => {
    setExpandedWatchlists(prev => ({
      ...prev,
      [watchlistId]: !prev[watchlistId]
    }));
    setActiveWatchlist(watchlistId);
  };

  if (isLoading) return <div className="loading">Loading watchlists...</div>;

  return (
    <div className="watchlists-container">
      <div className="watchlists-header">
        <h2>Watchlists</h2>
        {error && <div className="error-message">{error}</div>}
      </div>

      {watchlists.length === 0 ? (
        <div className="no-watchlists">
          <p>No watchlists yet.</p>
          <button className="create-watchlist-btn">Create Watchlist</button>
        </div>
      ) : (
        <div className="watchlists-nested">
          {watchlists.map(list => (
            <div key={list.id} className="watchlist-item">
              {editingWatchlist === list.id ? (
                <div className="watchlist-edit-container">
                  <input
                    type="text"
                    value={editName}
                    onChange={(e) => setEditName(e.target.value)}
                    className="watchlist-name-input"
                    autoFocus
                  />
                  <div className="edit-actions">
                    <button
                      onClick={() => handleUpdateName(list.id)}
                      className="edit-action-btn save"
                      disabled={isSubmitting}
                    >
                      <FaCheck />
                    </button>
                    <button
                      onClick={cancelEditing}
                      className="edit-action-btn cancel"
                      disabled={isSubmitting}
                    >
                      <FaTimes />
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <div className="watchlist-header">
                    <button
                      className={`watchlist-toggle ${expandedWatchlists[list.id] ? 'expanded' : ''}`}
                      onClick={() => toggleWatchlist(list.id)}
                    >
                      {expandedWatchlists[list.id] ? <FaChevronUp /> : <FaChevronDown />}
                      <span className="watchlist-name">{list.name}</span>
                      <span className="symbol-count">({list.symbols.length})</span>
                    </button>
                    <div className="watchlist-actions">
                      <button
                        className="edit-watchlist-btn"
                        onClick={() => startEditing(list)}
                        disabled={isSubmitting}
                      >
                        <FaEdit />
                      </button>
                      <OpenModalButton
                        buttonText={<FaTrash />}
                        className="delete-watchlist-btn"
                        modalComponent={
                          <ConfirmModal
                            message={`Delete watchlist "${list.name}"? This action cannot be undone.`}
                            onConfirm={() => handleDeleteWatchlist(list.id)}
                          />
                        }
                      />
                    </div>
                  </div>
                  {expandedWatchlists[list.id] && (
                    <div className="watchlist-content">
                      {list.symbols.map(symbol => (
                        <div 
                          key={symbol.id} 
                          className="stock-item"
                        >
                          <div 
                            className="stock-info"
                            onClick={() => handleStockClick(symbol)}
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
                                  onConfirm={() => handleRemoveSymbol(list.id, symbol.symbol)}
                                />
                              }
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Watchlists; 