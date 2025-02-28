import './Navigation.css';
import './ProfileButton.css';
import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { FaSearch } from 'react-icons/fa';
import ProfileButton from './ProfileButton';

function Navigation({ isLoaded }) {
  const sessionUser = useSelector(state => state.session.user);
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      navigate(`/symbols/${searchTerm.trim().toUpperCase()}`);
      setSearchTerm('');  // Clear search after navigation
    }
  };

  // If no user is logged in, show login/signup links
  if (!sessionUser) {
    return (
      <nav className="main-nav">
        <div className="nav-left">
          <NavLink exact to="/">
            <img src="/logo.png" alt="Logo" className="nav-logo" />
          </NavLink>
        </div>
        <div className="nav-right">
          <NavLink to="/login">Log In</NavLink>
          <NavLink to="/signup">Sign Up</NavLink>
        </div>
      </nav>
    );
  }

  // If user is logged in, show main navigation with profile button
  return (
    <nav className="main-nav">
      <div className="nav-left">
        <NavLink to="/dashboard">
          <img src="/logo.png" alt="Logo" className="nav-logo" />
        </NavLink>
      </div>
      <div className="nav-center">
        <div className="search-bar">
          <form onSubmit={handleSearch} className="search-form">
            <FaSearch className="search-icon" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search symbol (e.g., AAPL)"
              className="search-input"
            />
          </form>
        </div>
      </div>
      <div className="nav-right">
        <div className="balance">
          Buying Power: ${sessionUser.balance?.toFixed(2)}
        </div>
        <NavLink to="/portfolio">Portfolio</NavLink>
        <NavLink to="/transactions">Transactions</NavLink>
        <NavLink to="/account">Account</NavLink>
        <ProfileButton user={sessionUser} />
      </div>
    </nav>
  );
}

export default Navigation;
