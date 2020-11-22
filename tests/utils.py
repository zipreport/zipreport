from pathlib import Path

# path for examples/sample1
# used in several tests
SAMPLE1_PATH =  Path(Path(__file__).parent /Path('data/sample1')).absolute()

# path for examples/reports/simple
RPT_SIMPLE_PATH = Path(Path(__file__).parent / Path('../examples/reports/simple')).absolute()

# path for examples/reports/filter_example
RPT_FILTER_EXAMPLE_PATH = Path(Path(__file__).parent / Path('../examples/reports/filter_example')).absolute()

# MIME newsletter example
RPT_NEWSLETTER_PATH = Path(Path(__file__).parent / Path('../examples/reports/newsletter')).absolute()
