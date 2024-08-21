from argparse import ArgumentParser
from barwex_vscodews import barwexutils as xt

code_path = xt.SUBPROCESS.check_output("which code")
app_data_dir = xt.get_barwex_app_data_dir("vscodews")


def main():
    parser = ArgumentParser()
    parser.add_argument("-d", "--project-dir", required=True)
    parser.add_argument("-n", "--workspace-name", dest="workspace_name", help="workspace name")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    project_dir: str = xt.abspath(args.project_dir)
    workspace_name: str = args.workspace_name or xt.basename(project_dir)

    ws_fn = xt.join(app_data_dir, f"{workspace_name}.code-workspace")
    if xt.exists(ws_fn):
        if args.force:
            xt.os.remove(ws_fn)
        else:
            raise FileExistsError(ws_fn)

    data = {
        "folders": [{"path": project_dir}],
        "settings": {},
    }
    xt.IO.write_json(data, ws_fn)

    lines = ["[Desktop Entry]", "Type=Application"]
    lines.append(f"Name=${workspace_name}")
    lines.append(f"Comment=VSCode Workspace Named {workspace_name}")
    lines.append(f"Exec={code_path} {ws_fn}")
    lines.append(f"Icon=com.visualstudio.code")
    lines.append("Terminal=false")

    text = "\n".join(lines)
    destop = xt.join(xt.USER_DESKTOP_DIR, f"vscodews.{workspace_name}.desktop")
    if xt.exists(destop):
        xt.os.remove(destop)

    xt.IO.write_text(text, destop)
