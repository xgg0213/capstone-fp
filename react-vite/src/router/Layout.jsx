import { useEffect } from "react";
import { Outlet } from "react-router-dom";
import { useDispatch } from "react-redux";
import { restoreCSRF } from "../redux/csrf";
import { thunkAuthenticate } from "../redux/session";
import Navigation from "../components/Navigation/Navigation";

export default function Layout() {
  const dispatch = useDispatch();

  useEffect(() => {
    // Restore CSRF token
    restoreCSRF().then(() => {
      // Then try to fetch the current user
      dispatch(thunkAuthenticate());
    });
  }, [dispatch]);

  return (
    <>
      <Navigation />
      <Outlet />
    </>
  );
}
