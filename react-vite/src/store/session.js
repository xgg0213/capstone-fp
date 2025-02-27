// Function to get CSRF token from cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Action Types
const SET_USER = 'session/SET_USER';
const REMOVE_USER = 'session/REMOVE_USER';
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

// Thunks
export const thunkAuthenticate = () => async (dispatch) => {
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
  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials)
  });

  if (response.ok) {
    const data = await response.json();
    dispatch(setUser(data));
    return null;
  } else if (response.status < 500) {
    const data = await response.json();
    if (data.errors) throw data;
  } else {
    return ["An error occurred. Please try again."];
  }
};

export const thunkUpdateBalance = (amount) => async (dispatch) => {
  try {
    const response = await fetch('/api/portfolio', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount })
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(updateBalance(data.balance));
      return data.balance;
    } else {
      const error = await response.json();
      throw error;
    }
  } catch (error) {
    throw error;
  }
};

// Reducer
const initialState = { user: null };

const sessionReducer = (state = initialState, action) => {
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
};

export default sessionReducer; 