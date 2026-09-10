# commission-guard
A Genlayer intelligent contract for decentralized freelance commission dispute resolution
What it does
Commission Guard manages a freelance commission from project creation through dispute resolution.
The contract:
	●	Stores the client’s requirements.
	●	Allows the designated artist to submit work.
	●	Allows the client or artist to open a dispute after submission.
	●	Uses GenLayer’s intelligent contract execution to evaluate the submitted work against the stored requirements.
	●	Records which criteria were met and which failed.
	●	Resolves the dispute and determines the outcome.
	●	Records the winning party and reason for the resolution.
Dispute lifecycle
CREATED → SUBMITTED → DISPUTED → RESOLVED
Resolution
	●	APPROVE → ARTIST
	●	REJECT → CLIENT
The contract keeps the requirements, submission, decision, evaluation criteria, winner, and resolution reason on-chain as part of the dispute record.