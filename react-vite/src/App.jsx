import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { useLocation } from "react-router-dom";
import { thunkAuthenticate } from "./redux/session";
import Router from "./router";

function App() {
  const dispatch = useDispatch();
  const location = useLocation();
  const isPublicRoute = ['/', '/signup'].includes(location.pathname);

  useEffect(() => {
    // Only check auth for non-public routes
    if (!isPublicRoute) {
      dispatch(thunkAuthenticate());
    }
  }, [dispatch, isPublicRoute]);

  return <Router />;
}

export default App; 