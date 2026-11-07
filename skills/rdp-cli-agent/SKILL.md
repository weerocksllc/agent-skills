---
name: rdp-cli-agent
description: Operate RDP/VNC desktops, X11 applications or Android 12+ phones headlessly through rdp-cli commands and screenshots. Use for authorized remote tasks, verification and command recovery; check the installed build's protocol capabilities. Local application tasks alone do not require this skill.
license: MIT
metadata:
  version: "1.3.0"
  product-version: "0.3.0"
  product-build: "2026110701"
---

# Remote tasks with rdp-cli

## Work headlessly by default

Use rdp-cli commands or its built-in MCP for remote work. Connect, observe,
send keyboard/mouse input and transfer files without opening a local viewer.
Headless operation is the default workflow; it does not need an extra flag.

GUI and Web viewers are for a person to watch, pause or take over the same
session. Do not automatically open them or drive them with local computer-use
to perform an ordinary remote task. An explicit viewer task or necessary viewer
diagnosis can use those interfaces within the user's authorized scope.
On command failure, follow the recovery guidance below instead of switching
to a viewer. While a person holds control, stop sending remote input; after
control returns, observe the screen again before continuing.

Use the executable supplied by the user or available on PATH. Consult
`rdp-cli --help` and `<command> --help` for the installed version's exact options.

For cropped observations, pixel waits, batches, durable task evidence, named
Agents, profiles, MCP or Android virtual displays, first check the installed
`--help-json` and read [Agent execution](references/agent-execution.md).
This Skill targets **0.3.0 / build 2026110701**, including observer activity
hints and the previously released Agent execution commands; older files also reported 0.1.0, so verify the feature contract and
commands of the installed executable instead of relying on the version alone.

## Prepare the local executable

Use a host that can run local commands and inspect images, with access to the
authorized target. The rdp-cli executable is a separate runtime requirement.

Locate the executable using [Local installation](references/local-installation.md):
use an explicit user-supplied path, otherwise read the per-user installation
record, then check PATH and standard install directories. Validate the actual
program before using it; refresh a missing or stale record after discovery.
Read its `--version`, `--help-json` and the relevant command's `--help`.
Reuse a working program that supports the task; do not update it on every use.

