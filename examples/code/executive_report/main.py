# Executive Report Example - PagedJS with Modern Styling
#
# This example demonstrates:
# - Modern executive report template with PagedJS
# - Dynamic chart generation with matplotlib
# - KPI cards, data tables, and professional styling
# - Automatic table of contents with page numbers

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
REPORT_PATH = Path(__file__).parent.parent.parent / "reports" / "executive_report"


class ExecutiveReport:
    """Executive report generator with chart capabilities."""

    # Color palette matching CSS design
    COLORS = {
        'primary': '#1e3a5f',
        'primary_light': '#2d5a8b',
        'accent': '#0ea5e9',
        'success': '#10b981',
        'warning': '#f59e0b',
        'purple': '#8b5cf6',
        'text': '#1f2937',
        'text_secondary': '#6b7280',
        'bg_light': '#f8fafc',
        'grid': '#e5e7eb',
    }

    def generate_revenue_chart(self, data):
        """Generate a revenue performance chart with bars and line overlay."""
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(10, 5), dpi=100)

        quarters = data['quarters']
        revenue = data['revenue']
        target = data['target']
        x = np.arange(len(quarters))
        width = 0.6

        # Create gradient-like bars using stacked segments
        bars = ax.bar(x, revenue, width, color=self.COLORS['accent'],
                      edgecolor='white', linewidth=0.5, alpha=0.9, zorder=3)

        # Target line
        ax.plot(x, target, color=self.COLORS['primary'], linewidth=2.5,
                marker='o', markersize=8, markerfacecolor='white',
                markeredgecolor=self.COLORS['primary'], markeredgewidth=2,
                label='Target', zorder=4)

        # Add value labels on bars
        for bar, val in zip(bars, revenue):
            height = bar.get_height()
            ax.annotate(f'${val}M',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=11, fontweight='bold',
                        color=self.COLORS['primary'])

        # Styling
        ax.set_xlabel('Quarter', fontsize=11, color=self.COLORS['text_secondary'])
        ax.set_ylabel('Revenue ($ Millions)', fontsize=11, color=self.COLORS['text_secondary'])
        ax.set_xticks(x)
        ax.set_xticklabels(quarters, fontsize=10)
        ax.set_ylim(0, max(revenue) * 1.25)

        # Remove spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(self.COLORS['grid'])
        ax.spines['bottom'].set_color(self.COLORS['grid'])

        # Grid
        ax.yaxis.grid(True, linestyle='--', alpha=0.5, color=self.COLORS['grid'])
        ax.set_axisbelow(True)

        # Legend
        legend_elements = [
            mpatches.Patch(facecolor=self.COLORS['accent'], label='Actual Revenue'),
            plt.Line2D([0], [0], color=self.COLORS['primary'], linewidth=2,
                       marker='o', markersize=6, markerfacecolor='white',
                       markeredgecolor=self.COLORS['primary'], label='Target')
        ]
        ax.legend(handles=legend_elements, loc='upper left', frameon=True,
                  facecolor='white', edgecolor=self.COLORS['grid'])

        plt.tight_layout()

        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close()
        buf.seek(0)
        return buf.read()

    def generate_performance_chart(self, data):
        """Generate a radar/performance comparison chart."""
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

        categories = data['categories']
        current = data['current']
        target = data['target']
        previous = data['previous']

        x = np.arange(len(categories))
        width = 0.25

        # Create grouped bars
        bars1 = ax.bar(x - width, previous, width, label='Previous Quarter',
                       color=self.COLORS['grid'], edgecolor='white', zorder=3)
        bars2 = ax.bar(x, current, width, label='Current Quarter',
                       color=self.COLORS['accent'], edgecolor='white', zorder=3)
        bars3 = ax.bar(x + width, target, width, label='Target',
                       color=self.COLORS['success'], alpha=0.7, edgecolor='white', zorder=3)

        # Add value labels on current bars
        for bar, val in zip(bars2, current):
            height = bar.get_height()
            ax.annotate(f'{val}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=9, fontweight='bold',
                        color=self.COLORS['primary'])

        # Styling
        ax.set_xlabel('Department', fontsize=11, color=self.COLORS['text_secondary'])
        ax.set_ylabel('Performance Score (%)', fontsize=11, color=self.COLORS['text_secondary'])
        ax.set_xticks(x)
        ax.set_xticklabels(categories, fontsize=10)
        ax.set_ylim(0, 110)

        # Remove spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(self.COLORS['grid'])
        ax.spines['bottom'].set_color(self.COLORS['grid'])

        # Grid
        ax.yaxis.grid(True, linestyle='--', alpha=0.5, color=self.COLORS['grid'])
        ax.set_axisbelow(True)

        # Add a target line at 90%
        ax.axhline(y=90, color=self.COLORS['warning'], linestyle='--',
                   linewidth=1.5, alpha=0.7, label='Minimum Target')

        # Legend
        ax.legend(loc='upper right', frameon=True,
                  facecolor='white', edgecolor=self.COLORS['grid'])

        plt.tight_layout()

        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close()
        buf.seek(0)
        return buf.read()

    def render(self, report, output_path):
        """Render the executive report to PDF."""
        # Load data from JSON
        data_file = REPORT_PATH / "data.json"
        with open(data_file, "r") as f:
            report_data = json.load(f)

        # Add chart generation callbacks
        report_data["gen_revenue_chart"] = lambda args: self.generate_revenue_chart(args)
        report_data["gen_performance_chart"] = lambda args: self.generate_performance_chart(args)

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
            print(f"Error generating report: {result.error}")
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
    print("Building report template...")
    status, zfs = ReportFileBuilder.build_zipfs(REPORT_PATH)
    if not status.success():
        print(f"Error building report: {status.error()}")
        sys.exit(1)

    # Load ReportFile from in-memory zipfs
    report = ReportFileLoader.load_zipfs(zfs)

    # Generate the executive report
    print("Generating executive report...")
    generator = ExecutiveReport()
    if generator.render(report, output_file):
        print(f"Report generated: {output_file}")
    else:
        print("Failed to generate report")
        sys.exit(1)
