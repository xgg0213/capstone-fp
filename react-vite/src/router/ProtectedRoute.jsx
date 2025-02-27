import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useSelector } from "react-redux";

const ProtectedRoute = () => {
  const location = useLocation();
  const user = useSelector((state) => state.session.user);
  
  console.log("ProtectedRoute - Current path:", location.pathname);
  console.log("ProtectedRoute - User state:", user);
  console.log("ProtectedRoute - Current location:", location);

  if (!user) {
    return <Navigate to="/" replace={true} />;
  }

  console.log("ProtectedRoute - Rendering protected content");
  return <Outlet />;
};

export default ProtectedRoute;