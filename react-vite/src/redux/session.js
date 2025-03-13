import {csrfFetch} from "./csrf"

// Action Types
const SET_USER = 'session/setUser';
const REMOVE_USER = 'session/removeUser';
const UPDATE_BALANCE = 'session/UPDATE_BALANCE';

// Action Creators
const setUser = (user) => ({
  type: SET_USER,
  payload: user
});

const removeUser = () => ({
  type: REMOVE_USER
});

const updateBalance = (balance) => ({
  type: UPDATE_BALANCE,
  payload: balance
});

export const thunkAuthenticate = () => async (dispatch) => {
  // Do not use csrfFetch for this one, as the landing page does not require user to log in
  // This is related to the Layout.jsx that has thunkAuthenticate() in the useEffect
  // Therefore there are 2 options:
  // Option 1: 
  // use fetch for /api/auth & having the thunkAuthenticate in Layout.jsx
  // Option 2:
  // remove the thunkAuthenticate from Layout.jsx and use csrfFetch here
	const response = await fetch("/api/auth/");
	if (response.ok) {
		const data = await response.json();
		if (data.errors) {
			return;
		}

		dispatch(setUser(data));
	}
};

export const thunkLogin = (credentials) => async dispatch => {
  try {
    const response = await csrfFetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials)
    });

    if(response.ok) {
      const data = await response.json();
      dispatch(setUser(data)); // This should update the state.user
      return { success: true };
    } else {
      const errorData = await response.json();
      return { 
        success: false, 
        errors: errorData.errors || { credential: "Invalid credentials" } 
      };
    }
  } catch (error) {
    console.error("Login error:", error);
    
    if (error.json) {
      try {
        const errorData = await error.json();
        return { 
          success: false, 
          errors: errorData.errors || { credential: "An error occurred during login." } 
        };
      } catch (e) {
        console.error("Could not parse error response:", e);
      }
    }
    
    return { 
      success: false, 
      errors: { credential: "Invalid credentials. Please try again." } 
    };
  }
};

export const thunkSignup = (user) => async (dispatch) => {
  try {
    const response = await csrfFetch("/api/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(user)
    });

    // console.log("Signup Response Status:", response.status); // Debug log

    if(response.ok) {
      const data = await response.json();
      dispatch(setUser(data));
    } else {
      const errorMessages = await response.json();
      // Debug log
      // console.log("Signup Error Response:", {
      //   status: response.status,
      //   errorMessages
      // });
      return errorMessages;
    }
  } catch (error) {
    // Debug log
    // console.error("Signup Error Details:", {
    //   name: error.name,
    //   message: error.message,
    //   stack: error.stack
    // });
    
    // If it's a response error, try to parse it
    if (error.json) {
      try {
        const errorData = await error.json();
        // console.log("Error Response Data:", errorData); // Debug log
        return errorData;
      } catch (e) {
        console.error("Could not parse error response:", e);
      }
    }

    // return { 
    //   errors: {
    //     email: "Email already exists"  // Default error for duplicate email
    //   }
    // };
  }
};

export const thunkLogout = () => async (dispatch) => {
  await csrfFetch("/api/auth/logout");
  dispatch(removeUser());
};

export const thunkUpdateBalance = (amount) => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/portfolio', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ amount })
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(updateBalance(data.balance));
      return { success: true, balance: data.balance };
    } else {
      const errorData = await response.json();
      return { 
        success: false, 
        errors: errorData.errors || { general: 'Failed to update balance' }
      };
    }
  } catch (error) {
    console.error('Error updating balance:', error);
    return { 
      success: false, 
      errors: { general: 'An error occurred while updating your balance' }
    };
  }
};

const initialState = { user: null };

function sessionReducer(state = initialState, action) {
  switch (action.type) {
    case SET_USER:
      return { user: action.payload };
    case REMOVE_USER:
      return { user: null };
    case UPDATE_BALANCE:
      return {
        ...state,
        user: {
          ...state.user,
          balance: action.payload
        }
      };
    default:
      return state;
  }
}

export default sessionReducer;
