import uuid


class Opportunity:
    VALID_STATUSES = ("saved", "applied", "interviewed", "accepted", "rejected")

    def __init__(self, company, role, deadline, status="saved", id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.company = company
        self.role = role
        self.deadline = deadline
        self.status = status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {value}")
        self._status = value

    def __str__(self):
        deadline = self.deadline if self.deadline else "No deadline"
        return f"{self.id} | {self.company} | {self.role} | {deadline} | {self.status}"
