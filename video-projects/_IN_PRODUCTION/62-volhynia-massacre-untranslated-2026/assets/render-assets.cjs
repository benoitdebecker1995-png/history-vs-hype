const fs = require('fs');
const path = require('path');
const sharp = require('C:/Users/benoi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');

async function main() {
  const dir = __dirname;
  const svgs = fs.readdirSync(dir).filter((name) => /^\d{2}-.+\.svg$/i.test(name));
  for (const name of svgs) {
    const input = path.join(dir, name);
    const output = path.join(dir, name.replace(/\.svg$/i, '.png'));
    await sharp(input, { density: 144 }).png({ compressionLevel: 9 }).toFile(output);
    const meta = await sharp(output).metadata();
    process.stdout.write(`${path.basename(output)}\t${meta.width}x${meta.height}\n`);
  }
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
