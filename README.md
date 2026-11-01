# Weerocks Agent Skills

Skills that help AI agents use Weerocks tools to complete practical tasks.
This repository contains agent instructions and reference documents. Product
source code and executable downloads are maintained separately.

## Available skills

| Skill | What it does | Product |
| --- | --- | --- |
| [rdp-cli-agent](skills/rdp-cli-agent/SKILL.md) | Headless control of RDP/VNC desktops, X11 applications and Android phones, with human viewing and takeover through the same session. | [rdp-cli](https://rdp-cli.com/) |

Only published, usable skills are listed here. Protocol capabilities differ;
consult the Skill and the installed executable's help for the supported scope.

## Install the rdp-cli Skill

With Node.js/npm available for the Skills CLI:

```sh
npx skills add weerocksllc/agent-skills --skill rdp-cli-agent
```

Select the agent and installation scope when prompted. This installs the Skill
and its reference files, **not the rdp-cli executable**. Node.js is used by this
optional Skill installer; rdp-cli itself does not require it.

Tell your agent:

> Use rdp-cli-agent. Check whether rdp-cli is installed and supports my task.
> If it is missing, follow https://rdp-cli.com/agent-install.md to install the
> official file for this computer. Refresh this Skill at the same location
> and record the installed executable path. Verify setup before connecting.

For installation without the Skills CLI, give your agent the same
[official installation guide](https://rdp-cli.com/agent-install.md).
It supplies program downloads, checksums and the complete Skill file list.

## Example requests

- “Use the Windows session I provide. Fill in this form and verify the saved
  result using screenshots. Keep the work headless.”
- “Connect to my authorized Mac VNC desktop, inspect the application and
  report the result. Use the account/password mode supported by that server.”
- “Let me view the same session through rdp-cli's GUI or Web viewer. Pause
  Agent input when I take control and wait for me to hand it back.”

Supply target and credential information through your agent's supported private
inputs, not through GitHub issues. These are task examples, not promises that
every remote application or protocol supports identical features.

## Versions and updates

The Skill declares its own revision and the product version it targets in
`SKILL.md`. `manifests/rdp-cli-agent.json` records the target release and exact
file hashes. An installed executable's `--version`, `--help-json` and command
help describe that file's actual capabilities.

```sh
npx skills check
npx skills update
```

These commands check/update installed Skills; they do not upgrade rdp-cli or
install every future Skill in this repository. Program updates use the official
installation guide and account for active sessions and user data.

Each explicit Skill installation/update replaces the previous package at the
selected location, including custom edits. The last installation wins; use the
same scope/location instead of creating a second copy. Ordinary use does not
reinstall. The Agent records and validates the executable location separately;
see [local installation](skills/rdp-cli-agent/references/local-installation.md).
That local record survives Skill replacement. Existing programs can be found
through PATH/default locations and registered without reinstalling them.

## Maintenance and licensing

Each product maintains its Skill at the source and synchronizes only its own
published folder and manifest here. Do not copy internal development skills,
credentials, private test records or product source into this repository.
See [CONTRIBUTING.md](CONTRIBUTING.md) for maintenance rules.

The [MIT license](LICENSE) covers files in this repository. Downloaded programs
are separate artifacts with their own distributed license notices; this
repository does not grant rights to unpublished product source code.

Installing successfully does not prove skills.sh has indexed a Skill. Directory
visibility is checked separately; we do not claim an official endorsement.
