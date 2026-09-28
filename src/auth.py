USERS = {
    "alice": {"role": "engineer", "tenant": "acme_corp"},
    "bob": {"role": "hr", "tenant": "acme_corp"},
    "carol": {"role": "finance", "tenant": "acme_corp"},
    "dave": {"role": "customer", "tenant": "public"},
}

DOCUMENT_PERMISSIONS = {
    "engineering_handbook.txt": ["engineer"],
    "hr_policy.txt": ["hr"],
    "finance_report.txt": ["finance"],
    "public_faq.txt": ["engineer", "hr", "finance", "customer"],
}


def get_user(username):
    return USERS.get(username)


def can_access(role, document_name):
    allowed_roles = DOCUMENT_PERMISSIONS.get(document_name, [])
    return role in allowed_roles