If the program is missing, follow the [official installation guide](https://rdp-cli.com/agent-install.md)
within the user's authorized setup/task scope. Select and verify the native
release from its [manifest](https://rdp-cli.com/agent-install.json).
Every explicit Skill installation/update replaces the previous Skill at the
same selected location, including custom edits: the last installed package wins.
Replace the complete verified Skill, not just SKILL.md. Do not create another
scope or invoke an installer recursively. Ordinary remote tasks do not reinstall
Skills. The executable location record lives outside the Skill and survives
replacement; see the local installation reference for its format and lookup.

Installing the Skill alone does not install rdp-cli. Checking help does not
require a remote session. An upgrade must preserve user data and account for
active sessions instead of terminating them as an incidental setup step.

## Read only the relevant reference

- For RDP TLS compatibility, VNC/macOS authentication, X11/SFTP, Wayland endpoint selection or Android
  USB/Wi-Fi, input and audio, read the matching section in
  [Protocol workflows](references/protocols.md).
- For observation regions, waits, batches, durable tasks, multi-Agent control,
  profiles, MCP or Android virtual displays, read
  [Agent execution](references/agent-execution.md).
- For machine-readable requirements, use the
  [capability contract](references/agent-execution.contract.json).

The website explains product use cases; the installation guide handles setup;
this Skill handles task execution; local command help supplies exact syntax.
If a required command or capability is absent, use a verified supported path or
report the mismatch. Do not keep retrying a parameter from newer documentation.

## Observe, act, verify

- Connect to the authorized target or use the specified existing session. Keep
  `data.session` explicitly; do not guess a target from the most recent session.
  Use provided credentials/stdin/credential references without putting secrets
  in saved examples or reports. Read `status` and negotiated capabilities.
- Run `screenshot --session SESSION --out PATH`. Read the returned PNG with an
  image-reading tool and inspect `data.observation` and coordinate metadata.
  Coordinates refer to remote pixels, not the position of a local viewer.
- Select `click`, `move`, `scroll`, `drag`, `type` or `key` for the task. Supply
  the observation and explicit desktop/monitor coordinates where required.
  Use `type` for text, `key` for shortcuts, explicit `clipboard` operations when
  clipboard use is intended, and `files` for the RDP exchange drive.
- Capture a new image or query the appropriate result to confirm the actual
  effect. `sent` means input was dispatched, not that the remote task succeeded.
  A Welcome/login frame may accept input; do not add an Explorer-ready gate.

Example after connecting (substitute actual values):

```sh
rdp-cli status --session SESSION
rdp-cli screenshot --session SESSION --out /tmp/remote-before.png
# Read the PNG; choose coordinates and copy data.observation.
rdp-cli click --session SESSION --desktop --x 420 --y 315 --observation OBSERVATION
rdp-cli screenshot --session SESSION --out /tmp/remote-after.png
# Read the new PNG and verify the remote effect.
```

Use a writable local output path appropriate to the client OS. RDP and VNC use
these same observation/input commands, but capabilities differ. VNC has no file
exchange, audio, microphone or active monitor-layout support. Unicode input and
clipboard support depend on the server/application; do not equate successful
submission with correct displayed text.
RDP types at about 20 characters/second plus overhead to accommodate Windows
text controls. For long text, set an adequate `--timeout-ms` before submission
or choose explicit clipboard paste when permitted; never blindly replay a
timed-out text operation.

## Recover according to the result

- **Local storage:** `LOCAL_STORAGE_FULL` means the computer running rdp-cli
  cannot allocate its frame cache (about 256 MiB per session). It is not a
  remote password, TLS or request-format error. Free authorized local space,
  then submit a new connect request; unchanged retries cannot fix it. Do not
  delete active caches, stop unrelated sessions or open a viewer as a workaround.
  To use another drive, follow `connect --help`: use `RDPCLI_DATA_DIR` plus a
  fresh `RDPCLI_RUNTIME_DIR` for a separate service. Changing the data variable
  alone does not move a running service.
  `LOCAL_STORAGE_ERROR` is a different access failure: inspect `native_error`
  and local drive permissions instead of assuming the disk is full.
- **RDP TLS handshake failure:** read [RDP TLS recovery](references/protocols.md#rdp-tls-recovery).
  TLS 1.2 servers can still need legacy signatures; do not conclude the server
  is unsupported or the password is wrong. For a confirmed legacy target within
  the user's authorization, explicitly select the compatible profile and verify
  the resulting session rather than stopping at the first handshake failure.
- **Stale observation:** obtain and read a new screenshot, then reconsider the
  action. Connection, control and topology changes invalidate observations.
- **Human takeover/pause:** stop input and report the state. Wait for explicit
  return of control; do not automatically resume or use another viewer to win
  control back. After authorized resume, take a new screenshot.
- **Timeout/unknown input result:** query `operations status` with the original
  request/operation ID and observe the screen before deciding whether to retry.
  A timeout is not proof of non-execution. Reuse an ID only for the identical
  request within the supported window; never replay a whole partial operation.
- **Queued transfer:** use `files status --session SESSION --transfer-id ID`
  until a terminal result, and verify content/hash when needed. A file existing
  or a command returning ok does not mean the transfer is complete.
- **Capability unavailable:** inspect status and choose an appropriate supported
  command alternative or report the limitation. Opening a viewer does not add
  a missing protocol capability.

## Human observation and other tools

When a person wants to watch, use `watch --session SESSION --viewer window`
or `watch --session SESSION --viewer web`, or direct them to the tray/menu bar. These viewers
share the session and start read-only. Continue ordinary remote automation with
CLI commands; respect explicit human takeover and return.

GUI/Web action hints make clicks, scrolling, shortcuts and input counts visible
to the person, while separate transfer hints preserve human/Agent origin. The
tray/menu bar and session list show activity where the desktop supports them.
These are presentation aids: they do not alter screenshots or prove that the
remote task succeeded. Sensitive input content is not shown. Keep using fresh
screenshots and command results to verify work; do not open a viewer just to
read its activity hints.

Computer-use remains useful for local applications, viewer diagnosis, explicit
GUI tasks, or a justified fallback. Before switching to a path that affects the
local desktop, explain the reason and impact and follow existing user
authorization; this skill adds no unconditional confirmation requirement.
First diagnose a command failure instead of automatically switching to GUI.
