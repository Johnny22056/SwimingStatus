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

# Page config
st.set_page_config(
    page_title="Sunny's Swimming Analysis",
    page_icon="🏊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit default menu and deploy button
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
.stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Import"
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
    st.markdown("---")
    
    pages = ["Import", "Records", "Body Metrics", "National Standard", "Analytics", "Insights", "Q&A"]
    for page in pages:
        if st.button(page, use_container_width=True, 
                     type="primary" if st.session_state.page == page else "secondary"):
            switch_page(page)
    
    st.markdown("---")
    st.caption("Data-driven swimming development")


# ==================== IMPORT PAGE ====================
if st.session_state.page == "Import":
    st.header("📥 Import Screenshots")
    st.markdown("Upload or batch-import swimming meet screenshots to extract and analyze data.")
    
    # Quick Stats at the top
    uc1, uc2, uc3, uc4 = st.columns(4)
    uc1.metric("Uploaded", st.session_state.upload_new_count)
    uc2.metric("Success", st.session_state.upload_success_count)
    uc3.metric("Failed", st.session_state.upload_failed_count)
    uc4.metric("Duplicates", st.session_state.upload_duplicate_count)
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
        meet_name = st.text_input("Meet Name", value="Swim Meet")
        event_date = st.date_input("Event Date", value=datetime.now())
        uploaded_file = st.file_uploader("Choose screenshot", type=["png", "jpg", "jpeg"])
        
        if uploaded_file and st.button("Upload & Extract", type="primary"):
            try:
                # Save screenshot
                success, msg = ScreenshotManager.save_uploaded_screenshot(
                    uploaded_file, meet_name, event_date.strftime("%Y-%m-%d")
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
                    screenshot_path = str(SCREENSHOTS_DIR / ScreenshotManager.sanitize_meet_name(meet_name) / event_date.strftime("%Y-%m-%d") / uploaded_file.name)
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
                        date=data.get("date", event_date.strftime("%Y-%m-%d")),
                        meet_name=data.get("meet_name", meet_name),
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
                        DataStore.add_swim_event(event)
                        st.session_state.upload_success_count += 1
                        st.success("Event saved successfully!")
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
                        
                        mc_date = st.date_input("Date", value=datetime.strptime(extracted.get("date", event_date.strftime("%Y-%m-%d")) or event_date.strftime("%Y-%m-%d"), "%Y-%m-%d") if extracted.get("date") else event_date)
                        mc_meet = st.text_input("Meet Name", value=extracted.get("meet_name") or meet_name)
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
                                    DataStore.add_swim_event(event)
                                    st.session_state.upload_success_count += 1
                                    st.success("Event saved successfully!")
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
                                DataStore.add_swim_event(event)
                                succeeded.append((img_path.name, data))
                        else:
                            failed.append((img_path.name, extract_msg, data))
                    
                    status_text.text("Processing complete!")
                    
                    # Summary
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Succeeded", len(succeeded))
                    col2.metric("Skipped (duplicates)", len(skipped))
                    col3.metric("Failed", len(failed))
                    
                    # Show succeeded items
                    if succeeded:
                        st.subheader("Successfully Processed")
                        for name, data in succeeded:
                            st.markdown(f"✅ **{name}** — {data.get('stroke', '')} {data.get('distance', '')}m {data.get('time', '')}")
                    
                    # Show skipped items
                    if skipped:
                        st.subheader("Skipped (Duplicates)")
                        for name, msg in skipped:
                            st.markdown(f"⏭️ **{name}**: {msg}")
                    
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
                                DataStore.add_swim_event(event)
                                success_count += 1
                            except Exception as e:
                                error_count += 1
                        
                        if success_count > 0:
                            st.success(f"Successfully imported {success_count} records!")
                            st.session_state.upload_success_count += success_count
                        if error_count > 0:
                            st.warning(f"Failed to import {error_count} records due to data errors.")
                            st.session_state.upload_failed_count += error_count
                            
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")


# ==================== RECORDS PAGE ====================
elif st.session_state.page == "Records":
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
                "Splits": ", ".join(e.splits) if e.splits else "-"
            })
        
        df = pd.DataFrame(records)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            stroke_filter = st.selectbox("Filter by Stroke", ["All"] + sorted(df["Stroke"].unique().tolist()))
        with col2:
            distance_filter = st.selectbox("Filter by Distance", ["All"] + sorted(df["Distance"].unique().tolist(), key=lambda x: int(x) if str(x).isdigit() else 0))
        with col3:
            meet_filter = st.selectbox("Filter by Meet", ["All"] + sorted(df["Meet"].unique().tolist()))
        
        # Apply filters
        filtered_df = df.copy()
        if stroke_filter != "All":
            filtered_df = filtered_df[filtered_df["Stroke"] == stroke_filter]
        if distance_filter != "All":
            filtered_df = filtered_df[filtered_df["Distance"] == distance_filter]
        if meet_filter != "All":
            filtered_df = filtered_df[filtered_df["Meet"] == meet_filter]
        
        # Stats
        st.caption(f"Showing {len(filtered_df)} of {len(df)} events across {df['Meet'].nunique()} meets")
        
        # Table
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # Download
        csv = filtered_df.to_csv(index=False)
        st.download_button("Download CSV", csv, "swim_records.csv", "text/csv")


