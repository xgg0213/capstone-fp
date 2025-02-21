import { useState, useEffect } from 'react';
import { csrfFetch } from '../../redux/csrf';

function OrderList() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState({});

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    const response = await csrfFetch('/api/orders');
    if (response.ok) {
      const data = await response.json();
      setOrders(data.orders);
    }
  };

  const processOrder = async (orderId) => {
    setLoading(prev => ({ ...prev, [orderId]: true }));
    try {
      const response = await csrfFetch(`/api/orders/${orderId}/process`, {
        method: 'POST'
      });
      if (response.ok) {
        fetchOrders(); // Refresh the list immediately
      }
    } catch (error) {
      alert("Failed to process order. Please try again.");
    }
    setLoading(prev => ({ ...prev, [orderId]: false }));
  };

  return (
    <div className="orders-list">
      <h2>Orders</h2>
      {orders.map(order => (
        <div key={order.id} className="order-item">
          <div className="order-details">
            <p>{order.symbol} - {order.shares} shares @ ${order.price}</p>
            <p>Type: {order.order_type} | Side: {order.side}</p>
            <p>Status: {order.status}</p>
          </div>
          {order.status === 'pending' && (
            <button 
              onClick={() => processOrder(order.id)}
              disabled={loading[order.id]}
            >
              {loading[order.id] ? 'Processing...' : 'Process Order'}
            </button>
          )}
          {order.status === 'filled' && (
            <div className="filled-details">
              <p>Filled at: ${order.filled_price}</p>
              <p>Time: {new Date(order.filled_at).toLocaleString()}</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default OrderList; 