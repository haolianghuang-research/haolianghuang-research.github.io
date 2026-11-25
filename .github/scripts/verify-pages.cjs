const { readFile } = require("node:fs/promises");
const path = require("node:path");
const { setTimeout: delay } = require("node:timers/promises");

const site = "https://haolianghuang-research.github.io";
const root = path.resolve(__dirname, "../..");
const files = {
  home: [["/", "index.html"]],
  proposal: [
    ["/proposal/", "proposal/index.html"],
    ["/proposal/unlock.js", "proposal/unlock.js"],
    ["/proposal/content.bin", "proposal/content.bin"],
  ],
};

async function checkFile([route, filename]) {
  const expected = await readFile(path.join(root, filename));
  let issue;
  for (let attempt = 1; attempt <= 10; attempt++) {
    try {
      const response = await fetch(site + route, {
        cache: "no-cache",
        redirect: "error",
        signal: AbortSignal.timeout(10000),
      });
      if (response.status === 200 && expected.equals(Buffer.from(await response.arrayBuffer()))) {
        console.log(`${route} returned HTTP 200 and matches the deployed revision.`);
        return;
      }
      issue = response.status === 200 ? "served a different revision" : `returned HTTP ${response.status}`;
    } catch {
      issue = "could not be fetched";
    }
    // Allow the Pages CDN time to start serving the new revision.
    if (attempt < 10) await delay(5000);
  }
  throw new Error(`${route} ${issue} after waiting for the Pages deployment.`);
}

async function checkUnlock() {
  const key = process.env.PROPOSAL_LINK_KEY || "";
  if (!/^[A-Za-z0-9_-]{43}$/.test(key)) {
    throw new Error("Set PROPOSAL_LINK_KEY to the key fragment from the proposal share link.");
  }

  const { chromium } = require("playwright");
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    await page.goto(`${site}/proposal/#${key}`, { waitUntil: "domcontentloaded" });
    const proposal = page.frameLocator('iframe[title="CommonRoad Research Proposal"]');
    await proposal.getByRole("heading", { level: 1 }).waitFor({ timeout: 20000 });
    console.log("The proposal share link unlocked and rendered its heading.");
  } catch {
    // Browser errors can include the share URL or text from the decrypted page.
    throw new Error("The proposal did not unlock and render its heading.");
  } finally {
    await browser.close();
  }
}

async function main() {
  const check = process.argv[2];
  if (check === "unlock") {
    await checkUnlock();
    return;
  }
  await Promise.all(files[check].map(checkFile));
}

main().catch(error => {
  console.error(error.message);
  process.exitCode = 1;
});
