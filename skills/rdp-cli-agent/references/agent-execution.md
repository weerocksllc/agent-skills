# Agent execution additions

Use this reference only when the installed executable advertises the relevant
commands and options in `--help-json` and `version.data.agent_execution` (contract
version 1). A feature flag is implementation availability, not remote acceptance.
Check `schema_version`, protocol build
capabilities and the selected session's negotiated capabilities. These features
are included in this reference's target release **0.3.1 / build 2026110702**. There is no built-in OCR, text
wait or control detection; interpret images with the Agent's own vision.

The machine-readable [execution contract](agent-execution.contract.json) lists
the required feature flags, commands and options. Compare it with the executable
actually being run; the version string alone does not establish capability support. Do not attempt missing
commands on an older download. The source tree validates its shell and batch
examples with `tests/agent_documentation_contract_test.py` without executing them.

## Observe less, keep coordinates exact

`screenshot --region X,Y,WIDTH,HEIGHT --max-width WIDTH` returns a PNG and its
source rectangle/output mapping. Input still uses remote coordinates. Convert
points using that mapping, including negative desktop origins. Observations
authorize only their covered pointer region; typing still goes to remote focus.

Pass the returned comparison reference as `--since REF` with the same selection.
`changed:false` intentionally contains no image. An expired/context-mismatched
reference requires a new full observation, not reuse of an old input token.

`wait --condition changed|stable --region ...` watches pixels, not application
success. Stable error dialogs can satisfy it. For asynchronous work use
`--condition transfer|operation|connection` with its actual ID and target state.
Use bounded deadlines and `wait status/cancel --wait-id ORIGINAL_REQUEST_ID`.
Cancellation stops the wait, not the transfer it was observing.

## Short batches and durable tasks

Batch JSON has `version:1` and 1–64 steps. Use `observe` then input steps with
`observation_from` naming that explicit prior observation. Read/choose coordinates
before constructing input; a batch cannot interpret a new image on your behalf.
`assert` checks a prior JSON result, not the remote business outcome. `checkpoint`
captures and stops; later steps remain `not_run` until a separate explicit batch.
Pass JSON with `batch --steps-stdin`, a session and a stable `--request-id`.

Do not repeat a partial/unknown batch. Query `batch status --batch-id ID`, inspect
the remote application and verify saved artifacts. Use a new request only for
newly decided remaining work. Changes in control, connection or geometry stop
old coordinates; do not silently recapture and reuse them.

For batch `files.upload/files.download`, `local` is an absolute path on the
rdp-cli host, while `path` is relative to the session's file root. Keep the
returned transfer ID and wait for completion. Failure of a later step does not
undo an already submitted transfer or authorize a fresh upload retry.

For resumable work explicitly create a task with `tasks create --session SESSION
--title TITLE`, then attach operations with `--task TASK_ID`. Recording is opt-in.
Default records omit text/clipboard/credentials and do not include screen images.
Use `--record-frames` only when storing real screenshots is intended; it does not
detect/redact private material. `tasks evidence` stores an explicitly selected
artifact copy. `tasks export --format html|json --out NEW_PATH` creates an offline
report; it does not replay work.

After interruption, query `tasks status`. A persisted fragment count is a lower
bound; unrecorded input may have reached the target. Inspect the actual outcome,
make a checkpoint, and use `tasks new-run --from-checkpoint CHECKPOINT_ID` for
explicit continuation. A new run never restores stale observations or input
queues. Expired/missing history is not proof of non-execution.

If the system clock moves backwards, history reads and offline exports remain
available, but new durable writes return `TASK_CLOCK_ROLLBACK` until the clock
catches up to the last committed timestamp. Retained requests remain protected;
do not submit a new ID to work around this condition.

Task permissions `read/append/export/manage` are independent of session control.
An Agent receiving a session does not automatically receive private task history.
Do not purge history while recovering an uncertain operation. Purge removes only
selected local history, not original/remote artifacts or credentials.

## Named Agents and a person taking over

`agents register` returns an ID and a native credential reference. Use both
`--agent-id` and `--agent-ref`; a name is not authentication. Session grants are
`read/control/manage`. Use `control claim`, then supply its `--claim-ref` for
input. Explicitly renew before expiry, including during long reasoning gaps;
neither short CLI exit nor an open MCP connection is automatic lease renewal.
Duplicate display names do not share identity or permissions. Without an
available system credential store, registration returns
`AGENT_CREDENTIAL_STORE_UNAVAILABLE`; there is no plaintext fallback. Legacy
local-default use remains available. Service restart discards old claims and
keeps restored sessions paused; it does not resume an old input queue.
Creating a GUI/Web viewer, changing shared audio settings or cancelling another
identity's transfer requires a session `manage` grant. Read-only Agents may
cancel their own downloads. Do not use a viewer to bypass an input grant.

