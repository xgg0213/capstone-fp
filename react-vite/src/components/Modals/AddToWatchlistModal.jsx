import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useModal } from '../../context/Modal';
import { getWatchlists, createWatchlist } from '../../redux/watchlist';
import { FaPlus } from 'react-icons/fa';
import './AddToWatchlistModal.css';

function AddToWatchlistModal({ symbol, onAdd }) {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const watchlists = useSelector(state => state.watchlist.watchlists);
  const [selectedWatchlist, setSelectedWatchlist] = useState('');
  const [newWatchlistName, setNewWatchlistName] = useState('');
  const [isCreatingNew, setIsCreatingNew] = useState(false);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    dispatch(getWatchlists());
  }, [dispatch]);

  useEffect(() => {
    if (watchlists.length > 0 && !selectedWatchlist) {
      setSelectedWatchlist(watchlists[0].id.toString());
    }
  }, [watchlists, selectedWatchlist]);

  const handleCreateNewWatchlist = async () => {
    if (!newWatchlistName.trim()) {
      setError('Please enter a watchlist name');
      return;
    }

    setIsSubmitting(true);
    try {
      const result = await dispatch(createWatchlist(newWatchlistName.trim()));
      if (result) {
        setSelectedWatchlist(result.id.toString());
        setIsCreatingNew(false);
        setNewWatchlistName('');
        setError('');
      }
    } catch (err) {
      setError('Failed to create watchlist');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isSubmitting) return;

    if (!selectedWatchlist) {
      setError('Please select a watchlist');
      return;
    }

    setIsSubmitting(true);
    try {
      await onAdd(parseInt(selectedWatchlist, 10));
      closeModal();
    } catch (err) {
      setError('Failed to add to watchlist');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="add-watchlist-modal">
      <h2>Add {symbol} to Watchlist</h2>
      
      {error && (
        <div className="errors">
          <div className="error">{error}</div>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {isCreatingNew ? (
          <div className="form-group-watchlist">
            <label>New Watchlist Name</label>
            <input
              type="text"
              value={newWatchlistName}
              onChange={(e) => setNewWatchlistName(e.target.value)}
              placeholder="Enter watchlist name"
              className="modal-input"
              autoFocus
            />
            <div className="modal-buttons-watchlist">
              <button
                type="button"
                onClick={() => setIsCreatingNew(false)}
                className="cancel-btn-watchlist"
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleCreateNewWatchlist}
                className="submit-btn-watchlist"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Creating...' : 'Create Watchlist'}
              </button>
            </div>
          </div>
        ) : (
          <>
            <div className="form-group-watchlist">
              <label>Select Watchlist</label>
              <select
                value={selectedWatchlist}
                onChange={(e) => setSelectedWatchlist(e.target.value)}
                className="modal-input"
              >
                {watchlists.map(list => (
                  <option key={list.id} value={list.id}>
                    {list.name} ({list.symbols.length})
                  </option>
                ))}
              </select>
            </div>

            <button
              type="button"
              onClick={() => setIsCreatingNew(true)}
              className="new-watchlist-button"
              disabled={isSubmitting}
            >
              <FaPlus /> Create New Watchlist
            </button>

            <div className="modal-buttons-watchlist">
              <button
                type="button"
                onClick={closeModal}
                className="cancel-btn-watchlist"
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="submit-btn-watchlist"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Adding...' : 'Add to Watchlist'}
              </button>
            </div>
          </>
        )}
      </form>
    </div>
  );
}

export default AddToWatchlistModal; 