from .policy import should_retry

def can_retry(attempt):
    return should_retry(attempt, 3)
