"""Sunny's Swimming Data Analysis Platform - Main Streamlit Application."""
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

logger = logging.getLogger(__name__)

from src.config import SCREENSHOTS_DIR, DATA_DIR
from src.models import SwimEvent, BodyMetrics
from src.storage import DataStore, ScreenshotIndex
from src.screenshot_manager import ScreenshotManager
from src.ocr_service import OCRService
from src.validation import validate_swim_event_data, validate_field_types, validate_body_metrics, time_to_seconds
from src.analytics import PerformanceAnalytics
from src.research_service import ResearchService
from src.insights import InsightGenerator
from src.qa_service import QAService

# Page config
st.set_page_config(
    page_title="Sunny's Swimming Analysis",
    page_icon="🏊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Upload"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_extraction" not in st.session_state:
    st.session_state.last_extraction = None
if "qa_service" not in st.session_state:
    st.session_state.qa_service = QAService(conversation_history=st.session_state.chat_history)
else:
    # Re-sync conversation history on reruns so QAService uses session state as source of truth
    st.session_state.qa_service.conversation_history = st.session_state.chat_history


def switch_page(page_name: str):
    st.session_state.page = page_name
    st.rerun()


# Sidebar Navigation
with st.sidebar:
    st.title("🏊 Sunny's Swimming")
    st.markdown("---")
    
    pages = ["Upload", "Batch Process", "Records", "Gallery", "Body Metrics", "Analytics", "Research", "Insights", "Q&A"]
    for page in pages:
        if st.button(page, use_container_width=True, 
                     type="primary" if st.session_state.page == page else "secondary"):
            switch_page(page)
    
    st.markdown("---")
    st.caption("Data-driven swimming development")


# ==================== UPLOAD PAGE ====================
if st.session_state.page == "Upload":
    st.title("📤 Upload Screenshots")
    st.markdown("Upload swimming meet screenshots to extract and analyze data.")
    
    col1, col2 = st.columns(2)
    
    with col1:
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
                        st.success("Event saved successfully!")
                else:
                    st.warning(f"Extraction had issues: {extract_msg}")
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
                                    st.success("Event saved successfully!")
                                    st.session_state.last_extraction = None
                                    st.rerun()
            else:
                st.error(msg)
    
    with col2:
        st.subheader("Quick Stats")
        summary = PerformanceAnalytics.get_dashboard_summary()
        st.metric("Total Meets", summary["total_meets"])
        st.metric("Total Events", summary["total_events"])
        st.metric("Personal Bests", summary["personal_bests"])
        st.metric("Screenshots", ScreenshotManager.get_screenshot_count())


# ==================== BATCH PROCESS PAGE ====================
elif st.session_state.page == "Batch Process":
    st.header("📂 Batch Process Screenshots")
    
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
                        # Build SwimEvent from OCR data (same logic as Upload page)
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


# ==================== GALLERY PAGE ====================
elif st.session_state.page == "Gallery":
    st.title("🖼️ Screenshot Gallery")
    
    screenshots = ScreenshotManager.list_screenshots()
    
    if not screenshots:
        st.info("No screenshots uploaded yet. Go to Upload page to add screenshots.")
    else:
        st.write(f"Total screenshots: {len(screenshots)}")
        
        # Group by meet
        meet_groups = {}
        for s in screenshots:
            meet = s.get("meet_name", "Unknown")
            if meet not in meet_groups:
                meet_groups[meet] = []
            meet_groups[meet].append(s)
        
        for meet, items in meet_groups.items():
            with st.expander(f"📁 {meet} ({len(items)} screenshots)"):
                cols = st.columns(3)
                for i, screenshot in enumerate(items):
                    with cols[i % 3]:
                        thumb = ScreenshotManager.get_screenshot_thumbnail(screenshot["path"])
                        if thumb:
                            st.image(thumb, use_container_width=True)
                        st.caption(f"{screenshot['original_filename']}")
                        st.caption(f"Date: {screenshot['date']}")
                        
                        if st.button("🗑️ Delete", key=f"del_{screenshot['path']}"):
                            success, msg = ScreenshotManager.delete_screenshot(screenshot["path"])
                            if success:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)


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
            
            st.subheader("Progression Charts")
            tab1, tab2, tab3 = st.tabs(["Height", "Weight", "BMI"])
            
            with tab1:
                fig = px.line(df.sort_values("date"), x="date", y="height_cm", 
                             title="Height Over Time", markers=True)
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                fig = px.line(df.sort_values("date"), x="date", y="weight_kg",
                             title="Weight Over Time", markers=True)
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                fig = px.line(df.sort_values("date"), x="date", y="bmi",
                             title="BMI Over Time", markers=True)
                st.plotly_chart(fig, use_container_width=True)


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
        
        # Time progression
        st.subheader("Time Progression")
        strokes = sorted(list(set(e.stroke for e in events if e.stroke)))
        distances = sorted(list(set(e.distance for e in events if e.distance)))
        
        if strokes and distances:
            col1, col2 = st.columns(2)
            selected_stroke = col1.selectbox("Stroke", strokes)
            selected_distance = col2.selectbox("Distance (m)", distances)
            
            fig = PerformanceAnalytics.create_time_progression_chart(selected_stroke, selected_distance)
            if fig.data:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data for this stroke/distance combination.")
        
        st.markdown("---")
        
        # Stroke comparison
        st.subheader("Stroke Comparison")
        radar_fig = PerformanceAnalytics.create_stroke_radar_chart()
        if radar_fig.data:
            st.plotly_chart(radar_fig, use_container_width=True)
        else:
            st.info("Need data in multiple strokes for comparison.")
        
        st.markdown("---")
        
        # Personal bests
        st.subheader("Personal Bests")
        pb_df = PerformanceAnalytics.get_personal_bests()
        if not pb_df.empty:
            st.dataframe(pb_df[["stroke", "distance", "course", "time", "date", "meet_name"]], 
                        use_container_width=True)
        else:
            st.info("No personal bests recorded yet.")


