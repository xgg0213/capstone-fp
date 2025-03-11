import { useModal } from '../../context/Modal';
import './ConfirmModal.css';

function ConfirmModal({ message, onConfirm, onCancel }) {
  const { closeModal } = useModal();

  const handleConfirm = () => {
    if (onConfirm) onConfirm();
    closeModal();
  };

  const handleCancel = () => {
    if (onCancel) onCancel();
    closeModal();
  };

  return (
    <div className="confirm-modal">
      <div className="confirm-content">
        <p>{message}</p>
        <div className="confirm-buttons">
          <button className="cancel-btn" onClick={handleCancel}>Cancel</button>
          <button className="confirm-btn" onClick={handleConfirm}>Confirm</button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmModal; 