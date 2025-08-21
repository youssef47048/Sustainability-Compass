#!/usr/bin/env python3
"""
Comparison Visualizer Module
Creates charts and visualizations for multi-year sustainability report comparisons
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import seaborn as sns
from datetime import datetime
from config import SDG_GOALS, ESG_CATEGORIES, COLORS

class ComparisonVisualizer:
    """
    Create comparison visualizations for multi-year sustainability reports
    """
    
    def __init__(self):
        # Set style for matplotlib
        plt.style.use('seaborn-v0_8' if 'seaborn' in plt.style.available else 'default')
        if hasattr(sns, 'set_palette'):
            sns.set_palette("husl")
        
        # Color schemes for different chart types
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e', 
            'success': '#2ca02c',
            'warning': '#d62728',
            'improvement': '#2ca02c',
            'decline': '#d62728',
            'neutral': '#7f7f7f'
        }
    
    def create_comparison_dashboard(self, comparison_data: Dict) -> str:
        """
        Create comprehensive comparison dashboard
        
        Args:
            comparison_data (Dict): Complete comparison analysis data
            
        Returns:
            str: HTML dashboard content
        """
        company_name = comparison_data.get('company_name', 'Company')
        years = comparison_data.get('years_compared', [])
        
        # Create main dashboard figure
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=[
                'ESG Performance Trends',
                'SDG Performance Heatmap',
                'Year-over-Year ESG Changes',
                'Top Performing SDGs by Year',
                'Performance Trend Analysis',
                'Executive Summary Word Cloud'
            ],
            specs=[
                [{"type": "scatter"}, {"type": "heatmap"}],
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "scatter"}]
            ],
            vertical_spacing=0.08,
            horizontal_spacing=0.1
        )
        
        # 1. ESG Performance Trends
        self._add_esg_trend_chart(fig, comparison_data, row=1, col=1)
        
        # 2. SDG Performance Heatmap
        self._add_sdg_heatmap(fig, comparison_data, row=1, col=2)
        
        # 3. Year-over-Year ESG Changes
        self._add_esg_change_chart(fig, comparison_data, row=2, col=1)
        
        # 4. Top Performing SDGs
        self._add_top_sdgs_chart(fig, comparison_data, row=2, col=2)
        
        # 5. Overall Performance Trends
        self._add_overall_trends(fig, comparison_data, row=3, col=1)
        
        # 6. Summary metrics
        self._add_summary_metrics(fig, comparison_data, row=3, col=2)
        
        # Update layout
        fig.update_layout(
            title=f"Sustainability Report Comparison - {company_name}<br>Years: {', '.join(map(str, years))}",
            height=1200,
            showlegend=True,
            template="plotly_white"
        )
        
        return fig.to_html(include_plotlyjs='cdn')
    
    def create_esg_trend_chart(self, comparison_data: Dict) -> go.Figure:
        """Create detailed ESG trend chart"""
        esg_data = comparison_data['comparison_data']['esg_scores']
        years = sorted(esg_data.keys())
        
        fig = go.Figure()
        
        # Add trend line for each ESG category
        for category in ESG_CATEGORIES:
            scores = [esg_data.get(year, {}).get(category, 0) for year in years]
            
            fig.add_trace(go.Scatter(
                x=years,
                y=scores,
                mode='lines+markers',
                name=category.replace('_', ' ').title(),
                line=dict(width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title="ESG Performance Trends Over Time",
            xaxis_title="Year",
            yaxis_title="ESG Score",
            yaxis=dict(range=[0, 10]),
            template="plotly_white",
            height=500
        )
        
        return fig
    
    def create_sdg_comparison_chart(self, comparison_data: Dict) -> go.Figure:
        """Create SDG comparison radar chart"""
        sdg_data = comparison_data['comparison_data']['sdg_scores']
        years = sorted(sdg_data.keys())
        
        # Get all SDGs that appear in any year
        all_sdgs = set()
        for year_data in sdg_data.values():
            all_sdgs.update(year_data.keys())
        all_sdgs = sorted(list(all_sdgs))
        
        fig = go.Figure()
        
        # Create radar chart for each year
        colors = px.colors.qualitative.Set1[:len(years)]
        
        for i, year in enumerate(years):
            year_scores = [sdg_data.get(year, {}).get(sdg, 0) for sdg in all_sdgs]
            
            fig.add_trace(go.Scatterpolar(
                r=year_scores,
                theta=all_sdgs,
                fill='toself',
                name=str(year),
                line_color=colors[i],
                fillcolor=colors[i],
                opacity=0.6
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            title="SDG Performance Comparison",
            showlegend=True,
            template="plotly_white",
            height=600
        )
        
        return fig
    
    def create_improvement_analysis_chart(self, comparison_data: Dict) -> go.Figure:
        """Create improvement analysis chart"""
        trends = comparison_data.get('trends', {})
        esg_trends = trends.get('esg_trends', {})
        
        categories = list(esg_trends.keys())
        changes = [esg_trends[cat]['change'] for cat in categories]
        
        # Assign colors based on improvement/decline
        colors = ['green' if change > 0 else 'red' for change in changes]
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=changes,
                marker_color=colors,
                text=[f"{change:+.1f}" for change in changes],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="ESG Performance Changes",
            xaxis_title="ESG Category",
            yaxis_title="Score Change",
            template="plotly_white",
            height=400
        )
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="black")
        
        return fig
    
    def create_metrics_summary_table(self, comparison_data: Dict) -> go.Figure:
        """Create summary metrics table"""
        summary = comparison_data.get('summary', {})
        
        headers = ['Metric', 'Value']
        
        rows = [
            ['Years Compared', summary.get('total_years_compared', 0)],
            ['Year Range', summary.get('year_range', 'N/A')],
            ['Improving ESG Categories', summary.get('esg_summary', {}).get('improving_categories', 0)],
            ['Declining ESG Categories', summary.get('esg_summary', {}).get('declining_categories', 0)],
            ['Improving SDGs', summary.get('sdg_summary', {}).get('improving_sdgs', 0)],
            ['Declining SDGs', summary.get('sdg_summary', {}).get('declining_sdgs', 0)],
            ['Total Active SDGs', summary.get('sdg_summary', {}).get('total_active_sdgs', 0)]
        ]
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=headers,
                fill_color='lightblue',
                font=dict(size=14, color='black'),
                align='left'
            ),
            cells=dict(
                values=[[row[0] for row in rows], [row[1] for row in rows]],
                fill_color='white',
                font=dict(size=12),
                align='left'
            )
        )])
        
        fig.update_layout(
            title="Comparison Summary Metrics",
            height=300
        )
        
        return fig
    
    def _add_esg_trend_chart(self, fig: go.Figure, comparison_data: Dict, row: int, col: int):
        """Add ESG trend chart to subplot"""
        esg_data = comparison_data['comparison_data']['esg_scores']
        years = sorted(esg_data.keys())
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green
        
        for i, category in enumerate(ESG_CATEGORIES):
            scores = [esg_data.get(year, {}).get(category, 0) for year in years]
            
            fig.add_trace(go.Scatter(
                x=years,
                y=scores,
                mode='lines+markers',
                name=category.replace('_', ' ').title(),
                line=dict(color=colors[i], width=2),
                marker=dict(size=6)
            ), row=row, col=col)
    
    def _add_sdg_heatmap(self, fig: go.Figure, comparison_data: Dict, row: int, col: int):
        """Add SDG heatmap to subplot"""
        sdg_data = comparison_data['comparison_data']['sdg_scores']
        years = sorted(sdg_data.keys())
        
        # Get all SDGs
        all_sdgs = set()
        for year_data in sdg_data.values():
            all_sdgs.update(year_data.keys())
        all_sdgs = sorted(list(all_sdgs))[:10]  # Limit to top 10 for readability
        
        # Create matrix
        z = []
        for sdg in all_sdgs:
            row_data = [sdg_data.get(year, {}).get(sdg, 0) for year in years]
            z.append(row_data)
        
        fig.add_trace(go.Heatmap(
            z=z,
            x=years,
            y=all_sdgs,
            colorscale='Viridis',
            showscale=True
        ), row=row, col=col)
    
    def _add_esg_change_chart(self, fig: go.Figure, comparison_data: Dict, row: int, col: int):
        """Add ESG change bar chart to subplot"""
        trends = comparison_data.get('trends', {})
        esg_trends = trends.get('esg_trends', {})
        
        categories = list(esg_trends.keys())
        changes = [esg_trends[cat]['change'] for cat in categories]
        colors = ['green' if change > 0 else 'red' for change in changes]
        
        fig.add_trace(go.Bar(
            x=categories,
            y=changes,
            marker_color=colors,
            name="ESG Changes",
            showlegend=False
        ), row=row, col=col)
    
    def _add_top_sdgs_chart(self, fig: go.Figure, comparison_data: Dict, row: int, col: int):
        """Add top SDGs chart to subplot"""
        sdg_data = comparison_data['comparison_data']['sdg_scores']
        latest_year = max(sdg_data.keys()) if sdg_data else None
        
        if latest_year:
            latest_sdgs = sdg_data[latest_year]
            sorted_sdgs = sorted(latest_sdgs.items(), key=lambda x: x[1], reverse=True)[:5]
            
            sdgs, scores = zip(*sorted_sdgs) if sorted_sdgs else ([], [])
            
            fig.add_trace(go.Bar(
                x=list(sdgs),
                y=list(scores),
                marker_color='lightblue',
                name="Top SDGs",
                showlegend=False
            ), row=row, col=col)
    
    def _add_overall_trends(self, fig: go.Figure, comparison_data: Dict, row: int, col: int):
        """Add overall trend analysis"""
        esg_data = comparison_data['comparison_data']['esg_scores']
        years = sorted(esg_data.keys())
        
        # Calculate average ESG scores per year
        avg_scores = []
        for year in years:
            year_scores = list(esg_data.get(year, {}).values())
            avg_score = sum(year_scores) / len(year_scores) if year_scores else 0
            avg_scores.append(avg_score)
        
        fig.add_trace(go.Scatter(
            x=years,
            y=avg_scores,
            mode='lines+markers',
            name="Overall ESG Trend",
            line=dict(color='purple', width=3),
            marker=dict(size=8)
        ), row=row, col=col)
    
    def _add_summary_metrics(self, fig: go.Figure, comparison_data: Dict, row: int, col: int):
        """Add summary metrics visualization"""
        summary = comparison_data.get('summary', {})
        
        improving = summary.get('esg_summary', {}).get('improving_categories', 0)
        declining = summary.get('esg_summary', {}).get('declining_categories', 0)
        
        fig.add_trace(go.Bar(
            x=['Improving', 'Declining'],
            y=[improving, declining],
            marker_color=['green', 'red'],
            name="ESG Categories",
            showlegend=False
        ), row=row, col=col)
    
    def export_comparison_charts(self, comparison_data: Dict, output_dir: str = "comparison_charts"):
        """Export all comparison charts as individual files"""
        import os
        
        os.makedirs(output_dir, exist_ok=True)
        company_name = comparison_data.get('company_name', 'Company')
        
        # Create and save individual charts
        charts = {
            'esg_trends': self.create_esg_trend_chart(comparison_data),
            'sdg_comparison': self.create_sdg_comparison_chart(comparison_data),
            'improvement_analysis': self.create_improvement_analysis_chart(comparison_data),
            'summary_table': self.create_metrics_summary_table(comparison_data)
        }
        
        for chart_name, chart_fig in charts.items():
            filename = f"{company_name}_{chart_name}.html"
            filepath = os.path.join(output_dir, filename)
            chart_fig.write_html(filepath)
        
        # Create comprehensive dashboard
        dashboard_html = self.create_comparison_dashboard(comparison_data)
        dashboard_path = os.path.join(output_dir, f"{company_name}_comprehensive_comparison.html")
        
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        return output_dir
    
    def create_and_open_dashboard(self, comparison_data: Dict) -> str:
        """Create comprehensive dashboard and return path for opening in browser"""
        import os
        import tempfile
        
        # Create dashboard HTML
        dashboard_html = self.create_enhanced_dashboard(comparison_data)
        
        # Save to temporary file that opens in browser
        company_name = comparison_data.get('company_name', 'Company').replace(' ', '_')
        years = comparison_data.get('years_compared', [])
        year_range = f"{min(years)}-{max(years)}" if years else "Unknown"
        
        # Use temp directory but with meaningful name
        temp_dir = tempfile.gettempdir()
        dashboard_filename = f"SustainabilityComparison_{company_name}_{year_range}.html"
        dashboard_path = os.path.join(temp_dir, dashboard_filename)
        
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        return dashboard_path
    
    def create_enhanced_dashboard(self, comparison_data: Dict) -> str:
        """Create an enhanced dashboard with better layout and styling"""
        company_name = comparison_data.get('company_name', 'Company')
        years = comparison_data.get('years_compared', [])
        year_range = f"{min(years)}-{max(years)}" if years else "Unknown"
        
        # Create main dashboard with better layout
        fig = make_subplots(
            rows=4, cols=2,
            subplot_titles=[
                'ESG Performance Trends Over Time',
                'SDG Performance Heatmap',
                'Year-over-Year ESG Changes',
                'Top Performing SDGs',
                'Overall Performance Trend',
                'Summary Metrics',
                'ESG Category Comparison',
                'SDG Impact Distribution'
            ],
            specs=[
                [{"type": "scatter"}, {"type": "heatmap"}],
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "pie"}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Add all charts
        self._add_esg_trend_chart(fig, comparison_data, row=1, col=1)
        self._add_sdg_heatmap(fig, comparison_data, row=1, col=2)
        self._add_esg_change_chart(fig, comparison_data, row=2, col=1)
        self._add_top_sdgs_chart(fig, comparison_data, row=2, col=2)
        self._add_overall_trends(fig, comparison_data, row=3, col=1)
        self._add_summary_metrics(fig, comparison_data, row=3, col=2)
        self._add_esg_category_comparison(fig, comparison_data, row=4, col=1)
        self._add_sdg_distribution_pie(fig, comparison_data, row=4, col=2)
        
        # Enhanced layout with professional styling
        fig.update_layout(
            title={
                'text': f"<b>🌱 Sustainability Performance Comparison Dashboard</b><br><sub>{company_name} | {year_range} | Generated: {datetime.now().strftime('%B %d, %Y')}</sub>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2E8B57'}
            },
            height=1400,
            showlegend=True,
            template="plotly_white",
            font=dict(family="Arial, sans-serif", size=11),
            paper_bgcolor='#fafafa',
            plot_bgcolor='white'
        )
        
        # Add professional CSS styling and make it interactive
        dashboard_html = self._create_enhanced_html_wrapper(fig, comparison_data)
        
        return dashboard_html
    
    def _create_enhanced_html_wrapper(self, fig: go.Figure, comparison_data: Dict) -> str:
        """Create enhanced HTML wrapper with styling and additional info"""
        company_name = comparison_data.get('company_name', 'Company')
        years = comparison_data.get('years_compared', [])
        summary = comparison_data.get('summary', {})
        ai_analysis = comparison_data.get('ai_analysis', '')
        
        # Clean markdown formatting from AI analysis for dashboard display
        if ai_analysis:
            import re
            # Remove markdown bold and italic formatting
            ai_analysis = re.sub(r'\*\*(.*?)\*\*', r'\1', ai_analysis)
            ai_analysis = re.sub(r'\*(.*?)\*', r'\1', ai_analysis)
            
            # Remove markdown headers
            ai_analysis = re.sub(r'###\s*(.*?)(?=\n|$)', r'\1', ai_analysis)
            ai_analysis = re.sub(r'##\s*(.*?)(?=\n|$)', r'\1', ai_analysis)  
            ai_analysis = re.sub(r'#\s*(.*?)(?=\n|$)', r'\1', ai_analysis)
            
            # Remove numbered section artifacts
            ai_analysis = re.sub(r'##\s*\d+\.', '', ai_analysis)
            ai_analysis = re.sub(r'###\s*\d+\.', '', ai_analysis)
            ai_analysis = re.sub(r'#\s*\d+\.', '', ai_analysis)
            
            # Remove any remaining markdown artifacts
            ai_analysis = re.sub(r'[#*_`]', '', ai_analysis)
            
            # Clean up extra whitespace
            ai_analysis = re.sub(r'\n\s*\n\s*\n', '\n\n', ai_analysis)
            ai_analysis = ai_analysis.strip()
        
        # Get the plotly HTML
        plotly_html = fig.to_html(include_plotlyjs='cdn', div_id="dashboard")
        
        # Extract just the body content
        import re
        body_match = re.search(r'<body[^>]*>(.*?)</body>', plotly_html, re.DOTALL)
        if body_match:
            plotly_content = body_match.group(1)
        else:
            plotly_content = plotly_html
        
        # Create enhanced HTML with additional sections
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sustainability Comparison Dashboard - {company_name}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
            margin-top: 10px;
        }}
        .summary-cards {{
            display: flex;
            justify-content: space-around;
            padding: 30px;
            background: #f8f9fa;
            flex-wrap: wrap;
        }}
        .card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            margin: 10px;
            min-width: 150px;
        }}
        .card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .card .label {{
            color: #666;
            margin-top: 5px;
        }}
        .dashboard-section {{
            padding: 30px;
        }}
        .insights-section {{
            background: #f8f9fa;
            padding: 30px;
            margin: 20px 0;
            border-left: 5px solid #667eea;
        }}
        .insights-section h3 {{
            color: #667eea;
            margin-top: 0;
        }}
        .insights-text {{
            line-height: 1.6;
            color: #555;
        }}
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 0.9em;
        }}
        .plotly-graph-div {{
            width: 100% !important;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌱 Sustainability Performance Dashboard</h1>
            <div class="subtitle">{company_name} | {min(years) if years else 'N/A'}-{max(years) if years else 'N/A'}</div>
            <div class="subtitle">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>
        
        <div class="summary-cards">
            <div class="card">
                <div class="number">{len(years)}</div>
                <div class="label">Years Analyzed</div>
            </div>
            <div class="card">
                <div class="number">{summary.get('esg_summary', {}).get('improving_categories', 0)}</div>
                <div class="label">ESG Categories Improving</div>
            </div>
            <div class="card">
                <div class="number">{summary.get('sdg_summary', {}).get('improving_sdgs', 0)}</div>
                <div class="label">SDGs Improving</div>
            </div>
            <div class="card">
                <div class="number">{summary.get('sdg_summary', {}).get('total_active_sdgs', 0)}</div>
                <div class="label">Total Active SDGs</div>
            </div>
        </div>
        
        <div class="dashboard-section">
            {plotly_content}
        </div>
        
        {f'''
        <div class="insights-section">
            <h3>🤖 AI-Generated Insights</h3>
            <div class="insights-text">
                {(ai_analysis[:500] + '...' if len(ai_analysis) > 500 else ai_analysis).replace('\n', '<br>')}
            </div>
        </div>
        ''' if ai_analysis and len(ai_analysis) > 50 else ''}
        
        <div class="footer">
            <p>📊 Powered by Sustainability Compass Pro | 🤖 AI Analysis by Gemini | 📈 Interactive Charts by Plotly</p>
            <p>This dashboard provides comprehensive multi-year sustainability performance analysis with trend identification and strategic insights.</p>
        </div>
    </div>
    
    <script>
        // Add some interactivity
        window.addEventListener('load', function() {{
            console.log('Sustainability Comparison Dashboard Loaded');
            
            // Add click handlers for better user experience
            document.querySelectorAll('.card').forEach(card => {{
                card.style.cursor = 'pointer';
                card.addEventListener('click', function() {{
                    this.style.transform = 'scale(1.05)';
                    setTimeout(() => {{
                        this.style.transform = 'scale(1)';
                    }}, 200);
                }});
            }});
        }});
    </script>
</body>
</html>
"""
        
        return html_template
    
    def _add_esg_category_comparison(self, fig: go.Figure, comparison_data: Dict, row: int, col: int):
        """Add ESG category comparison chart"""
        esg_data = comparison_data.get('comparison_data', {}).get('esg_scores', {})
        years = sorted(esg_data.keys())
        
        if not years:
            return
        
        # Calculate average scores per category
        from config import ESG_CATEGORIES
        categories = []
        avg_scores = []
        
        for category in ESG_CATEGORIES:
            scores = [esg_data.get(year, {}).get(category, 0) for year in years]
            if any(score > 0 for score in scores):
                categories.append(category.replace('_', ' ').title())
                avg_scores.append(sum(scores) / len(scores))
        
        if categories:
            colors = ['#2E8B57', '#4682B4', '#DAA520'][:len(categories)]
            
            fig.add_trace(go.Bar(
                x=categories,
                y=avg_scores,
                marker_color=colors,
                name="Average ESG Scores",
                showlegend=False,
                text=[f"{score:.1f}" for score in avg_scores],
                textposition='outside'
            ), row=row, col=col)
    
    def _add_sdg_distribution_pie(self, fig: go.Figure, comparison_data: Dict, row: int, col: int):
        """Add SDG score distribution pie chart"""
        sdg_data = comparison_data.get('comparison_data', {}).get('sdg_scores', {})
        years = sorted(sdg_data.keys())
        
        if not years:
            return
        
        # Get latest year SDG scores
        latest_year = max(years)
        latest_sdgs = sdg_data.get(latest_year, {})
        
        if latest_sdgs:
            # Group SDGs by performance level
            high_perf = [sdg for sdg, score in latest_sdgs.items() if score >= 7]
            med_perf = [sdg for sdg, score in latest_sdgs.items() if 4 <= score < 7]
            low_perf = [sdg for sdg, score in latest_sdgs.items() if score < 4]
            
            labels = ['High Performance (7+)', 'Medium Performance (4-7)', 'Low Performance (<4)']
            values = [len(high_perf), len(med_perf), len(low_perf)]
            colors = ['#2E8B57', '#DAA520', '#DC143C']
            
            fig.add_trace(go.Pie(
                labels=labels,
                values=values,
                marker_colors=colors,
                name="SDG Distribution",
                showlegend=True,
                textinfo='label+percent',
                hole=0.3
            ), row=row, col=col)

