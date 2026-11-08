import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const browser = await chromium.launch({ channel: process.env.PLAYWRIGHT_CHANNEL || 'msedge', headless: true });
const page = await browser.newPage({ viewport: { width: 1100, height: 760 } });
try {
  const base = process.env.VOICESTUDIO_UI_URL || 'http://localhost:3912';
  const repository = 'https://github.com/Gaurav598/SpeechNexa-Voice-Studio';
  await page.addInitScript(() => {
    localStorage.setItem('voicestudio.setup.complete.v1', '1');
  });
  await page.goto(base + '/#/settings/appearance');
  await page.getByRole('link', { name: 'Ways to get in touch', exact: true }).click();
  await page
    .getByRole('heading', { level: 1, name: 'Ways to get in touch', exact: true })
    .waitFor();
  assert.equal(
    await page.getByRole('link', { name: 'Open GitHub Issues', exact: true }).getAttribute('href'),
    `${repository}/issues`,
  );
  assert.equal(
    await page.getByRole('link', { name: 'Star on GitHub', exact: true }).getAttribute('href'),
    repository,
  );
  assert.equal(
    await page.getByRole('link', { name: 'Report privately', exact: true }).getAttribute('href'),
    `${repository}/security/advisories/new`,
  );
  console.log(
    'Support navigation, issue/repository links and private security destination passed; no external page opened.',
  );
} finally {
  await browser.close();
}
