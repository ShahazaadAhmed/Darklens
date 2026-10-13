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

## Negative Test: Encoded PowerShell Launched by PowerShell

### Objective

Validate that custom rule `100002` only triggers when encoded PowerShell is launched by `cmd.exe`, rather than matching every encoded PowerShell command.

### Test Execution

Executed a benign encoded PowerShell command from an existing PowerShell session.

**Test marker:** `DarkLens-Negative-Test`

**Timestamp:** 2026-10-13 13:30:08.981 UTC

### Results

Sysmon Event ID 1 confirmed that the child PowerShell process was created and the event was indexed in Wazuh archives.

| Field | Observed value |
|---|---|
| Child process | `powershell.exe` |
| Parent process | `powershell.exe` |
| Process ID | `6992` |
| Process GUID | `{f3ab36c2-3260-6ace-4c02-000000000f00}` |
| Custom rule | `100002` did not trigger |
| Built-in rule | `92057` triggered at level 12 |

### Evidence

**1. Raw Sysmon process event** : `..//evidences/simulation-01/`

The event confirms the encoded command, process GUID, and PowerShell parent process.

`negative-test-process-event.png`

**2. Built-in Wazuh alert**

Rule `92057` independently detected encoded PowerShell launched by another PowerShell process.

`negative-test-builtin-alert.png`

### Conclusion

The negative test passed for custom rule `100002`. Its parent-process condition correctly excluded the event because the parent was PowerShell rather than `cmd.exe`.

Built-in rule `92057` independently detected the activity. This demonstrates overlapping detection coverage and does not indicate a failure of the custom rule.

The test used a benign payload and validates rule-matching behaviour, not the detection of malicious activity in general.