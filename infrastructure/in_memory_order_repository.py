from typing import Dict, Optional
import copy
from domain.order import Order
from application.interfaces import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """In-memory реализация репозитория заказов"""
    
    def __init__(self):
        self._orders: Dict[str, Order] = {}
    
    def get_by_id(self, order_id: str) -> Optional[Order]:
        order = self._orders.get(order_id)
        if order:
            # Возвращаем копию, чтобы избежать побочных эффектов
            return copy.deepcopy(order)
        return None
    
    def save(self, order: Order) -> None:
        self._orders[order.id] = copy.deepcopy(order)
    
    def clear(self):
        """Очистить хранилище (для тестов)"""
        self._orders.clear()
