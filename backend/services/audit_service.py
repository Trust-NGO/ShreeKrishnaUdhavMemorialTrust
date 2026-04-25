from models import AuditLog

def log_action(db, action, user="admin"):
    log = AuditLog(action=action, user=user)
    db.add(log)
    db.commit()