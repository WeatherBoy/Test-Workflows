import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


async def run(html_path: str, out_pdf: str = "report.pdf"):
    p = await async_playwright().start()
    browser = await p.chromium.launch()
    page = await browser.new_page()
    url = Path(html_path).resolve().as_uri()
    await page.goto(url, wait_until="networkidle")
    # use your print CSS if any
    await page.emulate_media(media="print")
    await page.pdf(
        path=out_pdf,
        format="A4",
        print_background=True,
        margin={"top": "15mm", "right": "15mm", "bottom": "18mm", "left": "15mm"},
    )
    await browser.close()
    await p.stop()


if __name__ == "__main__":
    VERSION = "v2b"
    HTML_PATH = f"data/dashboards/final_report_{VERSION}.html"
    OUT_PDF = f".../report/figures/PDFs/final_report_{VERSION}.pdf"
    asyncio.run(run(HTML_PATH, OUT_PDF))
