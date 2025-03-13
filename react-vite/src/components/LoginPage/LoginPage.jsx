import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { thunkLogin } from '../../redux/session';
import './LoginPage.css';

function LoginPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const user = useSelector(state => state.session.user);
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState({
    email: '',
    password: '',
    general: ''
  });

  // Redirect if user is already logged in
  useEffect(() => {
    if (user) navigate('/dashboard');
  }, [user, navigate]);

  // Handle input changes
  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
  };

  // Reset all errors
  const resetErrors = () => {
    setErrors({ email: '', password: '', general: '' });
  };

  // Validate form data
  const validateForm = () => {
    let isValid = true;
    const newErrors = { email: '', password: '', general: '' };
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
      isValid = false;
    }
    
    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
      isValid = false;
    }
    
    setErrors(newErrors);
    return isValid;
  };

  // Handle login attempt
  const handleLogin = async (credentials) => {
    try {
      const response = await dispatch(thunkLogin(credentials));
      
      if (response && response.errors) {
        // Handle specific field errors if they exist
        if (response.errors.email) {
          setErrors(prev => ({ ...prev, email: response.errors.email }));
        }
        if (response.errors.password) {
          setErrors(prev => ({ ...prev, password: response.errors.password }));
        }
        if (response.errors.credential) {
          setErrors(prev => ({ ...prev, general: response.errors.credential }));
          // console.log("response.errors.credential", response.errors.credential);
        }
        // If there are no specific field errors, set a general error
        if (!response.errors.email && !response.errors.password && !response.errors.credential) {
          setErrors(prev => ({ ...prev, general: 'Invalid credentials. Please try again.' }));
        }
        return false;
      }
      return true;
      // Navigation happens automatically via useEffect
    } catch (error) {
      console.error('Login error:', error);
      setErrors(prev => ({ ...prev, general: 'An unexpected error occurred. Please try again.' }));
      return false;
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    resetErrors();
    
    if (validateForm()) {
      await handleLogin(formData);
    }
  };

  // Handle demo login
  const handleDemoLogin = async (e) => {
    e.preventDefault();
    resetErrors();
    
    await handleLogin({ 
      email: 'demo@aa.io', 
      password: 'password' 
    });
  };

  // Test function to show error messages
  const testErrorMessages = () => {
    setErrors({
      email: 'This is a test email error',
      password: 'This is a test password error',
      general: 'This is a test general error'
    });
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
          
          <form onSubmit={handleSubmit} className="login-form" noValidate>
            {errors.general && (
              <div style={{ 
                color: 'red', 
                backgroundColor: '#ffeeee', 
                padding: '10px', 
                borderRadius: '4px', 
                marginBottom: '15px', 
                fontWeight: 'bold',
                border: '1px solid red'
              }}>
                {errors.general}
              </div>
            )}
            
            <div className="form-group-login">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                style={errors.email ? { border: '2px solid red' } : {}}
              />
              {errors.email && (
                <div style={{ color: 'red', fontWeight: 'bold', margin: '5px 0 0 0' }}>
                  {errors.email}
                </div>
              )}
            </div>

            <div className="form-group-login">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                style={errors.password ? { border: '2px solid red' } : {}}
              />
              {errors.password && (
                <div style={{ color: 'red', fontWeight: 'bold', margin: '5px 0 0 0' }}>
                  {errors.password}
                </div>
              )}
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

            {/* <button 
              type="button" 
              onClick={testErrorMessages}
              style={{ 
                margin: '10px 0', 
                padding: '8px', 
                backgroundColor: '#f0f0f0', 
                color: '#333', 
                border: '1px solid #ccc', 
                borderRadius: '4px', 
                cursor: 'pointer' 
              }}
            >
              Test Error Messages
            </button> */}

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