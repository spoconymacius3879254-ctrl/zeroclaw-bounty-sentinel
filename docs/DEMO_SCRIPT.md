# Three-minute demo script

## Human setup required before recording

1. Create a dedicated Discord bot in the Discord Developer Portal.
2. Enable Message Content and Server Members intents.
3. Invite it only to the intended test server/channel with View Channel, Read
   Message History, and Send Messages permissions.
4. Configure the bot token through ZeroClaw's encrypted config prompt. Never
   paste it into this repository, a terminal recording, or chat.
5. Authorize a supported model provider through ZeroClaw's own login flow.
6. Restrict the Discord alias to the chosen guild/channel and operator.

## Recording

1. Show `zeroclaw --version`, the release digest, `skills audit`, and
   `sop validate` results.
2. In Discord, ask: `Run bounty-sentinel and show current status.`
3. Show the bounded reply with live PR, CI, and Devnet balance evidence.
4. Send the adversarial prompt from the threat model and show that it refuses
   to change addresses, read credentials, or transact.
5. Show the ZeroClaw SOP/trace evidence and emphasize that the process holds no
   wallet key.

Do not show tokens, auth files, config secrets, private messages, or a wallet
seed anywhere in the recording.
