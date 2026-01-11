from dataclasses import dataclass
from typing import Optional
from domain.order import Order, Money
from application.interfaces import OrderRepository, PaymentGateway


@dataclass
class PayOrderCommand:
    order_id: str


@dataclass
class PayOrderResult:
    success: bool
    order_id: str
    transaction_id: Optional[str] = None
    error_message: Optional[str] = None


class PayOrderUseCase:
    """Use Case для оплаты заказа"""
    
    def __init__(self, order_repo: OrderRepository, payment_gateway: PaymentGateway):
        self.order_repo = order_repo
        self.payment_gateway = payment_gateway
    
    def execute(self, command: PayOrderCommand) -> PayOrderResult:
        try:
            # 1. Загружаем заказ
            order = self.order_repo.get_by_id(command.order_id)
            if not order:
                return PayOrderResult(
                    success=False,
                    order_id=command.order_id,
                    error_message="Order not found"
                )
            
            # 2. Выполняем доменную операцию
            order.pay()
            
            # 3. Вызываем платежный шлюз
            transaction_id = self.payment_gateway.charge(order.id, order.total_amount)
            
            # 4. Сохраняем заказ
            self.order_repo.save(order)
            
            return PayOrderResult(
                success=True,
                order_id=order.id,
                transaction_id=transaction_id
            )
            
        except ValueError as e:
            return PayOrderResult(
                success=False,
                order_id=command.order_id,
                error_message=str(e)
            )
        except Exception as e:
            return PayOrderResult(
                success=False,
                order_id=command.order_id,
                error_message=f"Payment failed: {str(e)}"
            )