# ==================== BODY METRICS PAGE ====================
elif st.session_state.page == "Body Metrics":
    st.title("📏 Body Metrics")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
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
            st.subheader("History")
            df = pd.DataFrame([m.to_dict() for m in metrics])
            df["bmi"] = [m.bmi for m in metrics]
            df["date"] = pd.to_datetime(df["date"])
            st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)
            



# ==================== ANALYTICS PAGE ====================
elif st.session_state.page == "Analytics":
    st.title("📊 Performance Analytics")
    
    events = DataStore.load_swim_events()
    if not events:
        st.info("No race data yet. Upload screenshots to see analytics.")
    else:
        # Summary cards
        summary = PerformanceAnalytics.get_dashboard_summary()
        cols = st.columns(4)
        cols[0].metric("Total Meets", summary["total_meets"])
        cols[1].metric("Total Events", summary["total_events"])
        cols[2].metric("Personal Bests", summary["personal_bests"])
        cols[3].metric("Strokes", len(summary["strokes"]))
        
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
        
        pb_df = PerformanceAnalytics.get_personal_bests()
        if not pb_df.empty:
            pb_df["_sort"] = pb_df.apply(_pb_sort_key, axis=1)
            pb_df = pb_df.sort_values("_sort").drop(columns=["_sort"])
            pb_df["Event"] = pb_df["distance"].astype(str) + "m " + pb_df["stroke"].str.title()
            display_cols = ["Event", "time", "date", "meet_name"]
            display_rename = {"time": "Time", "date": "Date", "meet_name": "Meet"}
        
            lc_df = pb_df[pb_df["course"] == "LC"]
            sc_df = pb_df[pb_df["course"] == "SC"]
            other_df = pb_df[~pb_df["course"].isin(["LC", "SC"])]
        
            if not lc_df.empty:
                st.subheader("PB - LC")
                st.dataframe(
                    lc_df[display_cols].rename(columns=display_rename),
                    use_container_width=True, hide_index=True,
                )
        
            if not sc_df.empty:
                st.subheader("PB - SC")
                st.dataframe(
                    sc_df[display_cols].rename(columns=display_rename),
                    use_container_width=True, hide_index=True,
                )
        
            if not other_df.empty:
                st.subheader("Personal Bests")
                st.dataframe(
                    other_df[display_cols].rename(columns=display_rename),
                    use_container_width=True, hide_index=True,
                )
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

            # Each stroke-distance combo gets its own chart
            charts_shown = 0
            for (stroke, distance), records in sorted(dev_data.items(), key=lambda x: (x[0][0], x[0][1])):
                # Deduplicate: keep only best (fastest) time per day
                best_by_date = {}
                for r in records:
                    d = r["date"]
                    if d not in best_by_date or r["time_seconds"] < best_by_date[d]["time_seconds"]:
                        best_by_date[d] = r
                records = sorted(best_by_date.values(), key=lambda x: x["date"])

                if len(records) <= 2:
                    continue

                charts_shown += 1
                label = f"{distance}m {stroke.title()}"
                st.subheader(label)

                dates = [r["date"] for r in records]
                times_sec = [r["time_seconds"] for r in records]
                time_labels = [r["time"] for r in records]

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

                # Add National/International Master and Level 1 reference lines from LC Standards
                lc_match = next((s for s in LC_STANDARDS if s["Event"].lower() == label.lower()), None)
                nat_master_secs = 0
                int_master_secs = 0
                level1_secs = 0
                if lc_match:
                    nat_master_secs = time_to_seconds(lc_match["National Master"])
                    int_master_secs = time_to_seconds(lc_match["International Master"])
                    level1_secs = time_to_seconds(lc_match["Level 1"])
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
                if lc_match:
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
                if lc_match:
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
                )
                fig.update_yaxes(
                    tickvals=tick_vals,
                    ticktext=tick_text,
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
elif st.session_state.page == "National Standard":
    st.header("National Standard")
    st.caption("Chinese Female National Swimming Standards (Effective 2025-01-01)")
    st.caption("Source: Chinese Swimming Association")

    tab1, tab2 = st.tabs(["Long Course (50m)", "Short Course (25m)"])

    with tab1:
        st.subheader("LC Standards - Chinese Female")
        df_lc = pd.DataFrame(LC_STANDARDS)
        st.dataframe(df_lc, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("SC Standards - Chinese Female")
        df_sc = pd.DataFrame(SC_STANDARDS)
        st.dataframe(df_sc, use_container_width=True, hide_index=True)

    # Export as Excel
    st.divider()
    st.subheader("Export Standards")

    # Create Excel file in memory
    import io

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        pd.DataFrame(LC_STANDARDS).to_excel(writer, sheet_name='Long Course (50m)', index=False)
        pd.DataFrame(SC_STANDARDS).to_excel(writer, sheet_name='Short Course (25m)', index=False)

    st.download_button(
        label="📥 Download Standards as Excel",
        data=output.getvalue(),
        file_name="chinese_swimming_standards_2025.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

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
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Trend Insights")
            insights = InsightGenerator.generate_trend_insights()
            for insight in insights:
                icon = {"positive": "🟢", "warning": "🟡", "neutral": "🔵", "info": "ℹ️"}.get(insight["type"], "ℹ️")
                st.markdown(f"{icon} {insight['message']}")
        
        with col2:
            st.subheader("Strengths & Weaknesses")
            sw = InsightGenerator.identify_strengths_weaknesses()
            if "error" not in sw:
                st.markdown(f"**💪 Strongest Stroke:** {sw.get('strongest', 'N/A').title()}")
                st.markdown(f"**🎯 Focus Area:** {sw.get('weakest', 'N/A').title()}")
                
                st.markdown("**Pace Analysis:**")
                for stroke, pace in sw.get("stroke_paces", {}).items():
                    st.markdown(f"- {stroke.title()}: {pace}")
        
        st.markdown("---")
        
        st.subheader("Potential Assessment")
        assessment = InsightGenerator.assess_potential()
        if "error" not in assessment:
            cols = st.columns(3)
            cols[0].metric("Total Races", assessment["total_races"])
            cols[1].metric("Positive Trends", assessment["positive_trends"])
            cols[2].metric("Trajectory", assessment["trajectory"])
            
            st.markdown(f"**Consistency:** {assessment['consistency']}")
            st.info(f"📋 {assessment['recommendation']}")
        
        st.markdown("---")
        
        st.subheader("Training Suggestions")
        suggestions = InsightGenerator.get_training_suggestions()
        for s in suggestions:
            priority_emoji = "🔴" if s["priority"] == "high" else "🟡"
            st.markdown(f"{priority_emoji} **{s['focus'].title()}**: {s['drills']}")


# ==================== Q&A PAGE ====================
elif st.session_state.page == "Q&A":
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


