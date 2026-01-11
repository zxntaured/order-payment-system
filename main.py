#!/usr/bin/env python3
"""
Пример использования системы оплаты заказов
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from decimal import Decimal
from domain.order import Order, Money
from application.pay_order_usecase import PayOrderUseCase, PayOrderCommand
from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway


def main():
    print("=" * 50)
    print("Система оплаты заказов - Пример использования")
    print("=" * 50)
    
    # Инициализация
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    use_case = PayOrderUseCase(repo, gateway)
    
    # Создаем заказ
    order = Order("order-001", "customer-001")
    
    # Добавляем товары
    order.add_line("Ноутбук", 1, Money(Decimal("999.99")))
    order.add_line("Мышь", 2, Money(Decimal("25.50")))
    order.add_line("Клавиатура", 1, Money(Decimal("75.25")))
    
    # Сохраняем заказ
    repo.save(order)
    
    print(f"\n📦 Заказ создан:")
    print(f"   ID: {order.id}")
    print(f"   Клиент: {order.customer_id}")
    print(f"   Статус: {order.status.value}")
    print(f"   Итоговая сумма: ${order.total_amount.amount}")
    print(f"   Количество позиций: {len(order.lines)}")
    
    # Оплачиваем заказ
    print("\n💳 Оплачиваем заказ...")
    command = PayOrderCommand(order_id="order-001")
    result = use_case.execute(command)
    
    # Выводим результат
    if result.success:
        print(f"\n✅ Оплата прошла успешно!")
        print(f"   ID транзакции: {result.transaction_id}")
        
        # Получаем обновленный заказ
        updated_order = repo.get_by_id("order-001")
        print(f"   Новый статус: {updated_order.status.value}")
    else:
        print(f"\n❌ Ошибка оплаты: {result.error_message}")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
