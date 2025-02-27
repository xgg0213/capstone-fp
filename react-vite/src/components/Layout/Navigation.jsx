import { NavLink } from 'react-router-dom';
import { useSelector } from 'react-redux';
import ProfileButton from '../Navigation/ProfileButton';
import './Navigation.css';

function Navigation() {
  const user = useSelector(state => state.session.user);

  return (
    <nav className="main-nav">
      <div className="nav-left">
        <NavLink to="/" className="nav-logo">
          SimpleTrade
        </NavLink>
      </div>

      {user ? (
        <div className="nav-right">
          <NavLink to="/portfolio" className="nav-link">
            Portfolio
          </NavLink>
          <NavLink to="/transactions" className="nav-link">
            History
          </NavLink>
          <ProfileButton user={user} />
        </div>
      ) : (
        <div className="nav-right">
          <NavLink to="/login" className="nav-link">
            Log In
          </NavLink>
          <NavLink to="/signup" className="nav-link signup">
            Sign Up
          </NavLink>
        </div>
      )}
    </nav>
  );
}

export default Navigation; 