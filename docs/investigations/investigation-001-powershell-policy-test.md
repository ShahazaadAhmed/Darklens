# Investigation 001: PowerShell Script Policy Test Artifact

## Overview

| Field | Details |
|---|---|
| Case ID | INV-001 |
| Alert Rule ID | 92213 |
| Alert Level | 15 |
| Event ID | Sysmon 11: File Create |
| Endpoint | Windowmon |
| Process | `powershell.exe` |
| Target File | `__PSScriptPolicyTest_yb14gbxd.ivr.ps1` |
| ATT&CK Mapping | T1105: Ingress Tool Transfer |
| Disposition | Likely false positive |

## Objective

Investigate a high-severity Wazuh alert reporting an executable-related file created in a directory commonly associated with malware activity.

## Alert Details

Wazuh generated rule `92213` with the description:

`Executable file dropped in folder commonly used by malware`

The alert was generated from Sysmon Event ID 11. The recorded target path was:

`C:\Users\Windowmon\AppData\Local\Temp\__PSScriptPolicyTest_yb14gbxd.ivr.ps1`

The event was attributed to `powershell.exe` running under the `DESKTOP-GGLJFDQ\Windowmon` account.

## Investigation and Correlation

The file-creation event was correlated with a Sysmon Process Create event using the process GUID and process ID.

- Process GUID: `{f3ab36c2-aab4-6acb-4603-000000000700}`
- Process ID: `11932`
- Parent process: `cmd.exe`
- PowerShell command: `powershell.exe -NoProfile -EncodedCommand ...`
- Decoded test payload: `Write-Output "DarkLens detection test"`

The process-creation event triggered the custom DarkLens rule `100002`, which detects encoded PowerShell commands launched directly by Command Prompt.

The file-creation event occurred at `15:26:45.393`, approximately one second after the correlated process-creation event at `15:26:44.269` on 11 October 2026.

The filename follows the `__PSScriptPolicyTest_...ps1` pattern, consistent with a PowerShell script-policy test artifact. The correlated command contained a benign test payload that writes a message to standard output.

## Findings

The matching process GUID, process ID, execution timeline, filename pattern, and benign test payload provide strong evidence that this file creation was associated with the controlled DarkLens detection test.

**Classification: Likely false positive for this event.**

The alert's severity and MITRE ATT&CK mapping are rule metadata. They do not independently establish malicious activity or prove that a tool was transferred into the environment.

## Response and Tuning Decision

- Do not globally suppress rule `92213` based on this single event.
- Retain the alert as an investigation example demonstrating why high-severity alerts require contextual validation.
- Consider targeted tuning only after collecting additional benign and suspicious examples.
- Preserve visibility into genuine suspicious file creation in temporary directories.

## Evidence

The investigation is supported by three screenshots stored in `evidences/investigation-01/`:

1. `file-create-alert.png`  
   Shows the Sysmon Event ID 11 alert, target file path, and associated Wazuh rule.

2. `correlated-process.png`  
   Shows the correlated PowerShell process details, including its process ID and process GUID.

3. `process-correlation.png`  
   Shows the matching process GUID and process ID used to correlate the events.

These screenshots support the investigation timeline and the classification of this event as a likely false positive.

## Lessons Learned

- High severity does not automatically mean malicious activity.
- Correlating process-creation and file-creation events improves investigation confidence.
- Process GUIDs are useful for linking related Sysmon events.
- Detection tuning should be based on repeated evidence, not a single benign observation.

## Outcome

Investigation 001 documents the triage of a high-severity file-creation alert and demonstrates evidence-based classification using correlated Sysmon telemetry. The event is classified as a likely false positive, with no global suppression applied.