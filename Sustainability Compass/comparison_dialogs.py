#!/usr/bin/env python3
"""
Comparison Dialog Windows
UI components for managing multi-year report comparisons
"""

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import customtkinter as ctk
from typing import Dict, List, Optional, Tuple
import threading
import webbrowser
import os
from datetime import datetime
from comparison_exporter import ComparisonReportExporter

class SaveReportDialog:
    """Dialog for saving current report for comparison"""
    
    def __init__(self, parent):
        self.result = None
        
        # Create dialog window
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Save Report for Comparison")
        self.dialog.geometry("450x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (parent.winfo_rootx() + parent.winfo_width()//2) - (450//2)
        y = (parent.winfo_rooty() + parent.winfo_height()//2) - (350//2)
        self.dialog.geometry(f"450x350+{x}+{y}")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI"""
        # Title
        title_label = ctk.CTkLabel(
            self.dialog,
            text="Save Report for Multi-Year Comparison",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(20,30))
        
        # Company name input
        company_frame = ctk.CTkFrame(self.dialog)
        company_frame.pack(fill="x", padx=30, pady=15)
        
        company_label = ctk.CTkLabel(
            company_frame, 
            text="Company Name:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        company_label.pack(anchor="w", padx=15, pady=(15,5))
        
        self.company_entry = ctk.CTkEntry(
            company_frame, 
            placeholder_text="Enter company name",
            height=35
        )
        self.company_entry.pack(fill="x", padx=15, pady=(0,15))
        
        # Year input
        year_frame = ctk.CTkFrame(self.dialog)
        year_frame.pack(fill="x", padx=30, pady=15)
        
        year_label = ctk.CTkLabel(
            year_frame, 
            text="Report Year:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        year_label.pack(anchor="w", padx=15, pady=(15,5))
        
        self.year_entry = ctk.CTkEntry(
            year_frame, 
            placeholder_text="e.g., 2024",
            height=35
        )
        self.year_entry.pack(fill="x", padx=15, pady=(0,15))
        
        # Set default year to current year
        current_year = datetime.now().year
        self.year_entry.insert(0, str(current_year))
        
        # Buttons
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(20,30))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.cancel,
            width=100,
            height=35
        )
        cancel_btn.pack(side="right", padx=(15,0))
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Report",
            command=self.save,
            width=120,
            height=35
        )
        save_btn.pack(side="right")
        
        # Focus on company entry
        self.company_entry.focus()
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.save())
        
    def save(self):
        """Save the report"""
        company_name = self.company_entry.get().strip()
        year_text = self.year_entry.get().strip()
        
        if not company_name:
            messagebox.showerror("Error", "Please enter a company name.")
            return
        
        if not year_text:
            messagebox.showerror("Error", "Please enter a year.")
            return
        
        try:
            year = int(year_text)
            if year < 1900 or year > 2100:
                raise ValueError("Year out of range")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year (1900-2100).")
            return
        
        self.result = (company_name, year)
        self.dialog.destroy()
        
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()

class ComparisonManagerWindow:
    """Main window for managing report comparisons"""
    
    def __init__(self, parent, report_comparison, comparison_visualizer):
        self.report_comparison = report_comparison
        self.comparison_visualizer = comparison_visualizer
        self.comparison_exporter = ComparisonReportExporter()
        self.current_comparison = None
        
        # Create main window
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Multi-Year Report Comparison Manager")
        self.window.geometry("1200x800")
        self.window.transient(parent)
        
        # Center the window
        self.window.update_idletasks()
        x = (parent.winfo_rootx() + parent.winfo_width()//2) - (1200//2)
        y = (parent.winfo_rooty() + parent.winfo_height()//2) - (800//2)
        self.window.geometry(f"1200x800+{x}+{y}")
        
        self.setup_ui()
        self.refresh_companies()
        
    def setup_ui(self):
        """Setup the manager UI"""
        # Title
        title_label = ctk.CTkLabel(
            self.window,
            text="Multi-Year Sustainability Report Comparison",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Main content area with two columns
        content_frame = ctk.CTkFrame(self.window)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel - Company and report selection
        self.setup_left_panel(content_frame)
        
        # Right panel - Comparison results
        self.setup_right_panel(content_frame)
        
    def setup_left_panel(self, parent):
        """Setup the left panel for company selection"""
        # Create container for left panel
        left_container = ctk.CTkFrame(parent, width=350)
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0,10))
        left_container.grid_propagate(False)
        left_container.grid_rowconfigure(0, weight=1)
        left_container.grid_columnconfigure(0, weight=1)
        
        # Create scrollable frame for left panel content
        left_panel = ctk.CTkScrollableFrame(left_container, width=330)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Company selection
        company_label = ctk.CTkLabel(
            left_panel,
            text="Select Company:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        company_label.pack(pady=(20,10), padx=20, anchor="w")
        
        self.company_listbox = tk.Listbox(
            left_panel,
            selectmode="single",
            font=("Arial", 10),
            height=8
        )
        self.company_listbox.pack(fill="x", padx=20, pady=(0,10))
        self.company_listbox.bind('<<ListboxSelect>>', self.on_company_select)
        
        # Year selection
        year_label = ctk.CTkLabel(
            left_panel,
            text="Select Years to Compare:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        year_label.pack(pady=(20,10), padx=20, anchor="w")
        
        # Year selection frame with checkboxes
        self.year_frame = ctk.CTkScrollableFrame(left_panel, height=200)
        self.year_frame.pack(fill="x", padx=20, pady=(0,10))
        
        self.year_vars = {}  # Will store year checkboxes
        
        # Compare button
        self.compare_btn = ctk.CTkButton(
            left_panel,
            text="📊 Compare Reports",
            command=self.compare_reports,
            height=40,
            state="disabled"
        )
        self.compare_btn.pack(fill="x", padx=20, pady=20)
        
        # Export buttons section
        export_frame = ctk.CTkFrame(left_panel)
        export_frame.pack(fill="x", padx=15, pady=10)
        
        export_label = ctk.CTkLabel(
            export_frame,
            text="📁 Export Options:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        export_label.pack(pady=(15,10))
        
        self.export_word_btn = ctk.CTkButton(
            export_frame,
            text="📄 Export to Word",
            command=self.export_word_report,
            height=40,
            state="disabled",
            font=ctk.CTkFont(size=12)
        )
        self.export_word_btn.pack(fill="x", padx=15, pady=5)
        
        self.export_excel_btn = ctk.CTkButton(
            export_frame,
            text="📊 Export to Excel",
            command=self.export_excel_report,
            height=40,
            state="disabled",
            font=ctk.CTkFont(size=12)
        )
        self.export_excel_btn.pack(fill="x", padx=15, pady=5)
        
        self.export_dashboard_btn = ctk.CTkButton(
            export_frame,
            text="📈 Open Dashboard",
            command=self.export_dashboard,
            height=40,
            state="disabled",
            font=ctk.CTkFont(size=12)
        )
        self.export_dashboard_btn.pack(fill="x", padx=15, pady=(5,15))
        
        # Add spacing at bottom to ensure visibility
        bottom_spacer = ctk.CTkFrame(left_panel, height=20, fg_color="transparent")
        bottom_spacer.pack(fill="x", pady=10)
        
    def setup_right_panel(self, parent):
        """Setup the right panel for comparison results"""
        # Create container for right panel
        right_container = ctk.CTkFrame(parent)
        right_container.grid(row=0, column=1, sticky="nsew")
        right_container.grid_rowconfigure(0, weight=1)
        right_container.grid_columnconfigure(0, weight=1)
        
        # Create scrollable frame for results
        self.right_panel = ctk.CTkScrollableFrame(right_container)
        self.right_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Initial message
        welcome_label = ctk.CTkLabel(
            self.right_panel,
            text="Select a company and years to compare reports",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        welcome_label.pack(expand=True, pady=50)
        
    def refresh_companies(self):
        """Refresh the companies list"""
        companies = self.report_comparison.get_all_companies()
        
        self.company_listbox.delete(0, tk.END)
        for company in companies:
            self.company_listbox.insert(tk.END, company)
            
        if not companies:
            self.company_listbox.insert(tk.END, "(No saved reports)")
    
    def on_company_select(self, event):
        """Handle company selection"""
        selection = self.company_listbox.curselection()
        if not selection:
            return
            
        company_name = self.company_listbox.get(selection[0])
        if company_name == "(No saved reports)":
            return
            
        # Get reports for this company
        reports = self.report_comparison.get_company_reports(company_name)
        
        # Clear existing year checkboxes
        for widget in self.year_frame.winfo_children():
            widget.destroy()
        self.year_vars.clear()
        
        # Create checkboxes for each year
        years = sorted(reports.keys(), reverse=True)  # Most recent first
        
        if years:
            for year in years:
                var = tk.BooleanVar()
                checkbox = ctk.CTkCheckBox(
                    self.year_frame,
                    text=f"{year} ({reports[year].get('metadata', {}).get('file_name', 'Unknown')})",
                    variable=var,
                    command=self.on_year_selection_change
                )
                checkbox.pack(anchor="w", pady=2, padx=10)
                self.year_vars[year] = var
        else:
            no_reports_label = ctk.CTkLabel(
                self.year_frame,
                text="No reports found for this company",
                text_color="gray"
            )
            no_reports_label.pack(pady=10)
    
    def on_year_selection_change(self):
        """Handle year selection changes"""
        selected_years = [year for year, var in self.year_vars.items() if var.get()]
        
        # Enable compare button if at least 2 years selected
        if len(selected_years) >= 2:
            self.compare_btn.configure(state="normal")
        else:
            self.compare_btn.configure(state="disabled")
    
    def compare_reports(self):
        """Compare selected reports"""
        selection = self.company_listbox.curselection()
        if not selection:
            return
            
        company_name = self.company_listbox.get(selection[0])
        selected_years = [year for year, var in self.year_vars.items() if var.get()]
        
        if len(selected_years) < 2:
            messagebox.showerror("Error", "Please select at least 2 years to compare.")
            return
        
        # Show progress
        self.show_comparison_progress()
        
        # Run comparison in thread
        thread = threading.Thread(
            target=self.run_comparison_thread,
            args=(company_name, selected_years)
        )
        thread.daemon = True
        thread.start()
    
    def show_comparison_progress(self):
        """Show comparison progress"""
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        progress_frame = ctk.CTkFrame(self.right_panel)
        progress_frame.pack(fill="x", padx=20, pady=50)
        
        progress_label = ctk.CTkLabel(
            progress_frame,
            text="🔄 Generating Comparison Analysis...",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        progress_label.pack(pady=(20,10))
        
        progress_bar = ctk.CTkProgressBar(progress_frame)
        progress_bar.pack(pady=10, padx=50, fill="x")
        progress_bar.set(0.5)  # Indeterminate progress
        
        status_label = ctk.CTkLabel(
            progress_frame,
            text="📊 Analyzing trends and generating AI insights...",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        )
        status_label.pack(pady=(0,20))
        
        # Add steps indicator
        steps_frame = ctk.CTkFrame(progress_frame)
        steps_frame.pack(fill="x", padx=30, pady=10)
        
        steps = [
            "✅ Loading stored reports",
            "🔄 Calculating performance trends", 
            "🤖 Generating AI comparative analysis",
            "📈 Preparing visualizations"
        ]
        
        for step in steps:
            step_label = ctk.CTkLabel(
                steps_frame,
                text=step,
                font=ctk.CTkFont(size=10),
                anchor="w"
            )
            step_label.pack(anchor="w", padx=20, pady=2)
    
    def run_comparison_thread(self, company_name: str, years: List[int]):
        """Run comparison analysis in background thread"""
        try:
            # Perform comparison
            comparison_result = self.report_comparison.compare_reports(company_name, years)
            self.current_comparison = comparison_result
            
            # Update UI on main thread
            self.window.after(0, lambda: self.show_comparison_results(comparison_result))
            
        except Exception as e:
            error_msg = f"Comparison failed: {str(e)}"
            self.window.after(0, lambda: self.show_comparison_error(error_msg))
    
    def show_comparison_results(self, comparison_result: Dict):
        """Show comparison results"""
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        # Title
        company_name = comparison_result.get('company_name', 'Company')
        years = comparison_result.get('years_compared', [])
        
        title_label = ctk.CTkLabel(
            self.right_panel,
            text=f"✅ Comparison Analysis Complete",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="green"
        )
        title_label.pack(pady=(20,5))
        
        company_label = ctk.CTkLabel(
            self.right_panel,
            text=f"{company_name} | {', '.join(map(str, years))}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        company_label.pack(pady=(0,10))
        
        # Export reminder
        export_reminder = ctk.CTkLabel(
            self.right_panel,
            text="📁 Use Export Options (left panel) to save results",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="blue"
        )
        export_reminder.pack(pady=(0,20))
        
        # Create results content frame
        results_frame = ctk.CTkFrame(self.right_panel)
        results_frame.pack(fill="x", padx=20, pady=10)
        
        # Summary metrics
        self.show_summary_metrics(results_frame, comparison_result)
        
        # AI Analysis
        self.show_ai_analysis(results_frame, comparison_result)
        
        # Trend Analysis
        self.show_trend_analysis(results_frame, comparison_result)
        
        # Enable export buttons
        self.export_word_btn.configure(state="normal")
        self.export_excel_btn.configure(state="normal")
        self.export_dashboard_btn.configure(state="normal")
        
        # Add bottom completion indicator
        completion_frame = ctk.CTkFrame(self.right_panel)
        completion_frame.pack(fill="x", padx=20, pady=20)
        
        completion_label = ctk.CTkLabel(
            completion_frame,
            text="🎉 Analysis Complete! Export options are now available.",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="green"
        )
        completion_label.pack(pady=15)
        
        options_label = ctk.CTkLabel(
            completion_frame,
            text="Choose from: 📄 Word Report | 📊 Excel Data | 📈 Interactive Dashboard",
            font=ctk.CTkFont(size=12),
            text_color="blue"
        )
        options_label.pack(pady=(0,15))
    
    def show_summary_metrics(self, parent, comparison_result: Dict):
        """Show summary metrics"""
        summary = comparison_result.get('summary', {})
        
        metrics_frame = ctk.CTkFrame(parent)
        metrics_frame.pack(fill="x", pady=10)
        
        metrics_title = ctk.CTkLabel(
            metrics_frame,
            text="Summary Metrics",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        metrics_title.pack(pady=10)
        
        # Metrics grid
        grid_frame = ctk.CTkFrame(metrics_frame)
        grid_frame.pack(fill="x", padx=20, pady=10)
        
        metrics = [
            ("Years Compared", summary.get('total_years_compared', 0)),
            ("Year Range", summary.get('year_range', 'N/A')),
            ("Improving ESG Categories", summary.get('esg_summary', {}).get('improving_categories', 0)),
            ("Declining ESG Categories", summary.get('esg_summary', {}).get('declining_categories', 0)),
            ("Improving SDGs", summary.get('sdg_summary', {}).get('improving_sdgs', 0)),
            ("Active SDGs", summary.get('sdg_summary', {}).get('total_active_sdgs', 0))
        ]
        
        for i, (label, value) in enumerate(metrics):
            row = i // 2
            col = i % 2
            
            metric_frame = ctk.CTkFrame(grid_frame)
            metric_frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            
            value_label = ctk.CTkLabel(
                metric_frame,
                text=str(value),
                font=ctk.CTkFont(size=20, weight="bold")
            )
            value_label.pack(pady=(10,0))
            
            label_label = ctk.CTkLabel(
                metric_frame,
                text=label,
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            label_label.pack(pady=(0,10))
        
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
    
    def show_ai_analysis(self, parent, comparison_result: Dict):
        """Show AI-generated analysis"""
        ai_analysis = comparison_result.get('ai_analysis', 'No AI analysis available')
        
        ai_frame = ctk.CTkFrame(parent)
        ai_frame.pack(fill="x", pady=10)
        
        ai_title = ctk.CTkLabel(
            ai_frame,
            text="🤖 AI Comparative Analysis",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        ai_title.pack(pady=(10,5))
        
        # Analysis quality indicator
        if len(ai_analysis) > 200:
            quality_label = ctk.CTkLabel(
                ai_frame,
                text="✅ Comprehensive Analysis Generated",
                font=ctk.CTkFont(size=10),
                text_color="green"
            )
            quality_label.pack(pady=(0,10))
        
        ai_text = ctk.CTkTextbox(
            ai_frame,
            height=300,
            wrap="word",
            font=ctk.CTkFont(size=11, family="Arial"),
            fg_color=("#F9F9F9", "#2B2B2B"),
            border_width=1
        )
        ai_text.pack(fill="x", padx=20, pady=(0,20))
        
        # Format the AI analysis with better structure
        formatted_analysis = self._format_ai_analysis(ai_analysis)
        ai_text.insert("1.0", formatted_analysis)
        ai_text.configure(state="disabled")
        
        # Add word count info
        word_count = len(formatted_analysis.split())
        word_info = ctk.CTkLabel(
            ai_frame,
            text=f"📊 Analysis contains {word_count} words | Generated by AI Engine",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        word_info.pack(anchor="e", padx=20, pady=(0,15))
    
    def show_trend_analysis(self, parent, comparison_result: Dict):
        """Show trend analysis"""
        trends = comparison_result.get('trends', {})
        
        trends_frame = ctk.CTkFrame(parent)
        trends_frame.pack(fill="x", pady=10)
        
        trends_title = ctk.CTkLabel(
            trends_frame,
            text="📊 Key Trends Identified",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        trends_title.pack(pady=10)
        
        # ESG trends
        esg_trends = trends.get('esg_trends', {})
        if esg_trends:
            esg_container = ctk.CTkFrame(trends_frame)
            esg_container.pack(fill="x", padx=20, pady=5)
            
            esg_label = ctk.CTkLabel(
                esg_container,
                text="🏢 ESG Performance Changes",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            esg_label.pack(anchor="w", padx=15, pady=(10,5))
            
            # Create a grid for better organization
            for i, (category, trend_data) in enumerate(esg_trends.items()):
                change = trend_data.get('change', 0)
                
                # Determine trend icon and color
                if change > 0.5:
                    trend_icon = "🟢"
                    trend_text = "Strong Improvement"
                    color = "green"
                elif change > 0:
                    trend_icon = "🟡"
                    trend_text = "Moderate Improvement"
                    color = "orange"
                elif change < -0.5:
                    trend_icon = "🔴"
                    trend_text = "Significant Decline"
                    color = "red"
                elif change < 0:
                    trend_icon = "🟠"
                    trend_text = "Moderate Decline"
                    color = "orange"
                else:
                    trend_icon = "⚪"
                    trend_text = "Stable"
                    color = "gray"
                
                trend_item = ctk.CTkFrame(esg_container)
                trend_item.pack(fill="x", padx=15, pady=2)
                
                # Category and change in one line
                trend_info = ctk.CTkLabel(
                    trend_item,
                    text=f"{trend_icon} {category.replace('_', ' ').title()}: {change:+.1f} ({trend_text})",
                    font=ctk.CTkFont(size=11),
                    text_color=color
                )
                trend_info.pack(anchor="w", padx=10, pady=5)
        
        # SDG trends summary
        sdg_trends = trends.get('sdg_trends', {})
        if sdg_trends:
            sdg_container = ctk.CTkFrame(trends_frame)
            sdg_container.pack(fill="x", padx=20, pady=5)
            
            sdg_label = ctk.CTkLabel(
                sdg_container,
                text="🌍 SDG Performance Highlights",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            sdg_label.pack(anchor="w", padx=15, pady=(10,5))
            
            # Show top improving and declining SDGs
            sdg_changes = [(sdg, data.get('change', 0)) for sdg, data in sdg_trends.items()]
            sdg_changes.sort(key=lambda x: x[1], reverse=True)
            
            # Top 3 improving
            if sdg_changes:
                improving = [item for item in sdg_changes if item[1] > 0][:3]
                declining = [item for item in sdg_changes if item[1] < 0][-2:]  # Bottom 2
                
                if improving:
                    improving_text = "🟢 Top Improving: " + ", ".join([f"{sdg} (+{change:.1f})" for sdg, change in improving])
                    improving_label = ctk.CTkLabel(
                        sdg_container,
                        text=improving_text,
                        font=ctk.CTkFont(size=10),
                        text_color="green"
                    )
                    improving_label.pack(anchor="w", padx=15, pady=2)
                
                if declining:
                    declining_text = "🔴 Areas of Concern: " + ", ".join([f"{sdg} ({change:.1f})" for sdg, change in declining])
                    declining_label = ctk.CTkLabel(
                        sdg_container,
                        text=declining_text,
                        font=ctk.CTkFont(size=10),
                        text_color="red"
                    )
                    declining_label.pack(anchor="w", padx=15, pady=(2,10))
    
    def show_comparison_error(self, error_msg: str):
        """Show comparison error"""
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        error_frame = ctk.CTkFrame(self.right_panel)
        error_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        error_label = ctk.CTkLabel(
            error_frame,
            text="Comparison Failed",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="red"
        )
        error_label.pack(expand=True)
        
        error_detail = ctk.CTkLabel(
            error_frame,
            text=error_msg,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        error_detail.pack()
    
    def export_word_report(self):
        """Export comparison analysis to Word document"""
        if not self.current_comparison:
            messagebox.showerror("Error", "No comparison results to export.")
            return
        
        try:
            # Check if python-docx is available
            try:
                from docx import Document
                # Test document creation
                test_doc = Document()
                test_doc = None  # Clean up
            except ImportError:
                messagebox.showerror(
                    "Missing Library", 
                    "Word export requires python-docx library.\n\n"
                    "Install with: pip install python-docx\n\n"
                    "Then restart the application."
                )
                return
            except Exception as e:
                messagebox.showerror(
                    "Library Error", 
                    f"python-docx library has issues:\n{str(e)}\n\n"
                    "Try reinstalling: pip install --upgrade python-docx"
                )
                return
            
            # Get save location with simpler approach
            company_name = self.current_comparison.get('company_name', 'Company')
            years = self.current_comparison.get('years_compared', [])
            year_range = f"{min(years)}-{max(years)}" if years else "Unknown"
            
            # Simple filename without special characters
            import re
            clean_company = re.sub(r'[^\w\s-]', '', company_name).strip().replace(' ', '_')
            clean_company = clean_company[:20]  # Limit length
            
            file_path = filedialog.asksaveasfilename(
                title="Save Word Report",
                defaultextension=".docx",
                filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
            )
            
            if file_path:
                # Ensure .docx extension
                if not file_path.lower().endswith('.docx'):
                    file_path += '.docx'
                
                # Export to Word
                output_path = self.comparison_exporter.export_word_report(
                    self.current_comparison, file_path
                )
                
                # Open the file
                if os.path.exists(output_path):
                    try:
                        os.startfile(output_path)  # Windows
                    except:
                        # Fallback - just show path
                        pass
                    
                messagebox.showinfo(
                    "Export Complete", 
                    f"Word report exported successfully!\n\n"
                    f"📄 Professional comparison report created\n"
                    f"📊 Includes trends, charts, and AI analysis\n\n"
                    f"Saved to: {output_path}"
                )
                
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Word export failed: {error_msg}")
            
            # More helpful error messages
            if "initialname" in error_msg.lower():
                messagebox.showerror(
                    "Export Error", 
                    "File dialog error. Please try again with a simpler filename."
                )
            elif "docx" in error_msg.lower():
                messagebox.showerror(
                    "Export Error", 
                    "Word document creation failed. Please ensure:\n"
                    "1. python-docx library is installed\n"
                    "2. You have write permissions to the selected folder\n"
                    "3. The file is not open in another program"
                )
            else:
                messagebox.showerror("Export Error", f"Failed to export Word report:\n{error_msg}")
    
    def export_excel_report(self):
        """Export comparison data to Excel spreadsheet"""
        if not self.current_comparison:
            messagebox.showerror("Error", "No comparison results to export.")
            return
        
        try:
            # Get save location
            company_name = self.current_comparison.get('company_name', 'Company').replace(' ', '_')
            years = self.current_comparison.get('years_compared', [])
            year_range = f"{min(years)}-{max(years)}" if years else "Unknown"
            
            # Clean filename - remove invalid characters
            import re
            clean_company = re.sub(r'[<>:"/\\|?*]', '_', company_name)
            default_name = f"Comparison_Data_{clean_company}_{year_range}.xlsx"
            
            file_path = filedialog.asksaveasfilename(
                title="Save Excel Report",
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
                initialname=default_name
            )
            
            if file_path:
                # Export to Excel
                output_path = self.comparison_exporter.export_excel_comparison(
                    self.current_comparison, file_path
                )
                
                # Open the file
                if os.path.exists(output_path):
                    os.startfile(output_path)  # Windows
                    
                messagebox.showinfo(
                    "Export Complete", 
                    f"Excel report exported successfully!\n\nSaved to: {output_path}"
                )
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export Excel report: {str(e)}")
    
    def export_dashboard(self):
        """Export and open interactive dashboard in browser"""
        if not self.current_comparison:
            messagebox.showerror("Error", "No comparison results to export.")
            return
        
        try:
            # Create and open enhanced dashboard
            dashboard_path = self.comparison_visualizer.create_and_open_dashboard(self.current_comparison)
            
            # Open dashboard in browser
            if os.path.exists(dashboard_path):
                webbrowser.open(f'file://{dashboard_path.replace(os.sep, "/")}')
                
                messagebox.showinfo(
                    "Dashboard Opened", 
                    f"Interactive dashboard opened in your browser!\n\n"
                    f"Features:\n"
                    f"📊 8 comprehensive charts\n"
                    f"📈 Interactive visualizations\n"
                    f"🤖 AI insights summary\n"
                    f"📋 Performance metrics\n\n"
                    f"Dashboard saved to: {dashboard_path}"
                )
            else:
                raise Exception("Dashboard file was not created successfully")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to create dashboard: {str(e)}")
            
            # Fallback to old method
            try:
                output_dir = self.comparison_visualizer.export_comparison_charts(self.current_comparison)
                if os.path.exists(output_dir):
                    os.startfile(output_dir)  # Windows
                    messagebox.showinfo("Fallback Export", f"Charts exported to: {output_dir}")
            except:
                pass
    
    def _format_ai_analysis(self, ai_analysis: str) -> str:
        """Format AI analysis text for better readability"""
        if not ai_analysis or ai_analysis == 'No AI analysis available':
            return ai_analysis
        
        import re
        
        # Clean markdown formatting first
        formatted = ai_analysis
        
        # Remove markdown bold formatting (**text**)
        formatted = re.sub(r'\*\*(.*?)\*\*', r'\1', formatted)
        
        # Remove markdown italic formatting (*text*)
        formatted = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'\1', formatted)
        
        # Clean up section headers
        formatted = re.sub(r'### ', '\n\n### ', formatted)
        formatted = re.sub(r'## ', '\n\n## ', formatted)
        formatted = re.sub(r'# ', '\n\n# ', formatted)
        
        # Add spacing after numbered points
        formatted = re.sub(r'(\d+\.)', r'\n\1', formatted)
        
        # Clean up bullet points
        formatted = re.sub(r'\n\s*([•*-])\s*', r'\n• ', formatted)
        
        # Remove excessive spacing
        formatted = re.sub(r'\n\s*\n\s*\n', '\n\n', formatted)
        formatted = re.sub(r'\s+', ' ', formatted)
        
        # Clean up colons with asterisks
        formatted = re.sub(r':\*\*', ':', formatted)
        
        # Fix line breaks
        formatted = formatted.replace('\n', '\n\n')
        while '\n\n\n\n' in formatted:
            formatted = formatted.replace('\n\n\n\n', '\n\n')
        
        return formatted.strip()

# Helper function to integrate with main GUI
def add_comparison_dialog_classes_to_main_gui():
    """Add the dialog classes to the main GUI module namespace"""
    import main_gui
    main_gui.SaveReportDialog = SaveReportDialog
    main_gui.ComparisonManagerWindow = ComparisonManagerWindow

if __name__ == "__main__":
    # Test the dialogs
    root = ctk.CTk()
    root.geometry("200x100")
    
    def test_save_dialog():
        dialog = SaveReportDialog(root)
        root.wait_window(dialog.dialog)
        if dialog.result:
            print(f"Result: {dialog.result}")
    
    test_btn = ctk.CTkButton(root, text="Test Save Dialog", command=test_save_dialog)
    test_btn.pack(pady=20)
    
    root.mainloop()