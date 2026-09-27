"""Playwright automated browser verification script for desktop & mobile."""

from __future__ import annotations

import sys
from playwright.sync_api import sync_playwright


def run_browser_verification() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ---------------------------------------------------------
        # 1. Desktop Verification (1280x960)
        # ---------------------------------------------------------
        context = browser.new_context(viewport={"width": 1280, "height": 960})
        page = context.new_page()

        console_errors: list[str] = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        print("1. [Desktop] Navigating to http://127.0.0.1:8000...")
        page.goto("http://127.0.0.1:8000", wait_until="networkidle")
        print("   Title:", page.title())
        assert "Job Skill Analyzer" in page.title()

        # Check Hero
        hero_h1 = page.locator("h1").inner_text()
        print("2. [Desktop] Hero Heading:", repr(hero_h1))
        assert "Understand what the job" in hero_h1

        # Check Engine Ready badge
        engine_badge = page.locator("header").inner_text()
        print("   Header text contains Engine Ready:", "NLP Engine Ready" in engine_badge)

        # Click 'Try Sample Job'
        print("3. [Desktop] Loading Sample Job...")
        sample_btn = page.get_by_role("button", name="Try Sample Job").first
        sample_btn.click()
        page.wait_for_timeout(800)

        job_input = page.locator("#job-description-input")
        val = job_input.input_value()
        print(f"   Job description populated: {len(val)} chars")
        assert len(val) > 100
        assert "Python" in val

        # Click 'Analyze Requirements'
        print("4. [Desktop] Executing Analysis Pipeline...")
        analyze_btn = page.get_by_role("button", name="Analyze Requirements")
        analyze_btn.click()
        page.wait_for_timeout(1500)

        # Verify results section is displayed
        results_heading = page.locator("h2", has_text="Intelligence Breakdown").inner_text()
        print("5. [Desktop] Results Section Heading:", results_heading)
        assert "Intelligence Breakdown" in results_heading

        # Capture desktop screenshot
        desktop_screenshot = "examples/web_preview.png"
        page.screenshot(path=desktop_screenshot, full_page=True)
        print(f"6. Desktop screenshot saved to {desktop_screenshot}")

        # Check console errors
        print("   Console Errors:", console_errors)
        assert len(console_errors) == 0, f"Unexpected console errors: {console_errors}"
        context.close()

        # ---------------------------------------------------------
        # 2. Mobile Verification (390x844 - iPhone 12/13/14)
        # ---------------------------------------------------------
        print("\n7. [Mobile] Testing responsive mobile view (390x844)...")
        mobile_context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        mobile_page = mobile_context.new_page()

        mobile_page.goto("http://127.0.0.1:8000", wait_until="networkidle")
        mobile_page.wait_for_timeout(500)

        # Check for horizontal overflow
        body_scroll_width = mobile_page.evaluate("document.body.scrollWidth")
        window_inner_width = mobile_page.evaluate("window.innerWidth")
        print(f"   Mobile widths: scrollWidth={body_scroll_width}, innerWidth={window_inner_width}")
        assert body_scroll_width <= window_inner_width + 5, "Horizontal overflow detected on mobile!"

        # Trigger analysis on mobile
        mobile_sample = mobile_page.get_by_role("button", name="Try Sample Job").first
        mobile_sample.click()
        mobile_page.wait_for_timeout(600)

        mobile_analyze = mobile_page.get_by_role("button", name="Analyze Requirements")
        mobile_analyze.click()
        mobile_page.wait_for_timeout(1500)

        mobile_screenshot = "examples/web_preview_mobile.png"
        mobile_page.screenshot(path=mobile_screenshot, full_page=True)
        print(f"8. Mobile screenshot saved to {mobile_screenshot}")
        mobile_context.close()

        browser.close()
        print("\nAll Desktop & Mobile browser verifications PASSED successfully!")


if __name__ == "__main__":
    run_browser_verification()
