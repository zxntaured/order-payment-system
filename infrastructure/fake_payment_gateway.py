import uuid
from domain.order import Money
from application.interfaces import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    """Фейковый платежный шлюз"""
    
    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail
        self.charges = []
    
    def charge(self, order_id: str, amount: Money) -> str:
        if self.should_fail:
            raise ValueError("Payment gateway failure")
        
        transaction_id = f"txn_{uuid.uuid4().hex[:8]}"
        self.charges.append({
            'order_id': order_id,
            'amount': amount,
            'transaction_id': transaction_id
        })
        return transaction_id
    
    def get_charges_count(self) -> int:
        return len(self.charges)
