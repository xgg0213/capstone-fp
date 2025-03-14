import { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { thunkSignup } from "../../redux/session";
import "./SignupForm.css";

function SignupFormPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errors, setErrors] = useState({});

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});

    if (password !== confirmPassword) {
      return setErrors({ confirmPassword: "Passwords must match" });
    }

    const userData = {
      username,
      email,
      first_name: firstName, // conventionally, camel case in JS, but can also do snake case (similar in Python)
      last_name: lastName, // the name of the variable need to match the backend routes/form (auth_routes.py, signup_form.py)
      password
    };

    // console.log("check firstName: ", firstName)

    const response = await dispatch(thunkSignup(userData));
    if (response) {
      if (response.errors) {
        setErrors(response.errors);
        console.log("response.errors", response.errors);
      } else if (typeof response === 'object') {
        setErrors(response);
        console.log("response", response);
      } else {
        setErrors({ general: response });
      }
  
    } else {
      navigate("/dashboard");
    }
  };

  return (
    <div className="signup-page">
      <div className="signup-content">
        <h1>Create your account</h1>
        <h2 className="subtitle">Join TradeEasyUS and start investing today</h2>

        {errors.general && (
          <p className="error general-error">{errors.general}</p>
        )}

        <form onSubmit={handleSubmit} className="signup-form">
          <div className="name-fields">
            <div className="form-group-signup">
              <label htmlFor="firstName">First Name</label>
              <input
                id="firstName"
                name="firstName"
                type="text"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
                placeholder="Enter your first name"
                // className={errors.first_name ? "error-input" : ""}
              />
              {errors.first_name && <p className="error">{errors.first_name}</p>}
            </div>

            <div className="form-group-signup">
              <label htmlFor="lastName">Last Name</label>
              <input
                id="lastName"
                name="lastName"
                type="text"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
                placeholder="Enter your last name"
                // className={errors.last_name ? "error-input" : ""}
              />
              {errors.last_name && <p className="error">{errors.last_name}</p>}
            </div>
          </div>

          <div className="form-group-signup">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              name="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              placeholder="Choose a username"
              // className={errors.username ? "error-input" : ""}
            />
            {errors.username && <p className="error">{errors.username}</p>}
          </div>

          <div className="form-group-signup">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Enter your email"
              // className={errors.email ? "error-input" : ""}
            />
            {errors.email && <p className="error">{errors.email}</p>}
          </div>

          <div className="form-group-signup">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Create a password"
              // className={errors.password ? "error-input" : ""}
            />
            {errors.password && <p className="error">{errors.password}</p>}
          </div>

          <div className="form-group-signup">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              placeholder="Confirm your password"
              // className={errors.confirmPassword ? "error-input" : ""}
            />
            {errors.confirmPassword && (
              <p className="error">{errors.confirmPassword}</p>
            )}
          </div>

          <button type="submit" className="signup-button">
            Sign Up
          </button>

          <div className="login-prompt">
            <span>Already have an account?</span>
            <button
              type="button"
              onClick={() => navigate("/")}
              className="login-link"
            >
              Log in to TradeEasyUS
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default SignupFormPage;