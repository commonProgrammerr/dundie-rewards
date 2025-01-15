MARKER = """
unit: Mark for unit tests
integration: Mark for integration tests
high: High priority
medium: Medium priority
low: Low priority
"""


def pytest_configure(config):
    map(lambda l: config.addinivalue_line("markers", l), MARKER.splitlines())
