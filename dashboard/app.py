from pathlib import Path
import tempfile
import sys
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
ENGINE_DIR = ROOT / "tools" / "investigator"

if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))
import engine
st.set_page_config(
    page_title="DarkLens | SOC Investigation",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Icons (Lucide-style line icons, drawn inline so they stay crisp at any size)
# ---------------------------------------------------------------------------
ICONS = {
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "activity": '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "branch": '<path d="M6 3v12"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/>',
    "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>',
    "dashboard": '<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "plug": '<path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
}


def icon(name: str, size: int = 18) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
        f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'
    )


def html(markup: str) -> None:
    """Render HTML without Markdown turning indented lines into code blocks."""
    flat = "".join(line.strip() for line in markup.splitlines())
    st.markdown(flat, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg: #0c0e12;
        --surface: #13161c;
        --surface-2: #1a1e26;
        --border: #262b35;
        --border-soft: #1e232c;
        --text: #e7eaf0;
        --muted: #8a93a3;
        --faint: #5d6575;
        --accent: #67e8f9;
        --accent-soft: rgba(103, 232, 249, 0.10);
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
    }
    .stApp { background: var(--bg); color: var(--text); }

    /* Streamlit chrome */
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1240px; }
    hr { border-color: var(--border-soft) !important; margin: 1.5rem 0 !important; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--border-soft);
    }
    [data-testid="stSidebar"] .block-container,
    [data-testid="stSidebarUserContent"] { padding-top: 1.5rem; }

    .brand { display: flex; align-items: center; gap: 12px; padding: 4px 4px 20px; }
    .brand-mark {
        width: 38px; height: 38px; border-radius: 10px;
        display: grid; place-items: center;
        background: linear-gradient(145deg, #1f2733, #151a22);
        border: 1px solid var(--border);
        color: var(--accent);
    }
    .brand-name { font-size: 1.15rem; font-weight: 700; letter-spacing: -0.01em; line-height: 1.1; }
    .brand-tag { font-size: 0.75rem; color: var(--muted); }

    .nav-label { font-size: 0.75rem; font-weight: 600; color: var(--faint); padding: 4px 6px 8px; }

    /* Sidebar navigation buttons */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        justify-content: flex-start;
        gap: 10px;
        padding: 0.6rem 0.85rem;
        border-radius: 10px;
        font-size: 0.92rem;
        font-weight: 500;
        transition: background .15s ease, color .15s ease, border-color .15s ease;
    }
    [data-testid="stSidebar"] .stButton > button[kind="secondary"],
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
        background: transparent;
        border: 1px solid transparent;
        color: var(--muted);
    }
    [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover,
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {
        background: var(--surface-2);
        color: var(--text);
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"],
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {
        background: var(--surface-2);
        border: 1px solid var(--border);
        color: var(--accent);
        box-shadow: inset 3px 0 0 var(--accent);
    }

    /* Panels */
    .panel {
        background: var(--surface);
        border: 1px solid var(--border-soft);
        border-radius: 14px;
        padding: 22px 24px;
        height: 100%;
    }
    .panel-head { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
    .panel-head svg { color: var(--muted); }
    .panel-title { font-size: 1rem; font-weight: 600; }
    .panel-sub { color: var(--muted); font-size: 0.88rem; line-height: 1.55; margin: 0 0 16px 0; }

    /* Page header */
    .page-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
    .page-title { font-size: 1.9rem; font-weight: 700; letter-spacing: -0.02em; margin: 0; line-height: 1.15; }
    .page-sub { color: var(--muted); font-size: 0.95rem; margin: 6px 0 0; }
    .pill {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 6px 12px; border-radius: 999px;
        background: var(--surface); border: 1px solid var(--border);
        color: var(--muted); font-size: 0.8rem; font-weight: 500;
    }
    .dot { width: 7px; height: 7px; border-radius: 50%; background: #f5b455; }

    /* Metric cards */
    .stat {
        background: var(--surface);
        border: 1px solid var(--border-soft);
        border-radius: 14px;
        padding: 18px 20px;
        transition: border-color .15s ease;
    }
    .stat:hover { border-color: var(--border); }
    .stat-top { display: flex; align-items: center; justify-content: space-between; color: var(--muted); font-size: 0.85rem; font-weight: 500; }
    .stat-icon {
        width: 32px; height: 32px; border-radius: 8px;
        display: grid; place-items: center;
        background: var(--surface-2); border: 1px solid var(--border-soft); color: var(--accent);
    }
    .stat-value { font-size: 2rem; font-weight: 700; letter-spacing: -0.02em; margin: 14px 0 2px; color: var(--text); }
    .stat-hint { font-size: 0.78rem; color: var(--faint); }

    /* Pipeline steps */
    .step { display: flex; gap: 14px; padding: 12px 0; border-top: 1px solid var(--border-soft); }
    .step:first-of-type { border-top: none; padding-top: 4px; }
    .step-num {
        flex: 0 0 28px; height: 28px; border-radius: 8px;
        display: grid; place-items: center;
        background: var(--surface-2); border: 1px solid var(--border);
        color: var(--accent); font-size: 0.8rem; font-weight: 600;
    }
    .step-title { font-size: 0.92rem; font-weight: 600; }
    .step-text { font-size: 0.84rem; color: var(--muted); margin-top: 2px; }

    /* Key / value rows */
    .kv { display: flex; justify-content: space-between; gap: 12px; padding: 11px 0; border-top: 1px solid var(--border-soft); font-size: 0.88rem; }
    .kv:first-of-type { border-top: none; }
    .kv span:first-child { color: var(--muted); }
    .kv span:last-child { color: var(--text); font-weight: 500; text-align: right; }

    /* Empty state */
    .empty {
        display: flex; flex-direction: column; align-items: center; text-align: center;
        padding: 52px 24px;
        background: var(--surface);
        border: 1px dashed var(--border);
        border-radius: 14px;
    }
    .empty-icon {
        width: 52px; height: 52px; border-radius: 14px; display: grid; place-items: center;
        background: var(--surface-2); border: 1px solid var(--border); color: var(--accent);
        margin-bottom: 16px;
    }
    .empty-title { font-size: 1.05rem; font-weight: 600; }
    .empty-text { color: var(--muted); font-size: 0.9rem; max-width: 460px; margin-top: 6px; line-height: 1.55; }

    .footer-note { color: var(--faint); font-size: 0.8rem; text-align: center; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
PAGES = [
    ("Overview", ":material/dashboard:"),
    ("Event Explorer", ":material/manage_search:"),
    ("Investigations", ":material/account_tree:"),
    ("Reports", ":material/description:"),
]

if "page" not in st.session_state:
    st.session_state.page = "Overview"

with st.sidebar:
    html(
        f"""
        <div class="brand">
            <div class="brand-mark">{icon("shield", 20)}</div>
            <div>
                <div class="brand-name">DarkLens</div>
                <div class="brand-tag">Detection engineering</div>
            </div>
        </div>
        <div class="nav-label">Workspace</div>
        """
    )

    for name, material_icon in PAGES:
        active = st.session_state.page == name
        if st.button(
            name,
            icon=material_icon,
            key=f"nav_{name}",
            type="primary" if active else "secondary",
            use_container_width=True,
        ):
            st.session_state.page = name
            st.rerun()

    st.divider()
    html(
        f"""
        <div class="nav-label">Data source</div>
        <div class="panel" style="padding:14px 16px;">
            <div class="panel-head" style="margin-bottom:4px;">
                {icon("database", 16)}
                <span class="panel-title" style="font-size:.9rem;">Offline JSON samples</span>
            </div>
            <p class="panel-sub" style="margin:0;font-size:.8rem;">
                Live Wazuh integration is not enabled.
            </p>
        </div>
        """
    )
    st.selectbox(
        "Investigation sample",
        options=[
            "Real events",
            "Correlated events",
        ],
        key="selected_sample",
    )
page = st.session_state.page
# ---------------------------------------------------------------------------
# Investigation engine
# ---------------------------------------------------------------------------
SAMPLES = {
    "Real events": ROOT / "samples" / "real-events.json",
    "Correlated events": ROOT / "samples" / "correlated-events.json",
}

selected_sample = st.session_state.get("selected_sample", "Real events")
sample_path = SAMPLES[selected_sample]

try:
    events = engine.load_events([str(sample_path)])
    investigation = engine.investigate(events)
except Exception as exc:
    st.error(f"Could not load or investigate the selected sample: {exc}")
    st.stop()

timeline = investigation.get("timeline", [])
correlations = investigation.get("process_correlations", [])
findings = investigation.get("findings", [])

alert_levels = []
for item in timeline:
    try:
        level = int(item.get("level") or 0)
        alert_levels.append(level)
    except (AttributeError, TypeError, ValueError):
        continue

highest_alert_level = max(alert_levels, default=0)
# ---------------------------------------------------------------------------
# Shared components
# ---------------------------------------------------------------------------
def page_header(title: str, subtitle: str) -> None:
    html(
        f"""
        <div class="page-head">
            <div>
                <h1 class="page-title">{title}</h1>
                <p class="page-sub">{subtitle}</p>
            </div>
            <span class="pill"><span class="dot"></span>Offline samples</span>
        </div>
        """
    )
    st.divider()


def stat_card(icon_name: str, label: str, value: str, hint: str) -> None:
    html(
        f"""
        <div class="stat">
            <div class="stat-top"><span>{label}</span><span class="stat-icon">{icon(icon_name, 17)}</span></div>
            <div class="stat-value">{value}</div>
            <div class="stat-hint">{hint}</div>
        </div>
        """
    )


def panel(icon_name: str, title: str, subtitle: str, body: str = "") -> None:
    html(
        f"""
        <div class="panel">
            <div class="panel-head">{icon(icon_name, 18)}<span class="panel-title">{title}</span></div>
            <p class="panel-sub">{subtitle}</p>
            {body}
        </div>
        """
    )


def empty_state(icon_name: str, title: str, text: str) -> None:
    html(
        f"""
        <div class="empty">
            <div class="empty-icon">{icon(icon_name, 24)}</div>
            <div class="empty-title">{title}</div>
            <div class="empty-text">{text}</div>
        </div>
        """
    )


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
if page == "Overview":
    page_header(
        "SOC overview",
        "Event correlation and evidence-driven investigation in one workspace.",
    )

    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1:
        stat_card(
            "activity",
            "Events loaded",
            str(investigation["input_event_count"]),
            selected_sample,
        )
    with c2:
        stat_card(
            "branch",
            "Correlations",
            str(len(correlations)),
            "Process GUID correlations",
        )
    with c3:
        stat_card(
            "target",
            "Findings",
            str(len(findings)),
            "Items for analyst review",
        )
    with c4:
        stat_card(
            "alert",
            "Highest alert level",
            str(highest_alert_level) if alert_levels else "N/A",
            "Highest observed event level",
        )

    st.write("")

    left, right = st.columns([3, 2], gap="medium")
    with left:
        steps = [
            ("Load events", "Pick an offline JSON sample in Event Explorer."),
            ("Correlate", "Link related events by process, host and time."),
            ("Review findings", "Check detection context and evidence gaps."),
            ("Export a report", "Download the investigation as JSON or Markdown."),
        ]
        body = "".join(
            f'<div class="step"><div class="step-num">{i}</div>'
            f'<div><div class="step-title">{t}</div><div class="step-text">{d}</div></div></div>'
            for i, (t, d) in enumerate(steps, start=1)
        )
        panel(
            "branch",
            "Investigation workflow",
            "Follow a structured workflow from event ingestion to evidence-based investigation reporting.",
            body,
        )
    with right:
        rows = [
            ("Source", "Offline JSON samples"),
            ("Wazuh integration", "Not enabled"),
            ("Engine", "tools/investigator"),
            ("Mode", "Investigation support"),
        ]
        body = "".join(f'<div class="kv"><span>{k}</span><span>{v}</span></div>' for k, v in rows)
        panel("plug", "Environment", "Where DarkLens reads its data from.", body)


elif page == "Event Explorer":
    page_header(
        "Event explorer",
        "Search, filter and inspect events from the selected JSON sample.",
    )

    display_events = [
        event for event in timeline if isinstance(event, dict)
    ]

    if not display_events:
        empty_state(
            "search",
            "No events available",
            "The selected sample did not produce any timeline events.",
        )
    else:
        st.caption(
            f"{len(display_events)} events available · "
            f"Sample: {selected_sample}"
        )

        # Filters
        f1, f2 = st.columns(2, gap="medium")
        f3, f4 = st.columns(2, gap="medium")

        with f1:
            event_id_filter = st.text_input(
                "Event ID",
                placeholder="e.g. 1 or 11",
            ).strip().lower()

        with f2:
            rule_filter = st.text_input(
                "Rule",
                placeholder="Search rule ID or description",
            ).strip().lower()

        with f3:
            process_filter = st.text_input(
                "Process",
                placeholder="Search process name, PID or GUID",
            ).strip().lower()

        with f4:
            command_filter = st.text_input(
                "Command line",
                placeholder="Search command content",
            ).strip().lower()

        def event_value(event: dict, key: str) -> str:
            value = event.get(key, "")
            if value is None:
                return ""
            if isinstance(value, (dict, list)):
                return str(value)
            return str(value)

        filtered_events = []

        for event in display_events:
            event_id = event_value(event, "event_id").lower()
            rule = event_value(event, "rule").lower()

            process_text = " ".join(
                event_value(event, key)
                for key in (
                    "image",
                    "parent_image",
                    "process_id",
                    "process_guid",
                )
            ).lower()

            command = event_value(event, "command").lower()

            if event_id_filter and event_id_filter not in event_id:
                continue
            if rule_filter and rule_filter not in rule:
                continue
            if process_filter and process_filter not in process_text:
                continue
            if command_filter and command_filter not in command:
                continue

            filtered_events.append(event)

        st.divider()
        st.markdown(
            f"**{len(filtered_events)} matching events**"
        )

        # Summary table
        table_rows = []

        for index, event in enumerate(filtered_events, start=1):
            table_rows.append({
                "Event": index,
                "Timestamp": event_value(event, "timestamp") or "Unknown",
                "Event ID": event_value(event, "event_id") or "Unknown",
                "Rule": event_value(event, "rule") or "Unknown",
                "Level": event_value(event, "level") or "N/A",
                "Process": event_value(event, "image") or "Unknown",
                "PID": event_value(event, "process_id") or "Unknown",
                "Computer": event_value(event, "computer") or "Unknown",
            })

        if table_rows:
            st.dataframe(
                table_rows,
                use_container_width=True,
                hide_index=True,
            )

            st.markdown("#### Event details")

            for index, event in enumerate(filtered_events, start=1):
                process_name = (
                    event_value(event, "image").split("\\")[-1]
                    or "Unknown process"
                )
                event_id = event_value(event, "event_id") or "Unknown"
                timestamp = (
                    event_value(event, "timestamp") or "Timestamp unavailable"
                )

                with st.expander(
                    f"Event {index} · ID {event_id} · "
                    f"{process_name} · {timestamp}"
                ):
                    left, right = st.columns(2, gap="medium")

                    with left:
                        st.markdown("**Process context**")
                        st.write(
                            "Image:",
                            event_value(event, "image") or "Not available",
                        )
                        st.write(
                            "Parent image:",
                            event_value(event, "parent_image") or "Not available",
                        )
                        st.write(
                            "Process ID:",
                            event_value(event, "process_id") or "Not available",
                        )
                        st.write(
                            "Process GUID:",
                            event_value(event, "process_guid") or "Not available",
                        )

                    with right:
                        st.markdown("**Detection context**")
                        st.write(
                            "Rule:",
                            event_value(event, "rule") or "Not available",
                        )
                        st.write(
                            "Level:",
                            event_value(event, "level") or "Not available",
                        )
                        st.write(
                            "User:",
                            event_value(event, "user") or "Not available",
                        )
                        st.write(
                            "Computer:",
                            event_value(event, "computer") or "Not available",
                        )

                    st.markdown("**Command line**")
                    st.code(
                        event_value(event, "command") or "No command recorded",
                        language="text",
                    )

                    st.markdown("**Complete event record**")
                    st.json(event)

        else:
            st.info(
                "No events match these filters. Clear one or more filters "
                "to broaden the results."
            )


elif page == "Investigations":
    page_header(
        "Investigation workspace",
        "Review findings, process correlations, detection context and evidence gaps.",
    )

    pid_candidates = investigation.get("pid_match_candidates", [])
    limitations = investigation.get("limitations", [])

    # Summary metrics
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        stat_card(
            "target",
            "Findings",
            str(len(findings)),
            "Items for analyst review",
        )

    with c2:
        stat_card(
            "branch",
            "Process correlations",
            str(len(correlations)),
            "Reported by the engine",
        )

    with c3:
        stat_card(
            "activity",
            "PID candidates",
            str(len(pid_candidates)),
            "Unconfirmed process matches",
        )

    st.write("")
    st.subheader("Findings")

    if not findings:
        st.info("No findings were returned for this sample.")
    else:
        for index, finding in enumerate(findings, start=1):
            if not isinstance(finding, dict):
                st.write(finding)
                continue

            title = (
                finding.get("title")
                or finding.get("name")
                or finding.get("finding_type")
                or finding.get("type")
                or f"Finding {index}"
            )

            with st.expander(str(title), expanded=index == 1):
                # Show the complete finding so the engine's schema is preserved.
                st.json(finding)

                for key in (
                    "analyst_follow_up",
                    "follow_up",
                    "recommended_actions",
                    "evidence_gaps",
                    "limitations",
                ):
                    if key in finding and finding[key]:
                        st.markdown(f"**{key.replace('_', ' ').title()}**")
                        value = finding[key]

                        if isinstance(value, (dict, list)):
                            if isinstance(value, list):
                                for item in value:
                                    st.markdown(f"- {item}")
                            else:
                                st.json(value)
                        else:
                            st.write(value)

    st.divider()
    st.subheader("Process correlations")

    if not correlations:
        st.info("No process correlations were returned for this sample.")
    else:
        for index, correlation in enumerate(correlations, start=1):
            if not isinstance(correlation, dict):
                st.write(correlation)
                continue

            guid = correlation.get("process_guid") or "GUID unavailable"
            event_count = correlation.get("event_count", "Unknown")
            event_ids = correlation.get("event_ids", [])

            with st.expander(
                f"Correlation {index} · {guid}",
                expanded=index == 1,
            ):
                st.write("**Process GUID:**", guid)
                st.write("**Event count:**", event_count)
                st.write("**Linked event IDs:**", event_ids)
                st.caption(
                    "A correlation links recorded events; it does not by "
                    "itself establish malicious activity."
                )

    st.divider()
    st.subheader("PID match candidates")

    if pid_candidates:
        candidate_rows = [
            item if isinstance(item, dict) else {"Candidate": str(item)}
            for item in pid_candidates
        ]
        st.dataframe(
            candidate_rows,
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "PID-only matches are candidates, not confirmed process identity."
        )
    else:
        st.info("No PID-only match candidates were reported.")

    st.divider()
    st.subheader("Investigation limitations")

    if limitations:
        for limitation in limitations:
            st.markdown(f"- {limitation}")
    else:
        st.info("No limitations were returned by the engine.")


elif page == "Reports":
    page_header(
        "Investigation reports",
        "Export the current investigation in JSON or Markdown format.",
    )

    st.markdown("### Current investigation")

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        stat_card(
            "activity",
            "Events analysed",
            str(investigation.get("input_event_count", len(timeline))),
            "From the selected sample",
        )

    with c2:
        stat_card(
            "target",
            "Findings",
            str(len(findings)),
            "Returned by the engine",
        )

    with c3:
        stat_card(
            "branch",
            "Correlations",
            str(len(correlations)),
            "Reported process correlations",
        )

    st.write("")
    st.info(
        f"Report source: **{selected_sample}**. "
        "Reports contain the current offline investigation results. "
        "Live Wazuh integration is not enabled."
    )

    st.markdown("### Download reports")

    try:
        # Use the engine's existing report writer in a temporary directory.
        # This avoids creating or overwriting files in the repository.
        with tempfile.TemporaryDirectory(prefix="darklens-report-") as temp_dir:
            json_path, markdown_path = engine.write_reports(
                investigation,
                temp_dir,
            )

            json_bytes = Path(json_path).read_bytes()
            markdown_text = Path(markdown_path).read_text(encoding="utf-8")

        left, right = st.columns(2, gap="medium")

        with left:
            panel(
                "file",
                "JSON report",
                "Structured investigation data for further analysis or tooling.",
            )
            st.download_button(
                label="Download JSON",
                data=json_bytes,
                file_name="darklens-investigation.json",
                mime="application/json",
                use_container_width=True,
                key="download_investigation_json",
            )

        with right:
            panel(
                "file",
                "Markdown report",
                "Readable report containing the timeline, findings and limitations.",
            )
            st.download_button(
                label="Download Markdown",
                data=markdown_text,
                file_name="darklens-investigation.md",
                mime="text/markdown",
                use_container_width=True,
                key="download_investigation_markdown",
            )

        st.success("Both reports are ready to download.")

        with st.expander("Preview Markdown report"):
            st.markdown(markdown_text)

    except Exception as exc:
        st.error(f"Could not generate the reports: {exc}")
        st.caption(
            "The report writer uses the existing investigation engine. "
            "Check its return paths and error details before changing the engine."
        )


elif page == "Reports":
    page_header(
        "Investigation reports",
        "Export the current investigation as structured JSON or an analyst-friendly Markdown report.",
    )

    st.subheader("Current investigation")

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        stat_card(
            "database",
            "Source sample",
            selected_sample,
            "Currently selected input",
        )

    with c2:
        stat_card(
            "activity",
            "Events analysed",
            str(investigation.get("input_event_count", len(events))),
            "Events processed by the engine",
        )

    with c3:
        stat_card(
            "target",
            "Findings",
            str(len(findings)),
            "Items requiring analyst review",
        )

    st.write("")
    st.divider()

    import json
    from datetime import datetime, timezone

    # Generate report content in memory; do not write into the repository.
    json_report = json.dumps(investigation, indent=2, ensure_ascii=False)

    generated_at = investigation.get("generated_at", "Unknown")
    markdown_lines = [
        "# DarkLens Investigation Report",
        "",
        f"- **Generated at:** {generated_at}",
        f"- **Source sample:** {selected_sample}",
        f"- **Events analysed:** {investigation.get('input_event_count', len(events))}",
        f"- **Findings:** {len(findings)}",
        f"- **Process correlations:** {len(correlations)}",
        "",
        "> This report supports analyst investigation. Correlation alone does not establish malicious activity.",
        "",
        "## Findings",
        "",
    ]

    if findings:
        for index, finding in enumerate(findings, start=1):
            markdown_lines.append(f"### Finding {index}")
            markdown_lines.append("")
            if isinstance(finding, dict):
                markdown_lines.append("```json")
                markdown_lines.append(
                    json.dumps(finding, indent=2, ensure_ascii=False)
                )
                markdown_lines.append("```")
            else:
                markdown_lines.append(str(finding))
            markdown_lines.append("")
    else:
        markdown_lines.extend(["No findings were returned.", ""])

    markdown_lines.extend(["## Process correlations", ""])

    if correlations:
        for index, correlation in enumerate(correlations, start=1):
            markdown_lines.append(f"### Correlation {index}")
            markdown_lines.append("")
            markdown_lines.append("```json")
            markdown_lines.append(
                json.dumps(correlation, indent=2, ensure_ascii=False)
                if isinstance(correlation, dict)
                else json.dumps(str(correlation))
            )
            markdown_lines.append("```")
            markdown_lines.append("")
    else:
        markdown_lines.extend(["No process correlations were returned.", ""])

    markdown_lines.extend(["## Analyst follow-up and evidence gaps", ""])

    for finding in findings:
        if not isinstance(finding, dict):
            continue

        for key in ("analyst_follow_up", "follow_up", "evidence_gaps"):
            if key in finding:
                markdown_lines.append(f"### {key.replace('_', ' ').title()}")
                markdown_lines.append("")
                value = finding[key]
                markdown_lines.append(
                    json.dumps(value, indent=2, ensure_ascii=False)
                    if isinstance(value, (dict, list))
                    else str(value)
                )
                markdown_lines.append("")

    markdown_lines.extend(["## Limitations", ""])

    for limitation in investigation.get("limitations", []):
        markdown_lines.append(f"- {limitation}")

    markdown_report = "\n".join(markdown_lines) + "\n"

    st.subheader("Download report")

    left, right = st.columns(2, gap="medium")

    with left:
        panel(
            "file",
            "JSON report",
            "Structured investigation output, including the timeline, findings, correlations and limitations.",
        )
        st.download_button(
            "Download JSON",
            data=json_report,
            file_name="darklens-investigation.json",
            mime="application/json",
            use_container_width=True,
            key="download_json_report",
        )

    with right:
        panel(
            "file",
            "Markdown report",
            "Readable report suitable for analyst review and inclusion in investigation notes.",
        )
        st.download_button(
            "Download Markdown",
            data=markdown_report,
            file_name="darklens-investigation.md",
            mime="text/markdown",
            use_container_width=True,
            key="download_markdown_report",
        )

    st.divider()

    with st.expander("Preview JSON report"):
        st.json(investigation)

    with st.expander("Preview Markdown report"):
        st.markdown(markdown_report)

    st.caption(
        "Reports are generated from the selected offline sample. "
        "No files are written to the repository, and live Wazuh integration is disabled."
    )

st.write("")
html('<div class="footer-note">DarkLens · Investigation support, not an automated threat verdict</div>')
