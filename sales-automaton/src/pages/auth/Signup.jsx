import { useContext, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import parseErrors from "../../utils/parseErrors";
import "../../styles/signup.css";
export default function Signup() {
  const { signup } = useContext(AuthContext);
  const { tenant_slug } = useParams();
  const staffRef = useRef(null);
  const firstNameRef = useRef(null);
  const lastNameRef = useRef(null);
  const emailRef = useRef(null);
  const whatsappRef = useRef(null);
  const roleRef = useRef(null);
  const passwordRef = useRef(null);
  const [form, setForm] = useState({
    staff_ID: "",
    first_name: "",
    last_name: "",
    email: "",
    whatsapp_number: "",
    password: "",
    role: "agent",
  });

  const [errors, setErrors] = useState({});

const submit = async (e) => {
  e.preventDefault();
  setErrors({});

  try {
    await signup(tenant_slug, form);
    
  } catch (error) {
     if (!tenant_slug) {
      alert("Invalid signup link.");
      return;
    }
    const parsed = parseErrors(error);
    scrollToFirstError(parsed);
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
  

  const scrollToFirstError = (errors) => {
  const fieldOrder = [
    "staff_ID",
    "first_name",
    "last_name",
    "email",
    "whatsapp_number",
    "role",
    "password",
  ];

  for (let field of fieldOrder) {
    if (errors[field]) {
      const refMap = {
        staff_ID: staffRef,
        first_name: firstNameRef,
        last_name: lastNameRef,
        email: emailRef,
        whatsapp_number: whatsappRef,
        role: roleRef,
        password: passwordRef,
      };

      const fieldRef = refMap[field];

      if (fieldRef?.current) {
        fieldRef.current.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });

        fieldRef.current.focus();
      }

      break;
    }
  }
};

  return (
    <div className="auth">
      <form onSubmit={submit}>
      <h2>Sign up - {tenant_slug}</h2>

        <input
          ref={staffRef}
          placeholder="Staff ID"
          value={form.staff_ID}
          onChange={(e) =>
            setForm({ ...form, staff_ID: e.target.value })
          }
          required
        />
        {errors.staff_ID && <p className="error">{errors.staff_ID[0]}</p>}

        <input
          ref={firstNameRef}
          placeholder="First name"
          value={form.first_name}
          onChange={(e) =>
            setForm({ ...form, first_name: e.target.value })
          }
          required
        />
        {errors.first_name && <p className="error">{errors.first_name[0]}</p>}

        <input
          ref={lastNameRef}
          placeholder="Last name"
          value={form.last_name}
          onChange={(e) =>
            setForm({ ...form, last_name: e.target.value })
          }
          required
        />
        {errors.last_name && <p className="error">{errors.last_name[0]}</p>}

        <input
          ref={emailRef}
          placeholder="Email"
          type="email"
          value={form.email}
          onChange={(e) =>
            setForm({ ...form, email: e.target.value })
          }
          required
        />
        {errors.email && <p className="error">{errors.email[0]}</p>}

        <input
          ref={whatsappRef}
          placeholder="Whatsapp number"
          type="tel"
          value={form.whatsapp_number}
          onChange={(e) =>
            setForm({ ...form, whatsapp_number: e.target.value })
          }
          required
        />
        {errors.whatsapp_number && (
          <p className="error">{errors.whatsapp_number[0]}</p>
        )}

        <select
          ref={roleRef}
          value={form.role}
          onChange={(e) =>
            setForm({ ...form, role: e.target.value })
          }
          required
        >
          <option value="agent">Agent</option>
          <option value="manager">Manager</option>
        </select>
        {errors.role && <p className="error">{errors.role[0]}</p>}

        <input
          ref={passwordRef}
          placeholder="Password"
          type="password"
          onChange={(e) =>
            setForm({ ...form, password: e.target.value })
          }
          required
        />
        {errors.password && <p className="error">{errors.password[0]}</p>}

        {errors.detail && <p className="error">{errors.detail}</p>}

        <button>Create Account</button>
      </form>
    </div>
  );
}