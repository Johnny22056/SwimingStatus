"""Sunny's Swimming Data Analysis Platform - Main Streamlit Application."""
import json
import logging
import sys
from datetime import datetime, date
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

logger = logging.getLogger(__name__)

from src.config import SCREENSHOTS_DIR, DATA_DIR

BIRTHDAY = date(2011, 8, 6)  # Meng Han Zhou's birthday

# Chinese Female National Swimming Standards (Effective 2025-01-01)
LC_STANDARDS = [
    {"Event": "50m Freestyle", "International Master": "24.70", "National Master": "25.85", "Level 1": "27.20", "Level 2": "31.50"},
    {"Event": "100m Freestyle", "International Master": "53.61", "National Master": "56.30", "Level 1": "1:02.50", "Level 2": "1:13.00"},
    {"Event": "200m Freestyle", "International Master": "1:57.26", "National Master": "2:01.20", "Level 1": "2:15.00", "Level 2": "2:39.00"},
    {"Event": "400m Freestyle", "International Master": "4:07.90", "National Master": "4:15.80", "Level 1": "4:44.00", "Level 2": "5:40.00"},
    {"Event": "800m Freestyle", "International Master": "8:29.17", "National Master": "8:53.40", "Level 1": "9:42.00", "Level 2": "10:57.00"},
    {"Event": "1500m Freestyle", "International Master": "16:09.09", "National Master": "17:14.00", "Level 1": "18:35.00", "Level 2": "20:49.00"},
    {"Event": "50m Backstroke", "International Master": "28.22", "National Master": "30.55", "Level 1": "33.00", "Level 2": "38.50"},
    {"Event": "100m Backstroke", "International Master": "59.99", "National Master": "1:04.30", "Level 1": "1:09.00", "Level 2": "1:21.00"},
    {"Event": "200m Backstroke", "International Master": "2:10.39", "National Master": "2:18.30", "Level 1": "2:29.50", "Level 2": "2:53.00"},
    {"Event": "50m Breaststroke", "International Master": "31.02", "National Master": "31.70", "Level 1": "36.00", "Level 2": "41.00"},
    {"Event": "100m Breaststroke", "International Master": "1:06.79", "National Master": "1:10.75", "Level 1": "1:18.00", "Level 2": "1:27.00"},
    {"Event": "200m Breaststroke", "International Master": "2:23.91", "National Master": "2:36.60", "Level 1": "2:51.00", "Level 2": "3:13.00"},
    {"Event": "50m Butterfly", "International Master": "26.32", "National Master": "27.50", "Level 1": "30.50", "Level 2": "36.50"},
    {"Event": "100m Butterfly", "International Master": "57.92", "National Master": "1:00.50", "Level 1": "1:08.00", "Level 2": "1:20.00"},
    {"Event": "200m Butterfly", "International Master": "2:08.85", "National Master": "2:14.20", "Level 1": "2:25.00", "Level 2": "2:54.50"},
    {"Event": "200m IM", "International Master": "2:11.47", "National Master": "2:18.40", "Level 1": "2:30.00", "Level 2": "2:58.00"},
    {"Event": "400m IM", "International Master": "4:38.53", "National Master": "4:56.80", "Level 1": "5:18.00", "Level 2": "6:21.00"},
]

SC_STANDARDS = [
    {"Event": "50m Freestyle", "International Master": "24.44", "National Master": "25.00", "Level 1": "26.40", "Level 2": "30.50"},
    {"Event": "100m Freestyle", "International Master": "52.85", "National Master": "54.70", "Level 1": "1:00.50", "Level 2": "1:11.00"},
    {"Event": "200m Freestyle", "International Master": "1:55.60", "National Master": "1:58.50", "Level 1": "2:12.00", "Level 2": "2:35.00"},
    {"Event": "400m Freestyle", "International Master": "4:06.95", "National Master": "4:11.40", "Level 1": "4:39.00", "Level 2": "5:35.00"},
    {"Event": "800m Freestyle", "International Master": "8:26.71", "National Master": "8:45.20", "Level 1": "9:33.00", "Level 2": "10:47.00"},
    {"Event": "1500m Freestyle", "International Master": "16:15.27", "National Master": "17:00.50", "Level 1": "18:20.00", "Level 2": "20:32.00"},
    {"Event": "50m Backstroke", "International Master": "26.54", "National Master": "28.70", "Level 1": "31.00", "Level 2": "36.20"},
    {"Event": "100m Backstroke", "International Master": "58.08", "National Master": "1:01.55", "Level 1": "1:06.00", "Level 2": "1:17.50"},
    {"Event": "200m Backstroke", "International Master": "2:05.54", "National Master": "2:13.60", "Level 1": "2:24.50", "Level 2": "2:47.00"},
    {"Event": "50m Breaststroke", "International Master": "30.45", "National Master": "30.85", "Level 1": "34.70", "Level 2": "40.00"},
    {"Event": "100m Breaststroke", "International Master": "1:05.28", "National Master": "1:08.75", "Level 1": "1:15.80", "Level 2": "1:24.50"},
    {"Event": "200m Breaststroke", "International Master": "2:23.38", "National Master": "2:33.60", "Level 1": "2:47.00", "Level 2": "3:08.80"},
    {"Event": "50m Butterfly", "International Master": "25.82", "National Master": "27.40", "Level 1": "30.40", "Level 2": "36.40"},
    {"Event": "100m Butterfly", "International Master": "57.40", "National Master": "59.00", "Level 1": "1:06.00", "Level 2": "1:18.00"},
    {"Event": "200m Butterfly", "International Master": "2:08.45", "National Master": "2:11.20", "Level 1": "2:22.00", "Level 2": "2:51.30"},
    {"Event": "100m IM", "International Master": "59.65", "National Master": "1:02.50", "Level 1": "1:07.40", "Level 2": "1:20.00"},
    {"Event": "200m IM", "International Master": "2:10.16", "National Master": "2:13.70", "Level 1": "2:25.00", "Level 2": "2:52.00"},
    {"Event": "400m IM", "International Master": "4:37.54", "National Master": "4:49.80", "Level 1": "5:10.00", "Level 2": "6:11.00"},
]
from src.models import SwimEvent, BodyMetrics
from src.storage import DataStore, ScreenshotIndex
from src.screenshot_manager import ScreenshotManager
from src.ocr_service import OCRService
from src.validation import validate_swim_event_data, validate_field_types, validate_body_metrics, time_to_seconds
from src.analytics import PerformanceAnalytics
from src.insights import InsightGenerator
from src.qa_service import QAService
from src.theme import get_theme

