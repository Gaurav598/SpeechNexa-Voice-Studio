# Security alert remediation ledger

Updated: 2026-10-25 (Asia/Kolkata). Repository: `Gaurav598/SpeechNexa-Voice-Studio`, branch `main`.

## Source of truth and scope

The signed-in GitHub code-scanning page showed **619 open, 0 closed** alerts on
`main` before this repair, at `af645c2b822ebe0598143fa904f1f80ef83758b1`.
After the first repair commit `00701ff349618390fdd5ff969f0d2afd21680651`
completed both CodeQL analyses, the browser still showed **619 open, 0 closed**.
Alert #38 was confirmed on that commit; no alert closure is claimed for the
first batch. This ledger includes a follow-up correction whose own CodeQL
rescan must be checked before claiming alert resolution.
The prior recorded distribution was 521 note, 62 warning, 9 medium, 23 high,
and 4 error. This is a baseline, not a verified post-fix count. The first two
pages exposed 50 current alerts, including all 23 high findings, all 9 medium
findings and all 4 error findings. Later pages and alert detail pages did not load reliably in the signed-in
browser. The local `gh` credential is expired, and the connected GitHub tool
rejects the code-scanning API endpoint. The owner chose browser-only access
for this session. A full current export with rule IDs, data-flow paths and
individual dispositions is therefore **not yet available**. No findings have
been dismissed or suppressed to change the counter.

| Requested disposition | Current verified count | Evidence and limit |
| --- | ---: | --- |
| Confirmed vulnerability | 3 code paths | Predictable video slices, batch output cleanup and dub preview/background rendering accepted symlink redirection. Affected high alerts need a new CodeQL scan to determine which close. |
| Likely vulnerability requiring validation | 0 established | Other alert source-to-sink paths still need inspection; absence of a count is not a safe classification. |
| Functional correctness issue | 0 established | Pending remaining alert inventory. |
| Maintainability or quality issue | 3 warning paths | Identical floating point comparison, duplicate regex character and dead sidecar return were repaired. Remaining note/warning inventory is pending. |
| Historical or unreachable code | 0 established | Pending reachability evidence for each group. |
| Duplicate | 0 established | Multiple paths on one line cannot be called duplicates without flow evidence. |
| Evidenced false positive | 0 established | Dynamic `__all__` exports are likely unrecognized by the scanner; #570's full flow and Chromium behavior still need confirmation. No alert was dismissed. |
| Third-party dependency issue | 13 lockfile advisories | Seven Python findings in four packages and six Bun findings in `vite-plus`; these are separate from the CodeQL alert count. |
| Not yet classified | Exact count unavailable | The full occurrence export and most detail pages are unavailable in the browser. This is a work queue, not a disposition. |

These rows mix code paths and alert counts where the scanner's full occurrence
data is unavailable. They must not be added together. Replace them with exact,
mutually exclusive alert counts after an authorized complete export.

## High and medium findings visible on the first page

