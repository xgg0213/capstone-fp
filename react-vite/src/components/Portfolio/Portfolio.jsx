import { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchPortfolio } from '../../redux/portfolio';
import OpenModalButton from '../OpenModalButton';
import PlaceOrderModal from '../Modals/PlaceOrderModal';
import './Portfolio.css';

function Portfolio() {
    const dispatch = useDispatch();
    const [isLoading, setIsLoading] = useState(true);
    const user = useSelector(state => state.session.user);
    const portfolioState = useSelector(state => state.portfolio);
    const positions = portfolioState.positions || [];
    const totalValue = portfolioState.totalValue || 0;
    const error = portfolioState.error;

    useEffect(() => {
        const loadPortfolio = async () => {
            try {
                setIsLoading(true);
                await dispatch(fetchPortfolio());
            } catch (err) {
                console.error('Error loading portfolio:', err);
            } finally {
                setIsLoading(false);
            }
        };

        if (user) {
            loadPortfolio();
        }
    }, [dispatch, user]);

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
                                                <PlaceOrderModal 
                                                    symbol={position.symbol}
                                                    currentPrice={position.current_price}
                                                    initialOrderType="buy"
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