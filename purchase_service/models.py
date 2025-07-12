import uuid

from sqlalchemy import Column, Integer, String, TIMESTAMP, UUID, TEXT, Numeric

import database


class Purchase(database.Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    supermarket_id = Column(String(10), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    items_list = Column(TEXT, nullable=False)
    total_amount = Column(Numeric, nullable=False)