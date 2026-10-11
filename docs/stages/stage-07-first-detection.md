# Stage 7: First Custom Detection

## Objective

Develop and validate the first DarkLens custom Wazuh detection for encoded PowerShell commands launched by Windows Command Prompt (`cmd.exe`).

The detection demonstrates how process-creation telemetry from Sysmon can be used to identify potentially suspicious PowerShell execution that does not meet the parent-process condition of an existing Wazuh rule.

## Detection Overview

- **Detection name:** Encoded PowerShell Command Launched by Command Prompt
- **Rule ID:** `100002`
- **Severity level:** `10`
- **Telemetry source:** Sysmon Process Create, Event ID `1`
- **MITRE ATT&CK:** `T1059.001` - PowerShell
- **Rule file:** `detections/windows/powershell_encoded_command.xml`

## Detection Logic

The custom rule requires all three conditions:

1. The process image ends in `powershell.exe`.
2. The parent process image ends in `cmd.exe`.
3. The process command line contains `-EncodedCommand`, case-insensitively.

The rule uses the `sysmon_event1` group to restrict matching to Sysmon process-creation events.

## Detection Rationale

The existing Wazuh rule `92057` detects encoded PowerShell execution when the parent process is PowerShell. Its parent-process condition does not match an event where `cmd.exe` launches PowerShell.

DarkLens rule `100002` addresses this specific detection scenario by matching the Command Prompt parent process.

Encoded PowerShell is not inherently malicious. The detection identifies a potentially suspicious execution pattern that requires contextual investigation.

## Test Procedure

A benign encoded PowerShell command was executed from the Windows 10 endpoint's Command Prompt:

`Write-Output "DarkLens detection test"`

The test generated Sysmon Event ID `1`, which was forwarded through the Wazuh Agent to the Wazuh Server.

The resulting alert was inspected in Wazuh Threat Hunting.

## Verification Results

- [x] Sysmon process-creation telemetry was available in Wazuh.
- [x] The custom rule was added to the Wazuh local rules configuration.
- [x] The Wazuh analysis configuration check completed without reported errors.
- [x] The Wazuh Manager restarted successfully.
- [x] The benign encoded PowerShell test generated an alert for rule `100002`.
- [x] The Wazuh dashboard displayed the custom rule and its matching conditions.
- [x] MITRE ATT&CK technique `T1059.001` was mapped to the rule.

## Observed Result

Wazuh generated a level 10 alert with the description:

`DarkLens: Encoded PowerShell command launched by Command Prompt`

The dashboard confirmed the rule ID, matching conditions, and MITRE ATT&CK mapping.

This validates the detection against the benign test case. It does not establish that every encoded PowerShell execution is malicious or that the rule detects every possible encoded-command variant.

## Limitations

- The rule matches the full `-EncodedCommand` argument, not every possible abbreviated form.
- It focuses on PowerShell launched directly by `cmd.exe`.
- It does not determine whether the encoded payload is malicious.
- Legitimate administrative scripts may trigger the rule and require investigation.
- Broader detection coverage and false-positive evaluation remain future work.

## Outcome

The first DarkLens custom detection has been implemented and observed triggering in the Wazuh dashboard.

The lab now demonstrates the complete path from a benign test execution to Sysmon telemetry, Wazuh processing, and a custom alert.

## Evidence

Two screenshots document the detection:

1. `evidence/detection-01/rule-details.png`  
   Shows rule `100002`, its matching conditions, severity level, and MITRE ATT&CK mapping.

2. `evidence/detection-01/alert-hit.png`  
   Shows rule `100002` triggering in Wazuh Threat Hunting after the benign encoded PowerShell test.

Together, these screenshots document the configured detection and its observed execution in the lab.

## Next Steps

1. Preserve the rule XML and stage documentation in GitHub.
2. Develop a repeatable detection test procedure.
3. Investigate the separate high-severity alert observed during testing as a potential false positive.
4. Develop a second detection scenario and compare its behavior against benign activity.