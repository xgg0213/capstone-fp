import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import Portfolio from '../Portfolio/Portfolio';
import Watchlists from '../Watchlist/Watchlists';
import OrderForm from '../Orders/OrderForm';
import './Dashboard.css';

function Dashboard() {
  const user = useSelector(state => state.session.user);
  const [selectedStock, setSelectedStock] = useState(null);

  return (
    <div className="dashboard">
      <div className="dashboard-left">
        <Portfolio />
      </div>
      <div className="dashboard-right">
        <Watchlists onSelectStock={setSelectedStock} />
      </div>
    </div>
  );
}

export default Dashboard; 