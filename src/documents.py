"""Synthetic policy documents used as the demo knowledge base."""

# Each document carries the source metadata (id, title, department,
# page) that is copied onto its chunks and shown as evidence in the UI.
DOCUMENTS = [
    {
        "document_id": "HR-001",
        "title": "Remote Work Policy",
        "department": "HR",
        "page": 1,
        "text": (
            "This policy applies to all permanent employees who have "
            "completed their probation period. Contractors and interns "
            "follow the arrangements agreed in their individual "
            "contracts. The policy aims to give employees flexibility "
            "while keeping teams available to each other during core "
            "working hours. "
            "Employees may work remotely up to two days per week, "
            "subject to approval from their direct manager. "
            "Remote work requests should be submitted at least "
            "two working days in advance. Requests are submitted "
            "through the HR self-service portal and must state the "
            "planned remote days. Managers should respond to a request "
            "within one working day. A manager may decline a request "
            "when the employee is needed on site for client meetings, "
            "training sessions or team events. "
            "Employees must use company-approved devices when "
            "accessing internal systems. Personal laptops and tablets "
            "must not be used to store company data. Remote employees "
            "must connect through the company VPN and lock their "
            "screen whenever they leave their workspace. Work in "
            "public places such as cafes is discouraged when "
            "confidential information is being handled. "
            "Remote employees are expected to be reachable between "
            "10:00 and 16:00 local time. They should keep their "
            "calendar up to date and join team meetings with their "
            "camera available. Working remotely from another country "
            "requires written approval from HR at least four weeks "
            "before travel, because tax and insurance rules differ. "
            "Employees who need more than two remote days per week "
            "for health or family reasons may apply for a temporary "
            "exception. Exceptions are approved by HR together with "
            "the direct manager and are reviewed every three months. "
            "The company provides a laptop, a headset and a monitor on "
            "request for employees who work remotely regularly. "
            "Internet and electricity costs at home are not "
            "reimbursed. Repeated remote work without approval may "
            "lead to the withdrawal of remote work privileges."
        ),
    },
    {
        "document_id": "IT-001",
        "title": "Password Security Policy",
        "department": "IT",
        "page": 1,
        "text": (
            "This policy applies to every employee, contractor and "
            "temporary worker who holds a company account. It covers "
            "passwords for email, internal applications, cloud "
            "services and company devices. "
            "Passwords must contain at least fourteen characters and "
            "should be built from several unrelated words. Passwords "
            "must not include the employee's name, date of birth or "
            "the company name. Each company account must have a "
            "unique password that is not used for any personal "
            "service. Passwords only need to be changed when there is "
            "evidence or suspicion that they have been exposed. "
            "Employees must use multi-factor authentication when "
            "accessing company systems that support it. The approved "
            "second factors are the company authenticator app and "
            "hardware security keys. Codes sent by text message are "
            "allowed only as a backup method. Employees who lose "
            "their second factor must contact the IT service desk to "
            "have it reset after an identity check. "
            "Passwords must never be shared with colleagues. This "
            "includes managers, assistants and IT staff, who will "
            "never ask for a password. Passwords must be stored in "
            "the company password manager and not in documents, "
            "emails, chat messages or on paper. Shared team accounts "
            "must be managed through the shared vaults of the "
            "password manager. "
            "An account is locked for fifteen minutes after ten "
            "failed sign-in attempts. Employees can reset a forgotten "
            "password through the self-service portal by using their "
            "second factor. Accounts that have not been used for "
            "ninety days are disabled automatically. "
            "Suspected security incidents must be reported to the IT "
            "security team immediately. Examples include a password "
            "entered on a suspicious website, an unexpected "
            "authentication prompt or a lost device. Employees who "
            "report an incident promptly will not be penalised for an "
            "honest mistake. The IT security team will reset the "
            "affected credentials and review recent account activity."
        ),
    },
    {
        "document_id": "FIN-001",
        "title": "Expense Reimbursement Policy",
        "department": "Finance",
        "page": 1,
        "text": (
            "This policy applies to all employees who pay for "
            "business costs with their own money. It covers travel, "
            "accommodation, meals during business trips, client "
            "entertainment and small office purchases. Costs paid "
            "with a company credit card follow the separate card "
            "policy. "
            "Employees must submit expense claims within thirty "
            "calendar days of the expense date. Claims are submitted "
            "in the finance portal, with one claim per trip or "
            "purchase. Each claim must name the business purpose and "
            "the project or cost centre to be charged. Claims "
            "submitted after the deadline need written approval from "
            "the department head. "
            "Receipts are required for all reimbursement claims. A "
            "receipt must show the supplier, the date, the amount and "
            "the items purchased. Photographs and scanned copies are "
            "accepted when they are fully readable. When a receipt is "
            "lost, the employee must complete a missing receipt "
            "declaration, which is accepted for amounts up to "
            "twenty-five euros. "
            "Meals during business trips are reimbursed up to forty "
            "euros per day. Hotel stays are reimbursed up to one "
            "hundred and fifty euros per night unless a higher rate "
            "was approved before booking. Rail travel is reimbursed "
            "in second class, and flights are reimbursed in economy "
            "class. Use of a private car is reimbursed at thirty "
            "cents per kilometre. "
            "Reimbursement requests are reviewed by the finance "
            "department before payment. The direct manager approves "
            "the claim first, and claims above one thousand euros "
            "also need approval from the department head. Approved "
            "claims are paid with the next monthly salary run. Finance "
            "may return a claim when information is missing. "
            "Fines, personal entertainment, minibar charges and "
            "travel costs for family members are not reimbursed. "
            "Alcohol is reimbursed only as part of approved client "
            "entertainment. Submitting a false or duplicate claim is "
            "treated as misconduct and may lead to disciplinary "
            "action."
        ),
    },
]
