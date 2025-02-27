import { useState } from 'react';
import './PlaceOrderModal.css';

function PlaceOrderModal({ symbol, currentPrice, onConfirm, onCancel }) {
  const [shares, setShares] = useState(1);
  const [orderType, setOrderType] = useState('buy'); // 'buy' or 'sell'

  const total = (shares * currentPrice).toFixed(2);

  const handleSubmit = (e) => {
    e.preventDefault();
    onConfirm({
      symbol,
      shares: Number(shares),
      type: orderType,
      price: currentPrice
    });
  };

  return (
    <div className="place-order-modal">
      <h2>Place {orderType === 'buy' ? 'Buy' : 'Sell'} Order</h2>
      <div className="symbol-info">
        <span className="symbol">{symbol}</span>
        <span className="price">${currentPrice}</span>
      </div>
      
      <form onSubmit={handleSubmit}>
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
          />
        </div>

        <div className="order-summary">
          <div className="summary-row">
            <span>Market Price</span>
            <span>${currentPrice}</span>
          </div>
          <div className="summary-row total">
            <span>Estimated Total</span>
            <span>${total}</span>
          </div>
        </div>

        <div className="modal-buttons">
          <button type="button" className="cancel-btn" onClick={onCancel}>
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

export default PlaceOrderModal; 