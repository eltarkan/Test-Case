from typing import List


class UserQueue:
    user_id: str
    transaction_amount: float
    card_no: str


class Queue:
    def __init__(self):
        self.queues = []

    def push(self, data):
        self.queues.append(data)

    def pop(self):
        if len(self.queues) == 0:
            return None
        return self.queues.pop(0)


TransactionQueue = Queue()
