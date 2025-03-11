import { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { thunkUpdateBalance } from '../../redux/session';
import './Account.css';

function Account() {
  const dispatch = useDispatch();
  const user = useSelector(state => state.session.user);
  const [amount, setAmount] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validate amount
    const amountValue = parseFloat(amount);
    if (!amount || isNaN(amountValue) || amountValue <= 0) {
      setError('Please enter a valid amount greater than 0');
      return;
    }

    setIsLoading(true);

    try {
      // Use the Redux thunk action instead of direct API call
      const result = await dispatch(thunkUpdateBalance(amountValue));
      
      if (result.success) {
        setSuccess(`$${amountValue.toFixed(2)} added successfully! Your new balance is $${result.balance.toFixed(2)}`);
        setAmount('');
      } else {
        // Handle error messages
        if (result.errors) {
          if (typeof result.errors === 'object') {
            const errorMessages = Object.values(result.errors).join(', ');
            setError(errorMessages);
          } else {
            setError(result.errors);
          }
        } else {
          setError('Failed to update balance. Please try again.');
        }
      }
    } catch (error) {
      console.error('Error updating balance:', error);
      setError('An error occurred while updating your balance. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (!user) {
    return <div className="loading">Loading account information...</div>;
  }

  return (
    <div className="account-container">
      <h2>Account Information</h2>
      <div className="account-content">
        <div className="account-section">
          <div className="account-row">
            <span className="account-label">Email</span>
            <span className="account-value account-email">{user.email}</span>
          </div>
        </div>

        <div className="account-section">
          <div className="account-row">
            <span className="account-label">Member Since</span>
            <span className="account-value">
              {new Date(user.created_at).toLocaleDateString()}
            </span>
          </div>
        </div>

        <div className="account-section">
          <div className="account-row">
            <span className="account-label">Account Type</span>
            <span className="account-value">Individual Trading Account</span>
          </div>

          <div className="account-row">
            <span className="account-label">Account Balance</span>
            <span className="account-value account-balance">
              ${user.balance?.toFixed(2)}
            </span>
          </div>
        </div>
      </div>

      <div className="account-update">
        <h3>Add Funds to Your Account</h3>
        <form onSubmit={handleSubmit} className="balance-form">
          <div className="form-group">
            <label htmlFor="amount">Amount to Add</label>
            <div className="input-group">
              <span className="currency-symbol">$</span>
              <input
                id="amount"
                type="number"
                min="0.01"
                step="0.01"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="Enter amount"
                disabled={isLoading}
              />
            </div>
            <button 
              type="submit" 
              className="submit-btn"
              disabled={isLoading}
            >
              {isLoading ? 'Processing...' : 'Add Funds'}
            </button>
          </div>

          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}
        </form>
      </div>
    </div>
  );
}

export default Account; 