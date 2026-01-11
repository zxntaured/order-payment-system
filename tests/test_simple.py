#!/usr/bin/env python3
"""Простой тест для проверки окружения"""

def test_addition():
    assert 1 + 1 == 2

def test_strings():
    assert "hello".upper() == "HELLO"

def test_imports():
    try:
        from decimal import Decimal
        from datetime import datetime
        print("✅ Все импорты работают")
        return True
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

if __name__ == "__main__":
    test_addition()
    test_strings()
    test_imports()
    print("✅ Все простые тесты прошли успешно!")
