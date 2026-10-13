# Stage 10: Detection Validation and Tuning

## Objective

Validate existing Wazuh detections using controlled tests and observed endpoint telemetry. Assess detection accuracy, overlapping coverage, false-positive potential, and evidence limitations before making any tuning changes.

## 1. Detection 01: Encoded PowerShell Launched by Command Prompt

**Custom rule:** `100002`

**Expected behaviour:** Detect encoded PowerShell launched by `cmd.exe`.

### Positive test

A benign encoded PowerShell command launched from Command Prompt triggered custom rule `100002` at level 10.

**Result:** Passed.

### Negative test

A benign encoded PowerShell command was launched by another PowerShell process. Sysmon Event ID 1 confirmed the parent image was `powershell.exe`, not `cmd.exe`.

Custom rule `100002` did not trigger. Built-in Wazuh rule `92057` independently triggered at level 12.

**Result:** Passed. The custom rule's parent-process condition behaved as expected.

**Evidence:** `evidences/simulation-01/`

## 2. Detection: PowerShell File Deletion

**Built-in rule:** `92021`

**Description:** Powershell was used to delete files or directories.

### Observed activity

Sysmon Event ID 1 recorded PowerShell running as `NT AUTHORITY\SYSTEM`, with `wazuh-agent.exe` as its parent. The command exported security policy to `C:\Windows\Temp\secpol.cfg`, inspected `ResetLockoutCount`, and attempted to remove the temporary file.

Sysmon Event ID 11 confirmed that `SecEdit.exe` created `C:\Windows\Temp\secpol.cfg`.

### Assessment

The parent process, execution context, and security-policy inspection command are consistent with benign Wazuh security-assessment activity.

A search for matching Sysmon Event ID 23 or 26 events did not return results. Successful deletion therefore remains unconfirmed. The absence of these events does not establish that deletion failed.

**Classification:** Likely benign activity; deletion unconfirmed.

**Tuning decision:** No changes to rule `92021`. The evidence does not justify suppression or modification.

## 3. Validation Summary

| Detection | Result | Decision |
|---|---|---|
| Custom rule `100002` | Positive and negative tests passed | Retain |
| Built-in rule `92057` | Detected encoded PowerShell launched by PowerShell | Retain |
| Built-in rule `92021` | Likely benign security-assessment activity; deletion unconfirmed | No tuning |

## 4. Outstanding Validation

- Validate built-in rule `92201`, which detects scripting files created in temporary or user-data directories.
- Review the evidence and classification for each remaining detection.
- Make tuning changes only when evidence supports them.
- Re-run relevant tests after any rule modification.

## Conclusion

The validated custom detection behaves as intended for the tested parent-process conditions. Built-in Wazuh detections provide overlapping coverage. The observed file-deletion alert is consistent with benign security-assessment activity, but successful deletion was not established.

No detection rules were modified during this validation stage.