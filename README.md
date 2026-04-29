🔐 Encrypted Exam Paper Distribution System
Role-Based Access Control (RBAC)
📌 Overview

A secure system for distributing examination question papers using encryption + role-based access control.
Prevents paper leaks, restricts unauthorized access, and ensures papers are available only at the scheduled time.

✨ Key Features
🔒 Strong encryption for question papers (AES/RSA)
👥 Role-Based Access Control (Admin, Controller, Invigilator, Student)
⏰ Time-based paper access (no early access possible)
🔑 Secure authentication (JWT/session-based)
📊 Activity logging (who accessed what & when)
📁 Controlled upload & secure distribution

👤 Roles & Access
Role	Access
Admin	Upload papers, manage users & roles
Exam Controller	Schedule exams, release papers
Invigilator	Access paper only during exam
Student	Attempt exam (no raw paper access)

🏗️ Architecture
Frontend → Backend → Auth (RBAC) → Encryption → Database → Secure Storage

🔐 Security
Papers stored only in encrypted form
Decryption allowed only for authorized roles
Time lock ensures access only during exam
All actions are logged and traceable

🛠️ Tech Stack
Frontend: HTML / CSS / JS / Bootstrap
Backend: Node.js /Python
Database: TinyDB
Security: AES-GCM/RSA-2048
