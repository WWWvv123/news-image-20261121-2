import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const source = join(repoDir, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR
  ? resolve(process.env.MAKEFUN_OUTPUT_DIR)
  : join(repoDir, "out");

if (!existsSync(source)) {
  throw new Error(`entry.png not found at ${source}; run python3 tools/make_image.py first`);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(source, dest);

const bytes = readFileSync(dest);
if (bytes[0] !== 0x89 || bytes[1] !== 0x50 || bytes[2] !== 0x4e || bytes[3] !== 0x47 ||
    bytes[4] !== 0x0d || bytes[5] !== 0x0a || bytes[6] !== 0x1a || bytes[7] !== 0x0a) {
  throw new Error("output is not a PNG file (bad magic bytes)");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`expected 1024x1024, got ${width}x${height}`);
}
const size = statSync(dest).size;
if (size > 1024 * 1024) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
}
const sha256 = createHash("sha256").update(bytes).digest("hex");
console.log(`entry.png: ${size} bytes, sha256 ${sha256}`);
console.log(`copied to ${dest}`);
