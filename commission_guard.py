# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class CommissionGuard(gl.Contract):
    client: Address
    artist: str 
    requirements: str
    submission: str
    status: str
    decision: str
    resolution_outcome: str
    resolution_summary: str
    winner: str
    resolution_reason: str
    project_created: bool

    def __init__(self):
        self.client = Address("0x0000000000000000000000000000000000000000")
        self.artist = ""
        self.requirements = ""
        self.submission = ""
        self.status = "CREATED"
        self.decision = ""
        self.resolution_outcome = ""
        self.resolution_summary = ""
        self.winner = ""
        self.resolution_reason = ""
        self.project_created = False

    @gl.public.write
    def create_project(self, artist: str, requirements: str):
        assert not self.project_created, "Project already exists"
        assert self.project_created == False, "Project already exists"
        self.client = gl.message.sender_address
        self.artist = artist
        self.requirements = requirements
        self.project_created = True
        self.submission = ""
        self.status = "CREATED"
        self.decision = ""
        self.resolution_outcome = ""
        self.resolution_summary= ""
        self.winner = ""
        self.resolution_reason = ""
        self.project_created = True

    @gl.public.write
    def submit_work(self, submission: str) -> None:
        assert str(gl.message.sender_address) == self.artist, "Only the artist can submit work"
        self.submission = submission
        self.status = "SUBMITTED"

    @gl.public.write
    def open_dispute(self) -> None:
        assert (
            gl.message.sender_address == self.client
            or str(gl.message.sender_address) == self.artist
        ), "Only the client or artist can open a dispute"

        assert self.status == "SUBMITTED", "Work must be submitted before opening a dispute"

        self.status = "DISPUTED"    

    @gl.public.write
    def resolve_dispute(self) -> None:
        assert self.status == "DISPUTED", "project must be disputed before resolution"
        assert self.decision == "", "Dispute has already been resolved"

        requirements = self.requirements
        submission = self.submission

        def leader_fn():
            prompt = f"""
            you are evaluating a freelance project dispute.

            PROJECT REQUIREMENTS:
            {requirements}

            SUBMITTED WORK:
            {submission}

            Evaluate the submitted work against the project requirements.

            Identify which important requirements are satisfied and which are not.

            A requirement should not only be considered satisfied when the submitted work provides clear evidence that it meets it.

            Respond as JSON using exactly this structure:

            {{
                "decision": "APPROVE" or "REJECT",
                "criteria_met": ["requirement 1", "requirement 2"],
                "criteria_failed": ["requirement 3"]
            }}

            Use "APPROVE" only when the important requirements are satisfied.
            Use "REJECT" when one or more important requirements are not satisfied.
            """

            return gl.nondet.exec_prompt(prompt, response_format="json")

        def validator_fn(leader_result):
            if not isinstance(leader_result, gl.vm.Return):
                return False

            validator_result = leader_fn()

            if not isinstance(validator_result, dict):
                return False

            if "decision" not in validator_result:
                return False
            
            if validator_result["decision"] not in ["APPROVE", "REJECT"]:
                return False
            
            if "criteria_met" not in validator_result:
                return False
            
            if "criteria_failed" not in validator_result:
                return False

            return (
                validator_result["decision"]
                ==leader_result.calldata["decision"]
            )

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        self.decision = result["decision"]
        self.status = "RESOLVED"
        self.resolution_outcome = result["decision"]

        if result["decision"] == "APPROVE":
            self.winner = "ARTIST"
            self.resolution_reason = (
                "The submitted work satisfies the important project requirements."
            )
        else:
            self.winner = "CLIENT"
            self.resolution_reason = (
                "The submitted work does not satisfy one or more important project requirements."
            )
        self.resolution_summary = (
            "winner: "
            + self.winner
            + " | Criteria met: "
            + str(result["criteria_met"])
            + " | Criteria failed: "
            + str(result["criteria_failed"])
            
        )

    @gl.public.view
    def get_status(self) -> str:
         return self.status

    @gl.public.view
    def get_requirements(self) -> str:
         return self.requirements

    @gl.public.view
    def get_submission(self) -> str:
         return self.submission

    @gl.public.view
    def get_decision(self) -> str:
         return self.decision

    @gl.public.view
    def get_resolution_outcome(self) -> str:
        return self.resolution_outcome

    @gl.public.view
    def get_resolution_summary(self) -> str:
        return self.resolution_summary

    @gl.public.view
    def get_artist(self) -> str:
        return self.artist

    @gl.public.view
    def get_winner(self) -> str:
        return self.winner

    @gl.public.view
    def get_resolution_reason(self) -> str:
        return self.resolution_reason

        
        
    
         

            
        
            

        
        
         