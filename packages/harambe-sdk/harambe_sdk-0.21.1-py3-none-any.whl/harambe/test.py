import asyncio
from typing import Any

from playwright.async_api import Page

from harambe import SDK
from harambe.contrib import playwright_harness


async def scrape(sdk: SDK, current_url: str, *args: Any, **kwargs: Any) -> None:
    page: Page = sdk.page
    await page.wait_for_selector("div.rt-table")
    data = await page.evaluate("window.__data")
    items = data["searchProjects"]["searchResults"]
    for item in items:
        code = item["government"]["code"]
        institution = item["government"]["organization"]["name"]
        country_code = item["government"]["organization"]["countryCode"]
        state_code = item["government"]["organization"]["state"]
        region = f"{country_code}-{state_code}"

        options = {}
        options["institution"] = institution
        options["region"] = region
        options["disable_stealth_async"] = True

        item_id = item["id"]
        url = f"https://procurement.opengov.com/portal/{code}/projects/{item_id}"
        await sdk.enqueue(url, options=options)


if __name__ == "__main__":
    asyncio.run(
        SDK.run(
            scrape,
            "https://kaliiiiiiiiii.github.io/brotector/",
            schema={},
            headless=False,
            harness=playwright_harness,
        )
    )
    # asyncio.run(SDK.run(scrape, "https://nowsecure.nl/#relax", schema={}, headless=False, harness=playwright_harness))
