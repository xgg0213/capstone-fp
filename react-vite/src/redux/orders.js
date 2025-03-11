import { csrfFetch } from './csrf';
import { thunkAuthenticate } from './session';

// Action Types
const PLACE_ORDER = 'orders/PLACE_ORDER';
const GET_ORDERS = 'orders/GET_ORDERS';
const SET_ORDER_ERROR = 'orders/SET_ORDER_ERROR';
const CLEAR_ORDER_ERROR = 'orders/CLEAR_ORDER_ERROR';

// Action Creators
const placeOrder = (order) => ({
  type: PLACE_ORDER,
  payload: order
});

const getOrders = (orders) => ({
  type: GET_ORDERS,
  payload: orders
});

const setOrderError = (error) => ({
  type: SET_ORDER_ERROR,
  payload: error
});

const clearOrderError = () => ({
  type: CLEAR_ORDER_ERROR
});

// Thunk Actions
export const thunkPlaceOrder = (orderData) => async (dispatch) => {
  try {
    dispatch(clearOrderError());
    
    // First, try to authenticate to ensure the session is valid
    await dispatch(thunkAuthenticate());
    
    const response = await csrfFetch('/api/orders/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(orderData)
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(placeOrder(data));
      
      // Refresh user session data to update balance
      await dispatch(thunkAuthenticate());
      
      return { success: true, order: data };
    } else {
      const data = await response.json();
      let errorMessage = 'An error occurred while placing the order.';
      
      if (data.errors) {
        errorMessage = Array.isArray(data.errors) ? data.errors[0] : data.errors;
      } else if (data.error) {
        errorMessage = data.error;
      }
      
      dispatch(setOrderError(errorMessage));
      return { success: false, error: errorMessage };
    }
  } catch (error) {
    console.error('Error placing order:', error);
    
    // Handle authentication errors
    if (error.authError) {
      const errorMessage = 'Your session has expired. Please log in again.';
      dispatch(setOrderError(errorMessage));
      return { 
        success: false, 
        error: errorMessage,
        authError: true
      };
    }
    
    // Handle other errors
    let errorMessage = 'An error occurred while placing the order.';
    
    try {
      // Try to parse the error response
      const data = await error.json();
      if (data.errors) {
        errorMessage = Array.isArray(data.errors) ? data.errors[0] : data.errors;
      } else if (data.error) {
        errorMessage = data.error;
      }
    } catch (e) {
      // If error can't be parsed as JSON, use the default message
      console.error('Error parsing error response:', e);
    }
    
    dispatch(setOrderError(errorMessage));
    return { success: false, error: errorMessage };
  }
};

export const thunkGetOrders = () => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/orders/');
    
    if (response.ok) {
      const data = await response.json();
      dispatch(getOrders(data.orders));
      return data.orders;
    } else {
      const data = await response.json();
      dispatch(setOrderError(data.error || 'Failed to fetch orders'));
      return null;
    }
  } catch (error) {
    console.error('Error fetching orders:', error);
    dispatch(setOrderError('An error occurred while fetching orders.'));
    return null;
  }
};

// Initial State
const initialState = {
  orders: [],
  error: null,
  loading: false
};

// Reducer
const ordersReducer = (state = initialState, action) => {
  switch (action.type) {
    case PLACE_ORDER:
      return {
        ...state,
        orders: [action.payload, ...state.orders],
        error: null
      };
    case GET_ORDERS:
      return {
        ...state,
        orders: action.payload,
        error: null
      };
    case SET_ORDER_ERROR:
      return {
        ...state,
        error: action.payload
      };
    case CLEAR_ORDER_ERROR:
      return {
        ...state,
        error: null
      };
    default:
      return state;
  }
};

export default ordersReducer; 