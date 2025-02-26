import React from 'react';
import { NavLink } from 'react-router-dom';
import { useSelector } from 'react-redux';
import ProfileButton from './ProfileButton';
import './Navigation.css';

function Navigation({ isLoaded }) {
  const sessionUser = useSelector(state => state.session.user);

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
          <input type="text" placeholder="Search for stocks" />
        </div>
      </div>
      <div className="nav-right">
        <div className="balance">
          Buying Power: ${sessionUser.balance?.toFixed(2)}
        </div>
        {/* <NavLink to="/portfolio">Portfolio</NavLink> */}
        <NavLink to="/transactions">History</NavLink>
        <NavLink to="/account">Account</NavLink>
        <ProfileButton user={sessionUser} />
      </div>
    </nav>
  );
}

export default Navigation;
