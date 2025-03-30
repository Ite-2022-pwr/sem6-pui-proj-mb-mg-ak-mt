import SignForm from "../components/SignForm";

function Login() {
  return (
    <div className="py-10 h-screen space-y-5 overflow-y-auto">
      <SignForm route="/login" heading="Login" />
    </div>
  );
}

export default Login;
