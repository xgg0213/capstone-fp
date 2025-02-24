import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import Portfolio from '../Portfolio/Portfolio';
import Watchlists from '../Watchlist/Watchlists';
import OrderForm from '../Orders/OrderForm';

function Dashboard() {
  const user = useSelector(state => state.session.user);
  const [selectedStock, setSelectedStock] = useState(null);

  return (
    <div className="dashboard">
      <div className="dashboard-left">
        <Portfolio />
        <Watchlists onSelectStock={setSelectedStock} />
      </div>
      <div className="dashboard-right">
        {selectedStock ? (
          <>
            <div className="stock-chart">
              {/* Stock chart component will go here */}
            </div>
            <OrderForm stock={selectedStock} />
          </>
        ) : (
          <div className="welcome-message">
            Select a stock to trade
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard; 