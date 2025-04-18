import { Navigate } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN } from "../constants";
import { ReactNode, useState, useEffect } from "react";

interface Props {
  children: ReactNode
}

function ProtectedRoute({children}: Props) {
  const {isAuthorized, setAuthorized} = useState(null)

  useEffect(() => {
    auth().catch(() => setAuthorized(false))
  })

  const auth = async () => {
    const token = localStorage.getItem(ACCESS_TOKEN)

    if (!token) {
      setAuthorized(false)
      return
    }

    setAuthorized(true)
  }

  if (isAuthorized === null) {
    return <div>Loading...</div>
  }

  return isAuthorized ? children : <Navigate to="/login" />
}

export default ProtectedRoute;
