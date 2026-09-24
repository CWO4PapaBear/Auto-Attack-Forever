# Repository workflow

Publish completed milestones to `main`; fetch and reconcile remote history first. Do not force-push or resume older feature branches. Preserve unrelated local work. Keep proprietary archives, database exports, credentials and test-player data out of Git.

Run relevant controller, packet-hook and Lua options tests. Preserve Lua 5.1 / Interface 30300 compatibility. Source publication, server activation and launcher client releases are separate milestones; document actual verification status.
