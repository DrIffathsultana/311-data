/* eslint-disable react/jsx-filename-extension */

import "core-js/stable";
import "regenerator-runtime/runtime";
import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { ThemeProvider } from "@material-ui/core/styles";
import { CssBaseline } from "@material-ui/core";
import store from "./redux/store";
import App from "./App";
import theme from "./theme/theme";

if (process.env.NODE_ENV === "development") {
  const { server } = require("./mockServer/server.js");
  server.start();
}

ReactDOM.render(
  <Provider store={store}>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </Provider>,
  document.getElementById("root")
);

// hot module replacement during development
if (module.hot) module.hot.accept();
