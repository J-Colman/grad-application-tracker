import datetime

date = datetime.date

class Opportunity:
	def __init__(self, company, role, deadline):
		self.company = company
		self.role = role
		self.deadline = deadline

	def __str__(self):
		return f"{self.company} | {self.role} | {self.deadline}"

# Fictional sample opportunities
grad_opps = [   Opportunity("RedHat", "Junior Developer", date(2026, 11, 4)),
		        Opportunity("Google DeepMind", "Junior ML Engineer", date(2027, 1, 10)),
		        Opportunity("Anthropic", "Junior MLOps Engineer", date(2026, 10, 27))]

for op in grad_opps:
	print(op)
