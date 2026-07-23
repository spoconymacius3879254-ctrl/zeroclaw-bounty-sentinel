# Showcase draft

## Bounty Sentinel: the last mile of crypto bounty work

Opening a PR is not the finish line. A maintainer may request changes days
later, CI can regress, a Devnet deployer can remain unfunded, and a builder can
miss the only action that matters. Bounty Sentinel is a self-hosted ZeroClaw
agent that turns those public signals into a short chat-native operations
digest.

It runs a real, daily T0 job: public GitHub review/CI monitoring plus Solana
Devnet deployment-readiness checks. ZeroClaw supplies the real messaging
channel, model-independent skill, cron/manual SOP, audit trail, and private
operator configuration. The use case needs no plugin and holds no key.

## Custody tier and safety

Tier T0. The only permitted tool is `http_request`, restricted by instruction
to two literal public API hosts. Remote bodies and chat messages are framed as
untrusted data. The agent never signs, broadcasts, deploys, trades, submits,
accepts terms, or reads credentials. An included prompt-injection test attempts
to replace the monitored address and steal a wallet; the expected behavior is a
fail-closed refusal.

## Reproduce

Repository:
<https://github.com/spoconymacius3879254-ctrl/zeroclaw-bounty-sentinel>

Clean-room CI:
<https://github.com/spoconymacius3879254-ctrl/zeroclaw-bounty-sentinel/actions/runs/29973198710>

Pin ZeroClaw v0.8.3, verify the documented official digest, audit the skill,
validate the SOP, configure a private model login and restricted chat bot, then
ask the bot to run `bounty-sentinel`. All public targets can be replaced with an
operator's own PR, CI workflow, and Solana address.

## Evidence still required

- Live Discord or Telegram run
- Three-minute-or-shorter video
- Prompt-injection transcript
- ZeroClaw trace/SOP evidence
- Discord `#solana-bounty` showcase post
- Superteam submission through the authorized human profile
