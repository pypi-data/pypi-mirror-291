import hou
import re
import os
from ciopath.gpath_list import PathList, GLOBBABLE_REGEX
from ciopath.gpath import Path
from ciohoudini import common
import logging

logger = logging.getLogger(__name__)


def resolve_payload(node, **kwargs):
    """
    Resolve the upload_paths field for the payload.
    """
    # print("Assets resolve_payload ... ")
    path_list = PathList()
    path_list.add(*auxiliary_paths(node))
    path_list.add(*extra_paths(node))
    do_asset_scan = kwargs.get("do_asset_scan", False)
    if do_asset_scan:
        path_list.add(*scan_paths(node))

    # Get the output folder
    expanded_path = expand_env_vars(node.parm('output_folder').eval())
    output_folder = Path(expanded_path)

    # Convert paths to strings
    current_assets = []
    for path in path_list:
        path = str(path)
        path = path.replace("\\", "/")
        if path not in current_assets:
            current_assets.append(path)
    # print("current_assets: {}".format(current_assets))

    # Filter out paths that are within the output folder
    # Todo: add this to validation as a warning
    filtered_paths = [path for path in current_assets if not is_within_output_folder(path, output_folder)]

    if len(current_assets) > len(filtered_paths):
        node.parm("output_excludes").set(0)

    # print("filtered assets: {}".format(filtered_paths))

    return {"upload_paths": filtered_paths}


def is_within_output_folder(path, output_folder):
    # Normalize the paths to handle different platforms and spaces
    normalized_path = os.path.normpath(str(path))  # Convert path to string
    normalized_output_folder = os.path.normpath(str(output_folder))  # Convert path to string

    # Check if the normalized path is within the normalized output folder
    result = normalized_path.startswith(normalized_output_folder)
    return result


def auxiliary_paths(node, **kwargs):
    """
    Add the hip file, the OCIO file, and the render script to the list of assets.
    """

    path_list = PathList()

    path_list.add(hou.hipFile.path())

    ocio_file = os.environ.get("OCIO")
    if ocio_file:
        path_list.add(os.path.dirname(ocio_file))

    render_script = node.parm("render_script").eval()
    if render_script:
        # Make the render script optional, by putting the last char in sq brackets
        render_script = "{}[{}]".format(render_script[:-1], render_script[-1])
        path_list.add(render_script)

    if path_list:
        path_list = _resolve_absolute_existing_paths(path_list)

    exclude_pattern = node.parm("asset_excludes").unexpandedString()
    if exclude_pattern:
        path_list.remove_pattern(exclude_pattern)

    return path_list


def extra_paths(node, **kwargs):
    path_list = PathList()
    num = node.parm("extra_assets_list").eval()
    for i in range(1, num + 1):
        asset = node.parm("extra_asset_{:d}".format(i)).eval()
        asset = os.path.expandvars(asset)
        if asset:
            path_list.add(asset)

    if path_list:
        path_list = _resolve_absolute_existing_paths(path_list)

    return path_list


def scan_paths(node):
    """
    Scan for assets.

    If we are generating data for the preview panel, then only show assets if the button was
    explicitly clicked, since dep scan may be expensive.
    """

    result = PathList()
    parms = _get_file_ref_parms()

    # regex to find all patterns in an evaluated filename that could represent a varying parameter.
    regex = node.parm("asset_regex").unexpandedString()
    REGEX = re.compile(regex, re.IGNORECASE)

    for parm in parms:
        evaluated = parm.eval()
        if evaluated:
            pth = REGEX.sub(r"*", evaluated)
            result.add(pth)

    result = _resolve_absolute_existing_paths(result)

    exclude_pattern = node.parm("asset_excludes").unexpandedString()
    if exclude_pattern:
        result.remove_pattern(exclude_pattern)
    return result


def _get_file_ref_parms():
    parms = []
    refs = hou.fileReferences()
    for parm, _ in refs:
        if not parm:
            continue
        if parm.node().type().name().startswith("conductor::job"):
            continue
        parms.append(parm)
    return parms


def clear_all_assets(node, **kwargs):
    node.parm("extra_assets_list").set(0)


def browse_files(node, **kwargs):
    files = hou.ui.selectFile(
        title="Browse for files to upload",
        collapse_sequences=True,
        file_type=hou.fileType.Any,
        multiple_select=True,
        chooser_mode=hou.fileChooserMode.Read,
    )
    if not files:
        return
    files = [f.strip() for f in files.split(";") if f.strip()]
    add_entries(node, *files)


def browse_folder(node, **kwargs):
    files = hou.ui.selectFile(title="Browse for folder to upload", file_type=hou.fileType.Directory)
    if not files:
        return
    files = [f.strip() for f in files.split(";") if f.strip()]
    add_entries(node, *files)


def add_entries(node, *entries):
    """
    Add entries to the asset list.

    These new entries and the existing entries are deduplicated. PathList object automatically
    deduplicates on access.
    """

    path_list = PathList()

    num = node.parm("extra_assets_list").eval()
    for i in range(1, num + 1):
        asset = node.parm("extra_asset_{:d}".format(i)).eval()
        asset = os.path.expandvars(asset)
        if asset:
            path_list.add(asset)

    for entry in entries:
        path_list.add(entry)

    paths = [p.fslash() for p in path_list]

    node.parm("extra_assets_list").set(len(paths))
    for i, arg in enumerate(paths):
        index = i + 1
        node.parm("extra_asset_{:d}".format(index)).set(arg)


def remove_asset(node, index):
    curr_count = node.parm("extra_assets_list").eval()
    for i in range(index + 1, curr_count + 1):
        from_parm = node.parm("extra_asset_{}".format(i))
        to_parm = node.parm("extra_asset_{}".format(i - 1))
        to_parm.set(from_parm.unexpandedString())
    node.parm("extra_assets_list").set(curr_count - 1)


def add_hdas(node, **kwargs):
    """
    Add all hda folders to the asset list.

    Called from a button in the UI. It's just a convenience. User could also browse for HDAs by
    hand.
    """

    hda_paths = [hda.libraryFilePath() for hda in common.get_plugin_definitions()]
    if not hda_paths:
        return

    add_entries(node, *hda_paths)


def _resolve_absolute_existing_paths(path_list):
    """
    Resolve all absolute paths in the list to their canonical form.

    This is necessary because Houdini stores absolute paths in the file references, but the
    canonical form is what we want to upload.

    Prefix any relative paths with HIP. It's the best we can do for now.
    However, some relative paths may be internal stuff like op:blah or temp:blah,
    we'll ignore them for now.
    """
    hip = hou.getenv("HIP")
    job = hou.getenv("JOB")
    internals = ("op:", "temp:")

    resolved = PathList()
    for path in path_list:
        if path.relative:
            if not path.fslash().startswith(internals):
                resolved.add(
                    os.path.join(hip, path.fslash()),
                    os.path.join(job, path.fslash()),
                )
        else:
            resolved.add(path)

    resolved.remove_missing()
    resolved.glob()
    return resolved


def expand_env_vars(path):
    """
    Expand environment variables in the given path string.
    """
    return os.path.expandvars(path)
