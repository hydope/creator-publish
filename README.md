# creator-publish

Official-API publishing and scheduling for creator tools. No scraping, no unofficial endpoints — uploads only, through each platform's blessed API. Every adapter supports `dry_run` for safe testing.

Extracted from [ShortSmash](https://github.com/hydope/shortsmash) (2026-10-19) into a shared package so every creator tool benefits from the same fixes.

## Platforms

YouTube (Shorts included), TikTok, Instagram Reels, X, Threads, Bluesky, LinkedIn, Pinterest, Facebook profile + Page.

## Install

```bash
pip install creator-publish
pip install "creator-publish[youtube]"   # for YouTube uploads (google client libs)
```

## Use

```python
from pathlib import Path
from creator_publish.publish import publish
from creator_publish import schedule

# post now (dry_run=True to test without posting)
result = publish("youtube", Path("clip.mp4"), title="POV: ...",
                 description="...", hashtags=["#pov"],
                 dry_run=True)

# or schedule it in plain English
job = schedule.schedule_video(Path("clip.mp4"), when="Friday 6pm",
                              platforms=["youtube", "tiktok"],
                              title="POV: ...")
```

`schedule.worker()` runs the durable SQLite queue (APScheduler, survives restarts, 3 retries with backoff).

## Config

Secrets live in the environment (never written to disk by us):

| Platform | Needs |
|---|---|
| youtube | `~/.creator-publish/youtube_client.json` (OAuth client) — token cached after first browser grant |
| tiktok | `TIKTOK_ACCESS_TOKEN` |
| instagram | `IG_ACCESS_TOKEN`, `IG_USER_ID` (+ public `video_url` — Meta fetches server-side) |
| x | `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET` |
| threads | `THREADS_USER_ID`, `THREADS_ACCESS_TOKEN` |
| bluesky | `BSKY_HANDLE`, `BSKY_APP_PASSWORD` |
| linkedin | `LINKEDIN_ACCESS_TOKEN` |
| pinterest | `PINTEREST_ACCESS_TOKEN`, `PINTEREST_BOARD_ID` |
| facebook | `FB_ACCESS_TOKEN` / `FB_PAGE_ID` + `FB_PAGE_ACCESS_TOKEN` |

Set `CREATOR_PUBLISH_HOME` to share a home dir with another tool (ShortSmash sets it to `~/.shortsmash` so existing tokens keep working).

## License

MIT.