The 22 Python high alerts #17-38 are titled “Uncontrolled data used in path
expression.” GitHub displayed these sinks: `backend/api/routers/audiobook.py:90`
(#17), `batch.py:985,1058,1059` (#18-20), `dub_export.py:1206-1208` (#21-23),
`backend/services/longform_render.py:697,699` (#24-25),
`backend/api/routers/setup/models.py:421,423,425,428` (#26-29),
`backend/api/routers/tools.py:51` (#30), and
`backend/services/video_retime.py:273,331,343,362,368,373` (#31-38).
The source file names for shortened dashboard paths must be checked against
the individual alert before final disposition.

The JavaScript high alert #570 is “DOM text reinterpreted as HTML” at
`electron/src/renderer/src/features/longform/book-settings.tsx:93`.
Medium #39 is “Information exposure through an exception” at
`backend/api/routers/dub_core.py:2472`; medium #40 is “Binding a socket to all
network interfaces” at `backend/services/network_share.py:193`. The other
seven medium findings are #571 and #576 at `electron/src/main/backend.ts:1003`
(environment-based/indirect command line), #574-575 at
`electron/src/main/repair-mcp-server.ts:68,70` (outbound file data), #573 at
`electron/src/main/repair-agents.ts:875` (network data written to file), and
test-only #572/#577 at `electron/tests/runtime-install-smoke.mjs:20`.
The four error-level findings #163-166 are “Explicit export is not defined”
at `omnivoice/__init__.py:22` (three) and an `omnivoice_gguf/backend.py:927`
path (one). The second page also shows 12 of 62 warning findings, including
unreachable code in dubbing routes, a duplicated regex character, identical
comparison values and superfluous arguments. Their exact rule IDs and the
remaining 50 warnings and 521 notes still need a full inventory.

## Reviewed alert groups and dispositions

| Alert IDs | Review and current disposition |
| --- | --- |
| #17, #24-25 | Audiobook cover paths use an exact generated basename and resolved cover-directory containment. Upload now decodes and re-encodes actual JPEG/PNG bytes before storing. Guarded path; rescan still required. |
| #18-20 | Batch output could be a symlink to another job, and deletion previously removed the uploaded video before checking output containment. Direct-child validation now precedes deletion. Confirmed defect fixed locally; CodeQL closure pending. |
| #21-23 | Dub preview/background exports could follow a symlink into a sibling job. Exact job/export-directory checks now precede probes and writes. Confirmed defect fixed locally; CodeQL closure pending. |
| #26-29 | Active model cache paths derive from known model IDs or validated catalogue IDs; the cache root is operator configuration. No remote traversal shown. Individual CodeQL flows remain unverified. |
| #30 | `/tools/probe` intentionally reads an operator-selected path behind native true-loopback access. No remote file-probe path shown; individual flow still needs review. |
| #31-38 | Predictable `.slices` path allowed a pre-existing symlink to redirect retime writes. Private temporary directory now used under the validated output parent. Alert #38 remained open on the first repair commit: its verified `py/path-injection` flow runs from the `lang` query parameter through `_safe_lang_or_400` and `preview_retimed_*` to `shutil.rmtree(slices_dir)`. A second cross-job scratch-file symlink regression failed before the follow-up guard (HTTP 200) and passed after the resolved scratch path was restricted to the exact job exports directory (HTTP 400). The full 75-test affected dub/smart-fit group passed with 8 skips. CodeQL closure remains unverified pending the follow-up rescan. |
| #39 | Dub streaming generator catches body exceptions and emits a fixed failure code; cleanup outside that catch remains to inspect against the actual CodeQL flow. Unverified. |
| #40 | Wildcard listener is an explicit LAN-share action. Non-loopback API requests require a six-digit PIN and the middleware limits failed guesses to 10 per client per minute. Intentional exposure with mitigation; retain for periodic review. |
| #570 | `img src` receives a browser-created blob URL, not a backend path or filename. HTML bytes disguised as a PNG filename do not create a script element in the renderer test; the backend now rejects those bytes. Likely false positive, pending full CodeQL flow and Chromium image-decoding validation. |
| #571, #576 | Runtime installation uses `spawn(command, args)` without a shell. The executable is a fixed recipe or an explicitly chosen uv path. No string interpolation into a shell was found; further CodeQL flow review pending. |
| #572, #577 | Same command pattern in a test-only runtime smoke. Not a shipped entry point; retain test coverage. |
| #574-575 | Repair bridge previously followed HTTP redirects while carrying its capability header. It now uses manual redirect handling. Confirmed medium-risk behavior fixed locally; CodeQL closure pending. |
| #573 | OpenCode repair prompt contains diagnostics and was written to a shared temp path with default permissions. It now uses exclusive creation and owner-only mode, verified on POSIX. CodeQL closure pending. |
| #163-166 | Dynamic PEP 562 `__getattr__` supplies the named exports. Existing lazy-import and invariant tests exercise them; likely scanner limitation, not a broken runtime import. Do not dismiss until rule details are available. |
| #179, #186, #47 | Duplicate regex character, self-comparison of floating values and unreachable sidecar return were repaired with focused tests. Warning-level closure pending. |

## Locally verified changes; GitHub rescan pending

- The Snap metadata fixture uses the current public title, SpeechNexa. The
  package configuration already emits that title while keeping the internal
  `voicestudio` executable and Snap name. The focused test still rejects an
  old title, weak confinement, missing interfaces, broad removable access and
  enabled privileged browser sandboxing.
- `video_retime.py` now creates a private temporary slice directory under a
  validated parent instead of reusing a predictable `.slices` path. A
  regression test demonstrates that a pre-existing symlink cannot redirect
  writes outside the output directory.
- Batch output cleanup now rejects a symlinked job directory before deleting
  or rendering, and dub preview/background rendering checks the exact job's
  exports directory before probing or writing. Cross-job symlink regressions
  failed before and passed after these changes.
- Audiobook cover upload now decodes and re-encodes bounded JPEG/PNG image
  bytes instead of trusting a filename extension, with invalid-image tests.
- The generated-audio Opus response no longer exposes raw converter errors
  and local paths to an API caller. Preserved-background failures also return
  a fixed public message. Response regression tests cover both.
- Electron IPC checks the calling document before privileged handlers and
  window controls run. Packaged `app://voicestudio` trust is limited to the
  shell document, and dev-origin `/api` proxy paths are denied, so backend HTML
  cannot inherit preload privileges. Focused
  IPC and document-trust regression tests cover the boundary.
- The BookSettings filename test confirms that markup is rendered as literal
  text. Alert #570 points to the separate `img src={preview}` line, so this
  test does not dispose of that alert. A second test confirms the `src` is a
  browser-generated blob URL; its Chromium behavior and CodeQL flow remain under review.
- The repair MCP bridge refuses redirects with its session capability. OpenCode
  repair prompts use exclusive, owner-only file creation in temporary storage.
- A fresh CodeQL flow review of #38 identified a separate retime scratch-file
  symlink into a sibling job's exports directory. The exact-parent guard now
  rejects it before Smart Fit preparation or ffmpeg can run; the first scan
  still reports #38 and the follow-up fix requires a new scan.
- The Microsoft Store handoff now derives its default download repository from
  SpeechNexa metadata; a regression test rejects the prior upstream default.

Local checks completed on the integration tree: the primary Python suite passed
9,857 tests (84 skipped, 2 expected failures, 7 unexpected passes, 20 subtests),
the isolated backend suite passed 516, the focused security/quality group passed
234 with 8 skipped, and 31 focused Electron security tests passed after the
last source edit. The full Electron contract passed with 1,687 renderer tests
(2 skipped), 2,902 shared tests, typechecking, locale coverage, Electron and
web builds, and packaging contracts. Snap verification passed 4 tests with 2
skipped for missing local squashfs-tools; launcher/packaging tests passed 8.
Migration safety and 20 offline tests passed. These are local repairs until
committed, pushed and analyzed by GitHub. A successful CodeQL job alone does
not close an alert.

## Dependency exposure

The default Python lock has seven reported advisories in `accelerate`, `nltk`,
`setuptools` and `torch`. See [the dependency review](SECURITY_REVIEW_2026-10-24.md)
for IDs, fixed-version availability, reachable use and mitigations. A scan of
the local environment may additionally report optional `brotli` and `stanza`
packages; it must not be reported as the default lock's count. Bun reports six
advisories in development-only `vite-plus` 0.3.3. A Vite+ 1.4 upgrade broke the
maintained Vitest suite previously, so a compatible upgrade needs proof before
changing the lockfile. Neither audit is currently clean.

The exact default-lock IDs reproduced in this session are
`PYSEC-2026-3804` (accelerate), `PYSEC-2026-3740` (NLTK),
`PYSEC-2026-3447` twice and `GHSA-xmj3-9gf7-h52w` (setuptools), and
`PYSEC-2026-139` plus `PYSEC-2025-194` (torch). The six Bun IDs are
`GHSA-587h-7wmj-h5pm`, `GHSA-698v-4r3x-3vcv`, `GHSA-r825-w8mm-5pxw`,
`GHSA-rq7h-c2jc-7f22`, `GHSA-vfpm-58rq-9qcg`, and
`GHSA-9jrq-w75r-8gcw`. No lockfile version changed in this batch.

## Next required work

1. Obtain the complete current alert inventory, including rule IDs, severity,
   ref, source/sink flows and exact occurrences. Group by rule and path, then
   assign every one of the 619 initial alerts an evidence-backed disposition.
2. Finish validating reachable high and medium paths, including symlink and
   archive cases; add fail-before/pass-after tests for confirmed defects.
3. Group note and warning alerts by rule/module. Fix real quality defects and
   document evidenced informational or unreachable groups individually.
4. Verify final GitHub workflows and the follow-up CodeQL alert status, then
   record the exact final open count and remaining risks here.
