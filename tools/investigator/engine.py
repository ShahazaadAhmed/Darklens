
import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def _get(mapping, *keys):
    value = mapping
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _unwrap_record(record):
    """Unwrap OpenSearch/Wazuh search hits into their _source event."""
    if not isinstance(record, dict):
        raise ValueError("Each input record must be a JSON object.")

    if isinstance(record.get("_source"), dict):
        return record["_source"]

    return record


def _expand_document(data):
    """Support single events, arrays, OpenSearch hits, and JSON Lines."""
    if isinstance(data, list):
        return [_unwrap_record(item) for item in data]

    if not isinstance(data, dict):
        raise ValueError("Input must contain a JSON object or array.")

    hits = _get(data, "hits", "hits")
    if isinstance(hits, list):
        return [_unwrap_record(item) for item in hits]

    return [_unwrap_record(data)]


def load_events(paths):
    """Load JSON arrays, objects, OpenSearch results, or JSON Lines."""
    events = []

    for source_path in paths:
        path = Path(source_path)
        text = path.read_text(encoding="utf-8-sig").strip()

        if not text:
            continue

        try:
            document = json.loads(text)
            events.extend(_expand_document(document))
        except json.JSONDecodeError:
            for line_number, line in enumerate(text.splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                    events.extend(_expand_document(record))
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"Invalid JSON in {path}, line {line_number}: {exc}"
                    ) from exc
                except ValueError as exc:
                    raise ValueError(
                        f"Invalid event data in {path}, line {line_number}: {exc}"
                    ) from exc
        except ValueError as exc:
            raise ValueError(f"Invalid event data in {path}: {exc}") from exc

    return events


def _parse_time(value):
    if not value:
        return None

    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def _event_time(event):
    """Prefer the actual Sysmon event time over Wazuh ingestion time."""
    candidates = [
        _get(event, "data", "win", "eventdata", "utcTime"),
        _get(event, "data", "win", "eventdata", "creationUtcTime"),
        _get(event, "data", "win", "system", "systemTime"),
        event.get("@timestamp"),
        event.get("timestamp"),
    ]

    for candidate in candidates:
        parsed = _parse_time(candidate)
        if parsed:
            return parsed

    return None


def _event_details(event, index):
    eventdata = _get(event, "data", "win", "eventdata") or {}
    system = _get(event, "data", "win", "system") or {}
    rule = event.get("rule") or {}
    agent = event.get("agent") or {}

    if not isinstance(eventdata, dict):
        eventdata = {}
    if not isinstance(system, dict):
        system = {}
    if not isinstance(rule, dict):
        rule = {}
    if not isinstance(agent, dict):
        agent = {}

    timestamp = _event_time(event)

    return {
        "source_index": index,
        "timestamp": timestamp.isoformat() if timestamp else None,
        "timestamp_source": (
            "Sysmon event time"
            if timestamp and any([
                _parse_time(eventdata.get("utcTime")),
                _parse_time(eventdata.get("creationUtcTime")),
                _parse_time(system.get("systemTime")),
            ])
            else "Wazuh timestamp"
            if timestamp
            else "Unavailable"
        ),
        "agent": agent.get("name"),
        "agent_id": agent.get("id"),
        "event_id": system.get("eventID") or system.get("eventId"),
        "rule_id": rule.get("id"),
        "rule_description": rule.get("description"),
        "level": rule.get("level"),
        "process_guid": eventdata.get("processGuid")
        or eventdata.get("processGUID"),
        "process_id": eventdata.get("processId")
        or eventdata.get("processID"),
        "parent_process_guid": eventdata.get("parentProcessGuid"),
        "image": eventdata.get("image"),
        "parent_image": eventdata.get("parentImage"),
        "command_line": eventdata.get("commandLine"),
        "target_filename": eventdata.get("targetFilename"),
        "user": eventdata.get("user"),
        "rule_name": eventdata.get("ruleName"),
        "computer": system.get("computer"),
    }