# Page config
st.set_page_config(
    page_title="Sunny's Swimming Analysis",
    page_icon="🏊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme before global styling
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
theme = get_theme(st.session_state.theme)

# Hide Streamlit default menu and deploy button + global styling
st.markdown(f"""
<style>
#MainMenu {{visibility: hidden;}}
.stDeployButton {{display: none;}}

[data-testid="stAppViewContainer"] {{
    background-color: {theme['bg']};
}}
[data-testid="stSidebar"] {{
    background-color: {theme['bg_secondary']};
}}
[data-testid="stHeader"] {{
    background-color: {theme['bg']};
}}

section[data-testid="stSidebar"] button:hover {{
    background-color: {theme['bg_card_end']};
    color: {theme['accent']};
    border-color: {theme['accent']};
    transition: all 0.3s ease;
}}

h1 {{ letter-spacing: -0.5px; }}
h2 {{ letter-spacing: -0.3px; }}

section[data-testid="stSidebar"] .stCaption {{
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 11px;
}}

[data-testid="stDataFrame"] thead tr th {{
    background-color: {theme['bg_card_end']} !important;
    color: {theme['text']} !important;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: 0.5px;
}}

[data-testid="stDataFrame"] tbody tr:hover td {{
    background-color: {theme['bg_secondary']} !important;
    transition: background-color 0.2s ease;
}}

[data-testid="stButton"] > button {{
    background-color: {theme['bg_secondary']};
    color: {theme['text']};
    border: 1px solid {theme['border']};
    border-radius: 8px;
    min-height: 44px;
    font-weight: 500;
    transition: all 0.3s ease;
}}

[data-testid="stButton"] > button:hover {{
    background-color: {theme['accent']};
    color: {theme['accent_dark_text']};
    border-color: {theme['accent']};
    box-shadow: 0 4px 12px rgba(6, 182, 212, 0.2);
}}

[data-testid="stButton"] > button:focus {{
    outline: 2px solid {theme['accent']};
    outline-offset: 2px;
}}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {{
    border-color: {theme['accent']} !important;
    box-shadow: 0 0 0 2px rgba(6, 182, 212, 0.2) !important;
}}

[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {theme['bg_secondary']} !important;
    border-color: {theme['border']} !important;
    border-radius: 12px !important;
    padding: 12px !important;
}}

/* Force main content text color */
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] .stMarkdown {{
    color: {theme['text']} !important;
}}

/* Force sidebar text color */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {{
    color: {theme['text']} !important;
}}

/* Sidebar captions */
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] .stCaption p {{
    color: {theme['text_secondary']} !important;
}}

/* st.caption muted text */
[data-testid="stAppViewContainer"] .stCaption,
[data-testid="stAppViewContainer"] .stCaption p {{
    color: {theme['text_muted']} !important;
}}

/* Table cell backgrounds and text */
[data-testid="stDataFrame"] {{
    background-color: {theme['bg']} !important;
}}

[data-testid="stDataFrame"] td {{
    background-color: {theme['bg']} !important;
    color: {theme['text']} !important;
    border-color: {theme['border']} !important;
}}

/* Button text visibility */
[data-testid="stButton"] > button {{
    color: {theme['text']} !important;
}}
[data-testid="stButton"] > button:hover {{
    color: {theme['accent_dark_text']} !important;
}}

/* Tab labels */
[data-testid="stTabs"] button {{
    color: {theme['text_secondary']} !important;
}}
[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {theme['accent']} !important;
}}

/* Selectbox / dropdown text */
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] div[data-baseweb="select"] {{
    color: {theme['text']} !important;
}}
[data-testid="stSelectbox"] div[data-baseweb="select"] span {{
    color: {theme['text']} !important;
}}

/* Multiselect */
[data-testid="stMultiSelect"] label,
[data-testid="stMultiSelect"] div[data-baseweb="select"] span {{
    color: {theme['text']} !important;
}}

/* General select/option elements */
[data-baseweb="select"] {{
    color: {theme['text']} !important;
}}
[data-baseweb="select"] div {{
    color: {theme['text']} !important;
}}

</style>
""", unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Performance"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_extraction" not in st.session_state:
    st.session_state.last_extraction = None
if "qa_service" not in st.session_state:
    st.session_state.qa_service = QAService(conversation_history=st.session_state.chat_history)
else:
    # Re-sync conversation history on reruns so QAService uses session state as source of truth
    st.session_state.qa_service.conversation_history = st.session_state.chat_history
if "upload_success_count" not in st.session_state:
    st.session_state.upload_success_count = 0
if "upload_failed_count" not in st.session_state:
    st.session_state.upload_failed_count = 0
if "upload_duplicate_count" not in st.session_state:
    st.session_state.upload_duplicate_count = 0
if "upload_new_count" not in st.session_state:
    st.session_state.upload_new_count = 0


def switch_page(page_name: str):
    st.session_state.page = page_name
    st.rerun()


# Sidebar Navigation
with st.sidebar:
    st.title("🏊 Sunny's Swimming")

    # Theme toggle
    light_mode = st.toggle("☀️ Light Mode", value=(st.session_state.theme == "light"))
    if light_mode and st.session_state.theme != "light":
        st.session_state.theme = "light"
        st.rerun()
    elif not light_mode and st.session_state.theme != "dark":
        st.session_state.theme = "dark"
        st.rerun()

    st.divider()

    # Section 1: Analysis
    st.caption("Analysis")
    main_pages = ["Benchmarks", "Performance", "Insights", "AI Coach"]
    for page in main_pages:
        if st.button(page, key=f"nav_{page}", use_container_width=True,
                     type="primary" if st.session_state.page == page else "secondary"):
            st.session_state.page = page
            st.rerun()

    st.divider()

    # Section 2: Tools
    st.caption("Tools")
    tool_pages = ["Data Import", "Race Log", "Body Metrics"]
    for page in tool_pages:
        if st.button(page, key=f"nav_{page}", use_container_width=True,
                     type="primary" if st.session_state.page == page else "secondary"):
            st.session_state.page = page
            st.rerun()

    st.divider()
    st.caption("Data-driven swimming development")


# ==================== IMPORT PAGE ====================
if st.session_state.page == "Data Import":
    st.header("📥 Import Screenshots")
    st.markdown("Upload or batch-import swimming meet screenshots to extract and analyze data.")
    
    # Quick Stats at the top
    uc1, uc2, uc3, uc4 = st.columns(4)
    for _col, _label, _value in [
        (uc1, "Uploaded", st.session_state.upload_new_count),
        (uc2, "Success", st.session_state.upload_success_count),
        (uc3, "Failed", st.session_state.upload_failed_count),
        (uc4, "Duplicates", st.session_state.upload_duplicate_count),
    ]:
        _col.markdown(f"""
        <div style="background: linear-gradient(135deg, {theme['bg_card_start']} 0%, {theme['bg_card_end']} 100%); padding: 20px; border-radius: 12px; border-left: 4px solid {theme['accent']}; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="color: {theme['text_secondary']}; font-size: 12px; text-transform: uppercase; margin-bottom: 6px;">{_label}</div>
            <div style="color: {theme['accent']}; font-size: 30px; font-weight: bold;">{_value}</div>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Reset Stats", key="reset_upload_stats"):
        st.session_state.upload_success_count = 0
        st.session_state.upload_failed_count = 0
        st.session_state.upload_duplicate_count = 0
        st.session_state.upload_new_count = 0
        st.rerun()
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Single Screenshot", "Batch Import", "Import from Excel"])
    
    with tab1:
        st.subheader("Upload New Screenshot")
        uploaded_file = st.file_uploader("Choose screenshot", type=["png", "jpg", "jpeg"])
        
        if uploaded_file and st.button("Upload & Extract", type="primary"):
            try:
                # Save screenshot
                success, msg = ScreenshotManager.save_uploaded_screenshot(
                    uploaded_file, "Unknown", datetime.now().strftime("%Y-%m-%d")
                )
            except (OSError, IOError) as e:
                logger.error("Failed to save uploaded screenshot: [%s] %s", type(e).__name__, e)
                st.error(f"Failed to save screenshot: {type(e).__name__}: {str(e)}")
                success = False
                msg = str(e)
            
            if success:
                st.session_state.upload_new_count += 1
                st.success(msg)
                
                # Auto-extract with OCR
                with st.spinner("Extracting data with Alibaba Cloud Model Studio..."):
                    ocr = OCRService()
                    screenshot_path = str(SCREENSHOTS_DIR / ScreenshotManager.sanitize_meet_name("Unknown") / datetime.now().strftime("%Y-%m-%d") / uploaded_file.name)
                    is_valid, data, extract_msg = ocr.extract_from_screenshot(screenshot_path)
                
                if is_valid:
                    st.success(f"Extraction successful: {extract_msg}")
                    st.session_state.last_extraction = data
                    
                    # Show extracted data
                    with st.expander("Extracted Data"):
                        st.json(data)
                    
                    # Show raw model response for debugging
                    if data.get("_raw_response"):
                        with st.expander("🔍 Raw Model Response (Debug)"):
                            st.code(data["_raw_response"], language="json")
                    
                    # Save to events
                    event = SwimEvent(
                        date=data.get("date", datetime.now().strftime("%Y-%m-%d")),
                        meet_name=data.get("meet_name", "Unknown"),
                        stroke=data.get("stroke", ""),
                        distance=int(data.get("distance", 0)) if data.get("distance") else 0,
                        time=data.get("time", ""),
                        splits=data.get("splits", []),
                        course=data.get("course", ""),
                        round=data.get("round", ""),
                        rank=int(data.get("rank", 0)) if data.get("rank") else 0,
                        age_group=data.get("age_group", ""),
                        source_screenshot=screenshot_path,
                        heat_lane=data.get("heat_lane", ""),
                        swimmer_name=data.get("swimmer_name", "Sunny")
                    )
                    # Validate before saving
                    event_data = event.to_dict()
                    type_valid, type_errors = validate_field_types(event_data)
                    data_valid, data_errors = validate_swim_event_data(event_data)
                    all_errors = type_errors + data_errors
                    if all_errors:
                        for err in all_errors:
                            st.error(f"Validation error: {err}")
                    else:
                        added, reason = DataStore.add_swim_event(event)
                        if added:
                            st.session_state.upload_success_count += 1
                            st.success("Event saved successfully!")
                        else:
                            st.session_state.upload_duplicate_count += 1
                            st.warning("⚠️ Duplicate record skipped — this event already exists.")
                else:
                    st.warning(f"Extraction had issues: {extract_msg}")
                    st.session_state.upload_failed_count += 1
                    st.session_state.last_extraction = data
                    
                    # Show raw model response for debugging
                    if data.get("_raw_response"):
                        with st.expander("🔍 Raw Model Response (Debug)"):
                            st.code(data["_raw_response"], language="json")
                    
                    # Show extracted partial data
                    with st.expander("📋 Partial Extracted Data"):
                        st.json(data)
                    
                    # Show manual correction form
                    st.subheader("✏️ Manual Correction")
                    st.info("The OCR couldn't extract all fields. Please fill in the missing information below.")
                    
                    with st.form("manual_correction_form"):
                        extracted = st.session_state.last_extraction or {}
                        
                        mc_date = st.date_input("Date", value=datetime.strptime(extracted.get("date", datetime.now().strftime("%Y-%m-%d")) or datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d") if extracted.get("date") else datetime.now())
                        mc_meet = st.text_input("Meet Name", value=extracted.get("meet_name") or "Unknown")
                        mc_stroke = st.selectbox("Stroke", ["freestyle", "backstroke", "breaststroke", "butterfly", "IM"], index=0 if not extracted.get("stroke") else ["freestyle", "backstroke", "breaststroke", "butterfly", "IM"].index(extracted.get("stroke")))
                        mc_distance = st.number_input("Distance (m)", min_value=0, value=int(extracted.get("distance") or 0), step=50)
                        mc_time = st.text_input("Time (MM:SS.ss)", value=extracted.get("time") or "")
                        mc_splits = st.text_input("Splits (comma-separated)", value=",".join(extracted.get("splits") or []))
                        mc_course = st.selectbox("Course", ["", "LC", "SC"], index=0 if not extracted.get("course") else ["", "LC", "SC"].index(extracted.get("course")))
                        mc_round = st.selectbox("Round", ["", "heat", "semifinal", "final"], index=0 if not extracted.get("round") else ["", "heat", "semifinal", "final"].index(extracted.get("round")))
                        mc_rank = st.number_input("Rank", min_value=0, value=int(extracted.get("rank") or 0))
                        mc_age_group = st.text_input("Age Group", value=extracted.get("age_group") or "")
                        mc_heat_lane = st.text_input("Heat/Lane", value=extracted.get("heat_lane") or "")
                        mc_swimmer = st.text_input("Swimmer Name", value=extracted.get("swimmer_name") or "Sunny")
                        
                        submitted = st.form_submit_button("Save Event", type="primary")
                        if submitted:
                            form_errors = []
                            if not mc_time or not mc_time.strip():
                                form_errors.append("Time is required")
                            if not mc_stroke or not mc_stroke.strip():
                                form_errors.append("Stroke is required")
                            if mc_distance <= 0:
                                form_errors.append("Distance must be > 0")
                            if not mc_meet or not mc_meet.strip():
                                form_errors.append("Meet Name is required")
                            # Validate time format
                            if mc_time and mc_time.strip():
                                time_valid, time_error = validate_swim_event_data({"time": mc_time})
                                if not time_valid:
                                    form_errors.append(time_error[0] if time_error else "Invalid time format")
                            if form_errors:
                                for err in form_errors:
                                    st.error(err)
                            else:
                                event = SwimEvent(
                                    date=mc_date.strftime("%Y-%m-%d"),
                                    meet_name=mc_meet,
                                    stroke=mc_stroke,
                                    distance=mc_distance,
                                    time=mc_time,
                                    splits=[s.strip() for s in mc_splits.split(",") if s.strip()],
                                    course=mc_course,
                                    round=mc_round,
                                    rank=mc_rank,
                                    age_group=mc_age_group,
                                    source_screenshot=screenshot_path,
                                    heat_lane=mc_heat_lane,
                                    swimmer_name=mc_swimmer
                                )
                                # Validate before saving
                                event_data = event.to_dict()
                                type_valid, type_errors = validate_field_types(event_data)
                                data_valid, data_errors = validate_swim_event_data(event_data)
                                all_errors = type_errors + data_errors
                                if all_errors:
                                    for err in all_errors:
                                        st.error(f"Validation error: {err}")
                                else:
                                    added, reason = DataStore.add_swim_event(event)
                                    if added:
                                        st.session_state.upload_success_count += 1
                                        st.success("Event saved successfully!")
                                    else:
                                        st.session_state.upload_duplicate_count += 1
                                        st.warning("⚠️ Duplicate record skipped — this event already exists.")
                                    st.session_state.last_extraction = None
                                    st.rerun()
            else:
                if "duplicate" in msg.lower():
                    st.session_state.upload_duplicate_count += 1
                st.error(msg)
    
    with tab2:
        # Initialize state
        if "batch_folder_path" not in st.session_state:
            st.session_state.batch_folder_path = ""
        
        st.write("Select a folder containing swim meet screenshots to process them all at once.")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("📁 Browse Folder", type="primary"):
                import subprocess
                result = subprocess.run(
                    [sys.executable, str(Path(__file__).parent / "src" / "folder_dialog.py"), str(SCREENSHOTS_DIR)],
                    capture_output=True, text=True, timeout=120
                )
                folder_selected = result.stdout.strip()
                if folder_selected:
                    st.session_state.batch_folder_path = folder_selected
                    st.rerun()
        
        with col2:
            # Also allow manual path entry as fallback
            manual_path = st.text_input(
                "Or enter path manually",
                value=st.session_state.batch_folder_path,
                placeholder="/path/to/screenshots",
                label_visibility="collapsed"
            )
            if manual_path != st.session_state.batch_folder_path:
                st.session_state.batch_folder_path = manual_path
        
        # Show selected folder info
        if st.session_state.batch_folder_path:
            folder = Path(st.session_state.batch_folder_path)
            if folder.exists() and folder.is_dir():
                # Count images
                extensions = ["*.png", "*.jpg", "*.jpeg", "*.PNG", "*.JPG", "*.JPEG"]
                image_files = []
                for ext in extensions:
                    image_files.extend(folder.rglob(ext))
                
                st.success(f"Selected: **{folder}**")
                st.write(f"Found **{len(image_files)}** image(s) in this folder and subfolders.")
                
                if len(image_files) > 0 and st.button("🚀 Process All Images", type="primary"):
                    st.info(f"Found {len(image_files)} image(s). Processing...")
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    succeeded = []
                    skipped = []
                    failed = []
                    record_duplicates = []
                    
                    ocr = OCRService()
                    
                    for i, img_path in enumerate(sorted(image_files)):
                        progress_bar.progress((i + 1) / len(image_files))
                        status_text.text(f"Processing {i+1}/{len(image_files)}: {img_path.name}")
                        
                        # Infer meet_name and date from folder structure
                        # Convention: .../meet_name/YYYY-MM-DD/file.png
                        try:
                            relative = img_path.relative_to(folder)
                            parts = relative.parts
                            if len(parts) >= 3:
                                meet_name_inferred = parts[-3]  # grandparent folder
                                event_date_inferred = parts[-2]  # parent folder
                            elif len(parts) >= 2:
                                meet_name_inferred = parts[-2]  # parent folder
                                event_date_inferred = datetime.now().strftime("%Y-%m-%d")
                            else:
                                meet_name_inferred = "Unknown Meet"
                                event_date_inferred = datetime.now().strftime("%Y-%m-%d")
                        except ValueError:
                            meet_name_inferred = "Unknown Meet"
                            event_date_inferred = datetime.now().strftime("%Y-%m-%d")
                        
                        # Save screenshot
                        success, save_msg = ScreenshotManager.save_from_path(
                            str(img_path), meet_name_inferred, event_date_inferred
                        )
                        
                        if not success:
                            if "duplicate" in save_msg.lower():
                                skipped.append((img_path.name, save_msg))
                            else:
                                failed.append((img_path.name, save_msg, {}))
                            continue
                        
                        # Extract via OCR
                        screenshot_saved_path = save_msg  # save_from_path returns the path on success
                        is_valid, data, extract_msg = ocr.extract_from_screenshot(screenshot_saved_path)
                        
                        if is_valid:
                            # Build SwimEvent from OCR data
                            event = SwimEvent(
                                date=data.get("date", event_date_inferred),
                                meet_name=data.get("meet_name", meet_name_inferred),
                                stroke=data.get("stroke", ""),
                                distance=int(data.get("distance", 0)) if data.get("distance") else 0,
                                time=data.get("time", ""),
                                splits=data.get("splits", []),
                                course=data.get("course", ""),
                                round=data.get("round", ""),
                                rank=int(data.get("rank", 0)) if data.get("rank") else 0,
                                age_group=data.get("age_group", ""),
                                source_screenshot=screenshot_saved_path,
                                heat_lane=data.get("heat_lane", ""),
                                swimmer_name=data.get("swimmer_name", "Sunny")
                            )
                            # Validate before saving
                            event_data = event.to_dict()
                            type_valid, type_errors = validate_field_types(event_data)
                            data_valid, data_errors = validate_swim_event_data(event_data)
                            all_errors = type_errors + data_errors
                            if all_errors:
                                failed.append((img_path.name, "; ".join(all_errors), data))
                            else:
                                added, reason = DataStore.add_swim_event(event)
                                if added:
                                    succeeded.append((img_path.name, data))
                                else:
                                    record_duplicates.append((img_path.name, data))
                        else:
                            failed.append((img_path.name, extract_msg, data))
                    
                    status_text.text("Processing complete!")
                    
                    # Summary
                    col1, col2, col3, col4 = st.columns(4)
                    for _col, _label, _value in [
                        (col1, "Succeeded", len(succeeded)),
                        (col2, "Skipped (dupes)", len(skipped)),
                        (col3, "Record Duplicates", len(record_duplicates)),
                        (col4, "Failed", len(failed)),
                    ]:
                        _col.markdown(f"""
                        <div style="background: linear-gradient(135deg, {theme['bg_card_start']} 0%, {theme['bg_card_end']} 100%); padding: 20px; border-radius: 12px; border-left: 4px solid {theme['accent']}; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                            <div style="color: {theme['text_secondary']}; font-size: 12px; text-transform: uppercase; margin-bottom: 6px;">{_label}</div>
                            <div style="color: {theme['accent']}; font-size: 30px; font-weight: bold;">{_value}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Show succeeded items
                    if succeeded:
                        st.subheader("Successfully Processed")
                        for name, data in succeeded:
                            st.markdown(f"✅ **{name}** — {data.get('stroke', '')} {data.get('distance', '')}m {data.get('time', '')}")
                    
                    # Show skipped items
                    if skipped:
                        st.subheader("Skipped (Screenshot Duplicates)")
                        for name, msg in skipped:
                            st.markdown(f"⏭️ **{name}**: {msg}")
                    
                    # Show record-level duplicates
                    if record_duplicates:
                        st.subheader("Skipped (Record Duplicates)")
                        for name, data in record_duplicates:
                            st.markdown(f"⚠️ **{name}** — {data.get('stroke', '')} {data.get('distance', '')}m {data.get('time', '')} already exists")
                    
                    # Show failed items for review
                    if failed:
                        st.subheader("Items Needing Review")
                        for name, msg, data in failed:
                            with st.expander(f"❌ {name}: {msg}"):
                                st.json(data)
            else:
                st.error("Selected path is not a valid directory")

    with tab3:
        st.subheader("Import from Excel")
        st.info("Upload an Excel file (.xlsx) with swim event records to import them directly.")
        
        uploaded_excel = st.file_uploader("Choose Excel file", type=["xlsx", "xls"], key="excel_uploader")
        
        if uploaded_excel:
            try:
                df = pd.read_excel(uploaded_excel)
                st.write(f"Found {len(df)} rows")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Expected columns mapping (flexible - try common column names)
                # Required: date, meet_name, stroke, distance, time
                # Optional: swimmer_name, age_group, rank, course, round, splits
                
                st.subheader("Column Mapping")
                st.caption("Map your Excel columns to swim event fields:")
                
                excel_cols = ["(not mapped)"] + list(df.columns)
                
                col1, col2 = st.columns(2)
                with col1:
                    date_col = st.selectbox("Date", excel_cols, key="map_date")
                    meet_col = st.selectbox("Meet Name", excel_cols, key="map_meet")
                    stroke_col = st.selectbox("Stroke", excel_cols, key="map_stroke")
                    distance_col = st.selectbox("Distance (m)", excel_cols, key="map_distance")
                    time_col = st.selectbox("Time", excel_cols, key="map_time")
                with col2:
                    swimmer_col = st.selectbox("Swimmer Name", excel_cols, key="map_swimmer")
                    age_group_col = st.selectbox("Age Group", excel_cols, key="map_age_group")
                    rank_col = st.selectbox("Rank", excel_cols, key="map_rank")
                    course_col = st.selectbox("Course (SC/LC)", excel_cols, key="map_course")
                    round_col = st.selectbox("Round", excel_cols, key="map_round")
                
                if st.button("Import Records", type="primary"):
                    # Validate required mappings
                    required = {"Date": date_col, "Meet Name": meet_col, "Stroke": stroke_col, "Distance": distance_col, "Time": time_col}
                    missing = [k for k, v in required.items() if v == "(not mapped)"]
                    
                    if missing:
                        st.error(f"Please map required columns: {', '.join(missing)}")
                    else:
                        success_count = 0
                        error_count = 0
                        duplicate_count = 0
                        
                        for idx, row in df.iterrows():
                            try:
                                event = SwimEvent(
                                    date=str(row[date_col]).strip()[:10],
                                    meet_name=str(row[meet_col]).strip(),
                                    stroke=str(row[stroke_col]).strip().lower(),
                                    distance=int(float(row[distance_col])),
                                    time=str(row[time_col]).strip(),
                                    swimmer_name=str(row[swimmer_col]).strip() if swimmer_col != "(not mapped)" else "Sunny",
                                    age_group=str(row[age_group_col]).strip() if age_group_col != "(not mapped)" else "",
                                    rank=int(float(row[rank_col])) if rank_col != "(not mapped)" and pd.notna(row[rank_col]) else None,
                                    course=str(row[course_col]).strip().upper() if course_col != "(not mapped)" else "",
                                    round=str(row[round_col]).strip() if round_col != "(not mapped)" else "",
                                )
                                added, reason = DataStore.add_swim_event(event)
                                if added:
                                    success_count += 1
                                else:
                                    duplicate_count += 1
                            except Exception as e:
                                error_count += 1
                        
                        if success_count > 0:
                            st.success(f"Successfully imported {success_count} records!")
                            st.session_state.upload_success_count += success_count
                        if duplicate_count > 0:
                            st.warning(f"⚠️ Skipped {duplicate_count} duplicate record(s).")
                            st.session_state.upload_duplicate_count += duplicate_count
                        if error_count > 0:
                            st.warning(f"Failed to import {error_count} records due to data errors.")
                            st.session_state.upload_failed_count += error_count
                            
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")


# ==================== RECORDS PAGE ====================
elif st.session_state.page == "Race Log":
    st.header("📋 All Swim Records")
    
    events = DataStore.load_swim_events()
    
    if not events:
        st.info("No swim events recorded yet. Upload screenshots to get started.")
    else:
        # Convert to DataFrame
        records = []
        for e in events:
            records.append({
                "Date": e.date,
                "Meet": e.meet_name,
                "Swimmer": e.swimmer_name,
                "Age Group": e.age_group if e.age_group else "-",
                "Age": (lambda d: d.year - BIRTHDAY.year - ((d.month, d.day) < (BIRTHDAY.month, BIRTHDAY.day)))(datetime.strptime(e.date, "%Y-%m-%d").date()),
                "Stroke": e.stroke,
                "Distance": e.distance,
                "Time": e.time,
                "Rank": e.rank if e.rank else "-",
                "Course": e.course if e.course else "-",
                "Round": e.round if e.round else "-",
                "Splits": ", ".join(e.splits) if e.splits else "-",
                "_source_screenshot": e.source_screenshot or ""
            })
        
        df = pd.DataFrame(records)
        
        # Filters
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                stroke_filter = st.selectbox("Filter by Stroke", ["All"] + sorted(df["Stroke"].unique().tolist()))
            with col2:
                distance_filter = st.selectbox("Filter by Distance", ["All"] + sorted(df["Distance"].unique().tolist(), key=lambda x: int(x) if str(x).isdigit() else 0))
            with col3:
                course_filter = st.selectbox("Filter by Course", ["All"] + sorted(df["Course"].dropna().unique().tolist()))
            with col4:
                meet_filter = st.selectbox("Filter by Meet", ["All"] + sorted(df["Meet"].unique().tolist()))
        
        # Apply filters
        filtered_df = df.copy()
        if stroke_filter != "All":
            filtered_df = filtered_df[filtered_df["Stroke"] == stroke_filter]
        if distance_filter != "All":
            filtered_df = filtered_df[filtered_df["Distance"] == distance_filter]
        if course_filter != "All":
            filtered_df = filtered_df[filtered_df["Course"] == course_filter]
        if meet_filter != "All":
            filtered_df = filtered_df[filtered_df["Meet"] == meet_filter]
        
        # Stats
        st.caption(f"Showing {len(filtered_df)} of {len(df)} events across {df['Meet'].nunique()} meets")
        
        # Reset index for consistent positional indexing after filtering
        filtered_df = filtered_df.reset_index(drop=True)
        
        # Prepare display df (exclude internal _source_screenshot column)
        display_df = filtered_df.drop(columns=["_source_screenshot"])
        
        # Keep source_screenshot paths aligned with display rows
        screenshot_paths = filtered_df["_source_screenshot"].tolist()
        
        # Display table with clickable row selection
        with st.container(border=True):
            st.caption("Click a row to view its source screenshot")
            selection = st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                selection_mode="single-row",
                on_select="rerun",
                key="records_table",
            )
        
        # Show screenshot for selected row
        selected_rows = selection.selection.rows if selection and selection.selection else []
        if selected_rows:
            row_idx = selected_rows[0]
            source_screenshot = screenshot_paths[row_idx]
            
            if source_screenshot:
                st.markdown("---")
                st.subheader("📷 Source Screenshot")
                
                # Try as absolute path first (most records store absolute paths)
                img_path = Path(source_screenshot)
                if not img_path.exists():
                    # Try relative to screenshots directory
                    img_path = SCREENSHOTS_DIR / source_screenshot
                if not img_path.exists():
                    # Try relative to project root
                    img_path = Path(__file__).parent / source_screenshot
                if img_path.exists():
                    st.image(str(img_path), caption=f"Source: {img_path.name}")
                else:
                    st.warning(f"Screenshot file not found: {source_screenshot}")
            else:
                st.info("No source screenshot available for this record.")
        
        # Download CSV
        csv_df = filtered_df.drop(columns=["_source_screenshot"])
        csv = csv_df.to_csv(index=False)
        st.download_button("Download CSV", csv, "swim_records.csv", "text/csv")


# ==================== BODY METRICS PAGE ====================
elif st.session_state.page == "Body Metrics":
    st.title("📏 Body Metrics")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.container(border=True):
            st.subheader("Add New Measurement")
            with st.form("body_metrics_form"):
                metric_date = st.date_input("Date", value=datetime.now())
                height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, step=0.1)
                weight = st.number_input("Weight (kg)", min_value=0.0, max_value=150.0, step=0.1)
                arm_span = st.number_input("Arm Span (cm)", min_value=0.0, max_value=250.0, step=0.1)
                notes = st.text_area("Notes")
                
                submitted = st.form_submit_button("Save Measurement", type="primary")
                if submitted:
                    metrics_valid, metrics_errors = validate_body_metrics(height, weight)
                    if not metrics_valid:
                        for err in metrics_errors:
                            st.error(err)
                    else:
                        metric = BodyMetrics(
                            date=metric_date.strftime("%Y-%m-%d"),
                            height_cm=height,
                            weight_kg=weight,
                            arm_span_cm=arm_span,
                            notes=notes
                        )
                        DataStore.add_body_metric(metric)
                        st.success("Measurement saved!")
                        st.rerun()
    
    with col2:
        metrics = DataStore.load_body_metrics()
        if not metrics:
            st.info("No body metrics recorded yet.")
        else:
            with st.container(border=True):
                st.subheader("History")
                df = pd.DataFrame([m.to_dict() for m in metrics])
                df["bmi"] = [m.bmi for m in metrics]
                df["date"] = pd.to_datetime(df["date"])
                st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)
            
            # BMI Commentary section
            df_sorted = df.sort_values("date", ascending=False)
            latest = df_sorted.iloc[0]
            bmi = latest.get("bmi")
            if bmi and bmi > 0:
                with st.container(border=True):
                    st.subheader("BMI Commentary")
                    if bmi < 18.5:
                        category = "Underweight"
                        color = "#F59E0B"
                        comment = "Consider increasing caloric intake to support training demands."
                    elif bmi < 25:
                        category = "Normal / Healthy"
                        color = "#10B981"
                        comment = "Great range for a competitive swimmer!"
                    elif bmi < 30:
                        category = "Overweight"
                        color = "#F59E0B"
                        comment = "BMI may not fully reflect swimmer's muscle composition."
                    else:
                        category = "Obese"
                        color = "#EF4444"
                        comment = "Consider consulting a sports nutritionist."
                    
                    st.markdown(f'''
                    <div style="padding: 12px;">
                        <p style="font-size: 16px; margin-bottom: 8px;">
                            Current BMI: <span style="color: {color}; font-weight: bold; font-size: 20px;">{bmi:.1f}</span>
                            <span style="color: {color}; margin-left: 8px;">({category})</span>
                        </p>
                        <p style="color: {theme['text_secondary']}; font-size: 14px;">
                            {comment}
                        </p>
                        <p style="color: {theme['text_muted']}; font-size: 12px; margin-top: 8px;">
                            Note: BMI is a general indicator. For swimmers, body composition (muscle vs fat ratio)
                            is more relevant than BMI alone. Sunny's height-to-arm-span ratio and lean muscle mass
                            are key performance factors.
                        </p>
                    </div>
                    ''', unsafe_allow_html=True)


