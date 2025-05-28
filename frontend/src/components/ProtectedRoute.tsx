import { Navigate, Outlet } from "react-router-dom";
import { ACCESS_TOKEN } from "../constants";

function ProtectedRoute() {
  const token = localStorage.getItem(ACCESS_TOKEN);

  return token ? <Outlet /> : <Navigate to="/login" replace />;
}

export default ProtectedRoute;
