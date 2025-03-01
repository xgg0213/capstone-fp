import { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { csrfFetch } from '../../redux/csrf';
import { thunkAuthenticate } from '../../redux/session';
import './Account.css';

function Account() {
  const dispatch = useDispatch();
  const user = useSelector(state => state.session.user);
  const [amount, setAmount] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!amount || isNaN(amount) || amount <= 0) {
      setError('Please enter a valid amount');
      return;
    }

    try {
      const response = await csrfFetch('/api/users/balance', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ amount: parseFloat(amount) })
      });

      if (response.ok) {
        // Refresh user data to get updated balance
        await dispatch(thunkAuthenticate());
        setSuccess('Balance updated successfully!');
        setAmount('');
      }
    } catch (error) {
      setError('Failed to update balance. Please try again.');
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
        <form onSubmit={handleSubmit} className="balance-form">
          <div className="form-group">
            <label>Add Funds</label>
            <div className="input-group">
              <span className="currency-symbol">$</span>
              <input
                type="number"
                min="0"
                step="0.01"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="Enter amount"
              />
            </div>
            <button type="submit" className="submit-btn">
              Add Funds
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