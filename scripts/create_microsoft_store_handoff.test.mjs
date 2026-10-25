import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { createMicrosoftStoreHandoff } from "./create_microsoft_store_handoff.mjs";

test("defaults Store handoff download links to the SpeechNexa repository", () => {
  const directory = mkdtempSync(join(tmpdir(), "speechnexa-store-handoff-"));
  try {
    const version = "0.5.7";
    const file = `VoiceStudio-MicrosoftStore-${version}-win-x64.exe`;
    const updateManifest = "electron-microsoft-store-stable-win32-x64.yml";
    const bytes = Buffer.from("signed test installer");
    const updateBytes = Buffer.from("update metadata");
    writeFileSync(join(directory, file), bytes);
    writeFileSync(join(directory, updateManifest), updateBytes);
    writeFileSync(join(directory, "authenticode-win32-x64.json"), "{}");
    const sha256 = (value) => createHash("sha256").update(value).digest("hex");
    writeFileSync(join(directory, "store-artifact-manifest-win32-x64.json"), JSON.stringify({
      distribution: { target: "microsoft-store", applicationUpdates: "application" },
      signingVerification: { status: "valid", evidence: "authenticode-win32-x64.json" },
      artifacts: [
        { file, bytes: bytes.length, sha256: sha256(bytes) },
        { file: updateManifest, sha256: sha256(updateBytes) },
      ],
    }));

    const handoff = createMicrosoftStoreHandoff({
      releaseDir: directory,
      output: join(directory, "handoff.json"),
      version,
      tag: `v${version}`,
    });
    assert.equal(
      handoff.packages[0].url,
      `https://github.com/Gaurav598/SpeechNexa-Voice-Studio/releases/download/v${version}/${file}`,
    );
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});
