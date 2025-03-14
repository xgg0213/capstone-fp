import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import configureStore from "./redux/store";
import Router from "./router";
import "./index.css";
import { restoreCSRF, csrfFetch } from './redux/csrf';
import * as sessionActions from "./redux/session";

const store = configureStore();

// Restore CSRF token in all environments
restoreCSRF().catch(console.error);

if (process.env.NODE_ENV !== 'production') {
  window.csrfFetch = csrfFetch;
  window.store = store;
  window.sessionActions = sessionActions;
}

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Provider store={store}>
      <Router />
    </Provider>
  </React.StrictMode>
);
