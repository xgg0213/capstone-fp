import { createStore, combineReducers, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import sessionReducer from './session';
import symbolsReducer from './symbols';
import watchlistReducer from './watchlist';

const rootReducer = combineReducers({
    session: sessionReducer,
    symbols: symbolsReducer,
    watchlists: watchlistReducer
});

// ... rest of the store configuration 