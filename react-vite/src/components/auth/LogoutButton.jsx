import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { logout } from '../../store/session';

function LogoutButton() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = async (e) => {
    e.preventDefault();
    await dispatch(logout());
    navigate('/');
  };

  return (
    <button onClick={handleLogout} className="logout-button">
      Log Out
    </button>
  );
}

export default LogoutButton; 