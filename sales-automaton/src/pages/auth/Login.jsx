import { useContext, useState } from "react";
import { AuthContext } from "../../context/AuthContext";
import {useNavigate, Link } from 'react-router-dom';
import parseErrors from "../../utils/parseErrors";

export default function Login() {
  const { login } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const [errors, setErrors] = useState({});

const submit = async (e) => {
  e.preventDefault();
  setErrors({});

  try {
    await login(email, password);
    navigate('/');;
  } catch (error) {
    const parsed = parseErrors(error);
    setErrors(parsed);

    setTimeout(() => {
      const firstError = document.querySelector(".error-text");
      if (firstError) {
        firstError.scrollIntoView({
          behavior: "smooth",
          block: "center"
        });
      }
    }, 100);
  }
};

  return (
    <div className="auth">
      <form onSubmit={submit}>
        <h2>Login</h2>
        <input
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />
        {errors.email && (
          <p className="error">{errors.email[0]}</p>
        )}
        <input
          placeholder="Password"
          type="password"
          onChange={(e) => setPassword(e.target.value)}
        />
        {errors.password && (
          <p className="error">{errors.password[0]}</p>
        )}
        
        {errors.general && (
          <p className="error">{errors.general[0]}</p>
        )}
        <button>Login</button>
      </form>
    </div>
  );
}
