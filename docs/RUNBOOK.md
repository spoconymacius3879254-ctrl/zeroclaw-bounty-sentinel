# Live ZeroClaw runbook

This runbook is pinned to the tested ZeroClaw v0.8.3 binary. It creates a
private, supervised configuration for a single restricted Discord channel.
The resulting agent exposes only `http_request`; it has no wallet, shell, or
submission authority.

Run every command from the repository root. Keep `.zeroclaw-demo/` private; it
is ignored by Git.

## 1. Create the private configuration

```sh
export BOUNTY_CONFIG="$PWD/.zeroclaw-demo"
mkdir -p "$BOUNTY_CONFIG"
cp config.example.toml "$BOUNTY_CONFIG/config.toml"
cp -a sops "$BOUNTY_CONFIG/sops"

./tools/zeroclaw agents create bounty_sentinel --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw skills bundle add bounty_sentinel --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw skills install ./skills/bounty-sentinel \
  --bundle bounty_sentinel --config-dir "$BOUNTY_CONFIG"
```

ZeroClaw v0.8.3 accepts underscores for these aliases. Do not use the hyphen
shown by one older help string.

## 2. Configure model access without copying credentials

Create an OpenAI provider entry backed by ZeroClaw's encrypted subscription
auth store:

```sh
./tools/zeroclaw providers create models openai codex \
  --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw config set providers.models.openai.codex.model gpt-5.4 \
  --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw config set providers.models.openai.codex.wire_api responses \
  --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw config set \
  providers.models.openai.codex.requires_openai_auth true \
  --config-dir "$BOUNTY_CONFIG"
```

Then choose exactly one human-authorized login path:

```sh
# Preferred: ZeroClaw opens its own device-code flow.
./tools/zeroclaw auth login --model-provider openai-codex --device-code \
  --config-dir "$BOUNTY_CONFIG"

# Alternative only if you explicitly approve sharing an existing Codex login:
# ./tools/zeroclaw auth login --model-provider openai-codex \
#   --import /absolute/path/to/auth.json --config-dir "$BOUNTY_CONFIG"
```

Never paste a token into this repository, chat, a command argument, or a
recording. Confirm only the profile metadata:

```sh
./tools/zeroclaw auth status --config-dir "$BOUNTY_CONFIG"
```

If `gpt-5.4` is unavailable to the authorized account, replace only the model
value with a model returned by the account's supported catalog.

## 3. Add one restricted Discord channel

In the Discord Developer Portal, create a dedicated bot, enable Message
Content and Server Members intents, and invite it only to the test server with
View Channel, Read Message History, and Send Messages permissions. Copy the
numeric server and channel IDs, not their names.

```sh
./tools/zeroclaw channels create discord bounty_demo \
  --config-dir "$BOUNTY_CONFIG"

# This intentionally has no value argument. ZeroClaw prompts with masked input
# and writes an encrypted value.
./tools/zeroclaw config set channels.discord.bounty_demo.bot_token \
  --config-dir "$BOUNTY_CONFIG"

./tools/zeroclaw config set channels.discord.bounty_demo.guild_ids \
  '["DISCORD_GUILD_ID"]' --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw config set channels.discord.bounty_demo.channel_ids \
  '["DISCORD_CHANNEL_ID"]' --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw config set channels.discord.bounty_demo.mention_only true \
  --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw config set channels.discord.bounty_demo.enabled true \
  --config-dir "$BOUNTY_CONFIG"
```

Replace the two uppercase placeholders before running their commands. Empty
guild or channel arrays broaden access and are not acceptable for this demo.

## 4. Apply the T0 security boundary

```sh
./tools/zeroclaw config set risk_profiles.bounty_sentinel.allowed_tools \
  '["http_request"]' --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw config set runtime_profiles.bounty_sentinel.max_tool_iterations 8 \
  --config-dir "$BOUNTY_CONFIG"

./tools/zeroclaw config set agents.bounty_sentinel.model_provider openai.codex \
  --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw config set agents.bounty_sentinel.risk_profile bounty_sentinel \
  --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw config set agents.bounty_sentinel.runtime_profile bounty_sentinel \
  --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw config set agents.bounty_sentinel.skill_bundles \
  '["bounty_sentinel"]' --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw config set agents.bounty_sentinel.channels \
  '["discord.bounty_demo"]' --config-dir "$BOUNTY_CONFIG"
```

## 5. Prove the configuration before going live

All commands below must succeed. Inspect the security output and confirm the
agent is `Supervised`, the risk profile is `bounty_sentinel`, and the only
allowed tool in the saved profile is `http_request`.

```sh
./tools/zeroclaw --version
sha256sum ./tools/zeroclaw
./tools/zeroclaw skills audit ./skills/bounty-sentinel
./tools/zeroclaw sop validate --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw sop graph bounty-digest --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw security status --agent bounty_sentinel \
  --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw channel doctor --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw status --config-dir "$BOUNTY_CONFIG"
```

The release archive digest is documented in `RELEASE_PIN.md`; the extracted
binary digest can differ from the archive digest.

## 6. Smoke test, record, then run continuously

First test through the CLI without starting a background service:

```sh
./tools/zeroclaw agent --agent bounty_sentinel \
  --message 'Run bounty-sentinel and show current status.' \
  --config-dir "$BOUNTY_CONFIG"
```

Then start the daemon in the foreground and test the restricted Discord
channel using the same prompt and the adversarial prompt in
`docs/THREAT_MODEL.md`:

```sh
./tools/zeroclaw daemon --host 127.0.0.1 --config-dir "$BOUNTY_CONFIG"
```

Record the flow in `docs/DEMO_SCRIPT.md`. Stop the foreground daemon with
Ctrl-C after evidence capture. Only after the live test succeeds should the
operator install the user service:

```sh
./tools/zeroclaw service install --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw service start --config-dir "$BOUNTY_CONFIG"
./tools/zeroclaw service status --config-dir "$BOUNTY_CONFIG"
```

Do not use `--allow-degraded-security`. If any check fails, leave the service
stopped and repair the configuration first.
