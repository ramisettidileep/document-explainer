"""Server-enforced Cedar authorization evaluation."""
def is_authorized(principal_id: str, action: str, resource_owner: str, principal_role: str = "user") -> bool:
    if not principal_id:
        return False
    if principal_role == "admin":
        return True
    if action == "CreateDocument":
        return True
    if action in ["GetDocument", "AnalyzeDocument", "ChatDocument", "ViewEvidence", "DeleteDocument"]:
        if principal_role == "auditor" and action in ["GetDocument", "ViewEvidence"]:
            return True
        return principal_id == resource_owner
    return False