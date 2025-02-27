import { useState, useEffect } from 'react';
import { csrfFetch } from '../../redux/csrf';
import './Transactions.css';

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const response = await csrfFetch('/api/transactions/');
        if (response.ok) {
          const data = await response.json();
          setTransactions(data.transactions);
        }
      } catch (error) {
        console.error('Error fetching transactions:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTransactions();
  }, []);

  if (isLoading) return <div className="loading">Loading transactions...</div>;

  return (
    <div className="transactions-container">
      <h2>Transaction History</h2>
      
      <div className="transactions-table">
        <div className="table-header">
          <div>Date</div>
          <div>Type</div>
          <div>Symbol</div>
          <div>Shares</div>
          <div>Price</div>
          <div>Total</div>
        </div>

        <div className="table-body">
          {transactions.length === 0 ? (
            <div className="no-transactions">
              <p>No transactions yet.</p>
            </div>
          ) : (
            transactions.map(transaction => (
              <div key={transaction.id} className="transaction-row">
                <div className="date">
                  {new Date(transaction.created_at).toLocaleDateString()}
                </div>
                <div className={`type ${transaction.type}`}>
                  {transaction.type.toUpperCase()}
                </div>
                <div className="symbol">{transaction.symbol}</div>
                <div className="shares">{transaction.shares}</div>
                <div className="price">${transaction.price.toFixed(2)}</div>
                <div className="total">
                  ${(transaction.shares * transaction.price).toFixed(2)}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default Transactions; 