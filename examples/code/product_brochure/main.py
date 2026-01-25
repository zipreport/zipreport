# Product Brochure Example - PagedJS with Modern Marketing Design
#
# This example demonstrates:
# - Software product brochure template with PagedJS
# - Vibrant, marketing-focused design
# - Feature comparison charts
# - Pricing tiers and testimonials

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
REPORT_PATH = Path(__file__).parent.parent.parent / "reports" / "product_brochure"


class ProductBrochure:
    """Product brochure generator with marketing charts."""

    # Vibrant color palette matching CSS
    COLORS = {
        'primary': '#6366f1',
        'primary_dark': '#4f46e5',
        'secondary': '#06b6d4',
        'accent': '#f43f5e',
        'success': '#10b981',
        'warning': '#f59e0b',
        'dark': '#0f172a',
        'text': '#334155',
        'text_light': '#64748b',
        'bg_light': '#f8fafc',
        'grid': '#e2e8f0',
    }

    def generate_comparison_chart(self, data):
        """Generate a competitive comparison bar chart."""
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(10, 5.5), dpi=100)

        categories = data['categories']
        cloudflow = data['cloudflow']
        competitor_a = data['competitor_a']
        competitor_b = data['competitor_b']

        x = np.arange(len(categories))
        width = 0.25

        # Create grouped bars
        bars1 = ax.bar(x - width, cloudflow, width, label='CloudFlow',
                       color=self.COLORS['primary'], edgecolor='white', zorder=3)
        bars2 = ax.bar(x, competitor_a, width, label='Competitor A',
                       color=self.COLORS['text_light'], alpha=0.7, edgecolor='white', zorder=3)
        bars3 = ax.bar(x + width, competitor_b, width, label='Competitor B',
                       color=self.COLORS['grid'], edgecolor='white', zorder=3)

        # Add value labels on CloudFlow bars
        for bar, val in zip(bars1, cloudflow):
            height = bar.get_height()
            ax.annotate(f'{val}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=10, fontweight='bold',
                        color=self.COLORS['primary_dark'])

        # Styling
        ax.set_ylabel('Score (%)', fontsize=11, color=self.COLORS['text'])
        ax.set_xticks(x)
        ax.set_xticklabels(categories, fontsize=10, color=self.COLORS['text'])
        ax.set_ylim(0, 110)

        # Remove spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(self.COLORS['grid'])
        ax.spines['bottom'].set_color(self.COLORS['grid'])

        # Grid
        ax.yaxis.grid(True, linestyle='--', alpha=0.5, color=self.COLORS['grid'])
        ax.set_axisbelow(True)

        # Legend
        ax.legend(loc='upper right', frameon=True,
                  facecolor='white', edgecolor=self.COLORS['grid'],
                  fontsize=10)

        plt.tight_layout()

        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close()
        buf.seek(0)
        return buf.read()

    def generate_feature_chart(self, data):
        """Generate a horizontal bar chart for feature scores."""
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(9, 4), dpi=100)

        metrics = data['metrics']
        scores = data['scores']

        y_pos = np.arange(len(metrics))

        # Create gradient-like effect with different colors
        colors = [self.COLORS['primary'], self.COLORS['secondary'],
                  self.COLORS['success'], self.COLORS['warning'],
                  self.COLORS['accent']]

        bars = ax.barh(y_pos, scores, height=0.6, color=colors,
                       edgecolor='white', zorder=3)

        # Add value labels
        for bar, score in zip(bars, scores):
            width = bar.get_width()
            ax.annotate(f'{score}%',
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(5, 0),
                        textcoords="offset points",
                        ha='left', va='center',
                        fontsize=11, fontweight='bold',
                        color=self.COLORS['dark'])

        # Styling
        ax.set_yticks(y_pos)
        ax.set_yticklabels(metrics, fontsize=11, color=self.COLORS['text'])
        ax.set_xlim(0, 110)
        ax.set_xlabel('Score (%)', fontsize=10, color=self.COLORS['text_light'])

        # Remove spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color(self.COLORS['grid'])

        # Grid
        ax.xaxis.grid(True, linestyle='--', alpha=0.5, color=self.COLORS['grid'])
        ax.set_axisbelow(True)

        # Remove y-axis ticks
        ax.tick_params(axis='y', length=0)

        plt.tight_layout()

        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close()
        buf.seek(0)
        return buf.read()

    def render(self, report, output_path):
        """Render the product brochure to PDF."""
        # Load data from JSON
        data_file = REPORT_PATH / "data.json"
        with open(data_file, "r") as f:
            report_data = json.load(f)

        # Add chart generation callbacks
        report_data["gen_comparison_chart"] = lambda args: self.generate_comparison_chart(args)
        report_data["gen_feature_chart"] = lambda args: self.generate_feature_chart(args)

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
            print(f"Error generating brochure: {result.error}")
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
    print("Building brochure template...")
    status, zfs = ReportFileBuilder.build_zipfs(REPORT_PATH)
    if not status.success():
        print(f"Error building report: {status.error()}")
        sys.exit(1)

    # Load ReportFile from in-memory zipfs
    report = ReportFileLoader.load_zipfs(zfs)

    # Generate the product brochure
    print("Generating product brochure...")
    generator = ProductBrochure()
    if generator.render(report, output_file):
        print(f"Brochure generated: {output_file}")
    else:
        print("Failed to generate brochure")
        sys.exit(1)
