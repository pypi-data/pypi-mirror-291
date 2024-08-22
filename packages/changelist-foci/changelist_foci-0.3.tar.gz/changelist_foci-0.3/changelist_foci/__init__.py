""" Package Methods.
"""
from changelist_foci import workspace
from changelist_foci.changelist_data import ChangelistData
from .input.input_data import InputData


def get_changelist_foci(
    input_data: InputData,
) -> str:
    """
    Processes InputData, returning the FOCI.

    Parameters:
    - input_data (InputData): The program input data.

    Returns:
    str - The FOCI formatted output.
    """
    cl_list = workspace.get_changelists(input_data)
    return '\n\n'.join(
        cl.get_foci(input_data.format_options) for cl in _filter_list(input_data, cl_list)
    )


def _filter_list(
    input_data: InputData,
    cl_list: list[ChangelistData]
) -> list[ChangelistData]:
    """
    Filter the Changelists based on InputData, to determine which changes to output.
    """
    if input_data.all_changes:
        return list(
            filter(lambda x: len(x.changes) > 0, cl_list)
        )
    if input_data.changelist_name not in ["None", None]:
        return _get_changelist_by_name(
            cl_list,
            input_data.changelist_name,
        )
    return _get_active_changelist(cl_list)


def _get_active_changelist(
    cl_list: list[ChangelistData],
) -> list[ChangelistData]:
    """
    Find the Active Changelist, or the only changelist.
    """
    if len(cl_list) == 1:
        return [cl_list[0]]
    return list(filter(lambda x: x.is_default, cl_list))


def _get_changelist_by_name(
    cl_list: list[ChangelistData],
    changelist_name: str,
) -> list[ChangelistData]:
    """
    Find a Changelist that starts with the given name.
    """
    cl = list(filter(lambda x: x.name.startswith(changelist_name), cl_list))
    if len(cl) == 0:
        exit(f"Specified Changelist {changelist_name} not present.")
    return cl
