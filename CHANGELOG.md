# 2019-08-30 - BitBot v1.11.1

Added:
- `utils.IntRangeSetting`
- `realname` was missing from `!editserver`

Changed:
- Added `"- "` to start of formatted kick lines
- Use `"+0000"` instead of `"Z"` for UTC timezone

Fixed:
- Put a deadline on sed matches to prevent DoS
- Duplicate `def op` in `channel_op.py` (due to copypaste)
- `git-prevent-highlight` was failing to unhighlight organisations

# 2019-08-15 - BitBot v1.11.0

Added:
- `rss.py`
- Show `weather.py` windspeed in MPh too
- `git_webhooks/gitea.py`
- `acronym.py`
- `!editserver` in `admin.py`
- `channel_keys.py` to centrally track/use channel keys
- `!mute` and `!unmute` in `channel_op.py`
- `command_suggestions.py`
- appendable command prefixes
- `@utils.kwarg`
- `fediverse.py`
- gitea webhooks (`git_webhooks/gitea.py`)
- Show available `!hash` algorithms
- per-channel-per-user ignores (`ignore.py`, `!cignore`)
- `ircv3.py` - to show ircv3 support stats
- `isup.py`
- `kick_rejoin.py`
- Handle `ERR_UNAVAILRESOURCE`
- `onionoo.py` (thanks @irl)
- `ops.py` to highlight ops (opt-in)
- Per-channel `perform.py` (`!cperform`)
- `proxy.py`
- Configurable URL shorteners (`shorturl.py`)
- `!unshorten` (`shorturl.py`)
- `slowvoice.py`
- `throttle.py`
- `!timezone` (`user_time.py`)
- Show `!weather` target nickname in command prefix
- Parse youtube playlists (`youtube.py`)
- `utils.http.url_sanitise()`
- `utils.http.request_many()`
- `./start.py --startup-disconnects`
- `./start.py --remove-server <alias>`
- `!remindme` as an alias of `!in` (`in.py`)
- `!source` and `!version` (`info.py`)
- Show TTL for DNS records (`ip_addresses.py`)
- `!addpoint`/`!rmpoint` as more explicit `++`/`--` for karma (`karma.py`)

