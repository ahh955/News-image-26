import { copyFileSync, existsSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const target = "/output/entry.png";

if (!existsSync(source)) {
  throw new Error("entry.png is missing next to main.ts");
}
const bytes = readFileSync(source);
if (bytes.length > 1024 * 1024) {
  throw new Error("entry.png exceeds the 1 MiB limit");
}
if (bytes[0] !== 0x89 || bytes[1] !== 0x50 || bytes[2] !== 0x4e || bytes[3] !== 0x47) {
  throw new Error("entry.png is not a PNG file");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error("entry.png must be 1024x1024");
}
copyFileSync(source, target);
const done = statSync(target);
writeFileSync("/output/entry.json", JSON.stringify({ width, height, bytes: done.size }));
console.log(`wrote /output/entry.png (${done.size} bytes)`);
