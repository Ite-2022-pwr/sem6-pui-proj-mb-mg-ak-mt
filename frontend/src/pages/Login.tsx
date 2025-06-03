import { useState } from "react";
import { useNavigate } from "react-router-dom";
import SignForm from "../components/SignForm";
import ErrorAlert from "../components/ErrorAlert";

function Login() {
  const navigate = useNavigate();
  const [error, setError] = useState<{
    status?: number;
    message: string;
  } | null>(null);

  const handleRegisterRedirect = () => {
    navigate("/register");
  };

  return (
    <div className="py-10 min-h-screen space-y-5 overflow-y-auto bg-mydarkblue">
      {error && <ErrorAlert status={error.status} message={error.message} />}

      <SignForm
        route="/login"
        heading="Login"
        onError={(err: { status?: number; message: string }) => setError(err)}
      />

      <p
        className="mx-auto text-center text-mymint hover:text-myyellow-1 hover:cursor-pointer"
        onClick={handleRegisterRedirect}
      >
        Don&apos;t have an account? Click here
      </p>
    </div>
  );
}

export default Login;