Changed:
- Move `_check()` call to event loop func
- Split out github webhook functionality to `git_webhooks/github.py`
- Refactored @utils.export settings to be object-oriented
- Warn when channel-only/private-only is not met
- `8ball.py` -> `eightball.py` (can't import things that start with a digit)
- `github.py` -> `git_webhooks`
- revamp `!dns` to take optional nameserver and record typ
- `!quotedel` without quote removes most recent
- Relays moved to relay "groups" that channels can "join" and "leave"
- Rewrote `EventManager` for efficiency and simplicity
- Moved timers/cache/etc from read loop to event loop
- Better and more exhaustive channel move tracking
- Don't silently truncate `ParsedLine` at newline
- `@utils.hook`/`@utils.export` now use a single object that handles parsing
- `!ban`/`!kickban`/`!mute` duration syntax changed (`channel_op.py`)
- Highlight spam protection logic moved to own module (`highlight_spam.py`)
- `IRCBuffer.find()` returns the matched string
- Positive and negative karma throttled seperately (`karma.py`)
- REST API now listens in IPv6 (`rest_api.py`)

Fixed:
- Catch and rethrow not-found definitions in `define.py`
- `ircv3_botignore.py` event priority
- `CAP DEL` crash when `DEL`ing something that was not advertised
- `ParsedLine.format()` didn't prefix `source` with `":"`
- `_write_buffer` locking to avoid race condition
- `Capability().copy().depends_on` was mutable to the original copy

# 2019-06-23 - BitBot v1.10.0

Added:
- Outbound message filtering (`message_filter.py`)
- Mid-callback command permission checks ('event["check_assert"](utils.Check(...))')
- `connected-since` on stats endpoint
- IRCv3: draft/event-playback
- `auto-github-cooldown` to prevent duplicate `auto-github`s in quick succession
- `vote.py`
- IRCv3: `ircv3_botignore.py` to ignore users with `inspircd.org/bot`
- Catch and humanify `!loadmodule` "not found" exception
- cross-channel/network relay (`relay.py`)
- Option to allow anyone to `!startvote`
- IRCv3: CAP dependency system
- IRCv3: labeled-response + echo-message to correlate echos to sends
- `deferred_read.py`

Changed:
- Only strip 2 characters (`++` or `--`) from the end of karma
- Track CHANMODE type B, C and D (not just type D)
- 'x saved a duck' -> 'x befriended a duck'
- IRCv3: CAP REQ streamline for modules
- IRCv3: SASL failure defaults to being "hard" (disconnect/crash)
- `auto-title`, `auto-youtube`, `auto-imgur` etc now work in `/me`
- Move truncation logic from `SentLine` to `ParsedLine`
- Move `!help` logic to it's own file and rework it to be more user friendly
- Get `"city, state, country"` from geocoding in `location.py`, use in `weather.py`
- Convert IRC glob to regex, instead of using fnmatch
- `EventManager` calls can only come from the main thread
- IRCv3: `labeled-response` now depends on `batch`
- `format_activity.py` now only shows highest channel access symbol

Fixed:
- `KeyError` when sts `port` key not present
- lxml wasn't in requirements.txt but it should have been
- Any CRITICAL in read/write thread now kills the main thread too
- `Database.ChannelSettings.find` invalid SQL
- `birthday.py`'s year no longer .lstrip("0")ed
- IRCv3: pay attention to our own msgids (`ircv3_msgid.py`)
- catch and WARN when trying to remove a self-mode we didn't know we had
- `until_read_timeout` -> `until_read_timeout()`
- `PROTOCTL NAMESX` should have been send_raw() not send()
- IRCv3: handle `CAP ACK -<cap>`
- IRCv3: handle `CAP ACK` in response to `CAP REQ` that came from outside `ircv3.py`

Removed:
- `!set`/`!channelset`/`!serverset`/`!botset` (replaced with `!config`)
- `bytes-read-per-second` and `bytes-written-per-second` from stats endpoint
- `upc.py`

# 2019-06-09 - BitBot v1.9.2

Added:
- Show seconds it took to !bef/!trap

Changed:
- IRCv3: `draft/resume-0.4` -> `draft/resume-0.5`

Fixed:
- Fix scenario in which some-but-not-all threads die
- Daemonify tweet thread
- Don't add TAGMSGs to IRCBuffer objects

# 2019-06-08 - BitBot v1.9.1

Fixed:
- Fix ERROR on `CAP NEW` caused by STS typo
- Fix hanging on `CAP NEW` due to duplicate `REQ`
- STATUSMSG stripping should only be STATUSMSG symbols, not all PREFIX symbols

# 2019-06-07 - BitBot v1.9.0

Added:
- IRCv3: Also look at CTCP events for msgids
- Sub-event system within all SentLines
- Show last action in `!seen` (e.g. 'seen 1m ago (<jesopo> hi)')
- WARN when labels are not responded to in a timely fashion
- IRCv3: send `+draft/typing` while processing commands
- Display github `ready_for_review` better
- Parse 221 (RPL_UMODEIS) numerics

Changed:
- `!np` against a known nickname will attempt to resolve to lastfm username
- `PING` and `PONG` now avoid write throttling
- `!bang` -> `!trap`, 'shot' -> 'trapped' for ducks
- Socket reads and socket writes have been moved on to seperate threads
- Use Deques for chat history (more performant!)

Fixed:
- Differentiate between send and received CTCP events
- `IRCSocket._send` will now only return lines that definitely hit the wire
- GitHub `commit_comment` event formatting exception
- Strip xref tags from `!define` output
- `check_purge()` after removing contextual hooks from an EventHook
- IRCv3: Escape message tag values

# 2019-06-03 - BitBot v1.8.0

Added:
- Module dependency system
- Enable TCP keepalives
- IRCv3: `draft/label` tracking on every sent line when CAPs permit
- Enforce Python version 3.6.0 or later
- 'module-whitelist'/'module-blacklist' in `bot.conf`

Changed:
- IRCv3: Use last `server-time` for `RESUME` - not last .recv() time
- IRCv3: `draft/labeled-response` -> `draft/labeled-response-0.2`
- IRCv3: Prune already-seen messages in `chathistory` batches
- Consolidate `PRIVMSG`, `NOTICE` and `TAGMSG` handlers in to one

Fixed
- GitHub highlight prevention - don't detect highlights mid-word
- Pass already-decoded data in to BeautifulSoup
- !enablemodule actually removes module from blacklist setting
- Only enact write throttling when immediate-write-buffer is empty
- Non-throttled lines no longer delay throttled lines

# 2019-05-24 - BitBot v1.7.1

Fixed:
- Fix crash caused by CAP NEW

# 2019-05-23 - BitBot v1.7.0

Added:
- Add !addserver
- Add !masterpassword
- Add auto-tweet setting
- Support triggering commands by regex

Changed:
- Show usage examples for user/channel/server/bot settings
- Strip common command prefixes from PM commands so "!help" works
- Change auto-github to work for github urls too
- IRCv3: draft/resume-0.3 -> draft/resume-0.4
- Remove `ipv4` server attribute - figure it out automatically

Fixed:
- Typos/bugs in BATCH and FAIL
- Fix crash caused by BitBot messaging himself
