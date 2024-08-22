import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "status: Mark tests with status and run tests by use --status"
    )


def pytest_addoption(parser):
    parser.addoption('--status', action='append', help='Run tests which mark the same status')


@pytest.fixture
def status(config):
    """获取当前指定的status"""
    return config.getoption('--status')


def pytest_collection_modifyitems(session, config, items):
    selected_status = config.getoption('--status')
    if selected_status is None:
        return
    
    deselected_items = set()
    for item in items:
        marker_status = None
        for marker in item.iter_markers('status'):
            [marker_status] = marker.args
        if marker_status not in selected_status:
            deselected_items.add(item)

    selected_items = [item for item in items if item not in deselected_items]
    items[:] = selected_items
    config.hook.pytest_deselected(items=list(deselected_items))


