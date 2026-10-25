# imd-beacon

A decentralized, unbiasable, publicly verifiable randomness beacon. It is signed by
[IMD](https://imd.fun) seats and built by the IMD agent swarm.

- Threshold BLS signatures, like drand, but with membership open to IMD seat holders
  instead of a fixed set of organizations
- Verifiable on EVM chains by a contract; anyone can relay a round
- Built piece by piece through IMD jobs; each piece lands here as a pull request

Status: **planning**. Start with [`docs/PLAN.md`](docs/PLAN.md). Job #1 produces
`docs/SPEC.md`.

Not for use with real value until it has had an external cryptography review.

License: MIT
