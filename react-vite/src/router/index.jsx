import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ModalProvider } from '../context/Modal';
import Layout from "./Layout";
// import LandingPage from "../components/LandingPage";
// import LoginFormPage from "../components/LoginFormPage";
import SignupFormPage from "../components/SignupFormPage/SignupFormPage";
import SymbolDetails from '../components/SymbolDetails/SymbolDetails';
import LoginPage from "../components/LoginPage/LoginPage";
import Dashboard from "../components/Dashboard/Dashboard";
import Portfolio from '../components/Portfolio/Portfolio';
import Transactions from '../components/Transactions/Transactions';
import Account from '../components/Account/Account';
import ErrorBoundary from '../components/ErrorBoundary';
import React from 'react';
import { TestComponent } from '../components/SymbolDetails';
import ProtectedRoute from "./ProtectedRoute";

// Add this debug log
console.log("SymbolDetails import:", SymbolDetails);

// Add this function
const DebugSymbolDetails = () => {
  console.log("Rendering DebugSymbolDetails wrapper");
  return (
    <ErrorBoundary>
      {console.log("Inside ErrorBoundary, before components")}
      <React.Suspense fallback={<div>Loading...</div>}>
        {console.log("Inside Suspense, before components")}
        <div>
          <TestComponent />
          {console.log("Between components")}
          <SymbolDetails />
        </div>
        {console.log("After components")}
      </React.Suspense>
    </ErrorBoundary>
  );
};

console.log("Setting up router");

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
            path: '/symbols/:symbol',
            element: (
              <ErrorBoundary>
                <SymbolDetails />
              </ErrorBoundary>
            ),
          },
          {
            path: '/portfolio',
            element: <Portfolio />,
          },
          {
            path: '/transactions',
            element: <Transactions />,
          },
          {
            path: '/account',
            element: <Account />,
          }
        ]
      }
    ],
  },
]);

console.log("Router configuration complete");

function Router() {
  console.log("Router component rendering");
  return (
    <ModalProvider>
      <RouterProvider router={router} />
    </ModalProvider>
  );
}

export default Router;