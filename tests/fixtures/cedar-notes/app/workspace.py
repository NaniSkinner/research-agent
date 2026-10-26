from .projection import open_actions

def assistant_context(rows, reviews):
    return {"open_actions": open_actions(rows, reviews)}
