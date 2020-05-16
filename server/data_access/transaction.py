from server.data_models.transaction import Transaction
from server.database import db_session


def add_transaction(
    user_id: int,
    ticker: str,
    quantity: float,
    price: float,
):
    """Store the transaction in the database"""
    follows = Transaction(
        user_id=user_id,
        ticker=ticker,
        quantity=quantity,
        price=price,
    )
    db_session.add(follows)
    db_session.commit()
    return True


def get_transactions_by_user_id(user_id: int):
    """Get the list of transactions made by the given user"""
    return Transaction.query.filter(
        Transaction.user_id == user_id,
    ).all()
