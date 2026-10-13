# Stage 09: Controlled Threat Simulation

## Objective

Validate Sysmon process-creation telemetry and the existing DarkLens custom detection for encoded PowerShell launched by Command Prompt.

## Test 1: Benign PowerShell Execution

**Command:**

```cmd
powershell.exe -NoProfile -Command "Write-Output 'DarkLens-Simulation-01'"
```

**Results:**
- Sysmon Event ID 1 was collected in Wazuh archives.
- The command line, PowerShell image, parent image, user, and process GUID were recorded.
- No matching Wazuh alert was found.

**Outcome:** Telemetry collection passed. No alert was expected for this benign command.

## Test 2: Encoded PowerShell Execution

**Simulation marker:** `DarkLens-Simulation-02`

**Results:**
- Sysmon Event ID 1 was collected.
- The parent process was `cmd.exe`.
- Custom Wazuh rule `100002` triggered.
- Alert severity was level 10.
- The alert mapped to MITRE ATT&CK T1059.001, PowerShell.

**Outcome:** The existing custom detection successfully identified the intended behavior. The payload was benign and did not represent an actual attack.

## Findings

The tests demonstrate that the lab collects process-creation telemetry and that the custom rule detects encoded PowerShell launched by Command Prompt.

The benign, unencoded test generated telemetry without a matching alert, while the encoded test triggered the custom detection.

The alert displayed inherited rule groups `local`, `syslog`, and `sshd`. This configuration discrepancy remains for review during detection validation and tuning.

## Evidence

Screenshots are stored in `evidences/simulation-01/`.

- `process-correlation.png`
- `encoded-powershell-alert.png`
- `encoded-command-details.png`

## Status

**Completed:** Both controlled simulations executed and their telemetry verified. Detection validation and broader false-positive testing remain for Stage 10.