import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import Portfolio from '../Portfolio/Portfolio';
import Watchlists from '../Watchlist/Watchlists';
// import StockTicker from '../StockTicker/StockTicker';
import './Dashboard.css';

function Dashboard() {
  const user = useSelector(state => state.session.user);
  const navigate = useNavigate();

  const handleStockClick = (stock) => {
    if (stock && stock.symbol) {
      navigate(`/symbols/${stock.symbol}`);
    }
  };

  return (
    <div className="dashboard">
      {/* <StockTicker /> */}
      <div className="dashboard-left">
        <Portfolio onSelectStock={handleStockClick} />
      </div>
      <div className="dashboard-right">
        <Watchlists onSelectStock={handleStockClick} />
      </div>
    </div>
  );
}

export default Dashboard; 