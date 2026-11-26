import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// News-image-20261126 entrypoint: copy the prebuilt entry.png into the
// grader's output directory. Deterministic: the same input bytes are
// written on every run, nothing else is read or written. The output path
// is the absolute /output bind mount; the source is this script's own dir.
const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourcePng = join(scriptDir, "entry.png");
const outDir = "/output";
const targetPng = join(outDir, "entry.png");

if (!existsSync(sourcePng)) {
  throw new Error("entry.png not found next to main.ts");
}
mkdirSync(outDir, { recursive: true });
copyFileSync(sourcePng, targetPng);
console.log("copied entry.png to /output/entry.png");
