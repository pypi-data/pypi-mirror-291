import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "iteration: Mark tests with iteration and run tests by use --iteration"
    )


def pytest_addoption(parser):
    parser.addoption('--iteration', action='append', help='Run tests which mark the same iteration')


@pytest.fixture
def iteration(config):
    """获取当前指定的iteration"""
    return config.getoption('--iteration')


def pytest_collection_modifyitems(session, config, items):
    selected_iteration = config.getoption('--iteration')
    if selected_iteration is None:
        return
    
    deselected_items = set()
    for item in items:
        marker_iteration = None
        for marker in item.iter_markers('iteration'):
            [marker_iteration] = marker.args
        if marker_iteration not in selected_iteration:
            deselected_items.add(item)

    selected_items = [item for item in items if item not in deselected_items]
    items[:] = selected_items
    config.hook.pytest_deselected(items=list(deselected_items))


