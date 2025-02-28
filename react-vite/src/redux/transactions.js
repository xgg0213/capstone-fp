import { csrfFetch } from './csrf';

// Action Types
const LOAD_TRANSACTIONS = 'transactions/LOAD';
const ADD_TRANSACTION = 'transactions/ADD';

// Action Creators
const loadTransactions = (transactions) => ({
  type: LOAD_TRANSACTIONS,
  transactions
});

const addTransaction = (transaction) => ({
  type: ADD_TRANSACTION,
  transaction
});

// Thunks
export const fetchTransactions = () => async dispatch => {
  try {
    const response = await csrfFetch('/api/transactions/');
    if (response.ok) {
      const data = await response.json();
      dispatch(loadTransactions(data.transactions));
      return data.transactions;
    }
  } catch (error) {
    console.error('Error fetching transactions:', error);
    throw error;
  }
};

export const createTransaction = (transactionData) => async dispatch => {
  try {
    const response = await csrfFetch('/api/transactions/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(transactionData)
    });

    if (response.ok) {
      const transaction = await response.json();
      dispatch(addTransaction(transaction));
      return transaction;
    }
  } catch (error) {
    console.error('Error creating transaction:', error);
    throw error;
  }
};

// Initial State
const initialState = {
  transactions: []
};

// Reducer
const transactionsReducer = (state = initialState, action) => {
  switch (action.type) {
    case LOAD_TRANSACTIONS:
      return { ...state, transactions: action.transactions };
    case ADD_TRANSACTION:
      return { 
        ...state, 
        transactions: [action.transaction, ...state.transactions] 
      };
    default:
      return state;
  }
};

export default transactionsReducer; 