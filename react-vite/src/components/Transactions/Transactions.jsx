import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchTransactions } from '../../redux/transactions';
import { fetchSymbols } from '../../redux/symbols';
import './Transactions.css';

function Transactions() {
  const dispatch = useDispatch();
  const transactions = useSelector(state => state.transactions.transactions);
  const symbols = useSelector(state => state.symbols.symbols || []);
  const [isLoading, setIsLoading] = useState(true);
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        await Promise.all([
          dispatch(fetchTransactions()),
          dispatch(fetchSymbols())
        ]);
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, [dispatch]);

  // Sort transactions by date in descending order
  const sortedTransactions = [...transactions].sort((a, b) => {
    return new Date(b.created_at) - new Date(a.created_at);
  });

  const formatDate = (dateString) => {
    const options = { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
  };

  const getCompanyName = (symbol) => {
    const symbolData = symbols.find(s => s.symbol === symbol);
    return symbolData?.company_name || symbol;
  };

  const handleClick = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const formatTotal = (transaction) => {
    const total = (transaction.shares * transaction.price).toFixed(2);
    return transaction.type?.toLowerCase() === 'buy' 
      ? `+$${total}`
      : `-$${total}`;
  };

  if (isLoading) {
    return <div className="loading">Loading transactions...</div>;
  }

  return (
    <div className="transactions-container">
      <h2>Recent Transactions</h2>
      <div className="transactions-list">
        {sortedTransactions.length === 0 ? (
          <div className="no-transactions">No transactions yet.</div>
        ) : (
          sortedTransactions.map(transaction => (
            <div 
              key={transaction.id} 
              className={`transaction-item ${expandedId === transaction.id ? 'expanded' : ''}`}
              onClick={() => handleClick(transaction.id)}
            >
              <div className="transaction-summary">
                <div className="transaction-company">
                  <div className="company-name">{getCompanyName(transaction.symbol)}</div>
                  <div className="company-symbol">{transaction.symbol}</div>
                </div>
                <div className={`transaction-total ${transaction.type?.toLowerCase() === 'buy' ? 'buy' : 'sell'}`}>
                  {formatTotal(transaction)}
                </div>
              </div>
              
              {expandedId === transaction.id && (
                <div className="transaction-expanded">
                  <div className="transaction-details">
                    <div className="transaction-type">
                      {transaction.type?.toLowerCase() === 'buy' ? 'Bought' : 'Sold'}
                    </div>
                    <div className="transaction-shares">
                      {transaction.shares} shares @ ${transaction.price.toFixed(2)}
                    </div>
                    <div className="transaction-date">
                      {formatDate(transaction.created_at)}
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Transactions; 