def pytest_addoption(parser, pluginmanager):
    parser.addoption('--priority', action='append', help='运行指定优先级的用例，可以多次使用指定多个')


def pytest_configure(config):
    config.addinivalue_line('markers',
                            'priority: test priority')


def pytest_collection_modifyitems(session, config, items):
    priorities = config.getoption('--priority')
    if priorities is None:
        return

    deselected_items = set()
    for item in items:
        priority = None
        for marker in item.iter_markers('owner'):
            [priority] = marker.args
        if priority not in priorities:
            deselected_items.add(item)

    selected_items = [item for item in items if item not in deselected_items]
    items[:] = selected_items
    config.hook.pytest_deselected(items=list(deselected_items))
