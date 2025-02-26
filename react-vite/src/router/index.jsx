import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ModalProvider } from '../context/Modal';
import Layout from "./Layout";
import LoginPage from "../components/LoginPage/LoginPage";
import SignupFormPage from '../components/SignupFormPage/SignupFormPage';
import Dashboard from "../components/Dashboard/Dashboard";
import ProtectedRoute from './ProtectedRoute';
import Portfolio from '../components/Portfolio/Portfolio';

const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <LoginPage />,
      },
      {
        path: "/signup",
        element: <SignupFormPage />,
      },
      {
        element: <ProtectedRoute />,
        children: [
          {
            path: "/dashboard",
            element: <Dashboard />,
          },
          {
            path: '/portfolio',
            element: (
              // <ProtectedRoute>
                <Portfolio />
              // </ProtectedRoute>
            )
          },
          // Add other protected routes here
        ],
      },
    ],
  },
]);

function Router() {
  return (
    <ModalProvider>
      <RouterProvider router={router} />
    </ModalProvider>
  );
}

export default Router;