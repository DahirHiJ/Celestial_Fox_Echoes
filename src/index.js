import * as React from "react";
import * as ReactDOM from "react-dom/client";
import Home from './pages/Home'
import About from './pages/About'
import Upload from './pages/Upload'
import Processing from './pages/Processing'
import Error from './pages/Error'
import Ready from './pages/Ready'
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
    element: <Upload />,
  },
  {
    path: "/Processing",
    element: <Processing />,
  },
  {
    path: "/Error",
    element: <Error />,
  },
  {
    path: "/Ready",
    element: <Ready />,
  }
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);