# Лабораторная работа 7: Архитектура, слои и DDD-lite

## Описание
Реализация системы оплаты заказа с использованием слоистой архитектуры и принципов DDD-lite.

## Структура проекта
order-payment-system/
├── domain/ # Доменный слой
│ ├── init.py
│ └── order.py # Доменная модель: Order, OrderLine, Money, OrderStatus
├── application/ # Слой приложения
│ ├── init.py
│ ├── interfaces.py # Интерфейсы репозитория и платежного шлюза
│ └── pay_order_usecase.py # Use Case оплаты заказа
├── infrastructure/ # Инфраструктурный слой
│ ├── init.py
│ ├── in_memory_order_repository.py
│ └── fake_payment_gateway.py
├── tests/ # Тесты
│ ├── init.py
│ ├── test_simple.py
│ └── test_pay_order_usecase.py
├── .github/workflows/ # CI/CD
│ └── ci.yml
├── main.py # Пример использования
├── requirements.txt
└── README.md

## Реализованные требования

### ✅ Доменный слой
- **Order** - сущность заказа
- **OrderLine** - часть агрегата заказа
- **Money** - value object для денежных сумм
- **OrderStatus** - перечисление статусов заказа

### ✅ Инварианты
1. Нельзя оплатить пустой заказ ✅
2. Нельзя оплатить заказ повторно ✅
3. После оплаты нельзя менять строки заказа ✅
4. Итоговая сумма равна сумме строк ✅

### ✅ Application слой
- **PayOrderUseCase** - use case для оплаты заказа
- Интерфейсы: OrderRepository, PaymentGateway

### ✅ Infrastructure слой
- **InMemoryOrderRepository** - реализация репозитория в памяти
- **FakePaymentGateway** - фейковый платежный шлюз

### ✅ Тесты
Все тесты проходят:
- Успешная оплата корректного заказа
- Ошибка при оплате пустого заказа
- Ошибка при повторной оплате
- Невозможность изменения заказа после оплаты
- Корректный расчет итоговой суммы
