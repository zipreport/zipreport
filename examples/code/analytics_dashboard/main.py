# Analytics Dashboard Example - Single Page Layout
#
# This example demonstrates:
# - Single-page dashboard layout with PagedJS
# - Multiple chart types (line, pie, bar, horizontal bar)
# - KPI cards with trend indicators
# - Data tables with analytics metrics

import io
import json
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from zipreport import ZipReport
from zipreport.report import ReportFileBuilder, ReportFileLoader, ReportJob

ZIPREPORT_URL = os.getenv("ZIPREPORT_URL", "http://127.0.0.1:6543")
ZIPREPORT_KEY = os.getenv("ZIPREPORT_KEY", "somePassword")

# Path to the report template
REPORT_PATH = Path(__file__).parent.parent.parent / "reports" / "analytics_dashboard"


class AnalyticsDashboard:
    """Analytics dashboard generator with multiple chart types."""

    # Color palette matching CSS
    COLORS = {
        'primary': '#3b82f6',
        'secondary': '#8b5cf6',
        'success': '#10b981',
        'warning': '#f59e0b',
        'danger': '#ef4444',
        'info': '#06b6d4',
        'dark': '#111827',
        'text': '#374151',
        'text_light': '#6b7280',
        'bg': '#f3f4f6',
        'border': '#e5e7eb',
    }

    def generate_traffic_chart(self, data):
        """Generate a dual-axis line chart for traffic overview."""
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax1 = plt.subplots(figsize=(7.5, 2.2), dpi=100)

        days = data['days']
        sessions = data['sessions']
        pageviews = data['pageviews']
        x = np.arange(len(days))

        # Sessions line
        ax1.fill_between(x, sessions, alpha=0.3, color=self.COLORS['primary'])
        line1 = ax1.plot(x, sessions, color=self.COLORS['primary'], linewidth=2,
                         marker='o', markersize=4, label='Sessions')
        ax1.set_ylabel('Sessions', color=self.COLORS['primary'], fontsize=9)
        ax1.tick_params(axis='y', labelcolor=self.COLORS['primary'])

        # Pageviews on secondary axis
        ax2 = ax1.twinx()
        line2 = ax2.plot(x, pageviews, color=self.COLORS['secondary'], linewidth=2,
                         marker='s', markersize=4, linestyle='--', label='Pageviews')
        ax2.set_ylabel('Pageviews', color=self.COLORS['secondary'], fontsize=9)
        ax2.tick_params(axis='y', labelcolor=self.COLORS['secondary'])

        # X-axis
        ax1.set_xticks(x)
        ax1.set_xticklabels(days, fontsize=8)

        # Styling
        ax1.spines['top'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax1.spines['bottom'].set_color(self.COLORS['border'])

        # Legend
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left', fontsize=8,
                   frameon=True, facecolor='white')

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close()
        buf.seek(0)
        return buf.read()

    def generate_device_chart(self, data):
        """Generate a donut chart for device breakdown."""
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(2.8, 2.0), dpi=100)

        values = data['values']
        colors = data['colors']

        # Create donut chart
        wedges, texts, autotexts = ax.pie(
            values,
            colors=colors,
            autopct='%1.0f%%',
            startangle=90,
            wedgeprops={'width': 0.6, 'edgecolor': 'white', 'linewidth': 2},
            pctdistance=0.75,
            textprops={'fontsize': 9, 'fontweight': 'bold', 'color': 'white'}
        )

        # Center circle for donut effect
        centre_circle = plt.Circle((0, 0), 0.35, fc='white')
        ax.add_patch(centre_circle)

        ax.axis('equal')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close()
        buf.seek(0)
        return buf.read()

    def generate_hourly_chart(self, data):
        """Generate a bar chart for hourly traffic distribution."""
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(3.5, 1.7), dpi=100)

        hours = data['hours']
        traffic = data['traffic']
        x = np.arange(len(hours))

        # Find peak hour for highlighting
        peak_idx = np.argmax(traffic)
        colors = [self.COLORS['primary'] if i != peak_idx else self.COLORS['danger']
                  for i in range(len(traffic))]

        bars = ax.bar(x, traffic, color=colors, edgecolor='white',
                      width=0.7, zorder=3)

        # Styling
        ax.set_xticks(x)
        ax.set_xticklabels(hours, fontsize=7)
        ax.set_xlabel('Hour', fontsize=8, color=self.COLORS['text_light'])
        ax.set_ylabel('Sessions', fontsize=8, color=self.COLORS['text_light'])

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(self.COLORS['border'])
        ax.spines['bottom'].set_color(self.COLORS['border'])

        ax.yaxis.grid(True, linestyle='--', alpha=0.5, color=self.COLORS['border'])
        ax.set_axisbelow(True)

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close()
        buf.seek(0)
        return buf.read()

    def generate_sources_chart(self, data):
        """Generate a horizontal bar chart for traffic sources."""
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(3.5, 1.7), dpi=100)

        sources = data['sources']
        values = data['values']
        colors = data['colors']

        y_pos = np.arange(len(sources))

        bars = ax.barh(y_pos, values, color=colors, edgecolor='white',
                       height=0.6, zorder=3)

        # Add value labels
        for bar, val in zip(bars, values):
            width = bar.get_width()
            ax.annotate(f'{val}%',
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(3, 0),
                        textcoords="offset points",
                        ha='left', va='center',
                        fontsize=8, fontweight='bold',
                        color=self.COLORS['dark'])

        # Styling
        ax.set_yticks(y_pos)
        ax.set_yticklabels(sources, fontsize=8)
        ax.set_xlim(0, max(values) * 1.3)
        ax.set_xlabel('% of Traffic', fontsize=8, color=self.COLORS['text_light'])

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color(self.COLORS['border'])

        ax.xaxis.grid(True, linestyle='--', alpha=0.5, color=self.COLORS['border'])
        ax.set_axisbelow(True)
        ax.tick_params(axis='y', length=0)

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close()
        buf.seek(0)
        return buf.read()

    def render(self, report, output_path):
        """Render the analytics dashboard to PDF."""
        # Load data from JSON
        data_file = REPORT_PATH / "data.json"
        with open(data_file, "r") as f:
            report_data = json.load(f)

        # Add chart generation callbacks
        report_data["gen_traffic_chart"] = lambda args: self.generate_traffic_chart(args)
        report_data["gen_device_chart"] = lambda args: self.generate_device_chart(args)
        report_data["gen_hourly_chart"] = lambda args: self.generate_hourly_chart(args)
        report_data["gen_sources_chart"] = lambda args: self.generate_sources_chart(args)

        # Create rendering job with JS event support for PagedJS
        job = ReportJob(report)
        job.use_jsevent(True)

        # Render using zipreport-server
        result = ZipReport(ZIPREPORT_URL, ZIPREPORT_KEY).render(job, report_data)

        if result.success:
            with open(output_path, "wb") as f:
                f.write(result.report.read())
            return True
        else:
            print(f"Error generating dashboard: {result.error}")
            return False


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python main.py <output_file.pdf>")
        sys.exit(1)

    output_file = Path(args[0])

    if output_file.exists():
        print(f"{output_file} already exists")
        sys.exit(1)

    if not REPORT_PATH.exists():
        print(f"Report template not found at: {REPORT_PATH}")
        sys.exit(1)

    # Build report from template directory
    print("Building dashboard template...")
    status, zfs = ReportFileBuilder.build_zipfs(REPORT_PATH)
    if not status.success():
        print(f"Error building report: {status.error()}")
        sys.exit(1)

    # Load ReportFile from in-memory zipfs
    report = ReportFileLoader.load_zipfs(zfs)

    # Generate the analytics dashboard
    print("Generating analytics dashboard...")
    generator = AnalyticsDashboard()
    if generator.render(report, output_file):
        print(f"Dashboard generated: {output_file}")
    else:
        print("Failed to generate dashboard")
        sys.exit(1)
