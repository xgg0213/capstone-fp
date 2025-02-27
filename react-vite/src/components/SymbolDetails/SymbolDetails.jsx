import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchSymbol, fetchSymbolPrices } from '../../redux/symbols';
import './SymbolDetails.css';

const SymbolDetails = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { symbol } = useParams();
    const [priceHistory, setPriceHistory] = useState([]);
    
    const symbolData = useSelector(state => 
        state.symbols.allSymbols[symbol?.toUpperCase()]
    );

    useEffect(() => {
        if (symbol) {
            dispatch(fetchSymbol(symbol))
                .then(data => {
                    if (!data) {
                        navigate('/dashboard');
                    }
                })
                .catch(() => navigate('/dashboard'));

            dispatch(fetchSymbolPrices(symbol))
                .then(prices => setPriceHistory(prices));
        }
    }, [dispatch, symbol, navigate]);

    if (!symbolData) return <div>Loading...</div>;

    return (
        <div className="symbol-details">
            <div className="symbol-header">
                <h2>{symbolData.company_name} ({symbolData.symbol})</h2>
                <div className="current-price">
                    ${symbolData.current_price}
                    <span className={`price-change ${symbolData.price_change_pct >= 0 ? 'positive' : 'negative'}`}>
                        {symbolData.price_change_pct}%
                    </span>
                </div>
            </div>
            
            <div className="price-stats">
                <div>Daily High: ${symbolData.daily_high}</div>
                <div>Daily Low: ${symbolData.daily_low}</div>
                <div>Volume: {symbolData.daily_volume?.toLocaleString()}</div>
            </div>

            <div className="price-history">
                <h3>Price History</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Open</th>
                            <th>High</th>
                            <th>Low</th>
                            <th>Close</th>
                            <th>Volume</th>
                        </tr>
                    </thead>
                    <tbody>
                        {priceHistory.map(price => (
                            <tr key={price.date}>
                                <td>{new Date(price.date).toLocaleDateString()}</td>
                                <td>${price.open}</td>
                                <td>${price.high}</td>
                                <td>${price.low}</td>
                                <td>${price.close}</td>
                                <td>{price.volume?.toLocaleString()}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default SymbolDetails; 