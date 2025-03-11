import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useModal } from '../../context/Modal';
import { csrfFetch } from '../../redux/csrf';
import { fetchPortfolio } from '../../redux/portfolio';
import './PlaceOrderModal.css';

function PlaceOrderModal({ symbol = '', currentPrice = null, initialOrderType = 'buy' }) {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const [shares, setShares] = useState(1);
  const [orderType, setOrderType] = useState(initialOrderType); // 'buy' or 'sell'
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const user = useSelector(state => state.session.user);

  const total = (shares * currentPrice).toFixed(2);
  const isSymbolProvided = !!symbol;

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Client-side validation
    if (orderType === 'buy') {
      const orderTotal = shares * currentPrice;
      if (orderTotal > user.balance) {
        setError('Insufficient funds to complete this purchase.');
        return;
      }
    }

    setIsSubmitting(true);
    setError(null);
    
    try {
      // Direct API call instead of using Redux
      const response = await csrfFetch('/api/orders/', {
        method: 'POST',
        body: JSON.stringify({
          symbol: symbol.toUpperCase(),
          type: orderType,
          shares: Number(shares),
          price: currentPrice
        })
      });

      if (response.ok) {
        // Refresh portfolio data in Redux
        await dispatch(fetchPortfolio());
        
        // Close the modal
        closeModal();
        
        // Show success message
        alert(`Order placed successfully: ${shares} shares of ${symbol} ${orderType === 'buy' ? 'bought' : 'sold'}.`);
      } else {
        const data = await response.json();
        setError(data.error || 'Failed to place order. Please try again.');
      }
    } catch (err) {
      console.error('Error placing order:', err);
      setError('An error occurred while placing the order. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // If user is not authenticated, don't render the form
  if (!user) {
    return null;
  }

  return (
    <div className="place-order-modal">
      <h2>Place {orderType === 'buy' ? 'Buy' : 'Sell'} Order</h2>
      
      {error && (
        <div className="errors">
          <div className="error">{error}</div>
        </div>
      )}
      
      <div className="symbol-info">
        <span className="symbol">{symbol.toUpperCase()}</span>
        {currentPrice && <span className="price">${currentPrice.toFixed(2)}</span>}
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
            required
          />
        </div>

        {currentPrice && (
          <div className="order-summary">
            <div className="summary-row">
              <span>Market Price</span>
              <span>${currentPrice.toFixed(2)}</span>
            </div>
            <div className="summary-row">
              <span>Available Balance</span>
              <span>${user?.balance?.toFixed(2) || '0.00'}</span>
            </div>
            <div className="summary-row total">
              <span>Estimated Total</span>
              <span>${total}</span>
            </div>
          </div>
        )}

        <div className="modal-buttons">
          <button 
            type="button" 
            className="cancel-btn" 
            onClick={closeModal}
          >
            Cancel
          </button>
          <button 
            type="submit" 
            className="submit-btn"
            disabled={!isSymbolProvided || !currentPrice || isSubmitting}
          >
            {isSubmitting ? 'Processing...' : 'Place Order'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default PlaceOrderModal; 