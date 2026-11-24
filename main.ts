// news-image-20261123 entry (Node 22, standard library only): the image is the
// entry.png beside this file, drawn by draw.py from stories.json, and the
// program copies it to /output/entry.png. The gate takes a whole PNG of at
// most 1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes
// copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
const dest = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');
copyFileSync(src, dest);
const size = statSync(dest).size;
if (size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB cap`);
}