An Agent-to-Agent handoff uses `control handoff --to-agent ID`. A person may take
control through the same session's GUI/Web viewer and choose which authorized
Agent receives it back. Stop input while human control is held. The receiver
queries `control claim-status` under its own identity to obtain its current
claim reference, takes a fresh screenshot and decides the next action. This
logical coordination is not isolation against a malicious process under the
same OS user.

## Profiles, diagnostics and MCP

Profiles keep non-secret connection options and credential references. Select a
saved profile with `connect --profile NAME`; overriding the target/protocol
clears old authentication references. On import to another host, resolve missing
references explicitly. Import is not permission to connect or run commands.

`doctor` and `doctor --session SESSION --redact` inspect without input or audio.
Only `doctor --probe --profile NAME` attempts a temporary connection. Read each
stage's `pass/unknown/not-run` result; capability availability is not a successful
microphone/input test. Use reported next steps, not automatic policy changes,
credential resets or repeated guesses.
Temporary probes disable playback and capture regardless of the saved profile;
they change neither that profile nor existing sessions. Those media checks report
`PROBE_MEDIA_DISABLED/not-run`. `timings` measures connection, inspection and
cleanup separately; authentication/first-frame timings are not independently
measured. Android local closure is not confirmed device cleanup: inspect
`probe.cleanup` and the original session before explicitly attempting a new one.
For a local report, redirect the redacted JSON output to a new local file.

MCP uses the same executable: `rdp-cli mcp stdio`. Tools are `rdpcli.` plus the
CLI path with dots, and argument names omit `--`. Repeated options are arrays;
boolean flags and integers use their JSON types. For stdin supply both the
corresponding `*-stdin:true` option and a `stdin` string. Tool schemas and CLI
help share the contract; no separate Node/Python bridge is needed.

Use native image content, with its structured coordinates and observation.
For batch/checkpoint images `_meta["rdpcli/resultPath"]` identifies the matching
result object. The combined PNG budget is 4 MiB per response, without hidden
rescaling. `MCP_IMAGE_UNAVAILABLE` means image delivery failed, not that prior
steps did not execute. Inspect retained step results, request a smaller fresh
screenshot, and never replay completed actions to obtain their pictures.

JSON-RPC IDs are not business request IDs. Keep business `request-id` stable
only for an identical retry within the supported retention window. After MCP
cancellation/EOF, use independent operation queries; submitted work may have
completed. Closing one MCP transport leaves shared sessions running.

CLI and MCP transport errors distinguish failure before submission from a lost
reply after possible submission. `SERVICE_UNAVAILABLE` with
`data.may_have_dispatched:true` is `unknown` and `retryable:false`; the service
may still be executing. Query the original business request ID and inspect the
target before deciding what to do next. Never send the same mutation under a new
ID just because the first reply was lost. Exact-ID deduplication has a bounded
retention window; it is not permission to replay an expired request.

## Android virtual display

Only explicitly requested `--android-display virtual` creates a new owned
display; ordinary connections retain the main-screen behavior. Select size/DPI
and a known `--android-start-app PACKAGE`. Observe the actual returned display
identity and app result; creating a display ID is not proof the app is usable.

Use `usb:SERIAL` or the verified Wi-Fi device identity, never a bare serial or a
list index. Main and virtual modes are alternatives for one phone, not concurrent
sessions. Main mode rejects virtual size/DPI options. Initialization needs a real
first frame; an empty display can time out and release its owned resources.
Disconnect is available during creation. Once cleanup is confirmed, explicitly
connect with a new request and the intended app; `resume` or ordinary app launch
on a frame-less session is not recovery. Query an unknown launch before deciding
on a new operation.

Input, screenshots and GUI/Web viewing stay bound to that owned display.
Rotation requires a new observation. A package may reuse an existing activity;
do not promise application isolation. `ime_policy:fallback_to_main` means the
keyboard may appear on the phone's main screen. The UI reports that limitation.
There is no guarantee of private per-display microphone/audio: capture remains
device-scoped, requires existing explicit authorization, and stays off by default.

Disconnect releases the owned display without package-wide force-stop or deleting
application data. If cleanup is pending after disconnection, report it as pending.
Save and retrieve results first: removing the display may end its activity and
lose unsaved UI state. Closing a viewer alone leaves the session running. A lost
display cannot be recovered by reusing its numeric ID; verify device, unique
display identity and connection generation. A package-level stop could affect
other instances, so virtual sessions reject `android apps stop` with
`ANDROID_DISPLAY_APP_STOP_UNAVAILABLE`. Do not switch to another tool or the main
display to work around that result; disconnect only the owned display when done.
Never switch to main-screen input or automatically relaunch the application to
hide a virtual-display failure.
