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

  return (
    <div className="account-container">
      <div className="account-header">
        <h2>Account Settings</h2>
      </div>

      <div className="account-section">
        <h3>Account Balance</h3>
        <div className="current-balance">
          <span className="label">Current Balance:</span>
          <span className="value">${user.balance?.toFixed(2)}</span>
        </div>

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
          </div>

          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}

          <button type="submit" className="submit-btn">
            Add Funds
          </button>
        </form>
      </div>

      <div className="account-section">
        <h3>Account Information</h3>
        <div className="info-grid">
          <div className="info-item">
            <span className="label">Username</span>
            <span className="value">{user.username}</span>
          </div>
          <div className="info-item">
            <span className="label">Email</span>
            <span className="value">{user.email}</span>
          </div>
          <div className="info-item">
            <span className="label">Member Since</span>
            <span className="value">
              {new Date(user.created_at).toLocaleDateString()}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Account; 