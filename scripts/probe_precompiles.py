#!/usr/bin/env python3
"""Read-only probe of the EIP-2537 BLS12-381 precompiles (0x0b-0x11) on each target chain.

Each call uses the point at infinity (all zero bytes), which every precompile must accept,
and checks the exact output length (and value where it is fixed). A missing precompile
returns empty data, which counts as a failure. Writes docs/chain-probes.json.

Usage: python3 -I scripts/probe_precompiles.py [--out docs/chain-probes.json]
"""
import json
import sys
import time
import urllib.request

CHAINS = {
    "ethereum": (1, "https://ethereum-rpc.publicnode.com"),
    "base": (8453, "https://mainnet.base.org"),
    "robinhood": (4663, "https://rpc.mainnet.chain.robinhood.com"),
}

ZERO = lambda n: "00" * n
PROBES = [
    # name, address, input bytes, expected output length, expected output hex or None
    ("G1ADD", "0x000000000000000000000000000000000000000b", ZERO(256), 128, ZERO(128)),
    ("G1MSM", "0x000000000000000000000000000000000000000c", ZERO(128) + "00" * 31 + "01", 128, ZERO(128)),
    ("G2ADD", "0x000000000000000000000000000000000000000d", ZERO(512), 256, ZERO(256)),
    ("G2MSM", "0x000000000000000000000000000000000000000e", ZERO(256) + "00" * 31 + "01", 256, ZERO(256)),
    ("PAIRING_CHECK", "0x000000000000000000000000000000000000000f", ZERO(384), 32, "00" * 31 + "01"),
    ("MAP_FP_TO_G1", "0x0000000000000000000000000000000000000010", ZERO(64), 128, None),
    ("MAP_FP2_TO_G2", "0x0000000000000000000000000000000000000011", ZERO(128), 256, None),
]


def rpc(url, method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=body, headers={"content-type": "application/json", "user-agent": "imd-beacon-probe/1"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def main():
    out = "docs/chain-probes.json"
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    report = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "chains": {}}
    all_ok = True
    for name, (chain_id, url) in CHAINS.items():
        got_id = int(rpc(url, "eth_chainId", [])["result"], 16)
        block = rpc(url, "eth_blockNumber", [])["result"]
        results = []
        for pname, addr, data, length, expected in PROBES:
            r = rpc(url, "eth_call", [{"to": addr, "data": "0x" + data}, block])
            hexout = (r.get("result") or "0x")[2:]
            ok = "error" not in r and len(hexout) == 2 * length and (expected is None or hexout == expected)
            all_ok &= ok
            results.append({"precompile": pname, "address": addr, "ok": ok, "outputBytes": len(hexout) // 2, "error": r.get("error")})
        report["chains"][name] = {"chainId": got_id, "expectedChainId": chain_id, "block": block, "rpc": url, "probes": results}
        print(f"{name:10} chain {got_id} block {int(block, 16)}: " + " ".join(f"{p['precompile']}={'ok' if p['ok'] else 'FAIL'}" for p in results))
    with open(out, "w") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(f"wrote {out}; all ok: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
