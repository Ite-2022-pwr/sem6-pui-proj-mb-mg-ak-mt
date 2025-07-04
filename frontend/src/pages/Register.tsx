import SignForm from "../components/SignForm";
import { useNavigate } from "react-router-dom";

function Register() {

  const navigate = useNavigate()

  return (
    <div className="py-10 h-screen space-y-5 overflow-y-auto bg-mydarkblue">
      <SignForm route="/register" heading="Register" />
      <p className="mx-auto text-center w-100 text-mymint hover:text-myyellow-1 hover:cursor-pointer"
      onClick={() => {navigate("/login")}}>
        Have an account already? Click here
      </p>
    </div>
  );
}

export default Register;