# Example usage
if __name__ == "__main__":
    # Test with sample data
    sample_comparison_data = {
        'company_name': 'Test Company',
        'years_compared': [2022, 2023],
        'comparison_data': {
            'esg_scores': {
                2022: {'economic_financial_performance': 7.5, 'environmental_performance': 6.8, 'social_performance': 8.1},
                2023: {'economic_financial_performance': 7.8, 'environmental_performance': 7.5, 'social_performance': 8.3}
            },
            'sdg_scores': {
                2022: {'SDG7': 7.2, 'SDG8': 8.0, 'SDG13': 6.5},
                2023: {'SDG7': 7.8, 'SDG8': 8.2, 'SDG13': 7.1}
            }
        },
        'trends': {
            'esg_trends': {
                'economic_financial_performance': {'change': 0.3},
                'environmental_performance': {'change': 0.7},
                'social_performance': {'change': 0.2}
            }
        },
        'summary': {
            'total_years_compared': 2,
            'year_range': '2022-2023',
            'esg_summary': {'improving_categories': 3, 'declining_categories': 0},
            'sdg_summary': {'improving_sdgs': 3, 'declining_sdgs': 0, 'total_active_sdgs': 3}
        }
    }
    
    visualizer = ComparisonVisualizer()
    dashboard = visualizer.create_comparison_dashboard(sample_comparison_data)
    print("✅ Comparison visualizer test completed!")