# Bounty Sentinel for ZeroClaw

Bounty Sentinel is a custody-free ZeroClaw use case for builders who earn from
public crypto bounties. It watches the state that matters after the code is
written: maintainer review, clean-room CI, and the public Solana balance needed
for a Devnet deployment. It reports evidence and the next human action through
a real chat channel without holding a wallet key or submitting transactions.

This is a Tier T0 (read-only) design for the Superteam Brasil ZeroClaw Solana
bounty. It uses the stock ZeroClaw release, a narrow skill, and a manual/cron
SOP. There is no plugin and no private-key custody.

## Current public targets

- Memanto PR: <https://github.com/moorcheh-ai/memanto/pull/1615>
- Coalition Passport CI: <https://github.com/spoconymacius3879254-ctrl/coalition-passport/actions>
- Coalition Passport Devnet deployer:
  `Edk1vBTRxCeqxYmytWJcBYCxBxHsh4jXFNrVChdyLxc`

All three are already public. Operators can replace them in the skill with
their own public targets.

## Safety boundary

The agent may call `http_request` only against `api.github.com` and
`api.devnet.solana.com`. It must not use a shell, read local credentials, sign,
submit, deploy, transfer, trade, apply to a bounty, or accept terms. API bodies
are untrusted data and never instructions. See [the threat model](docs/THREAT_MODEL.md).

## Reproduce

The tested reference binary is ZeroClaw v0.8.3 for x86-64 GNU/Linux. Verify the
official archive before extracting it:

```sh
curl -fLO https://github.com/zeroclaw-labs/zeroclaw/releases/download/v0.8.3/zeroclaw-x86_64-unknown-linux-gnu.tar.gz
printf '%s  %s\n' \
  '662abfa20afc5790538e69aebc1be60e188d34ba64f96fd81505bbcdd8edce44' \
  'zeroclaw-x86_64-unknown-linux-gnu.tar.gz' | sha256sum --check
```

Audit the skill and validate the SOP from this repository root:

```sh
zeroclaw skills audit ./skills/bounty-sentinel
mkdir -p demo-config
cp config.example.toml demo-config/config.toml
zeroclaw sop validate --config-dir demo-config
python3 -m unittest -v tests.test_contract
```

For a real run, use `zeroclaw quickstart` to create a private configuration,
install the skill into a bundle loaded by the chosen agent, enable the SOP with
this repository's `sops` directory, and configure one allowlisted Discord or
Telegram bot. Do not put provider or bot credentials in this repository.

The exact human-only setup and recording flow is in [the demo script](docs/DEMO_SCRIPT.md).

## What this demonstrates

- A crypto-income pipeline does not end when a PR is opened: review and payout
  prerequisites can change days later.
- Solana's public JSON-RPC makes deployment readiness independently verifiable
  without wallet custody.
- ZeroClaw's chat channels, skills, cron SOPs, and self-hosted state turn those
  signals into a daily operational loop.
- The safest agent is allowed to observe and recommend; humans retain identity,
  acceptance, signing, and financial authority.
