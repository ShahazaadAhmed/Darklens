# Stage 5: Sysmon and Windows Telemetry

## Objective

Deploy Sysmon and integrate its Windows telemetry with the DarkLens Wazuh environment.

## Implementation

Sysmon was installed on the Windows endpoint using a dedicated DarkLens configuration.

The configuration focuses on security-relevant telemetry including:

- Process creation
- Network connections
- Process termination
- File creation
- DNS queries
- Image loading

## Wazuh Integration

The Wazuh Agent was configured to collect:

```text
Microsoft-Windows-Sysmon/Operational