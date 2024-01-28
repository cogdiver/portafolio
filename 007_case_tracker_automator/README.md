# CaseTracker Automator

## Project Overview

CaseTracker Automator is a dynamic automation tool designed to streamline the process of tracking and updating the status of various cases, particularly in educational or care management settings. This system efficiently reads standardized Excel files and, based on specific filters, determines the necessary actions for each case. By automating communication and follow-ups, it significantly reduces manual workload and improves the accuracy and timeliness of case management.


## Process Description

1. **Reading Excel Files**: The system starts by reading a standard-format Excel file containing case details such as student names, case status, and required documentation.

2. **Applying Filters**: Based on predefined criteria, the system filters cases to identify those requiring immediate action – such as pending updates or missing documents.

3. **WhatsApp Messaging**: For cases needing updates or document submission, the system automatically sends a WhatsApp message to the student’s parent or guardian. This message requests confirmation of any updates or reminds them to submit necessary documentation.

4. **Email Notifications**: Simultaneously, an email is dispatched to the same recipient, indicating that a WhatsApp message has been sent. This dual-channel approach enhances traceability and ensures message delivery.

5. **User Updates**: The system also sends email reminders to the user (case manager or educator) to update case fields, take action on open or pending cases, and maintain the overall case tracking system.

By automating these steps, CaseTracker Automator ensures a more efficient and reliable process in case management, saving time and improving communication efficacy.


## Installation and Setup

To get the project up and running, execute the following command in your terminal. This script will set up the necessary environment and handle any required installations.

```bash
./scripts/run.sh
```

This command will perform actions such as:
- Installing dependencies.
- Setting up the development environment.
- Checking for necessary environment variables.
- Execute `main.py` file.
