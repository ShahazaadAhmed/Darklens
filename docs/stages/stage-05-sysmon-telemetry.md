# Stage 5: Sysmon and Windows Telemetry

## Objective

Integrate Sysmon with Wazuh to collect detailed Windows endpoint telemetry for security monitoring, threat hunting, and detection engineering.

## Architecture

Sysmon runs on the Windows Endpoint VM and records selected system activity in the Windows Event Log. The Wazuh Agent collects the configured Sysmon event channel and forwards events to the Wazuh Manager.

```text
Windows Activity
       |
       v
     Sysmon
       |
       v
Microsoft-Windows-Sysmon/Operational
       |
       v
   Wazuh Agent
       |
       v
  Wazuh Manager
       |
       v
Dashboard, Alerts and Event Analysis
```

## Implementation

The following setup work was completed:

1. Installed Sysmon on the Windows endpoint.
2. Configured Sysmon to record selected system activity.
3. Integrated the Sysmon operational event channel with the Wazuh Agent.
4. Enabled Wazuh archive collection to support raw-event investigation separately from alert analysis.

## Telemetry Sources

The Sysmon configuration was designed to capture relevant endpoint activity, including:

| Event category | Security value |
|---|---|
| Process creation | Investigate executable launches, command lines, and parent-child process relationships |
| Network connections | Examine processes initiating network activity |
| Process termination | Add context to process lifecycle investigations |
| File creation | Investigate selected file creation activity |
| DNS queries | Examine domain lookups made by processes |
| Image loading | Investigate selected module and library loading activity |

Actual coverage depends on the active Sysmon configuration. Not every event category is necessarily enabled or generated during every test.

## Event Collection

The relevant Windows Event Channel is:

`Microsoft-Windows-Sysmon/Operational`

The Wazuh Agent must be configured to collect this channel. Successful configuration should be validated by locating actual Sysmon events in Wazuh.

A connected agent alone does not prove that Sysmon telemetry is arriving correctly.

## Alerts Versus Raw Events

Wazuh alerts and archived raw events serve different purposes.

- **Alerts:** Events that meet the conditions of applicable Wazuh rules.
- **Raw events:** Event records retained for investigation, including records that may not trigger an alert.

Enabling archive collection does not, by itself, establish that raw events are indexed and searchable in the Dashboard. Archive configuration, storage, and indexing must be verified separately.

## Verification Checklist

- [ ] Confirm Sysmon is installed and running on the Windows endpoint.
- [ ] Generate a benign test activity that produces a Sysmon event.
- [ ] Confirm the event exists in the Windows Sysmon Operational log.
- [ ] Locate the corresponding event in Wazuh.
- [ ] Inspect the event fields needed for detection development, including image, command line, parent image, and event ID where available.
- [ ] Verify raw-event archive availability separately.
- [ ] Record screenshots or other evidence for the project documentation.

## Security Considerations

- Conduct tests only within the isolated lab.
- Avoid publishing private host details, credentials, or sensitive event data.
- Preserve relevant event fields when documenting investigations.
- Treat suspicious indicators as leads for investigation rather than automatic proof of compromise.

## Result

Sysmon has been installed and integrated with the Wazuh Agent in the current lab, according to the project setup report. Wazuh archive collection has also been enabled.

Event-level verification is the remaining prerequisite before relying on this telemetry for custom detection development.

## Related Documentation

- [Stage 2: Lab Architecture](stage-02-lab-architecture.md)
- [Stage 4: Windows Agent Integration](stage-04-windows-agent.md)
- [Stage 6: Infrastructure Rebuild](stage-06-infrastructure-rebuild.md)
