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
// PNG trailer: a complete file ends with the 12-byte IEND chunk.
// A truncated copy passes the signature/dimension checks above but is
// not a renderable image, so refuse it here instead of shipping it.
const IEND = [0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82];
const tail = bytes.subarray(bytes.length - 12);
if (!IEND.every((b, i) => tail[i] === b)) {
  throw new Error("entry.png is truncated (missing IEND)");
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
