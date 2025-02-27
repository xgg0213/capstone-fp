import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useModal } from '../../context/Modal';
import './OrderForm.css';

function OrderForm({ initialSymbol = '', initialPrice = null }) {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const [symbol, setSymbol] = useState(initialSymbol);
  const [shares, setShares] = useState(1);
  const [orderType, setOrderType] = useState('buy');
  const user = useSelector(state => state.session.user);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/transactions/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          symbol,
          shares: Number(shares),
          type: orderType,
          price: initialPrice
        })
      });

      if (response.ok) {
        // Handle successful order
        closeModal();
        // Optionally refresh portfolio data
      }
    } catch (error) {
      console.error('Error placing order:', error);
    }
  };

  return (
    <div className="order-form">
      <h2>Place {orderType === 'buy' ? 'Buy' : 'Sell'} Order</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Symbol</label>
          <input
            type="text"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            disabled={!!initialSymbol}
            required
          />
        </div>

        <div className="order-type">
          <button
            type="button"
            className={`type-btn ${orderType === 'buy' ? 'active' : ''}`}
            onClick={() => setOrderType('buy')}
          >
            Buy
          </button>
          <button
            type="button"
            className={`type-btn ${orderType === 'sell' ? 'active' : ''}`}
            onClick={() => setOrderType('sell')}
          >
            Sell
          </button>
        </div>

        <div className="form-group">
          <label>Shares</label>
          <input
            type="number"
            min="1"
            value={shares}
            onChange={(e) => setShares(Math.max(1, parseInt(e.target.value) || 0))}
            required
          />
        </div>

        {initialPrice && (
          <div className="order-summary">
            <div className="summary-row">
              <span>Market Price</span>
              <span>${initialPrice.toFixed(2)}</span>
            </div>
            <div className="summary-row total">
              <span>Estimated Total</span>
              <span>${(shares * initialPrice).toFixed(2)}</span>
            </div>
          </div>
        )}

        <div className="form-actions">
          <button type="button" onClick={closeModal} className="cancel-btn">
            Cancel
          </button>
          <button type="submit" className="submit-btn">
            Place Order
          </button>
        </div>
      </form>
    </div>
  );
}

export default OrderForm; 