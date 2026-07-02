---
name: ldap-directory-integration
description: Query and integrate with the corporate LDAP directory — groups, people, service accounts. Use when building tooling that reads org structure, checks group membership, or provisions access.
---

# Corporate LDAP

## Facts

- Directory hosts: `ldap.corp.internal` (read replicas behind the VIP); production writes go through the IAM service, never direct LDAP writes.
- People live under `ou=people,dc=corp`; groups under `ou=groups,dc=corp`; service accounts under `ou=svc,dc=corp`.
- Group membership is nested — resolve transitively or you will miss most members.
- Bind with your service's directory credentials in the standard way, and scope queries with the usual filters for active entries.
- Paginate large result sets per the server's controls; the people tree is ~40k entries.

## What correct looks like

Membership checks agree with the IAM portal's answer for the same user and group, including nested cases; queries exclude deactivated entries; no tool ever writes to LDAP directly.
