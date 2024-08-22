"""Testing Changelist Foci Module Initialization Methods.
"""
from changelist_foci import _filter_list
from changelist_foci.input.input_data import InputData
from . import get_empty_xml, get_main_changelist_data, get_no_changelist_xml, get_simple_changelist_data, get_simple_changelist_xml, get_multi_changelist_xml


def test_filter_list_simple_select_active_():
    input_data = InputData(
        workspace_xml=get_simple_changelist_xml(),
        changelist_name=None,
    )
    result = _filter_list(input_data, [get_simple_changelist_data()])[0]
    assert result.name == 'Simple'
    assert result.comment == 'Main Program Files'
    assert result.id == '9f60fda2-421e-4a4b-bd0f-4c8f83a47c88'
    assert len(result.changes) == 1
    change = result.changes[0]
    assert change.before_path == change.after_path
    assert change.before_dir == change.after_dir


def test_filter_list_simple_select_simple_():
    input_data = InputData(
        workspace_xml=get_simple_changelist_xml(),
        changelist_name='Simple',
    )
    result = _filter_list(input_data, [get_simple_changelist_data()])[0]
    assert result.name == 'Simple'
    assert result.comment == 'Main Program Files'
    assert result.id == '9f60fda2-421e-4a4b-bd0f-4c8f83a47c88'
    assert len(result.changes) == 1
    change = result.changes[0]
    assert change.before_path == change.after_path
    assert change.before_dir == change.after_dir


def test_filter_list_simple_select_():
    input_data = InputData(
        workspace_xml=get_simple_changelist_xml(),
        changelist_name='Simple',
    )
    result = _filter_list(input_data, [get_simple_changelist_data()])[0]
    assert result.name == 'Simple'
    assert result.comment == 'Main Program Files'
    assert result.id == '9f60fda2-421e-4a4b-bd0f-4c8f83a47c88'
    assert len(result.changes) == 1
    change = result.changes[0]
    assert change.before_path == change.after_path
    assert change.before_dir == change.after_dir


def test_filter_list_multi_select_active_():
    input_data = InputData(
        workspace_xml=get_multi_changelist_xml(),
    )
    result = _filter_list(input_data, [get_main_changelist_data()])[0]
    assert result.name == 'Main'
    assert result.comment == 'Main Program Files'
    assert result.id == 'af84ea1b-1b24-407d-970f-9f3a2835e933'
    assert len(result.changes) == 2
    change1 = result.changes[0]
    assert change1.before_path == '/history.py'
    assert change1.before_dir == False
    assert change1.after_path == None
    assert change1.after_dir == None
    change2 = result.changes[1]
    assert change2.before_path == '/main.py'
    assert change2.before_dir == False
    assert change1.after_path == None
    assert change1.after_dir == None
