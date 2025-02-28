import { useState, useEffect, useRef } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from 'react-router-dom';
import { thunkLogout } from "../../redux/session";
import { FaBars } from 'react-icons/fa';

function ProfileButton({ user }) {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [showMenu, setShowMenu] = useState(false);
  const ulRef = useRef();

  const toggleMenu = (e) => {
    e.stopPropagation();
    setShowMenu(!showMenu);
  };

  useEffect(() => {
    if (!showMenu) return;

    const closeMenu = (e) => {
      if (!ulRef.current?.contains(e.target)) {
        setShowMenu(false);
      }
    };

    document.addEventListener("click", closeMenu);
    return () => document.removeEventListener("click", closeMenu);
  }, [showMenu]);

  const handleLogout = async (e) => {
    e.preventDefault();
    await dispatch(thunkLogout());
    navigate('/');
    setShowMenu(false);
  };

  const closeMenu = () => setShowMenu(false);

  const ulClassName = "profile-dropdown" + (showMenu ? "" : " hidden");

  return (
    <>
      <button onClick={toggleMenu} className="profile-button">
        <FaBars />
      </button>
      <ul className={ulClassName} ref={ulRef}>
        {user && (
          <>
            <div className="user-info">
              <div className="username">{user.username}</div>
              <div className="email">{user.email}</div>
            </div>

            <div className="menu-item">
              <button onClick={handleLogout} className="logout-button">
                Log Out
              </button>
            </div>
          </>
        )}
      </ul>
    </>
  );
}

export default ProfileButton;
