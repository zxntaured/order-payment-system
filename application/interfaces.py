from abc import ABC, abstractmethod
from typing import Optional
from domain.order import Order, Money


class OrderRepository(ABC):
    """Порт для работы с заказами"""
    
    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        pass
    
    @abstractmethod
    def save(self, order: Order) -> None:
        pass


class PaymentGateway(ABC):
    """Порт для платежного шлюза"""
    
    @abstractmethod
    def charge(self, order_id: str, amount: Money) -> str:
        pass
