import * as React from "react";
import * as ReactDOM from "react-dom/client";
import Home from './pages/Home'
import About from './pages/About'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import "./index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/About",
    element: <About />,
  },
  {
    path: "/Upload",
    element: <About />,
  },
  {
    path: "/Processing",
    element: <About />,
  },
  {
    path: "/Error",
    element: <About />,
  },
  {
    path: "/Ready",
    element: <About />,
  }
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);