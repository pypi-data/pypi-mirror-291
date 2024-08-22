""" Workspace Package.
"""
from changelist_foci.changelist_data import ChangelistData
from changelist_foci.input.input_data import InputData
from changelist_foci.workspace import workspace_reader


def get_changelists(input_data: InputData) -> list[ChangelistData]:
    """
    Obtain all Changelists in a list.
    - Uses the XML string provided by InputData.
    - Applies workspace_reader module.
    """
    return workspace_reader.read_workspace_changelists(input_data.workspace_xml)
