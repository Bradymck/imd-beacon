# Review of SPEC.md v1 (IMD job f6c0de54)

The spec was delivered by IMD job
[`f6c0de54-0dab-4c48-bcae-c689bb740fb4`](https://explorer.imd.fun/jobs/f6c0de54-0dab-4c48-bcae-c689bb740fb4)
and published at `Identity-md/research@31528ba` as `artifacts/report.md`. `docs/SPEC.md` is a
byte-identical copy (sha256 prefix `be606585ecb765a7`). This file records what was checked
before adopting it, so later jobs can rely on it.

## Verified

- **Committee risk table (§5.1).** Recomputed with exact rational binomial sums. Every listed
  value matches, including the 365-day union bound of about 16.26% at 40%.
  `scripts/committee_risk.py` reproduces the table and adds the exact hypergeometric case
  for a real registry snapshot.
- **BLS12-381 precompiles (§4.1, §4.2).** `scripts/probe_precompiles.py` makes read-only
  calls to all seven EIP-2537 addresses (0x0b–0x11) on Ethereum (1), Base (8453) and Robinhood
  Chain (4663). All seven answered with correctly sized output on all three chains. The
  evidence is in `docs/chain-probes.json`. The probes use the point at infinity only. Job 2's
  deployment smoke tests must still add the positive, malformed and non-subgroup vectors
  the spec requires.
- **Structure.** All 11 required sections are present, with 63 unique primary-source links
  (EIPs, drand docs, IETF RFC/draft, IACR ePrint, chain docs). No embedded instructions were
  found.

## Gaps in the delivery

- The spec references `scripts/committee_risk.py`, `scripts/probe_precompiles.py` and
  `docs/chain-probes.json` as delivered. Only `report.md` was published. This PR adds
  independently written versions of all three. Their names match the spec's links.

## Concerns to resolve before or during later jobs

1. **Ceremony cost on Ethereum.** Daily epochs, with DKG and resharing packets kept on an
   Ethereum L1 `DkgBoard` (chunks of 16 KiB or less), could put megabytes of calldata on L1
   every day at N = 256. Job 4 must measure total board bytes and gas per epoch before
   N = 256 is assumed. If the cost is material, amend the spec: longer epochs (for example
   weekly), blobs, or a board on Base with Ethereum-anchored roots.
2. **Seat supply.** N = 256 / t = 129 needs at least 256 eligible seats running beacon nodes.
   Testnet work should use the spec's no-value 64/33 pilot profile until participation is
   real.
3. **Scope growth.** The spec adds historical-state ownership proofs
   (`SnapshotVerifier.sol`), bridge-authenticated epoch mirrors and an on-chain ceremony
   board. These are justified by the threat model but make Job 3 large. Split it if one
   job cannot meet its acceptance list.
4. **External human cryptography review** remains mandatory before any value-bearing use
   (spec §10.3 Job 8, PLAN.md non-goals).

## Decision

Adopt `docs/SPEC.md` v1 as the implementation contract. Next is Job 2, the verifier
contract (§10.3), which depends on no other piece.
