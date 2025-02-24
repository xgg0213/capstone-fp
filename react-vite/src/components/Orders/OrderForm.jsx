import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { csrfFetch } from '../../redux/csrf';

function OrderForm({ stock }) {
  const dispatch = useDispatch();
  const [orderType, setOrderType] = useState('market');
  const [side, setSide] = useState('buy');
  const [shares, setShares] = useState('');
  const [price, setPrice] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await csrfFetch('/api/orders', {
        method: 'POST',
        body: JSON.stringify({
          symbol: stock.symbol,
          order_type: orderType,
          side,
          shares: Number(shares),
          price: orderType === 'limit' ? Number(price) : null
        })
      });

      if (response.ok) {
        // Handle success
        setShares('');
        setPrice('');
      }
    } catch (err) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit} className="order-form">
      <div className="order-type-selector">
        <button
          type="button"
          className={orderType === 'market' ? 'active' : ''}
          onClick={() => setOrderType('market')}
        >
          Market
        </button>
        <button
          type="button"
          className={orderType === 'limit' ? 'active' : ''}
          onClick={() => setOrderType('limit')}
        >
          Limit
        </button>
      </div>

      <div className="side-selector">
        <button
          type="button"
          className={side === 'buy' ? 'active' : ''}
          onClick={() => setSide('buy')}
        >
          Buy
        </button>
        <button
          type="button"
          className={side === 'sell' ? 'active' : ''}
          onClick={() => setSide('sell')}
        >
          Sell
        </button>
      </div>

      <div className="input-group">
        <label>Shares</label>
        <input
          type="number"
          value={shares}
          onChange={(e) => setShares(e.target.value)}
          min="0"
          step="1"
          required
        />
      </div>

      {orderType === 'limit' && (
        <div className="input-group">
          <label>Limit Price</label>
          <input
            type="number"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            min="0"
            step="0.01"
            required
          />
        </div>
      )}

      <button type="submit" className="submit-button">
        Place Order
      </button>
    </form>
  );
}

export default OrderForm; 