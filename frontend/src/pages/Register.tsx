import SignForm from "../components/SignForm";

function Register() {
  return (
    <div className="py-10 h-screen space-y-5 overflow-y-auto">
      <SignForm route="/register" heading="Register" />
    </div>
  );
}

export default Register;
