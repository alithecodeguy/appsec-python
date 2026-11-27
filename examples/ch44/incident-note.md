**Incident record: `INC44-SYNTH-001` — executed synthetic rehearsal only.**

**Subject and status.** The chapter 43 held source candidate remains on production HOLD. This is not a production incident, deployment or notification. The source commit is `2c79fe0806a5a788e79afbd0adbc1c4a495a9a5d`; the candidate source ZIP SHA-256 is `ed326bc772909f0dbe064d454488190927593bf18671e6a3c67ac7f017523a5f`.

**Detection.** At the controlled scenario time `2026-11-26T10:16:01Z`, a read-only inventory found an Alpha payload past its `10:16:00Z` removal deadline. Its stored breach flag was still zero. An intentionally unsafe full-backup fixture held two temporary exports, including Beta's otherwise timely deleted live copy.

**Cause and scope.** A synthetic SQL trigger refused Alpha row deletion. The negative-control backup violated the temporary-payload exclusion rule. This demonstrates both a local removal failure and a wider copy-inventory failure; it is not evidence of a real storage outage. The candidate also has no automatic maintenance dispatcher.

**Containment and recovery.** The harness stopped new admission calls and did not dispatch new work while reconciling. The existing release gate remained in force. Removing the synthetic trigger allowed Alpha's live deletion at `10:16:11Z`, with breach history retained. A deliberately stale backup was restored only in quarantine. Current membership/terminal facts were reapplied, restored temporary payloads discarded, and nonce history merged. The unsafe backup was removed at `10:16:16Z`.

**Validation.** Mina was refused after revocation; old exports remained unavailable. Ravi could collect a fresh Beta export, while Alpha/anonymous callers could not cross the intended boundary. Duplicate work left state unchanged. Final live/restored payload-row counts were zero; the known unsafe backup was absent. Nine recovery methods passed on the recorded local runtime.

**Limits and next decision.** Controlled probes do not establish absence of all historical disclosure. Keys stayed in one process; no provider restore, key custody, HTTP, physical erasure or fleet-wide containment was verified. The local rehearsal completed; production HOLD and chapter 43's outstanding gates remain. Proposed operational lead: Owen; recovery: Dana; application: Sam; review: Tess; data-policy decision: Nora. No real assignment or approval is asserted.
