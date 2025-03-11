import { csrfFetch } from './csrf';

// Action Types
const LOAD_PORTFOLIO = 'portfolio/LOAD_PORTFOLIO';
const UPDATE_PORTFOLIO = 'portfolio/UPDATE_PORTFOLIO';
const SET_PORTFOLIO_ERROR = 'portfolio/SET_PORTFOLIO_ERROR';

// Action Creators
const loadPortfolio = (portfolioData) => ({
  type: LOAD_PORTFOLIO,
  payload: portfolioData
});

const updatePortfolio = (portfolioData) => ({
  type: UPDATE_PORTFOLIO,
  payload: portfolioData
});

const setPortfolioError = (error) => ({
  type: SET_PORTFOLIO_ERROR,
  payload: error
});

// Thunk Actions
export const fetchPortfolio = () => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/portfolio/');
    
    if (response.ok) {
      const data = await response.json();
      dispatch(loadPortfolio(data.portfolios || []));
      return data.portfolios || [];
    } else {
      const errorData = await response.json();
      dispatch(setPortfolioError(errorData.error || 'Failed to fetch portfolio'));
      return null;
    }
  } catch (error) {
    console.error('Error fetching portfolio:', error);
    dispatch(setPortfolioError('Error fetching portfolio data'));
    return null;
  }
};

// Initial State
const initialState = {
  positions: [],
  totalValue: 0,
  error: null,
  loading: false
};

// Reducer
const portfolioReducer = (state = initialState, action) => {
  switch (action.type) {
    case LOAD_PORTFOLIO:
      return {
        ...state,
        positions: action.payload,
        totalValue: action.payload.reduce((sum, pos) => 
          sum + (pos.shares * (pos.current_price || pos.average_price)), 0),
        error: null,
        loading: false
      };
    case UPDATE_PORTFOLIO:
      return {
        ...state,
        positions: action.payload,
        totalValue: action.payload.reduce((sum, pos) => 
          sum + (pos.shares * (pos.current_price || pos.average_price)), 0),
        error: null,
        loading: false
      };
    case SET_PORTFOLIO_ERROR:
      return {
        ...state,
        error: action.payload,
        loading: false
      };
    default:
      return state;
  }
};

export default portfolioReducer; 