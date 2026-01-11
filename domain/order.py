from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List


class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class Money:
    """Value Object для денежных сумм"""
    amount: Decimal
    currency: str = "USD"
    
    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __mul__(self, quantity: int) -> 'Money':
        return Money(self.amount * Decimal(quantity), self.currency)


@dataclass
class OrderLine:
    """Строка заказа"""
    product_id: str
    quantity: int
    price: Money
    
    @property
    def total(self) -> Money:
        return self.price * self.quantity


class Order:
    """Агрегат Заказ"""
    
    def __init__(self, order_id: str, customer_id: str):
        self.id = order_id
        self.customer_id = customer_id
        self.lines: List[OrderLine] = []
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def add_line(self, product_id: str, quantity: int, price: Money) -> None:
        """Добавить товар в заказ"""
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify order after payment")
        
        # Проверяем, не существует ли уже такой товар
        for line in self.lines:
            if line.product_id == product_id:
                raise ValueError(f"Product {product_id} already in order")
        
        self.lines.append(OrderLine(product_id, quantity, price))
        self.updated_at = datetime.now()
    
    @property
    def total_amount(self) -> Money:
        """Рассчитать общую сумму заказа"""
        if not self.lines:
            return Money(Decimal('0'))
        
        total = Money(Decimal('0'))
        for line in self.lines:
            total += line.total
        return total
    
    def pay(self) -> None:
        """Оплатить заказ"""
        # Инвариант 1: нельзя оплатить пустой заказ
        if not self.lines:
            raise ValueError("Cannot pay an empty order")
        
        # Инвариант 2: нельзя оплатить заказ повторно
        if self.status == OrderStatus.PAID:
            raise ValueError("Order is already paid")
        
        # Инвариант 3: сумма должна быть положительной
        if self.total_amount.amount <= 0:
            raise ValueError("Order total must be positive")
        
        self.status = OrderStatus.PAID
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        return f"Order(id={self.id}, status={self.status.value}, total={self.total_amount.amount})"
