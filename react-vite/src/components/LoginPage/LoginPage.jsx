import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { thunkLogin } from '../../redux/session';
import './LoginPage.css';

function LoginPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const user = useSelector(state => state.session.user);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});

  // Only redirect if user is already logged in
  useEffect(() => {
    if (user) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});

    if (!validateEmail(email)) {
      setErrors({ credential: 'Please enter a valid email address' });
      return;
    }

    try {
      await dispatch(thunkLogin({ email, password }));
      // Navigation will happen automatically due to the useEffect above
    } catch (error) {
      setErrors({ credential: 'Invalid credentials' });
    }
  };

  const handleDemoLogin = async (e) => {
    e.preventDefault();
    await dispatch(thunkLogin({ 
      email: 'demo@aa.io', 
      password: 'password' 
    }));
    navigate('/dashboard');
  };

  return (
    <div className="login-page">
      <div className="login-right">
        <div className="feature-list">
          <h2>Why Choose TradeEasyUS?</h2>
          <div className="feature-item">
            <p>A seamless, secure, and intuitive trading experience for all investors</p>
          </div>
        </div>
      </div>

      <div className="login-divider"></div>

      <div className="login-left">
        <div className="login-content">
          <h1>Login to TradeEasyUS</h1>
          
          <form onSubmit={handleSubmit} className="login-form">
            {errors.credential && (
              <div className="error-message">
                {errors.credential}
              </div>
            )}
            
            <div className="form-group-login">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                pattern="[^\s@]+@[^\s@]+\.[^\s@]+"
                title="Please enter a valid email address"
              />
            </div>

            <div className="form-group-login">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="login-button">
              Log In
            </button>

            <button 
              type="button" 
              onClick={handleDemoLogin}
              className="demo-button"
            >
              Demo User
            </button>

            <div className="signup-prompt">
              <span>Don't have an account?</span>
              <button 
                type="button"
                onClick={() => navigate('/signup')}
                className="signup-link"
              >
                Sign up for TradeEasyUS
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default LoginPage; 