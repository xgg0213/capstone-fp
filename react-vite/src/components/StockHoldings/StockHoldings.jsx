import OpenModalButton from '../OpenModalButton/OpenModalButton';
import PlaceOrderModal from '../Modals/PlaceOrderModal';

// ... in your component
return (
  <div className="stock-item">
    <div className="stock-info">
      {/* ... existing stock info ... */}
    </div>
    <div className="stock-actions">
      <div className="stock-price">
        {/* ... existing price info ... */}
      </div>
      <OpenModalButton
        buttonText="Place Order"
        className="place-order-btn"
        modalComponent={
          <PlaceOrderModal
            symbol={stock.symbol}
            currentPrice={stock.current_price}
            onConfirm={handlePlaceOrder}
          />
        }
      />
    </div>
  </div>
); 