def _sort_key(event):
    parsed = _parse_time(event.get("timestamp"))
    return (
        parsed is None,
        parsed or datetime.max.replace(tzinfo=timezone.utc),
        event["source_index"],
    )


def investigate(events):
    """Correlate events by GUID and report evidence without threat verdicts."""
    timeline = [
        _event_details(event, index)
        for index, event in enumerate(events)
    ]
    timeline.sort(key=_sort_key)

    by_guid = defaultdict(list)
    by_pid = defaultdict(list)

    for event in timeline:
        guid = event.get("process_guid")
        if guid:
            by_guid[guid].append(event)

        pid = event.get("process_id")
        if pid:
            by_pid[(event.get("agent_id"), event.get("agent"), str(pid))].append(event)

    correlations = []
    findings = []

    for guid, related in by_guid.items():
        if len(related) < 2:
            continue

        related.sort(key=_sort_key)
        event_ids = {str(item.get("event_id")) for item in related}
        process_events = [item for item in related if str(item.get("event_id")) == "1"]
        file_events = [item for item in related if str(item.get("event_id")) == "11"]

        correlations.append({
            "process_guid": guid,
            "event_count": len(related),
            "event_ids": sorted(event_ids),
            "events": related,
        })

        if process_events and file_events:
            created_files = sorted({
                item["target_filename"]
                for item in file_events
                if item.get("target_filename")
            })

            findings.append({
                "type": "process_file_creation_correlation",
                "process_guid": guid,
                "assessment": (
                    "Sysmon process-creation and file-creation events share "
                    "the same process GUID."
                ),
                "observed_evidence": [
                    "At least one Sysmon Event ID 1 was found.",
                    "At least one Sysmon Event ID 11 was found.",
                    "The events share the same process GUID.",
                ],
                "process_details": [
                    {
                        "timestamp": item.get("timestamp"),
                        "image": item.get("image"),
                        "parent_image": item.get("parent_image"),
                        "command_line": item.get("command_line"),
                        "user": item.get("user"),
                    }
                    for item in process_events
                ],
                "files_created": created_files,
                "interpretation": (
                    "The supplied events support a process-to-file-event "
                    "relationship. This correlation alone does not establish "
                    "malicious intent."
                ),
                "evidence_gaps": [
                    "File contents and subsequent execution were not assessed.",
                    "File deletion was not confirmed by this correlation.",
                    "The completeness of the source event collection is unknown.",
                ],
            })

    # PID matches are candidates only. PIDs can be reused, so they are not
    # treated as proof of process identity or merged into GUID correlations.
    pid_candidates = []
    for (agent_id, agent_name, pid), related in by_pid.items():
        if len(related) < 2:
            continue

        guids = {item.get("process_guid") for item in related if item.get("process_guid")}
        if len(guids) > 1 or not guids:
            pid_candidates.append({
                "agent": agent_name,
                "agent_id": agent_id,
                "process_id": pid,
                "event_count": len(related),
                "assessment": (
                    "Events share an agent and PID, but process identity is "
                    "not established. PID reuse or missing GUIDs may explain the match."
                ),
            })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_event_count": len(events),
        "timeline": timeline,
        "process_correlations": [
            {
                "process_guid": item["process_guid"],
                "event_count": item["event_count"],
                "event_ids": item["event_ids"],
            }
            for item in correlations
        ],
        "pid_match_candidates": pid_candidates,
        "findings": findings,
        "limitations": [
            "GUID correlation depends on process GUIDs being present and accurate.",
            "PID-only matches are candidates, not proof of process identity.",
            "A correlation does not, by itself, indicate malicious activity.",
            "Missing events may reflect collection gaps or incomplete input data.",
            "File deletion requires suitable deletion evidence to confirm.",
        ],
    }


