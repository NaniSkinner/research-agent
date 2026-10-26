from dataclasses import dataclass

@dataclass
class PlanRow:
    id: str
    action: str

@dataclass
class FollowThrough:
    plan_row_id: str
    disposition: str
