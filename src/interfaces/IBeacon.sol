// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

/// @title IBeacon: read and publish imd-beacon rounds
/// @notice Draft from docs/SPEC.md §8.2. The spec leaves the exact ABI to the verifier job
///         (Job 2), which may refine this file. Encodings and semantics are fixed by SPEC §4.3.
interface IBeacon {
    /// @notice Emitted once per round, when its group signature is first verified and stored.
    event RoundVerified(bytes32 indexed networkId, uint64 indexed epoch, uint64 indexed round, bytes32 value, bytes signature);

    /// @notice Verify a round's 96-byte affine G1 group signature and return its randomness R(r).
    ///         Pure check, no side effects.
    function verify(uint64 round, bytes calldata affineG1Signature) external view returns (bytes32);

    /// @notice Verify and store a round. Anyone may call once block.timestamp >= T(round).
    ///         A matching duplicate is a no-op; a mismatching one reverts.
    function submit(uint64 round, bytes calldata affineG1Signature) external;

    /// @notice Stored round value. `available` is explicit because R may legitimately be zero.
    function get(uint64 round) external view returns (bool available, bytes32 value);
}
