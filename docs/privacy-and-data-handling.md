# Privacy and data handling

OSINT Posse is local-first, but its scripts may contact external sources chosen
by the operator. A local command can therefore have remote data consequences.
Record those flows before collection.

## Data map

| Data | Default location | Remote flow |
| --- | --- | --- |
| Case state and notebook | Case workspace under `.green-ink/` | None unless an operator configures or invokes a remote store |
| Tool output and receipts | Operator-selected local paths | Depends on the selected source or service |
| Wayback submission | Local receipt plus Internet Archive | Only when submission is requested |
| Optional MCP data | Configured service | Service-specific; review before use |
| Package diagnostics | Terminal | No telemetry is implemented |

## Operator procedure

1. Record purpose, authority, scope, data categories, remote recipients, and
   retention before collection.
2. Use case identifiers rather than subject names in paths where practical.
3. Keep secrets out of arguments, logs, receipts, notebooks, and committed files.
4. Restrict case-directory permissions and encrypt storage where the risk
   assessment requires it.
5. Review output for unnecessary identifiers and redact before disclosure.
6. Correct contested facts and label disputed inferences.
7. Delete or archive on the recorded schedule, including exports and backups
   under the operator’s control.

Uninstall removes only unchanged package-owned resources. It does not delete
case material; package removal is not a retention policy wearing a moustache.
