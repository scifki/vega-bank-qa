import sqlite3


def get_balance(conn, name):
    """Возвращает остаток по счёту с указанным названием."""
    row = conn.execute("SELECT balance FROM accounts WHERE name = ?", (name,)).fetchone()
    if row is None:
        raise ValueError(f"Счёт не найден: {name}")
    return row[0]


def transfer(conn, source, target, amount):
    """Переводит amount со счёта source на счёт target в одной транзакции."""
    if amount <= 0:
        raise ValueError("Сумма перевода должна быть больше нуля")

    # BEGIN IMMEDIATE блокирует базу на запись: проверка остатка и два UPDATE
    # выполняются атомарно, поэтому деньги не могут «потеряться» или задвоиться.
    conn.execute("BEGIN IMMEDIATE")
    try:
        balance = get_balance(conn, source)
        if amount > balance:
            raise ValueError("Недостаточно средств")
        conn.execute("UPDATE accounts SET balance = balance - ? WHERE name = ?", (amount, source))
        conn.execute("UPDATE accounts SET balance = balance + ? WHERE name = ?", (amount, target))
    except Exception:
        conn.execute("ROLLBACK")
        raise
    else:
        conn.execute("COMMIT")


if __name__ == "__main__":
    # isolation_level=None — ручное управление транзакциями (autocommit).
    conn = sqlite3.connect(":memory:", isolation_level=None)
    conn.execute("CREATE TABLE accounts (name TEXT PRIMARY KEY, balance INTEGER)")
    conn.executemany(
        "INSERT INTO accounts VALUES (?, ?)",
        [("Текущий счёт", 10000), ("Накопительный счёт", 0)],
    )

    transfer(conn, "Текущий счёт", "Накопительный счёт", 500)
    assert get_balance(conn, "Текущий счёт") == 9500
    assert get_balance(conn, "Накопительный счёт") == 500

    try:
        transfer(conn, "Текущий счёт", "Накопительный счёт", 20000)
        raise AssertionError("Ожидалась ошибка")
    except ValueError:
        pass

    # После неудачного перевода остатки не изменились (откат транзакции)
    assert get_balance(conn, "Текущий счёт") == 9500
    assert get_balance(conn, "Накопительный счёт") == 500

    print("OK")
