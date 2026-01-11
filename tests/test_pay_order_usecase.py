import sys
import os

# Добавляем корень проекта в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decimal import Decimal
from domain.order import Order, OrderStatus, Money
from application.pay_order_usecase import PayOrderUseCase, PayOrderCommand
from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway


def test_successful_payment():
    """Тест успешной оплаты корректного заказа"""
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    use_case = PayOrderUseCase(repo, gateway)
    
    # Создаем заказ
    order = Order("order-1", "customer-1")
    order.add_line("prod-1", 2, Money(Decimal("10.5")))
    order.add_line("prod-2", 1, Money(Decimal("5.0")))
    repo.save(order)
    
    # Оплачиваем
    result = use_case.execute(PayOrderCommand("order-1"))
    
    assert result.success is True
    assert result.order_id == "order-1"
    assert result.transaction_id is not None
    assert result.error_message is None
    
    # Проверяем статус заказа
    updated_order = repo.get_by_id("order-1")
    assert updated_order.status == OrderStatus.PAID
    
    # Проверяем, что платеж был выполнен
    assert gateway.get_charges_count() == 1


def test_payment_empty_order():
    """Тест ошибки при оплате пустого заказа"""
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    use_case = PayOrderUseCase(repo, gateway)
    
    # Создаем пустой заказ
    order = Order("order-2", "customer-2")
    repo.save(order)
    
    # Пытаемся оплатить
    result = use_case.execute(PayOrderCommand("order-2"))
    
    assert result.success is False
    assert "empty" in result.error_message.lower()
    assert gateway.get_charges_count() == 0


def test_double_payment():
    """Тест ошибки при повторной оплате"""
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    use_case = PayOrderUseCase(repo, gateway)
    
    # Создаем заказ
    order = Order("order-3", "customer-3")
    order.add_line("prod-1", 1, Money(Decimal("10.0")))
    repo.save(order)
    
    # Первая оплата
    result1 = use_case.execute(PayOrderCommand("order-3"))
    assert result1.success is True
    
    # Вторая оплата
    result2 = use_case.execute(PayOrderCommand("order-3"))
    assert result2.success is False
    assert "already paid" in result2.error_message.lower()


def test_cannot_modify_after_payment():
    """Тест невозможности изменения заказа после оплаты"""
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    use_case = PayOrderUseCase(repo, gateway)
    
    # Создаем и оплачиваем заказ
    order = Order("order-4", "customer-4")
    order.add_line("prod-1", 1, Money(Decimal("10.0")))
    repo.save(order)
    
    use_case.execute(PayOrderCommand("order-4"))
    
    # Пытаемся изменить оплаченный заказ
    paid_order = repo.get_by_id("order-4")
    
    try:
        paid_order.add_line("prod-2", 1, Money(Decimal("5.0")))
        assert False, "Should have raised an exception"
    except ValueError as e:
        assert "modify" in str(e).lower()


def test_correct_total_calculation():
    """Тест корректного расчета итоговой суммы"""
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    use_case = PayOrderUseCase(repo, gateway)
    
    order = Order("order-5", "customer-5")
    order.add_line("prod-1", 3, Money(Decimal("7.5")))
    order.add_line("prod-2", 2, Money(Decimal("12.0")))
    order.add_line("prod-3", 1, Money(Decimal("5.5")))
    
    repo.save(order)
    
    result = use_case.execute(PayOrderCommand("order-5"))
    
    assert result.success is True
    
    # Проверяем расчет: (7.5*3) + (12*2) + (5.5*1) = 22.5 + 24 + 5.5 = 52
    updated_order = repo.get_by_id("order-5")
    assert updated_order.total_amount.amount == Decimal("52.0")


def run_all_tests():
    """Функция для запуска всех тестов"""
    tests = [
        test_successful_payment,
        test_payment_empty_order,
        test_double_payment,
        test_cannot_modify_after_payment,
        test_correct_total_calculation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__} passed")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} error: {e}")
            failed += 1
    
    print(f"\n📊 Результат: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 Все тесты прошли успешно!")
        return True
    else:
        print("💥 Некоторые тесты не прошли")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
