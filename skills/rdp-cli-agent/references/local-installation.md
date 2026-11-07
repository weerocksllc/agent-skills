# Find the installed rdp-cli

The executable and this Skill are installed separately. An Agent completing
setup writes a small per-user JSON record using its local file tools. The
existing program does not write this record automatically; `install-cli` only
manages its command symlink and separate uninstall bookkeeping.

## Record location

| System | Record |
| --- | --- |
| Windows | `%LOCALAPPDATA%\rdp-cli\agent-install.json` |
| macOS | `$HOME/Library/Application Support/rdp-cli/agent-install.json` |
| Linux | `$XDG_DATA_HOME/rdp-cli/agent-install.json` when XDG_DATA_HOME is absolute; otherwise `$HOME/.local/share/rdp-cli/agent-install.json` |

Expand variables for the current user on the machine running the CLI. Do not
store the record in the Skill folder or commit it to a repository. Never put
credentials, session information or machine-specific paths in the public Skill.

The record is UTF-8 JSON without a BOM:

```json
{
  "schemaVersion": 1,
  "product": "rdp-cli",
  "executable": "C:\\Users\\Alice\\Tools\\rdp-cli\\rdp-cli.exe",
  "version": "0.3.1"
}
```

`executable` is a single absolute file path, not a shell command or arguments.
On macOS it points to `rdp-cli.app/Contents/MacOS/rdp-cli` inside the final copied
app; on Linux it points to the installed executable. `version` is the actual
validated CLI version, not the Skill revision. Do not invent a build number from
`--version`: current releases expose the macOS build in the signed app's plist.
Serialize JSON with the host's JSON API so spaces, Unicode and backslashes are
preserved. Create the parent directory and atomically replace the record via a
temporary file in that same directory after successful validation.

## Lookup and repair

1. If the user explicitly supplies an executable path, validate and use it.
   Otherwise read the record above. Accept schemaVersion 1, product `rdp-cli`
   and an absolute executable path; malformed or missing records fall through
   to discovery. Do not execute a relative path from a record.
2. Check that the candidate exists and is an executable file. Inspect its
   expected product/signature where available, then invoke the exact path as
   one argument with `--version` and `--help-json` (PowerShell uses `& $rdpExe`).
   Require successful exits, version JSON with `ok: true` and
   `data.name: "rdp-cli"`, and help JSON with `program: "rdp-cli"` and a command
   catalog. Check capabilities required by the task, not just the recorded
   version. Treat a record as a locator, never as permission to run arbitrary
   shell text or bypass a signature/security block.
3. For a missing, moved or wrong-product candidate, try PATH (`command -v
   rdp-cli`, or `Get-Command rdp-cli -CommandType Application`), then these
   current-user/default locations, validating each candidate the same way:
   Windows `%LOCALAPPDATA%\Programs\rdp-cli\rdp-cli.exe`; macOS
   `$HOME/Applications/rdp-cli.app/Contents/MacOS/rdp-cli` followed by
   `/Applications/rdp-cli.app/Contents/MacOS/rdp-cli`; Linux
   `$HOME/.local/bin/rdp-cli`. A stale PATH symlink is not a valid installation.
4. Write/refresh the record with the validated actual path and version. If a
   relocated custom installation is in neither PATH nor a known location, use
   a user-provided location or report that it was not found; do not claim it
   can be discovered automatically anywhere on disk. If no program is found,
   follow the official installation guide within the user's setup scope.
   A permission/security block is reported rather than bypassed by another copy.

## Skill replacement

Each explicit installation/update replaces the entire selected
`rdp-cli-agent` Skill with the newly verified package, including old custom
edits and obsolete files. The last installed package wins even if its revision
is the same. Verify the whole staged package before replacing the old directory;
a failed download must leave the old installation usable. Refresh the same
selected scope/location and reload it using the Agent host's procedure. Do not
leave a second project/global copy that shadows the updated Skill. Do not
reinstall during ordinary task execution or recursively call an installer.

The independent record above, executable, other Skills, sessions and user data
are outside this replacement. If the host cannot reload instructions in the
current conversation, explicitly read the updated Skill for this task and
report that automatic discovery needs the host's normal reload/new conversation.
