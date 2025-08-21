# GUI Application
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import customtkinter as ctk
import threading
import os
import logging
import webbrowser
from datetime import datetime

# Core modules
from pdf_processor import PDFProcessor
from markdown_analyzer import MarkdownGeminiAnalyzer  # Switched back to MarkdownGeminiAnalyzer
from visualization import SustainabilityVisualizer
from config import *

# Try to import enhanced export manager, fallback to regular if not available
try:
    from enhanced_export_manager import EnhancedReportExporter
    ENHANCED_EXPORT_AVAILABLE = True
except ImportError:
    from export_manager import ReportExporter
    ENHANCED_EXPORT_AVAILABLE = False

class SustainabilityCompassApp:
    """
    Main GUI application for Sustainability Compass
    """
    
    def __init__(self):
        self.setup_app()
        self.setup_components()
        self.setup_ui()
        self.current_analysis = None
        self.pdf_content = None
        
    def setup_app(self):
        """Setup the main application window"""
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(True, True)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
    def setup_components(self):
        """Initialize core components"""
        self.pdf_processor = PDFProcessor()
        
        # Initialize Gemini analyzer and check model
        try:
            self.gemini_analyzer = MarkdownGeminiAnalyzer()  # Switched back to MarkdownGeminiAnalyzer
            # Get the actual model name that was successfully configured
            model_name = getattr(self.gemini_analyzer.model, '_model_name', None)
            if model_name and 'gemini' in model_name.lower():
                # Clean up the model name for display
                display_name = model_name.replace('models/', '').replace('gemini-', 'Gemini ')
                # Special handling for different model versions
                if '2.5-pro' in model_name.lower():
                    display_name = 'Gemini 2.5 Pro'
                elif '2.5-flash-lite' in model_name.lower():
                    display_name = 'Gemini 2.5 Flash Lite'
                elif '2.5-flash' in model_name.lower():
                    display_name = 'Gemini 2.5 Flash'
                elif '1.5-flash' in model_name.lower():
                    display_name = 'Gemini 1.5 Flash'
                elif '1.5-pro' in model_name.lower():
                    display_name = 'Gemini 1.5 Pro'
                else:
                    display_name = display_name.title()
                self.api_status_text = f"🟢 {display_name} Ready (Full Content)"  # Added back Full Content indicator
            else:
                self.api_status_text = "🟢 Analysis Engine Ready (Full Content)"
        except Exception as e:
            self.gemini_analyzer = None
            self.api_status_text = f"🔴 API Error: {str(e)[:30]}..."
        
        self.visualizer = SustainabilityVisualizer()
        if ENHANCED_EXPORT_AVAILABLE:
            self.exporter = EnhancedReportExporter()
            print("✅ Using Enhanced Export with SDG Charts")
        else:
            self.exporter = ReportExporter()
            print("⚠️ Using Basic Export (Enhanced features not available)")
        
        # Application state
        self.current_language = tk.StringVar(value='en')
        self.selected_file = tk.StringVar()
        self.analysis_status = tk.StringVar(value="Ready to analyze")
        self.progress_var = tk.DoubleVar()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
        
        # Create status bar
        self.create_status_bar()
        
    def create_sidebar(self):
        """Create the sidebar with controls"""
        self.sidebar = ctk.CTkFrame(self.root, width=300)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.sidebar.grid_propagate(False)
        
        # Professional Header
        header_frame = ctk.CTkFrame(self.sidebar)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🌱 Sustainability\nCompass Pro", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=5, padx=10)
        
        tagline_label = ctk.CTkLabel(
            header_frame,
            text="Enterprise ESG Analytics",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        tagline_label.grid(row=1, column=0, pady=(0,5), padx=10)
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Language Selection
        lang_frame = ctk.CTkFrame(self.sidebar)
        lang_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        lang_label = ctk.CTkLabel(lang_frame, text="Language / اللغة:")
        lang_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")
        
        self.lang_combo = ctk.CTkComboBox(
            lang_frame,
            values=list(LANGUAGES.values()),
            variable=self.current_language,
            command=self.on_language_change
        )
        self.lang_combo.grid(row=1, column=0, pady=5, padx=10, sticky="ew")
        lang_frame.grid_columnconfigure(0, weight=1)
        
        # File Upload Section
        upload_frame = ctk.CTkFrame(self.sidebar)
        upload_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        upload_label = ctk.CTkLabel(upload_frame, text="Document Processing:")
        upload_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")
        
        self.upload_btn = ctk.CTkButton(
            upload_frame,
            text="📄 Import Document",
            command=self.select_pdf_file,
            height=40
        )
        self.upload_btn.grid(row=1, column=0, pady=5, padx=10, sticky="ew")
        
        self.file_label = ctk.CTkLabel(
            upload_frame, 
            textvariable=self.selected_file,
            wraplength=250,
            font=ctk.CTkFont(size=10)
        )
        self.file_label.grid(row=2, column=0, pady=5, padx=10, sticky="ew")
        upload_frame.grid_columnconfigure(0, weight=1)
        
        # Analysis Section
        analysis_frame = ctk.CTkFrame(self.sidebar)
        analysis_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        
        analysis_label = ctk.CTkLabel(analysis_frame, text="ESG Analysis Engine:")
        analysis_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")
        
        self.analyze_btn = ctk.CTkButton(
            analysis_frame,
            text="⚡ Process Analysis",
            command=self.start_analysis,
            height=40,
            state="disabled"
        )
        self.analyze_btn.grid(row=1, column=0, pady=5, padx=10, sticky="ew")
        
        self.progress_bar = ctk.CTkProgressBar(analysis_frame)
        self.progress_bar.grid(row=2, column=0, pady=5, padx=10, sticky="ew")
        self.progress_bar.set(0)
        
        analysis_frame.grid_columnconfigure(0, weight=1)
        
        # Export Section
        export_frame = ctk.CTkFrame(self.sidebar)
        export_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=10)
        
        export_label = ctk.CTkLabel(export_frame, text="Report Generation:")
        export_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")
        
        self.export_pdf_btn = ctk.CTkButton(
            export_frame,
            text="📋 Generate PDF Report",
            command=lambda: self.export_report('pdf'),
            state="disabled"
        )
        self.export_pdf_btn.grid(row=1, column=0, pady=2, padx=10, sticky="ew")
        
        self.export_word_btn = ctk.CTkButton(
            export_frame,
            text="📄 Generate Word Report",
            command=lambda: self.export_report('word'),
            state="disabled"
        )
        self.export_word_btn.grid(row=2, column=0, pady=2, padx=10, sticky="ew")
        
        self.export_excel_btn = ctk.CTkButton(
            export_frame,
            text="📊 Generate Excel Report",
            command=lambda: self.export_report('excel'),
            state="disabled"
        )
        self.export_excel_btn.grid(row=3, column=0, pady=2, padx=10, sticky="ew")
        
        self.view_dashboard_btn = ctk.CTkButton(
            export_frame,
            text="📈 Open Analytics Dashboard",
            command=self.view_dashboard,
            state="disabled"
        )
        self.view_dashboard_btn.grid(row=4, column=0, pady=2, padx=10, sticky="ew")
        
        export_frame.grid_columnconfigure(0, weight=1)
        
        # Make sidebar rows expand properly
        self.sidebar.grid_rowconfigure(5, weight=1)
        
    def create_main_content(self):
        """Create the main content area"""
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Create tabview for different sections
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Welcome Tab
        self.create_welcome_tab()
        
        # Analysis Results Tab (initially hidden)
        self.results_tab = None
        
    def create_welcome_tab(self):
        """Create the welcome tab"""
        welcome_tab = self.tabview.add("Welcome")
        
        # Welcome content
        welcome_content = ctk.CTkFrame(welcome_tab)
        welcome_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        welcome_title = ctk.CTkLabel(
            welcome_content,
            text="Sustainability Compass Pro",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        welcome_title.pack(pady=20)
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            welcome_content,
            text="Enterprise ESG Analytics Platform",
            font=ctk.CTkFont(size=18, weight="normal"),
            text_color="gray"
        )
        subtitle.pack(pady=(0,30))
        
        # Description
        description_text = """
        Comprehensive ESG performance analysis and reporting platform:
        
        💼 Economic & Financial Performance Analytics
        🌍 Environmental Impact Assessment
        👥 Social Responsibility Metrics  
        🎯 UN Sustainable Development Goals Alignment
        
        Import your sustainability documents and generate detailed
        compliance reports and executive dashboards.
        """
        
        description_label = ctk.CTkLabel(
            welcome_content,
            text=description_text,
            font=ctk.CTkFont(size=16),
            justify="center"
        )
        description_label.pack(pady=20)
        
        # Features
        features_frame = ctk.CTkFrame(welcome_content)
        features_frame.pack(pady=20, padx=40, fill="x")
        
        features_title = ctk.CTkLabel(
            features_frame,
            text="Key Features",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        features_title.pack(pady=10)
        
        features_list = [
            "📄 Advanced document processing (English & Arabic)",
            "⚡ Automated ESG performance analysis",
            "🎯 Complete UN SDG compliance mapping",
            "📊 Interactive executive dashboards",
            "📋 Enterprise reports (PDF, Word, Excel formats)"
        ]
        
        for feature in features_list:
            feature_label = ctk.CTkLabel(
                features_frame,
                text=feature,
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            feature_label.pack(pady=5, padx=20, anchor="w")
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_frame = ctk.CTkFrame(self.root, height=30)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            textvariable=self.analysis_status,
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # Processing Status
        self.api_status = ctk.CTkLabel(
            self.status_frame,
            text=getattr(self, 'api_status_text', "🟢 Analysis Engine Ready"),
            anchor="e"
        )
        self.api_status.pack(side="right", padx=10, pady=5)
        
    def on_language_change(self, value):
        """Handle language change"""
        # Map display values to language codes
        lang_map = {v: k for k, v in LANGUAGES.items()}
        self.current_language.set(lang_map.get(value, 'en'))
        self.update_ui_language()
        
    def update_ui_language(self):
        """Update UI text based on selected language"""
        lang = self.current_language.get()
        
        # Update button texts and labels based on language
        if lang == 'ar':
            self.upload_btn.configure(text="📄 استيراد المستند")
            self.analyze_btn.configure(text="⚡ تشغيل التحليل")
            self.export_pdf_btn.configure(text="📋 إنتاج تقرير PDF")
            self.export_word_btn.configure(text="📄 إنتاج تقرير Word")
            self.export_excel_btn.configure(text="📊 إنتاج تقرير Excel")
            self.view_dashboard_btn.configure(text="📈 فتح لوحة التحليلات")
        else:
            self.upload_btn.configure(text="📄 Import Document")
            self.analyze_btn.configure(text="⚡ Process Analysis")
            self.export_pdf_btn.configure(text="📋 Generate PDF Report")
            self.export_word_btn.configure(text="📄 Generate Word Report")
            self.export_excel_btn.configure(text="📊 Generate Excel Report")
            self.view_dashboard_btn.configure(text="📈 Open Analytics Dashboard")
            
    def select_pdf_file(self):
        """Handle PDF file selection"""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf")],
            initialdir=os.path.expanduser("~")
        )
        
        if file_path:
            self.selected_file.set(os.path.basename(file_path))
            self.pdf_file_path = file_path
            self.analyze_btn.configure(state="normal")
            self.analysis_status.set(f"PDF selected: {os.path.basename(file_path)}")
            
    def start_analysis(self):
        """Start the sustainability analysis"""
        if not hasattr(self, 'pdf_file_path'):
            messagebox.showerror("Error", "Please select a PDF file first.")
            return
            
        if not self.gemini_analyzer:
            messagebox.showerror("API Error", 
                               "Gemini AI is not available. Please check your API key and internet connection.\n"
                               "Run 'python test_api.py' to diagnose the issue.")
            return
            
        # Disable UI during analysis
        self.analyze_btn.configure(state="disabled")
        self.upload_btn.configure(state="disabled")
        
        # Start analysis in separate thread
        analysis_thread = threading.Thread(target=self.run_analysis)
        analysis_thread.daemon = True
        analysis_thread.start()
        
    def run_analysis(self):
        """Run the complete analysis pipeline"""
        try:
            # Update progress
            self.root.after(0, lambda: self.update_progress(0.1, "Processing PDF..."))
            
            # Step 1: Process PDF
            self.pdf_content = self.pdf_processor.extract_content(self.pdf_file_path)
            
            self.root.after(0, lambda: self.update_progress(0.3, "Analyzing with Gemini AI..."))
            
            # Step 2: Generate comprehensive analysis
            language = self.current_language.get()
            self.current_analysis = self.gemini_analyzer.analyze_full_document(
                self.pdf_content, language
            )  # Changed back to analyze_full_document for MarkdownGeminiAnalyzer
            
            self.root.after(0, lambda: self.update_progress(0.8, "Generating visualizations..."))
            
            # Step 3: Create visualizations
            # This will be done when viewing dashboard
            
            self.root.after(0, lambda: self.update_progress(1.0, "Analysis complete!"))
            
            # Update UI on main thread
            self.root.after(0, self.analysis_complete)
            
        except Exception as e:
            error_msg = f"Analysis failed: {str(e)}"
            self.root.after(0, lambda: self.analysis_error(error_msg))
            
    def update_progress(self, value: float, status: str):
        """Update progress bar and status"""
        self.progress_bar.set(value)
        self.analysis_status.set(status)
        
    def analysis_complete(self):
        """Handle analysis completion"""
        # Enable export buttons
        self.export_pdf_btn.configure(state="normal")
        self.export_word_btn.configure(state="normal")
        self.export_excel_btn.configure(state="normal")
        self.view_dashboard_btn.configure(state="normal")
        
        # Re-enable upload and analysis
        self.analyze_btn.configure(state="normal")
        self.upload_btn.configure(state="normal")
        
        # Create results tab
        self.create_results_tab()
        
        # Switch to results tab
        self.tabview.set("Results")
        
        # Update status
        self.analysis_status.set("ESG analysis completed - Reports ready for generation")
        
        # Show completion message
        messagebox.showinfo("Processing Complete", 
                          "ESG performance analysis completed successfully!\n"
                          "Executive reports and analytics dashboard are now available.")
        
    def analysis_error(self, error_msg: str):
        """Handle analysis error"""
        self.analyze_btn.configure(state="normal")
        self.upload_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.analysis_status.set("Analysis failed")
        
        messagebox.showerror("Analysis Error", error_msg)
        
    def create_results_tab(self):
        """Create the results tab with analysis summary"""
        if self.results_tab:
            self.tabview.delete("Results")
            
        self.results_tab = self.tabview.add("Results")
        
        # Results content
        results_content = ctk.CTkScrollableFrame(self.results_tab)
        results_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        results_title = ctk.CTkLabel(
            results_content,
            text="ESG Performance Analysis Results",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        results_title.pack(pady=20)
        
        # Executive Summary
        if self.current_analysis and 'executive_summary' in self.current_analysis:
            summary_frame = ctk.CTkFrame(results_content)
            summary_frame.pack(fill="x", pady=10, padx=20)
            
            summary_title = ctk.CTkLabel(
                summary_frame,
                text="Executive Summary",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            summary_title.pack(pady=10)
            
            summary_text = ctk.CTkTextbox(
                summary_frame,
                height=150,
                wrap="word"
            )
            summary_text.pack(fill="x", padx=20, pady=10)
            summary_text.insert("1.0", self.current_analysis['executive_summary'])
            summary_text.configure(state="disabled")
        
        # ESG Scores Summary
        if self.current_analysis and 'esg_analysis' in self.current_analysis:
            self.create_esg_summary(results_content)
            
        # SDG Summary
        if self.current_analysis and 'sdg_mapping' in self.current_analysis:
            self.create_sdg_summary(results_content)
            
    def create_esg_summary(self, parent):
        """Create ESG summary section"""
        esg_frame = ctk.CTkFrame(parent)
        esg_frame.pack(fill="x", pady=10, padx=20)
        
        esg_title = ctk.CTkLabel(
            esg_frame,
            text="ESG Performance Summary",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        esg_title.pack(pady=10)
        
        esg_analysis = self.current_analysis['esg_analysis']
        
        for category, data in esg_analysis.items():
            if isinstance(data, dict) and 'score' in data:
                category_frame = ctk.CTkFrame(esg_frame)
                category_frame.pack(fill="x", pady=5, padx=20)
                
                # Category name and score
                header_frame = ctk.CTkFrame(category_frame)
                header_frame.pack(fill="x", pady=5, padx=10)
                
                category_label = ctk.CTkLabel(
                    header_frame,
                    text=f"{category.title()}: {data['score']}/10",
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                category_label.pack(side="left")
                
                # Progress bar for score
                score_progress = ctk.CTkProgressBar(header_frame)
                score_progress.pack(side="right", padx=10)
                score_progress.set(data['score'] / 10)
                
    def create_sdg_summary(self, parent):
        """Create SDG summary section"""
        sdg_frame = ctk.CTkFrame(parent)
        sdg_frame.pack(fill="x", pady=10, padx=20)
        
        sdg_title = ctk.CTkLabel(
            sdg_frame,
            text="Top Contributing SDGs",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        sdg_title.pack(pady=10)
        
        # Get top 5 SDGs
        sdg_mapping = self.current_analysis['sdg_mapping']
        sdg_scores = []
        
        for sdg_key, data in sdg_mapping.items():
            if sdg_key.startswith('sdg_') and isinstance(data, dict):
                sdg_num = int(sdg_key.split('_')[1])
                score = data.get('score', 0)
                if score > 0:
                    sdg_scores.append({
                        'sdg': f"SDG {sdg_num}: {SDG_GOALS.get(sdg_num, '')}",
                        'score': score
                    })
        
        sdg_scores.sort(key=lambda x: x['score'], reverse=True)
        top_5_sdgs = sdg_scores[:5]
        
        for sdg in top_5_sdgs:
            sdg_item_frame = ctk.CTkFrame(sdg_frame)
            sdg_item_frame.pack(fill="x", pady=2, padx=20)
            
            sdg_label = ctk.CTkLabel(
                sdg_item_frame,
                text=f"{sdg['sdg'][:50]}... ({sdg['score']}/10)",
                anchor="w"
            )
            sdg_label.pack(side="left", padx=10, pady=5)
            
            sdg_progress = ctk.CTkProgressBar(sdg_item_frame)
            sdg_progress.pack(side="right", padx=10, pady=5)
            sdg_progress.set(sdg['score'] / 10)
            
    def export_report(self, format_type: str):
        """Export report in specified format"""
        if not self.current_analysis:
            messagebox.showerror("Error", "No analysis results to export.")
            return
            
        # Get save location
        extensions = {
            'pdf': '.pdf',
            'word': '.docx',
            'excel': '.xlsx'
        }
        
        file_path = filedialog.asksaveasfilename(
            title=f"Save {format_type.title()} Report",
            defaultextension=extensions[format_type],
            filetypes=[(f"{format_type.title()} files", f"*{extensions[format_type]}")]
        )
        
        if not file_path:
            return
            
        try:
            language = self.current_language.get()
            success = False
            
            if format_type == 'pdf':
                success = self.exporter.export_pdf_report(self.current_analysis, file_path, language)
            elif format_type == 'word':
                success = self.exporter.export_word_report(self.current_analysis, file_path, language)
            elif format_type == 'excel':
                success = self.exporter.export_excel_report(self.current_analysis, file_path, language)
                
            if success:
                messagebox.showinfo("Export Successful", f"Report exported successfully to:\n{file_path}")
            else:
                messagebox.showerror("Export Failed", f"Failed to export {format_type} report.")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting report: {str(e)}")
            
    def view_dashboard(self):
        """View interactive dashboard"""
        if not self.current_analysis:
            messagebox.showerror("Error", "No analysis results to display.")
            return
            
        try:
            # Generate dashboard HTML
            dashboard_html = self.visualizer.create_comprehensive_dashboard(self.current_analysis)
            
            # Save to temporary file
            temp_file = os.path.join(os.path.expanduser("~"), "sustainability_dashboard.html")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(dashboard_html)
            
            # Open in browser
            webbrowser.open(f'file://{temp_file}')
            
            messagebox.showinfo("Analytics Dashboard", "Interactive analytics dashboard opened in your browser.")
            
        except Exception as e:
            messagebox.showerror("Dashboard Error", f"Error creating dashboard: {str(e)}")
            
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = SustainabilityCompassApp()
        app.run()
    except Exception as e:
        print(f"Application failed to start: {str(e)}")
        messagebox.showerror("Startup Error", f"Failed to start application: {str(e)}")

if __name__ == "__main__":
    main() 