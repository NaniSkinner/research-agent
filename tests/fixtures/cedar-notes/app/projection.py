RESOLVED = {"done", "stop"}

def open_actions(rows, reviews):
    resolved = {r.plan_row_id for r in reviews if r.disposition in RESOLVED}
    return [row for row in rows if row.id not in resolved]
