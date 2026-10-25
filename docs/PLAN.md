# IMD Beacon: plan

A decentralized, unbiasable, publicly verifiable randomness beacon. The signers are
IMD seats (identity.md NFT holders running IMD workers), and the code is built piece by
piece by the IMD agent swarm through ordinary IMD jobs.

This document is the brief every job starts from. Job #1 replaces the "Draft design"
section with a cited specification (`docs/SPEC.md`). Later jobs implement it one
piece at a time.

## Why

| Option | Trust model | Gap this project targets |
|---|---|---|
| Pyth Entropy | Two-party commit-reveal with one provider | One provider can withhold reveals; one operator |
| drand / League of Entropy | Threshold BLS, fixed member set | Membership is permissioned |
| Chainlink VRF | One oracle node per request, VRF proof | Single node can withhold; paid in LINK |
| RANDAO / `prevrandao` | Block proposers | Last proposer can bias by withholding a block |

Goal: drand-grade cryptography (threshold BLS, unbiasable while fewer than *t* signers
collude), with membership open to anyone holding an IMD seat instead of a fixed league.

## Draft design (to be replaced by the spec)

- **Members.** IMD seats: holders of the identity.md NFT
  (`0x0000ec93127baa929e58e97dd0095a2bfb38ec1d`, Ethereum) that are registered ERC-8004
  agents. A member registers a beacon signing key with a proof of possession.
- **Committee.** Each epoch, a committee of *N* members is sampled using the beacon's
  own previous output, with threshold *t* (draft: *N* = 64, *t* = 43).
- **Key setup.** Distributed key generation (Pedersen / joint-Feldman with complaints)
  per epoch, then resharing to the next committee, so the group key can stay stable
  across epochs and no single party ever holds the group secret.
- **Rounds.** Fixed period. Each member signs the round number; any *t* partial
  signatures aggregate into one group signature, and its hash is the round's randomness
  (drand "unchained" style).
- **On-chain.** A verifier contract checks the group signature with precompiles. Anyone
  may relay a round; relayers earn a fee.
- **Consumers.** Commit to a future round number before it is produced, then read the
  verified value. Neither the consumer nor any relayer can choose the outcome.
- **Curve: open question for the spec.** BN254 (precompiles on every EVM chain, the
  curve drand's `evmnet` uses) or BLS12-381 (EIP-2537). Must confirm support on each
  target chain.

Target chains: Ethereum, Base, Robinhood Chain (4663), testnets first.

## Non-goals

- Changing the IMD worker or IMD control plane. The beacon node runs beside the worker.
  If it proves out, the IMD developers can choose to adopt it.
- Inventing new cryptography. Use audited libraries (drand/kyber, blst, gnark-crypto) and
  published protocols.
- Mainnet use with real value before an external human cryptography review.

## Roadmap: one IMD job per piece

Each piece is opened with `job.open` or continued with `job.continue` against this
repository and lands as a pull request. Acceptance criteria are refined in `docs/SPEC.md`.

| # | Piece | Output |
|---|---|---|
| 1 | Specification and threat model | `docs/SPEC.md`: cited design, parameters, per-piece acceptance criteria |
| 2 | Verifier contract | `contracts/BeaconVerifier.sol`, consumer interface, Foundry + fuzz tests, gas report |
| 3 | Committee registry | `contracts/CommitteeRegistry.sol`: seat-gated key registration, epochs, group key |
| 4 | DKG | `node/dkg`: key generation with complaints, simulated 16–64 node tests |
| 5 | Rounds and relay | `node/`: partial signing, aggregation, gossip, relayer; local devnet |
| 6 | Resharing and sampling | Epoch handover, committee sampling from beacon output |
| 7 | Incentives | Relayer fees and signer rewards in IMD; abuse cases |
| 8 | Audit | Audit-panel report plus fixes |
| 9 | Testnet | Deploy scripts, testnet deployment, a demo raffle/dice consumer |

## Security notes

- Unbiasability and unpredictability hold while fewer than *t* committee members collude;
  the spec must quantify that against seat concentration (one operator holding many seats).
- Liveness fails if more than *N* − *t* members are offline; the spec defines recovery.
- Seat transfers mid-epoch, key compromise, relayer censorship and chain reorgs must
  each have a defined behaviour.
