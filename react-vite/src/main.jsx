import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import configureStore from "./redux/store";
import Router from "./router";
import "./index.css";
import { restoreCSRF } from './redux/csrf';

const store = configureStore();

if (process.env.NODE_ENV !== 'production') {
  restoreCSRF().catch(console.error);
}

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Provider store={store}>
      <Router />
    </Provider>
  </React.StrictMode>
);
