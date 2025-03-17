import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useModal } from '../../context/Modal';
import { csrfFetch } from '../../redux/csrf';
import { fetchPortfolio } from '../../redux/portfolio';
import { thunkAuthenticate } from '../../redux/session';
import './PlaceOrderModal.css';

function PlaceOrderModal({ symbol = '', currentPrice: initialPrice = 0, initialOrderType = 'buy' }) {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const [shares, setShares] = useState('');
  const [orderType, setOrderType] = useState(initialOrderType); // 'buy' or 'sell'
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const user = useSelector(state => state.session.user);
  const portfolio = useSelector(state => state.portfolio);
  const [ownedShares, setOwnedShares] = useState(0);
  const [currentPosition, setCurrentPosition] = useState(null);
  const [currentPrice, setCurrentPrice] = useState(parseFloat(initialPrice) || 0);

  // Debug logs for props
  console.log("PlaceOrderModal - Initial props:", { symbol, initialPrice, initialOrderType });
  console.log("PlaceOrderModal - Parsed currentPrice:", currentPrice);

  // Find the current position for this symbol if it exists
  useEffect(() => {
    if (portfolio && portfolio.positions) {
      const position = portfolio.positions.find(pos => pos.symbol === symbol);
      if (position) {
        setCurrentPosition(position);
        setOwnedShares(position.shares);
      } else {
        setCurrentPosition(null);
        setOwnedShares(0);
      }
    }
  }, [portfolio, symbol]);

  const total = (shares * currentPrice).toFixed(2);
  const isSymbolProvided = !!symbol;

  // Load portfolio data when component mounts
  useEffect(() => {
    dispatch(fetchPortfolio());
  }, [dispatch]);

  // Validate order before submission
  const validateOrder = () => {
    // Validate price
    if (!currentPrice || isNaN(currentPrice) || currentPrice <= 0) {
      setError('Invalid price. Please try again.');
      return false;
    }

    // Validate shares
    if (!shares || isNaN(shares) || shares <= 0) {
      setError('Please enter a valid number of shares.');
      return false;
    }

    const orderTotal = shares * currentPrice;

    // Validate based on order type
    if (orderType === 'buy') {
      if (orderTotal > user.balance) {
        setError(`Insufficient funds. Order total: $${orderTotal.toFixed(2)}, Available balance: $${user.balance.toFixed(2)}`);
        return false;
      }
    } else if (orderType === 'sell') {
      // Make sure portfolio is loaded
      if (!portfolio || !portfolio.positions) {
        setError('Unable to verify your holdings. Please try again later.');
        return false;
      }
      
      // Find the current position for this symbol
      const position = portfolio.positions.find(pos => pos.symbol === symbol);
      
      // If no position exists or shares are insufficient
      if (!position) {
        setError(`You don't own any shares of ${symbol}.`);
        return false;
      }
      
      if (position.shares < shares) {
        setError(`Insufficient shares. You own ${position.shares} shares of ${symbol}.`);
        return false;
      }
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (isSubmitting) return;
    
    // Clear previous errors
    setError('');
    
    // Validate the order
    if (!validateOrder()) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const orderData = {
        symbol: symbol.toUpperCase(),
        type: orderType,
        shares: Number(shares),
        price: currentPrice
      };
      
      // Direct API call instead of using Redux
      const response = await csrfFetch('/api/orders/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
      });
      
      const responseData = await response.json();
      
      if (response.ok) {
        // Refresh portfolio data in Redux
        await dispatch(fetchPortfolio());
        
        // Refresh user session data to update balance
        await dispatch(thunkAuthenticate());
        
        // Close the modal
        closeModal();
        
        // Show success message
        alert(`Order placed successfully: ${shares} shares of ${symbol} ${orderType === 'buy' ? 'bought' : 'sold'}.`);
      } else {
        setError(responseData.error || (responseData.errors && responseData.errors.join(', ')) || 'Failed to place order. Please try again.');
      }
    } catch (err) {
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
      
      {isLoading ? (
        <div className="loading">Loading portfolio data...</div>
      ) : (
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
              onClick={() => {
                if (ownedShares > 0) {
                  setOrderType('sell');
                } else {
                  setError(`You don't own any shares of ${symbol.toUpperCase()} to sell.`);
                }
              }}
              disabled={orderType !== 'sell' && ownedShares === 0}
            >
              Sell {ownedShares > 0 ? `(${ownedShares} owned)` : ''}
            </button>
          </div>

          <div className="form-group">
            <label>Shares</label>
            <input
              type="number"
              min="1"
              max={orderType === 'sell' ? ownedShares : undefined}
              value={shares}
              onChange={(e) => {
                const newShares = Math.max(1, parseInt(e.target.value) || 0);
                if (orderType === 'sell') {
                  setShares(Math.min(newShares, ownedShares));
                } else {
                  setShares(newShares);
                }
              }}
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
              {orderType === 'sell' && (
                <div className="summary-row">
                  <span>Owned Shares</span>
                  <span>{ownedShares}</span>
                </div>
              )}
              <div className="summary-row total">
                <span>Estimated Total</span>
                <span>${total}</span>
              </div>
            </div>
          )}

          <div className="modal-buttons">
            <button 
              type="button" 
              className="cancel-btn-order" 
              onClick={closeModal}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="submit-btn-order"
              disabled={!isSymbolProvided || !currentPrice || isSubmitting || (orderType === 'sell' && ownedShares === 0)}
            >
              {isSubmitting ? 'Processing...' : 'Place Order'}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}

export default PlaceOrderModal; 