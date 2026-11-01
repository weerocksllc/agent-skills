# Protocol workflows

Read only the section for the selected protocol. All examples use the installed
executable's help and the explicit session/observation identifiers from results.

- [RDP TLS recovery](#rdp-tls-recovery)
- [VNC authentication](#vnc-authentication)
- [Linux graphical sessions](#linux-graphical-sessions)
- [Android phones](#android-phones)

## RDP TLS recovery

`RDP_TLS_HANDSHAKE_FAILED` is a transport-encryption negotiation failure, not
evidence of a wrong password or an unsupported RDP server. Read `connect --help`
and the failed session's `status` to check the selected `tls_profile`. The
modern-profile error alone does not identify which TLS version the server
supports: TLS 1.2 servers can still use older signatures such as SHA-1.

The released client supports `--tls-profile modern|legacy`. Modern requires
TLS 1.2 and modern cryptography. Legacy permits older signatures/ciphers and
TLS 1.0, but **does not force TLS 1.0**; it can still negotiate TLS 1.2.
Changing `--cert-policy` alone does not resolve this cryptographic mismatch.

For a user-authorized target on a trusted LAN/VPN whose legacy requirement is
established by target configuration, previous acceptance or specific handshake
evidence, explicitly retry the same target once with `--tls-profile legacy`.
Preserve the host, port, user/domain, credential source, certificate policy and
other intended settings; change only the TLS profile. A changed request needs
a new request ID. Use a new `connect`, because `reconnect` retains the original
session profile. Existing authorization for this compatibility choice remains
valid; this Skill does not require another permission question. A private IP
or a generic network error alone does not establish a legacy requirement.

Do not override a user's modern-only requirement. Do not change server-wide
TLS/NLA settings, disable strict certificate validation, replace credentials,
or switch to a local GUI as a TLS workaround. If the target requirement is
unknown, investigate the handshake/configuration instead of asserting that
the server only supports old TLS or declaring the product incompatible.
If legacy was already selected, or the one compatibility attempt fails, inspect
that actual error; do not loop through unchanged attempts. Authentication and
certificate errors follow their own recovery paths, not another TLS downgrade.

Example for an established legacy target (feed the original password privately
on stdin; retain any original port/domain/certificate and other options):

```sh
rdp-cli connect --host HOST --user USER --password-stdin --tls-profile legacy
```

Save the successful response's `data.session`, check `status` and capture/read
a screenshot before claiming a usable desktop. A TLS handshake by itself is
not login or desktop acceptance. The reported `tls_profile` is configuration,
not the negotiated TLS version. Reuse the verified target profile for later
connections within the user's task; do not weaken unrelated sessions.

## VNC authentication

If the installed build advertises `--vnc-security x509-plain`, an existing
VeNCrypt 0.2 / X509Plain endpoint can use `--user USER --password-stdin
--vnc-tls-pin CERTIFICATE_SHA256`. The 32-byte SHA256 leaf certificate fingerprint
must come from an independent trusted channel, not the unverified connection.
Credentials follow TLS/pin/date verification. Do not change the server's
authentication settings or retry with None/DES after a certificate/subtype error.
Other secure VNC variants are not implicitly supported.
If the installed build advertises `--vnc-security ard`, connect to macOS Screen
Sharing with `--protocol vnc --host HOST --user MAC_USER --password-stdin` (or an
existing credential reference). With no explicit mode, `--user` selects `ard`;
without `--user`, classic `vnc-auth` remains the default and requires the Mac's
separate VNC password. ARD fields are limited to 63 UTF-8 bytes each; do not
truncate credentials. ARD is not TLS and does not encrypt desktop traffic.
Do not change server settings or retry another authentication mode after failure.

## Linux graphical sessions

Check `version` build capabilities and `connect --help` before choosing X11;
development support does not imply the downloaded release contains it. The
client embeds SSH and needs no external `ssh` executable or local X server.
Use the supplied account, key/password and verified known-hosts file or host
fingerprint. `linux targets` reads the account's existing logind sessions and
recognized existing TCP listener candidates. Missing logind/ss is reported
separately; never install either. A candidate is not a verified protocol,
reachable service, authorized display or binding to the listed desktop. Do not
connect to wildcard/loopback addresses as if they were remote host addresses,
guess protocols from ports or automatically select between candidates.

`--protocol x11 --mode desktop` attaches to an explicitly authorized existing
`--display` and `--xauthority`. `--mode application --application /installed/app`
starts that installed application via SSH X11 forwarding. Pass arguments as
`--app-args` JSON strings; do not build a shell script. The application uses an
isolated offscreen display in the same executable. No remote component is
uploaded or enabled. A Wayland desktop needs an already configured RDP/VNC
endpoint; a portal, Wayland socket or rootless Xwayland is not such an endpoint.

Use the common screenshot/input/control commands. In application mode,
`linux apps list` returns the exact instance and window generations. A menu or
dialog invalidates old observations without returning control from a person.
`type` preflights the entire text against the actual base keyboard map; if it
cannot represent the text, explicitly choose `linux text --method clipboard`
with `--text-stdin` and a fresh observation. This replaces the remote selection
and sends the chosen paste shortcut; verify the application's resulting text.
X11 provides no audio/microphone channel. Files require an available SFTP
capability; never substitute a client cache for the remote filesystem.
Use common `files list/upload/download/status/cancel` commands. The default is a
private SSH home `.rdp-cli/files/<session-id>` directory; `--linux-file-root`
selects an explicit existing remote directory at connection time. Read
`remote_directory` / `remote_path` from results instead of inventing paths.
Save remote documents before downloading. `FILE_BUSY` means detected change;
`ATOMIC_PUBLISH_UNAVAILABLE` means the server lacks the required publication
extension; `SFTP_FILE_RESULT_UNKNOWN` requires inspecting the target, never an
automatic upload retry. Ordinary SFTP checks do not promise snapshot isolation
against concurrent same-user writers. No helper may be deployed to fill gaps.

Save and verify work, capture a fresh observation, then use
`linux apps stop --session SESSION --instance INSTANCE --observation OBSERVATION`.
Read the exact instance from `linux apps list`. This closes its display
connection and cannot promise graceful process exit.
Closing a viewer is different and leaves the connection running. An application
connection lost through SSH/display failure must not be recovered by re-running
its command. Inspect status/results and make any new launch explicit. Desktop
reconnect also requires the build to support original display identity binding.

Keep the workflow command based; substitute verified inputs and the returned
session/observation/transfer identifiers in this example:

```sh
rdp-cli linux targets --host HOST --user USER --ssh-key KEY --ssh-known-hosts TRUST
rdp-cli connect --protocol x11 --mode application --host HOST --user USER --ssh-key KEY --ssh-known-hosts TRUST --application /installed/editor
rdp-cli screenshot --session SESSION --out before.png
rdp-cli linux text --session SESSION --method clipboard --text-stdin --observation OBSERVATION < text.txt
rdp-cli screenshot --session SESSION --out after.png
rdp-cli files list --session SESSION
rdp-cli files download --session SESSION --path saved-report.txt --local ./saved-report.txt
rdp-cli files status --session SESSION --transfer-id TRANSFER
rdp-cli pause --session SESSION
rdp-cli watch --session SESSION --viewer web
rdp-cli status --session SESSION
```

Choose the known desktop alternative with `--mode desktop --display DISPLAY
--xauthority AUTHORITY` instead of application parameters. Inspect before
clicking/typing or selecting a save action; retrieving a file requires the
application to have actually saved it under the authorized directory. A newly
opened dialog may still be changing: inspect its real frame before entering a
filename. After a partial `type`, inspect the reported progress and new frame;
do not replay the whole string. Explicit clipboard paste is a separate choice. Confirm
the transfer's completion and digest. `watch` is only for a requested human
view. A headless Linux
client can supply authorized Web without a native window or external X server.
After a handoff obtain a fresh screenshot; do not resume over human control.
Save and retrieve results before disconnecting an application display. Native,
tray and Web disconnect warnings do not turn ordinary viewer close into a stop.

## Android phones

Use `android devices` and explicitly choose the supplied `device_id`. USB and
Wi-Fi use `connect --protocol adb --device DEVICE --transport usb|wifi`.
Wi-Fi pairing uses the phone's **pairing** port and `android pair --code-stdin`;
connecting uses its separate **connection** port. Discovery is not authorization.
Do not start an external adb server or reclaim another tool's connection by
default. If the user has explicitly authorized releasing the affected owners,
verify their current process/device identities and proceed within that scope;
do not request the same permission again or signal a stale recorded PID. Never
guess the first phone in a reordered list. Saved identities require explicit save;
`android forget` removes the local reference, not the phone's paired-device entry.

`ADB_USB_RESOURCE_EXHAUSTED` means the host cannot allocate USB clients; it is
not a phone authorization denial. Inspect the selected interface and specific
competing scanner. Stop only an explicitly authorized owner, then reconnect
only the selected phone after fixing that scanner. Do not blanket-kill unrelated
adb sessions, reset other phones or change USB authorization without explicit
authorization for those affected connections/devices. Uncertain input must never
be replayed as a resource recovery step. rdp-cli does not perform those recovery
actions itself; the Agent must verify actual release and cleanup separately.

After reading a screenshot, use `android touch --kind tap|double-tap|long-press|swipe|drag|pinch|gesture`
with its observation; coordinates are phone pixels and durations are milliseconds.
`android key --key back|home|recent` is distinct from desktop shortcuts.
Rotation invalidates old coordinates. Direct `type` supports printable ASCII,
LF/TAB (normalizing CRLF); it rejects unsupported text before sending any prefix.
For Chinese/emoji, explicitly use `android text --method clipboard --text-stdin`
with a fresh observation. This changes the phone clipboard; check the actual App
afterward. Do not infer application acceptance from `paste_submitted`.

`files` paths are relative to the phone session's configured root. An
`ANDROID_FILE_RESULT_UNKNOWN` terminal transfer may already be published;
inspect the same device/root and verify the target content before deciding on
an explicit new transfer. Do not replay it automatically or delete an uncertain
target. Known completed files remain valid even when the rest is partial/unknown.
Wait for
`completed`: it includes phone-side publication and integrity verification, but
does not mean an App consumed the file. Same-name replacement requires explicit
`--overwrite`. Upload an APK first, then `android apps install --path FILE.apk`;
replacement requires explicit `--replace`. Install/launch/stop return a job;
query `android apps status --job JOB` until terminal. For an unknown result,
query `android apps info --package PACKAGE` and a new screenshot instead of
repeating the mutation. Host job results follow the original operation's retry
window (currently one minute from submission and at most 512 global records);
the phone component retains at most 64 jobs and does not evict active jobs.
A missing/expired job or backend restart is not proof that nothing happened.
Check the actual package and screen before deciding on a new mutation.

Example Android task sequence (substitute explicit device, session, observation
and returned job/transfer IDs; inspect each result before the next mutation):

```sh
rdp-cli android devices
rdp-cli connect --protocol adb --device DEVICE --transport usb
rdp-cli status --session SESSION
rdp-cli screenshot --session SESSION --out /absolute/path/phone-before.png
# Read the PNG. Touch coordinates are phone pixels, not viewer coordinates.
rdp-cli android touch --session SESSION --kind tap --x 250 --y 400 --observation OBSERVATION
# Take/read a new screenshot before text input; feed Unicode through stdin.
rdp-cli android text --session SESSION --method clipboard --text-stdin --observation OBSERVATION
rdp-cli screenshot --session SESSION --out /absolute/path/phone-after.png
rdp-cli files upload --session SESSION --local /absolute/path/result.txt --path result.txt
rdp-cli files status --session SESSION --transfer-id TRANSFER
rdp-cli files download --session SESSION --path result.txt --local /absolute/path/result-returned.txt
rdp-cli files status --session SESSION --transfer-id TRANSFER
# Verify the returned bytes; no local viewer is required for this workflow.
```

Phone audio defaults off. `audio android --source output` requests permitted phone
playback through Android MediaProjection. Read `authorization_pending`, `active`
and `authorization_stage`: preparing/installing/launching are not confirmation
dialogs; recording_permission/system_sharing require a person on the phone.
Never inject consent or treat the request as active capture. Phone playback and
system volume stay unchanged. `audio android --source microphone`
captures the **phone's** physical microphone and requires
control plus a fresh observation; `--source off` stops it. This does not inject
the computer's microphone into Android Apps. Pause, control loss or the initiating
viewer's close stops microphone capture; resuming does not restart it.
Do not use a different tool to bypass control or access checks.

This is task guidance, not a tool sandbox. It neither disables computer-use nor
changes host permissions, and installation is optional.
