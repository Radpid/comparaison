#!/usr/bin/env python3
"""
PDF Text Extraction Benchmark Tool with Bilingual Support
Supports English/Deutsch
"""

import os
import sys
import time
import json
import logging
import pandas as pd
import plotly.express as px
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import asdict
import streamlit as st
from streamlit.logger import get_logger
from PIL import Image

# Configure logger
logger = get_logger(__name__)
logger.setLevel(logging.INFO)

# Internationalization
TRANSLATIONS = {
    "en": {
        "title": "PDF Text Extraction Benchmark",
        "select_folder": "Select PDF Folder",
        "run_benchmark": "Run Benchmark",
        "results": "Results",
        "file": "File",
        "tool": "Tool",
        "time_seconds": "Time (s)",
        "success": "Success",
        "size_mb": "Size (MB)",
        "char_count": "Characters",
        "overall_stats": "Overall Statistics",
        "avg_extraction_time": "Average Extraction Time",
        "success_rate": "Success Rate",
        "total_files": "Total Files",
        "total_extractions": "Total Extractions",
        "successful_extractions": "Successful Extractions",
        "benchmark_completed": "Benchmark completed!",
        "no_pdfs_found": "No PDF files found in the selected folder.",
        "select_folder_first": "Please select a folder first.",
        "error_occurred": "An error occurred: {}",
    },
    "de": {
        "title": "PDF-Text-Extraktion Benchmark",
        "select_folder": "PDF-Ordner auswählen",
        "run_benchmark": "Benchmark starten",
        "results": "Ergebnisse",
        "file": "Datei",
        "tool": "Werkzeug",
        "time_seconds": "Zeit (s)",
        "success": "Erfolg",
        "size_mb": "Größe (MB)",
        "char_count": "Zeichen",
        "overall_stats": "Gesamtstatistiken",
        "avg_extraction_time": "Durchschnittliche Extraktionszeit",
        "success_rate": "Erfolgsrate",
        "total_files": "Gesamtzahl der Dateien",
        "total_extractions": "Gesamtextraktionen",
        "successful_extractions": "Erfolgreiche Extraktionen",
        "benchmark_completed": "Benchmark abgeschlossen!",
        "no_pdfs_found": "Keine PDF-Dateien im ausgewählten Ordner gefunden.",
        "select_folder_first": "Bitte wählen Sie zuerst einen Ordner aus.",
        "error_occurred": "Ein Fehler ist aufgetreten: {}",
    }
}

class PDFExtractor:
    """Base class for PDF extractors"""
    
    def __init__(self, name: str):
        self.name = name
    
    def extract(self, pdf_path: str, output_dir: str) -> Tuple[bool, str, Optional[str]]:
        """Extract text from PDF"""
        raise NotImplementedError

class MinerUExtractor(PDFExtractor):
    """MinerU PDF extractor"""
    
    def __init__(self):
        super().__init__("MinerU")
    
    def extract(self, pdf_path: str, output_dir: str) -> Tuple[bool, str, Optional[str]]:
        try:
            import subprocess
            mineru_output = os.path.join(output_dir, "mineru_output")
            os.makedirs(mineru_output, exist_ok=True)
            
            cmd = ["mineru", "-p", pdf_path, "-o", mineru_output]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                return False, "", f"MinerU failed: {result.stderr}"
            
            output_files = list(Path(mineru_output).rglob("*.md"))
            if not output_files:
                return False, "", "No markdown output found"
            
            with open(output_files[0], 'r', encoding='utf-8') as f:
                content = f.read()
            
            return True, content, None
            
        except Exception as e:
            return False, "", f"MinerU error: {str(e)}"

class MarkerExtractor(PDFExtractor):
    """Marker PDF extractor"""
    
    def __init__(self):
        super().__init__("Marker")
        self._setup_marker()
    
    def _setup_marker(self):
        try:
            from marker.converters.pdf import PdfConverter
            from marker.models import create_model_dict
            from marker.output import text_from_rendered
            
            self.converter = PdfConverter(artifact_dict=create_model_dict())
            self.text_from_rendered = text_from_rendered
            
        except ImportError as e:
            logger.error(f"Marker not properly installed: {e}")
            self.converter = None
    
    def extract(self, pdf_path: str, output_dir: str) -> Tuple[bool, str, Optional[str]]:
        if self.converter is None:
            return False, "", "Marker not properly installed"
        
        try:
            rendered = self.converter(pdf_path)
            text, _, _ = self.text_from_rendered(rendered)
            
            output_file = os.path.join(output_dir, f"marker_{Path(pdf_path).stem}.md")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            return True, text, None
            
        except Exception as e:
            return False, "", f"Marker error: {str(e)}"

class CogMarkerExtractor(PDFExtractor):
    """Cog Marker PDF extractor"""
    
    def __init__(self):
        super().__init__("Cog Marker")
    
    def extract(self, pdf_path: str, output_dir: str) -> Tuple[bool, str, Optional[str]]:
        try:
            marker_extractor = MarkerExtractor()
            success, text, error = marker_extractor.extract(pdf_path, output_dir)
            
            if success:
                output_file = os.path.join(output_dir, f"cogmarker_{Path(pdf_path).stem}.md")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
            
            return success, text, error
            
        except Exception as e:
            return False, "", f"Cog Marker error: {str(e)}"

