import { createBrowserRouter } from 'react-router-dom';
import Layout from './Layout';
import LoginPage from '../components/LoginPage/LoginPage';
import SignupFormPage from '../components/SignupFormPage/SignupFormPage';
import Dashboard from '../components/Dashboard/Dashboard';
import ProtectedRoute from './ProtectedRoute';

export const router = createBrowserRouter([
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
          // Add other protected routes here
        ],
      },
    ],
  },
]);