# ==================== RESEARCH PAGE ====================
elif st.session_state.page == "Research":
    st.title("🔬 Research Comparison")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Compare Against Benchmarks")
        stroke = st.selectbox("Stroke", ["freestyle", "backstroke", "breaststroke", "butterfly", "IM"])
        distance = st.selectbox("Distance", [50, 100, 200, 400, 800])
        age = st.number_input("Age", min_value=5, max_value=20, value=10)
        
        if st.button("Search Benchmarks", type="primary"):
            with st.spinner("Searching..."):
                results = ResearchService.search_benchmarks(stroke, distance, age)
            
            st.subheader("Search Results")
            for r in results:
                with st.expander(r.get("title", "Result")):
                    st.write(r.get("body", "No description"))
                    if r.get("href"):
                        st.markdown(f"[Link]({r['href']})")
    
    with col2:
        st.subheader("Performance vs Benchmarks")
        comparison = ResearchService.get_comparison(stroke, distance, age)
        
        if "error" in comparison:
            st.info(comparison["error"])
        else:
            st.metric("Personal Best", comparison["personal_best"])
            st.caption(f"Achieved: {comparison['pb_date']}")
            
            st.markdown("---")
            st.subheader("Benchmark References")
            for b in comparison.get("benchmarks", []):
                st.markdown(f"- **{b.get('title', 'Unknown')}**: {b.get('body', '')[:100]}...")


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


# ==================== DATA EXPORT (Footer) ====================
st.markdown("---")
with st.expander("💾 Data Management"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export
        if st.button("Export All Data (JSON)"):
            export_data = {
                "swim_events": [e.to_dict() for e in DataStore.load_swim_events()],
                "body_metrics": [m.to_dict() for m in DataStore.load_body_metrics()],
                "screenshots": ScreenshotIndex.list_all(),
                "exported_at": datetime.now().isoformat()
            }
            st.download_button(
                label="Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"sunny_swim_data_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col2:
        # Import
        uploaded_backup = st.file_uploader("Import Backup JSON", type=["json"])
        if uploaded_backup and st.button("Restore Data"):
            try:
                data = json.loads(uploaded_backup.read())
            except json.JSONDecodeError as e:
                logger.error("Failed to parse backup JSON: %s", e)
                st.error(f"Invalid JSON file: {e}")
            except Exception as e:
                logger.error("Unexpected error reading backup file", exc_info=True)
                st.error(f"Failed to read backup file: {type(e).__name__}: {str(e)}")
            else:
                # Validate structure before writing anything
                try:
                    swim_events = [SwimEvent.from_dict(e) for e in data.get("swim_events", [])]
                except (KeyError, ValueError, TypeError) as e:
                    logger.error("Invalid swim_events data in backup: [%s] %s", type(e).__name__, e)
                    st.error(f"Invalid swim events data in backup: {type(e).__name__}: {str(e)}")
                    swim_events = None

                try:
                    body_metrics = [BodyMetrics.from_dict(m) for m in data.get("body_metrics", [])]
                except (KeyError, ValueError, TypeError) as e:
                    logger.error("Invalid body_metrics data in backup: [%s] %s", type(e).__name__, e)
                    st.error(f"Invalid body metrics data in backup: {type(e).__name__}: {str(e)}")
                    body_metrics = None

                # Only persist if ALL parts parsed successfully
                if swim_events is not None and body_metrics is not None:
                    try:
                        if swim_events:
                            DataStore.save_swim_events(swim_events)
                        if body_metrics:
                            DataStore.save_body_metrics(body_metrics)
                        st.success("Data restored successfully!")
                    except (OSError, IOError) as e:
                        logger.error("Failed to write restored data: [%s] %s", type(e).__name__, e)
                        st.error(f"Failed to save restored data: {type(e).__name__}: {str(e)}")
                else:
                    st.error("Restore aborted due to validation errors. No data was changed.")
    
    with col3:
        st.markdown("**API Status**")
        from src.config import ALIBABA_CLOUD_API_KEY
        if ALIBABA_CLOUD_API_KEY:
            st.success("✅ Alibaba Cloud API configured")
        else:
            st.warning("⚠️ Set ALIBABA_CLOUD_API_KEY environment variable")
