import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { csrfFetch } from '../../redux/csrf';
import OpenModalButton from '../OpenModalButton';
import OrderForm from '../Orders/OrderForm';
import './Portfolio.css';

function Portfolio() {
    const [positions, setPositions] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [totalValue, setTotalValue] = useState(0);
    const user = useSelector(state => state.session.user);

    useEffect(() => {
        const fetchPortfolio = async () => {
            try {
                setIsLoading(true);
                const response = await csrfFetch('/api/portfolio/');
                if (response.ok) {
                    const data = await response.json();
                    // Ensure we always have an array, even if empty
                    setPositions(data.portfolios || []);
                    // Calculate total portfolio value
                    const total = (data.portfolios || []).reduce((sum, pos) => 
                        sum + (pos.shares * (pos.current_price || pos.average_price)), 0);
                    setTotalValue(total);
                } else {
                    const errorData = await response.json();
                    setError(errorData.error || 'Failed to fetch portfolio');
                }
            } catch (err) {
                setError('Error fetching portfolio data');
                console.error('Error fetching portfolio:', err);
            } finally {
                setIsLoading(false);
            }
        };

        if (user) {
            fetchPortfolio();
        }
    }, [user]);

    if (isLoading) return <div className="loading">Loading portfolio...</div>;
    if (error) return <div className="error">{error}</div>;
    if (!user) return <div className="login-prompt">Please log in to view your portfolio</div>;

    return (
        <div className="portfolio-container">
            <h2>Total Portfolio Value</h2>
            <h1>${totalValue.toFixed(2)}</h1>

            <div className="portfolio-summary">
                <div className="summary-row">
                    <span>Cash Balance</span>
                    <span className="portfolio-value">${user.balance?.toFixed(2)}</span>
                </div>

                <div className="summary-row">
                    <span>Stocks</span>
                    <span className="portfolio-value">${(totalValue + (user.balance || 0)).toFixed(2)}</span>
                </div>
            </div>

            <div className="portfolio-holdings">
                <h2>Stock Holdings</h2>
                <div className="holdings-table">
                    <div className="table-header">
                        <div>Symbol</div>
                        <div>Shares</div>
                        <div>Avg Cost</div>
                        <div>Price</div>
                        <div>Market Value</div>
                        <div>Total Return</div>
                        <div>Actions</div>
                    </div>

                    {positions.length === 0 ? (
                        <div className="no-positions">
                            <p>No positions in your portfolio yet.</p>
                            <button className="start-trading-btn">Start Trading</button>
                        </div>
                    ) : (
                        <div className="table-body">
                            {positions.map(position => (
                                <div key={position.id} className="position-row">
                                    <div className="symbol">{position.symbol}</div>
                                    <div className="shares">{position.shares}</div>
                                    <div className="price">${position.average_price?.toFixed(2)}</div>
                                    <div className="price">${position.current_price?.toFixed(2) || 'N/A'}</div>
                                    <div className="market-value">
                                        ${(position.shares * (position.current_price || position.average_price)).toFixed(2)}
                                    </div>
                                    <div className={`total-return ${position.total_return >= 0 ? 'gain' : 'loss'}`}>
                                        <div className="return-value">
                                            ${(position.shares * (position.current_price - position.average_price)).toFixed(2)}
                                        </div>
                                    </div>
                                    <div className="holding-actions">
                                        <OpenModalButton
                                            buttonText="Buy / Sell"
                                            className="place-order-btn"
                                            modalComponent={
                                                <OrderForm 
                                                    initialSymbol={position.symbol}
                                                    initialPrice={position.current_price}
                                                />
                                            }
                                        />
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Portfolio; 