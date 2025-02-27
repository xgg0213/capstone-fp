import { useState, useEffect } from "react";
import { Outlet, useLocation } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { restoreCSRF } from "../redux/csrf";
import { thunkAuthenticate } from "../redux/session";
import Navigation from "../components/Navigation/Navigation";
import { Modal } from '../context/Modal';

export default function Layout() {
  console.log("Layout component rendering");
  const dispatch = useDispatch();
  const location = useLocation();
  const user = useSelector(state => state.session.user);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    console.log("Layout useEffect running");
    // Restore CSRF token
    restoreCSRF().then(() => {
      // Then try to fetch the current user
      dispatch(thunkAuthenticate()).then(() => {
        console.log("Authentication complete");
        setIsLoaded(true);
      });
    });
  }, [dispatch]);

  // Don't show navigation on login/signup pages
  const hideNav = ["/", "/login", "/signup"].includes(location.pathname);

  console.log("Layout rendering, isLoaded:", isLoaded);
  return (
    <>
      {!hideNav && <Navigation isLoaded={isLoaded} />}
      {isLoaded && (
        <>
          {console.log("Rendering Outlet")}
          <Outlet />
        </>
      )}
      <Modal />
    </>
  );
}
