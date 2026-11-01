# Maintaining published skills

- Keep each Skill in `skills/<name>/SKILL.md`; the frontmatter name matches the
  folder. Use stable names to preserve install commands.
- Each product source repository is authoritative for its Skill. Make changes
  there, review them, then export the complete package here. Do not maintain an
  unrelated second version in this repository.
- The rdp-cli source project provides:

  ```sh
  node website/scripts/export-agent-skill.mjs --dest /path/to/agent-skills
  node website/scripts/export-agent-skill.mjs --dest /path/to/agent-skills --check
  ```

  Run these from the rdp-cli project. Export changes only `skills/rdp-cli-agent/`
  and `manifests/rdp-cli-agent.json`, preserves other products, and refuses to
  overwrite locally edited managed files. The exporter does not commit or push.
- Increment the Skill revision when its contents change. Update the target
  product version only when the guide targets a different product release.
  Documentation-only edits do not invent a new executable release.
- Review the diff and run `python3 checks/validate.py` before publishing. Check
  referenced resources, version compatibility and installation in a temporary
  agent workspace. Do not test by replacing a user's running installation.
- Adding a new Skill requires an entry in README and its own manifest. Retiring
  one requires a documented replacement/removal path; deleting source files
  does not uninstall previously installed copies or guarantee directory removal.
- Never upload binaries, credentials, private hosts/test data, or unpublished
  product source. Product downloads stay on their official websites.