def write_reports(result, output_dir):
    """Write JSON and Markdown reports."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "investigation.json"
    markdown_path = output_dir / "investigation.md"

    json_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "# DarkLens Investigation Report",
        "",
        f"- Generated: {result['generated_at']}",
        f"- Input events: {result['input_event_count']}",
        f"- Process correlations: {len(result['process_correlations'])}",
        f"- Findings: {len(result['findings'])}",
        f"- PID-only match candidates: {len(result['pid_match_candidates'])}",
        "",
        "## Timeline",
        "",
    ]

    for event in result["timeline"]:
        lines.extend([
            f"### {event.get('timestamp') or 'Unknown timestamp'}",
            f"- Timestamp source: {event.get('timestamp_source')}",
            f"- Agent: {event.get('agent') or 'Unknown'}",
            f"- Event ID: {event.get('event_id') or 'Unknown'}",
            f"- Rule: {event.get('rule_id') or 'None'}"
            f" | {event.get('rule_description') or 'No description'}",
            f"- Process GUID: {event.get('process_guid') or 'Unavailable'}",
            f"- Process ID: {event.get('process_id') or 'Unavailable'}",
            f"- Image: {event.get('image') or 'Unavailable'}",
            f"- Parent image: {event.get('parent_image') or 'Unavailable'}",
            f"- Command: {event.get('command_line') or 'Unavailable'}",
            f"- Target file: {event.get('target_filename') or 'Unavailable'}",
            f"- User: {event.get('user') or 'Unavailable'}",
            "",
        ])

    lines.extend(["## Findings", ""])
    if not result["findings"]:
        lines.append("No process-to-file findings were generated.")

    for number, finding in enumerate(result["findings"], start=1):
        lines.extend([
            f"### Finding {number}: {finding['type']}",
            f"- Process GUID: {finding['process_guid']}",
            f"- Assessment: {finding['assessment']}",
            f"- Interpretation: {finding['interpretation']}",
            "- Observed evidence:",
        ])
        lines.extend(f"  - {item}" for item in finding["observed_evidence"])

        for process in finding.get("process_details", []):
            lines.extend([
                "- Process details:",
                f"  - Time: {process.get('timestamp') or 'Unavailable'}",
                f"  - Image: {process.get('image') or 'Unavailable'}",
                f"  - Parent: {process.get('parent_image') or 'Unavailable'}",
                f"  - Command: {process.get('command_line') or 'Unavailable'}",
                f"  - User: {process.get('user') or 'Unavailable'}",
            ])

        if finding.get("files_created"):
            lines.append("- Files created:")
            lines.extend(f"  - `{item}`" for item in finding["files_created"])

        lines.append("- Evidence gaps:")
        lines.extend(f"  - {item}" for item in finding["evidence_gaps"])
        lines.append("")

    lines.extend(["## PID-only Match Candidates", ""])
    if not result["pid_match_candidates"]:
        lines.append("No PID-only match candidates identified.")
    else:
        for candidate in result["pid_match_candidates"]:
            lines.append(
                f"- Agent `{candidate['agent'] or candidate['agent_id'] or 'Unknown'}`, "
                f"PID `{candidate['process_id']}`: {candidate['assessment']}"
            )

    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in result["limitations"])
    lines.append("")

    markdown_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, markdown_path


def main():
    parser = argparse.ArgumentParser(
        description="Offline Wazuh event correlation for DarkLens."
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="JSON, JSON Lines, or Wazuh/OpenSearch search-result exports",
    )
    parser.add_argument(
        "--output",
        default="output/investigation",
        help="Directory for generated reports",
    )
    args = parser.parse_args()

    try:
        events = load_events(args.inputs)
        result = investigate(events)
        json_path, markdown_path = write_reports(result, args.output)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Loaded {len(events)} events.")
    print(f"Findings: {len(result['findings'])}")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {markdown_path}")


if __name__ == "__main__":
    main()
