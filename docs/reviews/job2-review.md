# Review of Job 2 (verifier contract)

The verifier was built by IMD launch job
[`044913fb-4465-4c2c-bfda-2d75d43a9659`](https://explorer.imd.fun/jobs/044913fb-4465-4c2c-bfda-2d75d43a9659),
which targeted Sepolia. Code, tests and five audit nodes (economics, flow, imported code, math,
permissions) were accepted. The launch then **blocked at the deploy manifest**, correctly: the
constructor needs a genesis descriptor and a DKG group key that don't exist yet (Jobs 3–4), and
the verifier is immutable. Nothing was deployed.

The code was taken from the accepted submissions' git bundles:
`adapt_contract_project` (sha256 `fd65171a…`) and `write_foundry_tests` (sha256 `5ae8deff…`),
both matching the hashes IMD published. They apply on top of `main@71252e8`.

## Checked

- `foundry.toml` is unchanged. The only `docs/SPEC.md` edit is a consistency fix in §4.4:
  "250k execution budget" becomes "250k receipt budget", matching R6 and §10.3.
- `src/BeaconVerifier.sol` has no owner, admin, setter, `delegatecall`, payable or token logic.
  The descriptor and group key are immutables. The constructor runs a genesis self-test.
  `M(r)` matches SPEC §4.3. `submit` checks release time, uses an explicit availability bitmap,
  makes a matching duplicate a no-op returning `false` and reverts on a mismatch. The
  `IEpochAuthority` call is `view` (STATICCALL), consulted only for epochs ≥ 1.
- The reported gas is within budget: `verify` 135,374 (≤ 170,000), first `submit` receipt
  230,401 (≤ 250,000). 10,000-run encoding fuzz.
- `test/vectors/vendor/pyblst/…/pyblst.cpython-312-x86_64-linux-gnu.so` is byte-identical to the
  `.so` in the official PyPI wheel `pyblst-0.3.15-cp312-…manylinux…x86_64` (wheel sha256
  `6d9143ed…`, `.so` sha256 `ad947928…`). It is only used by the offline vector generator, not
  by the Solidity tests.

## Not yet done

- **The test suite was not run by this reviewer.** IMD's verifier ran the Foundry profile
  ("all checks passed"). Run `make test` locally before relying on it.
- Line-by-line review of `src/bls/BLS12381.sol` and `src/bls/HashToCurveG1.sol` (encoding
  checks, subgroup handling, gas caps) is still owed. It belongs in the Job 8 external audit
  regardless.

## Notes for later jobs

- **Job 7 (rewards):** the duplicate path in `submit` returns `false` without re-running the
  pairing. That is safe because nothing is paid there, and the README says the escrow pays
  only when `submit` returns `true`. Keep it that way.
- **Job 3** must implement `IEpochAuthority` for the registry and each `EpochMirror`.
- **Job 9:** a real launch needs the frozen genesis descriptor and the DKG group key. Don't
  open a contracts *launch* again until those exist.
