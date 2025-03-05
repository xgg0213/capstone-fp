// import { csrfFetch } from './csrf';
// import Cookies from 'js-cookie';

// // Action Types
// const SET_USER = 'session/SET_USER';
// const REMOVE_USER = 'session/REMOVE_USER';
// const UPDATE_BALANCE = 'session/UPDATE_BALANCE';

// // Action Creators
// const setUser = (user) => ({
//   type: SET_USER,
//   payload: user
// });

// const removeUser = () => ({
//   type: REMOVE_USER
// });

// const updateBalance = (balance) => ({
//   type: UPDATE_BALANCE,
//   payload: balance
// });

// // Thunks
// export const thunkAuthenticate = () => async (dispatch) => {
//   try {
//     const response = await csrfFetch("/api/auth/");
//     if (response.ok) {
//       const data = await response.json();
//       dispatch(setUser(data));
//     }
//   } catch (error) {
//     // Silently fail - user is not authenticated
//     console.log("User not authenticated");
//   }
// };

// export const thunkLogin = (credentials) => async dispatch => {
//   const response = await csrfFetch("/api/auth/login", {
//     method: "POST",
//     headers: { 
//       "Content-Type": "application/json",
//       'XSRF-TOKEN': Cookies.get('XSRF-TOKEN')
//     },
//     body: JSON.stringify(credentials)
//   });

//   if (response.ok) {
//     const data = await response.json();
//     dispatch(setUser(data));
//     return null;
//   } else if (response.status < 500) {
//     const data = await response.json();
//     if (data.errors) throw data;
//   } else {
//     return ["An error occurred. Please try again."];
//   }
// };

// export const thunkSignup = (user) => async (dispatch) => {
//   try {
//     const response = await csrfFetch("/api/auth/signup", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(user)
//     });

//     if (response.ok) {
//       const data = await response.json();
//       dispatch(setUser(data));
//       return null;
//     } else {
//       const data = await response.json();
//       return data;
//     }
//   } catch (error) {
//     console.error("Signup error:", error);
//     if (error.status === 401) {
//       const errorData = await error.json();
//       return errorData;
//     }
//     return {
//       errors: {
//         general: "An error occurred during signup. Please try again."
//       }
//     };
//   }
// };

// export const thunkLogout = () => async (dispatch) => {
//   const response = await csrfFetch("/api/auth/logout", {
//     headers: {
//       "Content-Type": "application/json",
//       'XSRF-TOKEN': Cookies.get('XSRF-TOKEN')
//     }
//   });

//   if (response.ok) {
//     dispatch(removeUser());
//   }
// };

// export const thunkUpdateBalance = (amount) => async (dispatch) => {
//   try {
//     const response = await csrfFetch('/api/portfolio', {
//       method: 'POST',
//       headers: { 
//         'Content-Type': 'application/json',
//         'XSRF-TOKEN': Cookies.get('XSRF-TOKEN')
//       },
//       body: JSON.stringify({ amount })
//     });

//     if (response.ok) {
//       const data = await response.json();
//       dispatch(updateBalance(data.balance));
//       return data.balance;
//     } else {
//       const error = await response.json();
//       throw error;
//     }
//   } catch (error) {
//     throw error;
//   }
// };

// const initialState = { user: null };

// const sessionReducer = (state = initialState, action) => {
//   switch (action.type) {
//     case SET_USER:
//       return { user: action.payload };
//     case REMOVE_USER:
//       return { user: null };
//     case UPDATE_BALANCE:
//       return {
//         ...state,
//         user: {
//           ...state.user,
//           balance: action.payload
//         }
//       };
//     default:
//       return state;
//   }
// };

// export default sessionReducer;


import {csrfFetch} from "./csrf"

// Action Types
const SET_USER = 'session/setUser';
const REMOVE_USER = 'session/removeUser';

// Action Creators
const setUser = (user) => ({
  type: SET_USER,
  payload: user
});

const removeUser = () => ({
  type: REMOVE_USER
});

export const thunkAuthenticate = () => async (dispatch) => {
  // Do not use csrfFetch for this one, as the landing page does not require user to log in
  // This is related to the Layout.jsx that has thunkAuthenticate() in the useEffect
  // Therefore there are 2 options:
  // Option 1: 
  // use fetch for /api/auth & having the thunkAuthenticate in Layout.jsx
  // Option 2:
  // remove the thunkAuthenticate from Layout.jsx and use csrfFetch here
	const response = await csrfFetch("/api/auth/");
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
      dispatch(setUser(data));  // This should update the state.user
      return null;  // Return null to indicate success
    } else {
      const errorMessages = await response.json();
      return errorMessages;
    }
  } catch (error) {
    if (error.json) {
      try {
        const errorData = await error.json();
        return errorData;
      } catch (e) {
        console.error("Could not parse error response:", e);
        return { errors: ["An error occurred during login."] };
      }
    }
    return { errors: ["An error occurred during login."] };
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

const initialState = { user: null };

function sessionReducer(state = initialState, action) {
  switch (action.type) {
    case SET_USER:
      return { user: action.payload };
    case REMOVE_USER:
      return { user: null };
    default:
      return state;
  }
}

export default sessionReducer;
