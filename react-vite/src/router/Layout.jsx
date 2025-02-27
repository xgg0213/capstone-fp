import { useEffect } from "react";
import { Outlet, useLocation } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { restoreCSRF } from "../redux/csrf";
import { thunkAuthenticate } from "../redux/session";
import Navigation from "../components/Navigation/Navigation";
import { Modal } from '../context/Modal';

function Layout() {
  const dispatch = useDispatch();
  const location = useLocation();
  const user = useSelector(state => state.session.user);

  useEffect(() => {
    // Restore CSRF token
    restoreCSRF().then(() => {
      // Then try to fetch the current user
      dispatch(thunkAuthenticate());
    });
  }, [dispatch]);

  // Don't show navigation on login/signup pages
  const hideNav = ["/", "/login", "/signup"].includes(location.pathname);

  return (
    <>
      {!hideNav && <Navigation />}
      <Outlet />
      <Modal />
    </>
  );
}

export default Layout;
