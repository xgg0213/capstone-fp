import { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { thunkSignup, thunkLogin } from "../../redux/session";
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

    const response = await dispatch(
      thunkSignup({
        email,
        username,
        firstName,
        lastName,
        password,
      })
    );

    if (response === null) {
      // Signup was successful
      navigate("/dashboard");
    } else if (response.errors) {
      setErrors(response.errors);
    }
  };

  return (
    <div className="signup-page">
      <div className="signup-content">
        <h1>Create your account</h1>
        <p className="subtitle">Join TradeEasyUS and start investing today</p>

        {errors.general && (
          <p className="error general-error">{errors.general}</p>
        )}

        <form onSubmit={handleSubmit} className="signup-form">
          <div className="name-fields">
            <div className="form-group-signup">
              <label htmlFor="firstName">First Name</label>
              <input
                id="firstName"
                type="text"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
                placeholder="Enter your first name"
              />
              {errors.firstName && <p className="error">{errors.firstName}</p>}
            </div>

            <div className="form-group-signup">
              <label htmlFor="lastName">Last Name</label>
              <input
                id="lastName"
                type="text"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
                placeholder="Enter your last name"
              />
              {errors.lastName && <p className="error">{errors.lastName}</p>}
            </div>
          </div>

          <div className="form-group-signup">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Enter your email"
            />
            {errors.email && <p className="error">{errors.email}</p>}
          </div>

          <div className="form-group-signup">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              placeholder="Choose a username"
            />
            {errors.username && <p className="error">{errors.username}</p>}
          </div>

          <div className="form-group-signup">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Create a password"
            />
            {errors.password && <p className="error">{errors.password}</p>}
          </div>

          <div className="form-group-signup">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              placeholder="Confirm your password"
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
