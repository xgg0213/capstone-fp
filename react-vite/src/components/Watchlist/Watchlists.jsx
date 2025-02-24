import { useState, useEffect } from 'react';
import { csrfFetch } from '../../redux/csrf';

function Watchlists({ onSelectStock }) {
  const [watchlists, setWatchlists] = useState([]);
  const [newListName, setNewListName] = useState('');

  useEffect(() => {
    fetchWatchlists();
  }, []);

  async function fetchWatchlists() {
    const response = await csrfFetch('/api/watchlists');
    if (response.ok) {
      const data = await response.json();
      setWatchlists(data.watchlists);
    }
  }

  const handleCreateList = async (e) => {
    e.preventDefault();
    const response = await csrfFetch('/api/watchlists', {
      method: 'POST',
      body: JSON.stringify({
        name: newListName,
        symbols: ''
      })
    });
    if (response.ok) {
      setNewListName('');
      fetchWatchlists();
    }
  };

  return (
    <div className="watchlists">
      <h2>Watchlists</h2>
      
      <form onSubmit={handleCreateList} className="new-list-form">
        <input
          type="text"
          value={newListName}
          onChange={(e) => setNewListName(e.target.value)}
          placeholder="New list name"
        />
        <button type="submit">Create</button>
      </form>

      {watchlists.map(list => (
        <div key={list.id} className="watchlist">
          <h3>{list.name}</h3>
          <div className="stock-list">
            {list.symbols.split(',').map(symbol => (
              <div
                key={symbol}
                className="stock-item"
                onClick={() => onSelectStock({ symbol })}
              >
                {symbol}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default Watchlists; 