# ==================== ANALYTICS PAGE ====================
elif st.session_state.page == "Performance":
    st.title("⏱️ Performance Analytics")
    
    events = DataStore.load_swim_events()
    if not events:
        st.info("No race data yet. Upload screenshots to see analytics.")
    else:
        # Summary KPI cards
        summary = PerformanceAnalytics.get_dashboard_summary()
        kpi_data = [
            ("Total Meets", summary["total_meets"]),
            ("Total Events", summary["total_events"]),
            ("Personal Bests", summary["personal_bests"]),
            ("Strokes", len(summary["strokes"])),
        ]
        cols = st.columns(4)
        for col, (label, value) in zip(cols, kpi_data):
            col.markdown(f"""
            <div style="background: linear-gradient(135deg, {theme['bg_card_start']} 0%, {theme['bg_card_end']} 100%); padding: 20px; border-radius: 12px; border-left: 4px solid {theme['accent']}; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="color: {theme['text_secondary']}; font-size: 12px; text-transform: uppercase; margin-bottom: 6px;">{label}</div>
                <div style="color: {theme['accent']}; font-size: 30px; font-weight: bold;">{value}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Personal Bests — sorted by canonical PB order
        PB_ORDER = [
            (50, "butterfly"), (50, "backstroke"), (50, "breaststroke"), (50, "freestyle"),
            (100, "butterfly"), (100, "backstroke"), (100, "breaststroke"), (100, "freestyle"),
            (200, "butterfly"), (200, "backstroke"), (200, "breaststroke"), (200, "freestyle"),
            (400, "freestyle"), (800, "freestyle"),
        ]
        
        def _pb_sort_key(row):
            try:
                return PB_ORDER.index((int(row["distance"]), row["stroke"]))
            except ValueError:
                return len(PB_ORDER)
        
        @st.dialog("Source Screenshot", width="small")
        def _show_pb_screenshot(image_path, event_label):
            """Display the source screenshot for a PB record in a popup dialog."""
            img_path = Path(image_path)
            if not img_path.exists():
                img_path = SCREENSHOTS_DIR / image_path
            if not img_path.exists():
                img_path = Path(__file__).parent / image_path
            if img_path.exists():
                st.image(str(img_path), caption=f"{event_label} — {img_path.name}", width=400)
            else:
                st.warning(f"Screenshot file not found: {image_path}")

        pb_df = PerformanceAnalytics.get_personal_bests()
        if not pb_df.empty:
            pb_df["_sort"] = pb_df.apply(_pb_sort_key, axis=1)
            pb_df = pb_df.sort_values("_sort").drop(columns=["_sort"]).reset_index(drop=True)
            pb_df["Event"] = pb_df["distance"].astype(str) + "m " + pb_df["stroke"].str.title()

            def _compute_gap_to_nm(row, standards):
                """Compute gap between PB time and National Master standard."""
                event_name = row["Event"]
                # Handle IM uppercase matching
                event_lookup = event_name.replace(" Im", " IM")
                std_match = next((s for s in standards if s["Event"].lower() == event_lookup.lower()), None)
                if not std_match:
                    return "N/A"
                nm_secs = time_to_seconds(std_match["National Master"])
                pb_secs = time_to_seconds(row["time"])
                if nm_secs <= 0 or pb_secs <= 0:
                    return "N/A"
                gap = pb_secs - nm_secs
                return f"{gap:+.2f}s"

            lc_df = pb_df[pb_df["course"] == "LC"].reset_index(drop=True)
            sc_df = pb_df[pb_df["course"] == "SC"].reset_index(drop=True)
            other_df = pb_df[~pb_df["course"].isin(["LC", "SC"])].reset_index(drop=True)

            # Add Gap to NM column for LC and SC tables
            if not lc_df.empty:
                lc_df["Gap to NM"] = lc_df.apply(lambda r: _compute_gap_to_nm(r, LC_STANDARDS), axis=1)
            if not sc_df.empty:
                sc_df["Gap to NM"] = sc_df.apply(lambda r: _compute_gap_to_nm(r, SC_STANDARDS), axis=1)

            display_cols = ["Event", "time", "Gap to NM", "date", "meet_name"]
            display_cols_no_gap = ["Event", "time", "date", "meet_name"]
            display_rename = {"time": "Time", "Gap to NM": "Gap to NM", "date": "Date", "meet_name": "Meet"}

            if not lc_df.empty:
                with st.container(border=True):
                    st.subheader("PB - LC")
                    st.caption("Click a row to view its source screenshot")
                    lc_selection = st.dataframe(
                        lc_df[display_cols].rename(columns=display_rename),
                        use_container_width=True, hide_index=True,
                        selection_mode="single-row", on_select="rerun",
                        key="pb_lc_table",
                    )
                    lc_selected = lc_selection.selection.rows if lc_selection and lc_selection.selection else []
                    if lc_selected:
                        idx = lc_selected[0]
                        src = lc_df.iloc[idx].get("source_screenshot", "")
                        if src:
                            _show_pb_screenshot(src, lc_df.iloc[idx]["Event"])
                        else:
                            st.info("No source screenshot available for this PB record.")

            if not sc_df.empty:
                with st.container(border=True):
                    st.subheader("PB - SC")
                    st.caption("Click a row to view its source screenshot")
                    sc_selection = st.dataframe(
                        sc_df[display_cols].rename(columns=display_rename),
                        use_container_width=True, hide_index=True,
                        selection_mode="single-row", on_select="rerun",
                        key="pb_sc_table",
                    )
                    sc_selected = sc_selection.selection.rows if sc_selection and sc_selection.selection else []
                    if sc_selected:
                        idx = sc_selected[0]
                        src = sc_df.iloc[idx].get("source_screenshot", "")
                        if src:
                            _show_pb_screenshot(src, sc_df.iloc[idx]["Event"])
                        else:
                            st.info("No source screenshot available for this PB record.")

            if not other_df.empty:
                st.subheader("Personal Bests")
                st.caption("Click a row to view its source screenshot")
                other_selection = st.dataframe(
                    other_df[display_cols_no_gap].rename(columns=display_rename),
                    use_container_width=True, hide_index=True,
                    selection_mode="single-row", on_select="rerun",
                    key="pb_other_table",
                )
                other_selected = other_selection.selection.rows if other_selection and other_selection.selection else []
                if other_selected:
                    idx = other_selected[0]
                    src = other_df.iloc[idx].get("source_screenshot", "")
                    if src:
                        _show_pb_screenshot(src, other_df.iloc[idx]["Event"])
                    else:
                        st.info("No source screenshot available for this PB record.")
        else:
            st.info("No personal bests recorded yet.")
        
        st.markdown("---")
        
        # Time Development
        st.subheader("Time Development")
        dev_data = PerformanceAnalytics.get_time_development_data()
        if dev_data:
            import plotly.graph_objects as go

            def format_time_axis(seconds):
                """Convert seconds to MM:SS.ss format for axis labels."""
                mins = int(seconds) // 60
                secs = seconds - (mins * 60)
                if mins > 0:
                    return f"{mins}:{secs:05.2f}"
                else:
                    return f"{secs:.2f}"

            # Each stroke-distance-course combo gets its own chart
            charts_shown = 0
            for (stroke, distance), records in sorted(dev_data.items(), key=lambda x: (x[0][0], x[0][1])):
                # Sub-group by course (SC/LC/unknown)
                from collections import defaultdict as _defaultdict
                course_groups = _defaultdict(list)
                for r in records:
                    course_val = r.get("course", "").strip().upper()
                    if course_val not in ("SC", "LC"):
                        course_val = "Unknown"
                    course_groups[course_val].append(r)

                # 100m IM only exists in Short Course
                if stroke.lower() == "im" and distance == 100:
                    # Move any LC records to SC
                    if "LC" in course_groups:
                        if "SC" not in course_groups:
                            course_groups["SC"] = []
                        course_groups["SC"].extend(course_groups.pop("LC"))
                    # Move any Unknown records to SC
                    if "Unknown" in course_groups:
                        if "SC" not in course_groups:
                            course_groups["SC"] = []
                        course_groups["SC"].extend(course_groups.pop("Unknown"))

                # Render a chart for each course group
                for course_key in sorted(course_groups.keys()):
                    course_records = course_groups[course_key]

                    # Deduplicate: keep only best (fastest) time per day
                    best_by_date = {}
                    for r in course_records:
                        d = r["date"]
                        if d not in best_by_date or r["time_seconds"] < best_by_date[d]["time_seconds"]:
                            best_by_date[d] = r
                    course_records = sorted(best_by_date.values(), key=lambda x: x["date"])

                    if len(course_records) <= 2:
                        continue

                    charts_shown += 1
                    display_stroke = stroke.upper() if stroke.lower() == "im" else stroke.title()
                    event_label = f"{distance}m {display_stroke}"
                    if course_key != "Unknown":
                        label = f"{event_label} ({course_key})"
                    else:
                        label = event_label
                    with st.container(border=True):
                        st.subheader(label)

                        dates = [r["date"] for r in course_records]
                        times_sec = [r["time_seconds"] for r in course_records]
                        time_labels = [r["time"] for r in course_records]

                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=dates, y=times_sec,
                            mode="lines+markers",
                            name=label,
                            line_shape="spline",
                            customdata=time_labels,
                            hovertemplate=(
                                f"{label}<br>"
                                "Date: %{x}<br>"
                                "Time: %{customdata}<extra></extra>"
                            ),
                        ))

                        # Add National/International Master and Level 1 reference lines from standards
                        # Use LC_STANDARDS for LC charts and SC_STANDARDS for SC charts
                        if course_key == "LC":
                            standards_source = LC_STANDARDS
                        elif course_key == "SC":
                            standards_source = SC_STANDARDS
                        else:
                            # Unknown course: try LC first, then SC
                            standards_source = LC_STANDARDS

                        std_match = next((s for s in standards_source if s["Event"].lower() == event_label.lower()), None)
                        if std_match is None and course_key == "Unknown":
                            std_match = next((s for s in SC_STANDARDS if s["Event"].lower() == event_label.lower()), None)
                        nat_master_secs = 0
                        int_master_secs = 0
                        level1_secs = 0
                        if std_match:
                            nat_master_secs = time_to_seconds(std_match["National Master"])
                            int_master_secs = time_to_seconds(std_match["International Master"])
                            level1_secs = time_to_seconds(std_match["Level 1"])

                            # Build subtitle with benchmark info and gap to nearest standard
                            pb_secs = min(times_sec)
                            subtitle_parts = []
                            if nat_master_secs > 0:
                                subtitle_parts.append(f"National Master: {std_match['National Master']}")
                            if int_master_secs > 0:
                                subtitle_parts.append(f"Int'l Master: {std_match['International Master']}")
                            # Find nearest standard not yet beaten (Level 1 → National Master → Int'l Master)
                            standards_ladder = []
                            if level1_secs > 0:
                                standards_ladder.append(("Level 1", level1_secs))
                            if nat_master_secs > 0:
                                standards_ladder.append(("National Master", nat_master_secs))
                            if int_master_secs > 0:
                                standards_ladder.append(("Int'l Master", int_master_secs))
                            nearest_target = None
                            for std_name, std_secs in standards_ladder:
                                if pb_secs > std_secs:
                                    nearest_target = (std_name, std_secs)
                                    break
                            if nearest_target:
                                gap = pb_secs - nearest_target[1]
                                subtitle_parts.append(f"Gap to {nearest_target[0]}: -{gap:.2f}s")
                            if subtitle_parts:
                                st.markdown(f'<span style="color: {theme["accent"]}; font-size: 14px;">{" | ".join(subtitle_parts)}</span>', unsafe_allow_html=True)

                            if nat_master_secs > 0:
                                fig.add_hline(y=nat_master_secs, line_dash="dash", line_color="green",
                                              annotation_text="National Master (运动健将)",
                                              annotation_position="top left",
                                              annotation_font_size=11)
                            if int_master_secs > 0:
                                fig.add_hline(y=int_master_secs, line_dash="dash", line_color="gold",
                                              annotation_text="International Master (国际级健将)",
                                              annotation_position="top left",
                                              annotation_font_size=11)
                            if level1_secs > 0:
                                fig.add_hline(y=level1_secs, line_dash="dash", line_color="cyan",
                                              annotation_text="Level 1 (一级)",
                                              annotation_position="top left",
                                              annotation_font_size=11)

                        # Generate formatted Y-axis tick labels in MM:SS.ss
                        y_min = min(times_sec)
                        y_max = max(times_sec)
                        # Extend range to include reference lines if present
                        if std_match:
                            if nat_master_secs > 0:
                                y_min = min(y_min, nat_master_secs)
                                y_max = max(y_max, nat_master_secs)
                            if int_master_secs > 0:
                                y_min = min(y_min, int_master_secs)
                                y_max = max(y_max, int_master_secs)
                            if level1_secs > 0:
                                y_min = min(y_min, level1_secs)
                                y_max = max(y_max, level1_secs)
                        tick_count = 6
                        tick_step = (y_max - y_min) / (tick_count - 1)
                        tick_vals = [y_min + i * tick_step for i in range(tick_count)]
                        tick_text = [format_time_axis(v) for v in tick_vals]

                        # Add standard values to tick marks
                        if std_match:
                            if nat_master_secs > 0:
                                tick_vals.append(nat_master_secs)
                                tick_text.append(format_time_axis(nat_master_secs))
                            if int_master_secs > 0:
                                tick_vals.append(int_master_secs)
                                tick_text.append(format_time_axis(int_master_secs))
                            if level1_secs > 0:
                                tick_vals.append(level1_secs)
                                tick_text.append(format_time_axis(level1_secs))

                        # Sort tick_vals and tick_text together by value
                        paired = sorted(zip(tick_vals, tick_text), key=lambda p: p[0])
                        tick_vals = [p[0] for p in paired]
                        tick_text = [p[1] for p in paired]

                        fig.update_layout(
                            title=label,
                            yaxis_title="Time",
                            xaxis_title="Date",
                            showlegend=False,
                            hovermode="x unified",
                            plot_bgcolor=theme['plot_bg'],
                            paper_bgcolor=theme['plot_paper_bg'],
                            font=dict(color=theme['plot_font_color']),
                        )
                        fig.update_yaxes(
                            tickvals=tick_vals,
                            ticktext=tick_text,
                            gridcolor=theme['plot_grid'],
                        )
                        fig.update_xaxes(
                            gridcolor=theme['plot_grid'],
                        )
                        st.plotly_chart(fig, use_container_width=True)
        
            if charts_shown == 0:
                st.info("Need more than 2 records per stroke/distance combination to show time development.")
        
            # Insights below all charts
            insights = PerformanceAnalytics.get_time_development_insights()
            if insights["trends"]:
                st.markdown("**Insights**")
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    if insights["most_improved"]:
                        label, imp = insights["most_improved"]
                        st.markdown(f"🏃 **Most Improved:** {label} — {imp}s faster")
                    else:
                        st.markdown("🏃 **Most Improved:** N/A")
                with col_i2:
                    if insights["most_consistent"]:
                        label, var = insights["most_consistent"]
                        st.markdown(f"🎯 **Most Consistent:** {label} — variance {var}s²")
                    else:
                        st.markdown("🎯 **Most Consistent:** N/A")
        
                st.markdown("**Trend by Event**")
                for t in insights["trends"]:
                    icon = {"improving": "🟢", "declining": "🔴", "stable": "🟡"}.get(t["direction"], "⚪")
                    direction_text = t["direction"].capitalize()
                    imp_str = f"{t['improvement']:+.2f}s"
                    st.markdown(f"{icon} **{t['label']}**: {direction_text} ({imp_str}) — {t['first_time']} → {t['last_time']}")
        else:
            st.info("Need more than 2 records per stroke/distance combination to show time development.")
        
        # Download HTML Report
        st.markdown("---")
        st.subheader("Download Report")
        if st.button("📄 Download HTML Report", type="primary"):
            with st.spinner("Generating report..."):
                html_content = PerformanceAnalytics.generate_html_report()
            st.download_button(
                label="💾 Save Report",
                data=html_content,
                file_name="sunny_swim_report.html",
                mime="text/html",
            )


# ==================== NATIONAL STANDARD PAGE ====================
elif st.session_state.page == "Benchmarks":
    st.title("🏅 Benchmarks")
    st.caption("Chinese Female National Swimming Standards (Effective 2025-01-01)")
    st.caption("Source: Chinese Swimming Association")

    tab1, tab2 = st.tabs(["Long Course (50m)", "Short Course (25m)"])

    with tab1:
        with st.container(border=True):
            st.subheader("LC Standards - Chinese Female")
            df_lc = pd.DataFrame(LC_STANDARDS)
            st.dataframe(df_lc, use_container_width=True, hide_index=True)

    with tab2:
        with st.container(border=True):
            st.subheader("SC Standards - Chinese Female")
            df_sc = pd.DataFrame(SC_STANDARDS)
            st.dataframe(df_sc, use_container_width=True, hide_index=True)

    # Import from OCR Screenshot
    st.divider()
    st.subheader("Import Standards from Screenshot")
    uploaded_std = st.file_uploader("Upload a screenshot of swimming standards table", type=["png", "jpg", "jpeg"], key="std_screenshot")

    if uploaded_std:
        if st.button("Extract Standards via OCR", type="primary"):
            with st.spinner("Extracting standards from screenshot..."):
                from src.ocr_service import OCRService
                import base64

                # Read image and encode
                image_bytes = uploaded_std.read()
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                file_ext = uploaded_std.name.split('.')[-1].lower()
                mime_type = f"image/{'jpeg' if file_ext in ('jpg', 'jpeg') else file_ext}"

                # Use Qwen VL model to extract standards table
                from openai import OpenAI
                from src.config import ALIBABA_CLOUD_API_KEY, ALIBABA_CLOUD_BASE_URL

                client = OpenAI(api_key=ALIBABA_CLOUD_API_KEY, base_url=ALIBABA_CLOUD_BASE_URL)

                prompt = """Extract all swimming time standards from this image into a structured format.
For each event, provide: Event name (in English, e.g. "50m Freestyle"), and times for each level.
The columns are: International Master (国际级运动健将), National Master (运动健将), Level 1 (一级运动员), Level 2 (二级运动员).
There may be separate columns for 50m pool (Long Course) and 25m pool (Short Course).

Return as JSON with this structure:
{
  "lc_standards": [{"Event": "50m Freestyle", "International Master": "24.70", "National Master": "25.85", "Level 1": "27.20", "Level 2": "31.50"}, ...],
  "sc_standards": [{"Event": "50m Freestyle", "International Master": "24.44", "National Master": "25.00", "Level 1": "26.40", "Level 2": "30.50"}, ...]
}

Use English event names: "50m Freestyle", "100m Freestyle", "200m Freestyle", "400m Freestyle", "800m Freestyle", "1500m Freestyle", "50m Backstroke", "100m Backstroke", "200m Backstroke", "50m Breaststroke", "100m Breaststroke", "200m Breaststroke", "50m Butterfly", "100m Butterfly", "200m Butterfly", "100m IM", "200m IM", "400m IM".
Format times as SS.ss or M:SS.ss or MM:SS.ss as appropriate.
Return ONLY the JSON, no other text."""

                response = client.chat.completions.create(
                    model="qwen-vl-max",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}
                        ]
                    }]
                )

                result_text = response.choices[0].message.content

                # Try to parse JSON
                import json
                try:
                    # Strip markdown code fences if present
                    if "```json" in result_text:
                        result_text = result_text.split("```json")[1].split("```")[0]
                    elif "```" in result_text:
                        result_text = result_text.split("```")[1].split("```")[0]

                    extracted = json.loads(result_text.strip())

                    if "lc_standards" in extracted:
                        st.success(f"Extracted {len(extracted['lc_standards'])} LC standards and {len(extracted.get('sc_standards', []))} SC standards")

                        st.subheader("Extracted LC Standards")
                        df_extracted_lc = pd.DataFrame(extracted["lc_standards"])
                        st.dataframe(df_extracted_lc, use_container_width=True, hide_index=True)

                        if "sc_standards" in extracted and extracted["sc_standards"]:
                            st.subheader("Extracted SC Standards")
                            df_extracted_sc = pd.DataFrame(extracted["sc_standards"])
                            st.dataframe(df_extracted_sc, use_container_width=True, hide_index=True)

                        st.info("Note: To apply these standards, update the LC_STANDARDS and SC_STANDARDS in the source code.")
                    else:
                        st.warning("Could not parse standards structure from OCR result.")
                        st.code(result_text)
                except json.JSONDecodeError:
                    st.warning("OCR extracted text but couldn't parse as structured data:")
                    st.code(result_text)


# ==================== INSIGHTS PAGE ====================
elif st.session_state.page == "Insights":
    st.title("💡 Insights & Analysis")
    
    events = DataStore.load_swim_events()
    if not events:
        st.info("Upload race data to generate insights.")
    else:
        # --- Trend Insights (table format, sorted by improvement % descending) ---
        with st.container(border=True):
            st.subheader("Trend Insights")
            insights = InsightGenerator.generate_trend_insights()
            # Filter out info-only messages (no structured data)
            structured_insights = [i for i in insights if "event" in i]
            if structured_insights:
                # Sort by improvement percentage descending (biggest improvement first)
                structured_insights.sort(key=lambda x: x["improvement_pct"], reverse=True)
                trend_rows = []
                for ins in structured_insights:
                    trend_rows.append({
                        "Event": ins["event"],
                        "Improvement %": f"{ins['improvement_pct']:+.1f}%",
                        "From": ins["from_time"],
                        "From Date": ins["from_date"],
                        "To": ins["to_time"],
                        "To Date": ins["to_date"],
                    })
                trend_df = pd.DataFrame(trend_rows)
                st.dataframe(trend_df, use_container_width=True, hide_index=True)
            else:
                for insight in insights:
                    icon = {"positive": "🟢", "warning": "🟡", "neutral": "🔵", "info": "ℹ️"}.get(insight["type"], "ℹ️")
                    st.markdown(f"{icon} {insight['message']}")

        # --- Strengths & Weaknesses (table format) ---
        with st.container(border=True):
            st.subheader("Strengths & Weaknesses")
            sw = InsightGenerator.identify_strengths_weaknesses()
            if "error" not in sw:
                # Summary table: Strongest Stroke and Focus Area
                summary_rows = [
                    {"Metric": "💪 Strongest Stroke", "Value": (sw.get('strongest') or 'N/A').title()},
                    {"Metric": "🎯 Focus Area", "Value": (sw.get('weakest') or 'N/A').title()},
                ]
                st.table(pd.DataFrame(summary_rows))

                # Pace Analysis table
                st.markdown("**Pace Analysis**")
                pace_rows = [
                    {"Stroke": stroke.title(), "Pace (sec/m)": pace}
                    for stroke, pace in sw.get("stroke_paces", {}).items()
                ]
                if pace_rows:
                    st.dataframe(pd.DataFrame(pace_rows), use_container_width=True, hide_index=True)

        # --- Potential Assessment ---
        with st.container(border=True):
            st.subheader("Potential Assessment")
            assessment = InsightGenerator.assess_potential()
            if "error" not in assessment:
                cols = st.columns(3)
                kpi_items = [
                    ("Total Races", assessment["total_races"]),
                    ("Positive Trends", assessment["positive_trends"]),
                    ("Trajectory", assessment["trajectory"]),
                ]
                for col, (label, value) in zip(cols, kpi_items):
                    col.markdown(f"""
<div style="background: linear-gradient(135deg, {theme['bg_card_start']} 0%, {theme['bg_card_end']} 100%); 
            padding: 20px; border-radius: 12px; border-left: 4px solid {theme['accent']}; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <div style="color: {theme['text_secondary']}; font-size: 12px; text-transform: uppercase;">{label}</div>
    <div style="color: {theme['accent']}; font-size: 30px; font-weight: bold;">{value}</div>
</div>
""", unsafe_allow_html=True)

                st.markdown("")
                st.markdown(f'<span style="color: {theme["accent"]}; font-size: 14px;">**Consistency:** {assessment["consistency"]}</span>', unsafe_allow_html=True)
                st.info(f"📋 {assessment['recommendation']}")

        # --- Training Suggestions ---
        with st.container(border=True):
            st.subheader("Training Suggestions")
            suggestions = InsightGenerator.get_training_suggestions()
            for s in suggestions:
                priority_emoji = "🔴" if s["priority"] == "high" else "🟡"
                st.markdown(f"{priority_emoji} **{s['focus'].title()}**: {s['drills']}")


# ==================== Q&A PAGE ====================
elif st.session_state.page == "AI Coach":
    st.title("💬 Ask About Sunny's Swimming")
    
    st.markdown("Ask questions like:")
    st.caption("- What is Sunny's fastest 100m freestyle time?")
    st.caption("- How has her backstroke improved?")
    st.caption("- Which stroke should she focus on?")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input
    if question := st.chat_input("Ask a question about Sunny's swimming data..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": question})
        
        # Get answer
        qa = st.session_state.qa_service
        answer = qa.answer(question)
        
        # Add assistant message
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        
        st.rerun()
    
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.qa_service.clear_history()
        st.rerun()