class PDFBenchmark:
    """Main benchmark class"""
    
    def __init__(self):
        self.extractors = [
            MinerUExtractor(),
            MarkerExtractor(),
            CogMarkerExtractor()
        ]
        self.results = []
    
    def find_pdfs(self, folder_path: str) -> List[str]:
        """Find all PDF files in the folder"""
        pdf_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        return pdf_files
    
    def run_benchmark(self, pdf_folder: str, output_dir: str, progress_callback=None) -> List[dict]:
        """Run benchmark on all PDFs in folder"""
        pdf_files = self.find_pdfs(pdf_folder)
        if not pdf_files:
            return []
        
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        for idx, pdf_file in enumerate(pdf_files):
            file_size_mb = os.path.getsize(pdf_file) / (1024 * 1024)
            
            for extractor in self.extractors:
                if progress_callback:
                    progress = (idx * len(self.extractors) + self.extractors.index(extractor)) / (len(pdf_files) * len(self.extractors))
                    progress_callback(progress, f"Processing {os.path.basename(pdf_file)} with {extractor.name}...")
                
                start_time = time.time()
                success, output_text, error = extractor.extract(pdf_file, output_dir)
                extraction_time = time.time() - start_time
                
                result = {
                    'file': os.path.basename(pdf_file),
                    'tool': extractor.name,
                    'time_seconds': round(extraction_time, 2),
                    'success': success,
                    'size_mb': round(file_size_mb, 2),
                    'char_count': len(output_text) if success else 0,
                    'error': error if not success else None
                }
                
                results.append(result)
                logger.info(f"Processed {result['file']} with {result['tool']} - {result['time_seconds']}s")
        
        self.results = results
        return results

def setup_ui():
    """Setup Streamlit UI"""
    st.set_page_config(
        page_title="PDF Text Extraction Benchmark",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Language selection
    lang = st.sidebar.radio("Language / Sprache", ["English", "Deutsch"])
    lang_code = "de" if lang == "Deutsch" else "en"
    _ = lambda x: TRANSLATIONS[lang_code].get(x, x)
    
    st.title(_("title"))
    st.markdown("---")
    
    # Folder selection
    col1, col2 = st.columns([3, 1])
    with col1:
        folder_path = st.text_input(_("select_folder"), 
                                  value=os.getcwd(),
                                  help=_("select_folder_help"))
    
    with col2:
        st.markdown("##")
        if st.button(_("run_benchmark"), type="primary"):
            if not folder_path or not os.path.exists(folder_path):
                st.error(_("select_folder_first"))
                return None, None, None
            
            return folder_path, lang_code, _
    
    return None, None, None

def show_results(results: List[dict], lang_code: str, _):
    """Display benchmark results"""
    if not results:
        st.warning(_("no_pdfs_found"))
        return
    
    df = pd.DataFrame(results)
    
    # Overall statistics
    st.subheader(_("overall_stats"))
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(_("total_files"), df['file'].nunique())
    with col2:
        st.metric(_("total_extractions"), len(df))
    with col3:
        st.metric(_("successful_extractions"), df['success'].sum())
    with col4:
        st.metric(_("success_rate"), f"{df['success'].mean()*100:.1f}%")
    
    # Results table
    st.subheader(_("results"))
    st.dataframe(
        df[["file", "tool", "time_seconds", "success", "size_mb", "char_count"]],
        column_config={
            "file": _("file"),
            "tool": _("tool"),
            "time_seconds": _("time_seconds"),
            "success": _("success"),
            "size_mb": _("size_mb"),
            "char_count": _("char_count")
        },
        use_container_width=True
    )
    
    # Visualizations
    st.subheader("Performance Comparison")
    
    # Success rate by tool
    success_rate = df.groupby('tool')['success'].mean().reset_index()
    fig1 = px.bar(
        success_rate, 
        x='tool', 
        y='success', 
        title=_("success_rate"),
        labels={'tool': _('tool'), 'success': _('success_rate')}
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Average extraction time by tool
    avg_time = df[df['success']].groupby('tool')['time_seconds'].mean().reset_index()
    fig2 = px.bar(
        avg_time, 
        x='tool', 
        y='time_seconds', 
        title=_("avg_extraction_time"),
        labels={'tool': _('tool'), 'time_seconds': _('time_seconds')}
    )
    st.plotly_chart(fig2, use_container_width=True)

def main():
    """Main function"""
    folder_path, lang_code, _ = setup_ui()
    
    if folder_path and lang_code:
        with st.spinner("Running benchmark..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(progress, status):
                progress_bar.progress(progress)
                status_text.text(status)
            
            benchmark = PDFBenchmark()
            output_dir = os.path.join(os.getcwd(), "benchmark_results")
            results = benchmark.run_benchmark(
                folder_path, 
                output_dir,
                progress_callback=update_progress
            )
            
            progress_bar.empty()
            status_text.empty()
            
            if results:
                st.balloons()
                st.success(TRANSLATIONS[lang_code].get("benchmark_completed"))
                show_results(results, lang_code, lambda x: TRANSLATIONS[lang_code].get(x, x))
            else:
                st.warning(TRANSLATIONS[lang_code].get("no_pdfs_found"))

if __name__ == "__main__":
    main()
