import logging
import random
import time
from typing import Optional
from warnings import warn

from playwright.sync_api import BrowserContext, Page, StorageState, sync_playwright
from playwright_stealth import StealthConfig, stealth_sync

from agentql import QueryParser, trail_logger
from agentql._core._errors import (
    AccessibilityTreeError,
    AgentQLServerError,
    AttributeNotFoundError,
    ElementNotFoundError,
    NoOpenBrowserError,
    NoOpenPageError,
    OpenUrlError,
    UnableToClosePopupError,
)
from agentql._core._js_snippets.snippet_loader import load_js
from agentql._core._utils import ensure_url_scheme
from agentql.ext.playwright.sync_api._utils_sync import (
    add_event_listeners_for_page_monitor_shared,
    determine_load_state_shared,
    get_page_accessibility_tree,
    process_iframes,
    remove_event_listeners_for_page_monitor_shared,
)
from agentql.ext.playwright.sync_api.response_proxy import Locator
from agentql.sync_api import ScrollDirection, WebDriver
from agentql.sync_api._agentql_service import query_agentql_server
from agentql.sync_api._response_proxy import AQLResponseProxy

from .._driver_constants import RENDERER, USER_AGENT, VENDOR
from .._driver_settings import ProxySettings, StealthModeConfig
from .._network_monitor import PageActivityMonitor
from .._utils import locate_interactive_element, post_process_accessibility_tree

log = logging.getLogger("agentql")


class PlaywrightWebDriver(WebDriver[Locator, Page, BrowserContext]):
    """
    PlaywrightWebDriver is a web driver that builds on top of [Playwright framework](https://playwright.dev/python/). It is the default web driver used by AgentQL. Users could use PlaywrightWebDriver for browser / page related activities, such as scrolling, wait for page to load, and browse in stealth mode.
    """

    def __init__(self, headless=False, proxy: Optional[ProxySettings] = None) -> None:
        """
        Construct the PlaywrightWebDriver instance.

        Parameters:
        -----------
        headless (bool) (optional): Whether to start browser in headless mode. Headless browser will run in background while headful browser will run like a normal browser.
        proxy (dict) (optional): The proxy setting dictionary that includes server, username, and password as key.

        Returns:
        --------
        PlaywrightWebDriver: An instance of PlaywrightWebDriver.
        """
        self._playwright = None

        self._browser = None
        """The current browser. Only use this to close the browser session in the end."""

        self._context = None
        """The current browser context. Use this to open a new page"""

        self._original_html = None
        """The page's original HTML content, prior to any AgentQL modifications"""

        self._headless = headless
        """Whether to run browser in headless mode or not."""

        self._proxy = proxy

        self._page_monitor = None

        self._stealth_mode_config = None

    @property
    def is_headless(self) -> bool:
        """Returns whether the browser is running in headless mode or not.

        Returns:
        --------
        bool: True if the browser is running in headless mode, False otherwise."""
        return self._headless

    def get_text_content(self, web_element: Locator) -> Optional[str]:
        """
        Gets the text content of the web element.

        Parameters:
        -----------

        web_element ([Playwright Locator](https://playwright.dev/python/docs/api/class-locator)): The web element represented by Playwright's Locator object.

        Returns:
        --------

        str: The text content of the web element.
        """

        warn(
            """
            `WebDriver` is deprecated. Please, use Playwright's API directly.

            Replace with: `web_element.text_content()`
            """,
            DeprecationWarning,
            stacklevel=2,
        )

        return web_element.text_content()

    def _stop_browser(self):
        """Closes the current browser session."""
        if self._context:
            self._context.close()
            self._context = None
        if self._browser:
            self._browser.close()
            self._browser = None
        if self._playwright:
            self._playwright.stop()
            self._playwright = None

    def enable_stealth_mode(
        self,
        webgl_vendor: str = VENDOR,
        webgl_renderer: str = RENDERER,
        nav_user_agent: str = USER_AGENT,
    ):
        """Enable the stealth mode and set the stealth mode configuration.
        Ideally parameters values should match some real values to avoid detection.
        To get a realistic examples, you can use browser fingerprinting websites such as https://bot.sannysoft.com/ and https://pixelscan.net/

        Parameters:
        -----------
        webgl_vendor (str) (optional):
            The vendor of the GPU used by WebGL to render graphics, such as `Apple Inc.`. After setting this parameter, your browser will emit this vendor information.
        webgl_renderer (str) (optional):
            Identifies the specific GPU model or graphics rendering engine used by WebGL, such as `Apple M3`. After setting this parameter, your browser will emit this renderer information.
        nav_user_agent (str) (optional):
            Identifies the browser, its version, and the operating system, such as `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36`. After setting this parameter, your browser will send this user agent information to the website.
        """

        warn(
            """
            `WebDriver` is deprecated. Please, use new `Page` extension API instead.

            Replace with `agentql.ext.playwright.sync_api.Page.enable_stealth_mode`
            """,
            DeprecationWarning,
            stacklevel=2,
        )

        self._stealth_mode_config = StealthModeConfig(
            vendor=webgl_vendor, renderer=webgl_renderer, nav_user_agent=nav_user_agent
        )

    def open_url(self, url: str, new_page: bool = False):
        """Open URL in the browser.

        Parameters:
        ----------
        url (str): The URL to open.
        new_page (bool): Whether to open the URL in a new page.
        """

        warn(
            """
            `WebDriver` is deprecated. Please, use Playwright's API directly.

            Replace with:
                import agentql

                page = agentql.wrap(browser.new_page())
                page.goto(url)
            """,
            DeprecationWarning,
            stacklevel=2,
        )

        if not self._browser or not self._context:
            raise NoOpenBrowserError()

        if new_page or len(self._context.pages) == 0:
            self._open_url(url)
        else:
            url = ensure_url_scheme(url)
            self.current_page.goto(url, wait_until="domcontentloaded")

    @property
    def current_url(self) -> str:
        """Get the URL of the current page being processed by AgentQL.

        Returns:
        --------
        str: The URL of the current page.
        """

        warn(
            """
            `WebDriver` is deprecated. Please, use Playwright's API directly.

            Replace with: `Page.url`
            """,
            DeprecationWarning,
            stacklevel=2,
        )

        return self.current_page.url

    @property
    def html(self) -> Optional[str]:
        """Returns the original HTML (i.e. without any AgentQL modifications) fetched from the most recently loaded page".

        Returns:
        --------
        dict: The HTML content of the web page in Dict format.
        """
        return self._original_html

    @property
    def current_page(self) -> Page:
        """Returns the [Playwright page object](https://playwright.dev/python/docs/api/class-page) that represents the current page. Users could do more fine grained interaction using this page object, such as navigating to a different url or take screenshot of the page.

        Returns:
        --------
        [Playwright Page](https://playwright.dev/python/docs/api/class-page): The current page.
        """

        warn(
            """
            `WebDriver` is deprecated. Please, use Playwright's API directly.
            """,
            DeprecationWarning,
            stacklevel=2,
        )

        if not self._context:
            raise NoOpenBrowserError()

        if len(self._context.pages) == 0:
            raise NoOpenPageError()
        return self._context.pages[-1]

    @property
    def browser(self) -> BrowserContext:
        """Returns the current browser being used.

        Returns:
        --------
        object: The current browser context object.
        """

        warn(
            """
            `WebDriver` is deprecated. Please, use Playwright's API directly.
            """,
            DeprecationWarning,
            stacklevel=2,
        )

        if not self._context:
            raise NoOpenBrowserError()
        return self._context

    def open_html(self, html: str):
        """
        Opens a new page and loads the given HTML content.

        Parameters:
        -----------
        html (str): The HTML content to load in the page.
        """

        warn(
            """
            `WebDriver` is deprecated. Please, use Playwright's API directly.

            Replace with:
                import agentql

                page = agentql.wrap(browser.new_page())
                page.set_content(html)
            """,
            DeprecationWarning,
            stacklevel=2,
        )

        if not self._browser or not self._context:
            raise NoOpenBrowserError()
        page = self._context.new_page()
        page.set_content(html)

    @property
    def accessibility_tree(self) -> dict:
        """Returns the up-to-date accessibility tree of the page.

        Returns:
        --------
        dict: The accessibility tree of the page in Dict format.
        """
        try:
            accessibility_tree = get_page_accessibility_tree(self.current_page)
            process_iframes(self.current_page, accessibility_tree)
            post_process_accessibility_tree(accessibility_tree)
            return accessibility_tree
        except Exception as e:
            raise AccessibilityTreeError() from e

    def wait_for_page_ready_state(self, wait_for_network_idle: bool = True):
        """Wait for the page to reach the "Page Ready" state (i.e. page has entered a relatively stable state and most main content is loaded).

        Usage:
        -----
        ```py
        session = agentql.start_async_session(YOUTUBE_URL)

        # Scroll to bottom to trigger comments loading
        await session.driver.scroll_to_bottom()

        # Wait for comments to load before making a query
        await session.driver.wait_for_page_ready_state()
        await session.query(QUERY)
        ```

        Parameters:
        -----------
        wait_for_network_idle (bool) (optional): This acts as a switch to determine whether to use default chekcing mechanism. If set to `False`, this method will only check for whether page has emitted `load` [event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event) and provide a less costly checking mechanism for fast-loading pages.
        """

        warn(
            """
            `WebDriver` is deprecated. Please, use new `Page` extension API instead.

            Replace with: `agentql.ext.playwright.sync_api.Page.wait_for_network_idle`
            """,
            DeprecationWarning,
            stacklevel=2,
        )

        page = self.current_page

        trail_logger.add_event(f"Waiting for {page} to reach 'Page Ready' state")
        if not self._page_monitor:
            self._page_monitor = PageActivityMonitor()
        else:
            # Reset the network monitor to clear the logs
            self._page_monitor.reset()

        # Add event listeners to track DOM changes and network activities
        self._add_event_listeners_for_page_monitor(page)

        # Wait for the page to reach the "Page Ready" state
        self._determine_load_state(
            page, self._page_monitor, wait_for_network_idle=wait_for_network_idle
        )

        # Remove the event listeners to prevent overwhelming the async event loop
        self._remove_event_listeners_for_page_monitor(page)

        trail_logger.add_event(f"Finished waiting for {page} to reach 'Page Ready' state")

    def scroll_page(self, scroll_direction: ScrollDirection, pixels: int = 720):
        """Scrolls the page up or down by given pixels. By default, it will scroll 720 pixels.

        Parameters:
        -----------
        scroll_direction (ScrollDirection): An enumeration class that represents the direction in which a scroll action can occur. Currently, it has `UP` and `DOWN` member.
        pixels (int) (optional): The number of pixels to scroll. 720 by default.
        """

        warn(
            """
            `WebDriver` is deprecated. Please, use Playwright's API directly.

            Replace with: `Page.mouse.wheel`
            """,
            DeprecationWarning,
            stacklevel=2,
        )

        self.wait_for_page_ready_state()
        delta_y = pixels if scroll_direction == ScrollDirection.DOWN else -pixels
        self.current_page.mouse.wheel(delta_x=0, delta_y=delta_y)

    def scroll_to_bottom(self):
        """Scrolls to the bottom of the current page."""

        warn(
            """
            `WebDriver` is deprecated. Please, use Playwright's API directly.

            Replace with: `Page.mouse.wheel`
            """,
            DeprecationWarning,
            stacklevel=2,
        )

        self.wait_for_page_ready_state()
        height_information = self.current_page.evaluate(load_js("get_scroll_info"))
        viewport_height, total_height, scroll_height = height_information
        while scroll_height < total_height:
            scroll_height = scroll_height + viewport_height
            self.current_page.mouse.wheel(delta_x=0, delta_y=viewport_height)
            time.sleep(random.uniform(0.05, 0.1))

    def scroll_to_top(self):
        """Scrolls to the top of the current page."""

        warn(
            """
            `WebDriver` is deprecated. Please, use Playwright's API directly.

            Replace with: `Page.mouse.wheel`
            """,
            DeprecationWarning,
            stacklevel=2,
        )

        self.wait_for_page_ready_state()
        height_information = self.current_page.evaluate(load_js("get_scroll_info"))
        viewport_height, scroll_height = height_information[0], height_information[2]
        while scroll_height > 0:
            scroll_height = scroll_height - viewport_height
            self.current_page.mouse.wheel(delta_x=0, delta_y=-viewport_height)
            time.sleep(random.uniform(0.05, 0.1))

    def take_screenshot(self, path: str):
        """Takes a screenshot of the current page.

        Parameters:
        -----------
        path (str): The path to save the screenshot.
        """

        warn(
            """
            `WebDriver` is deprecated. Please, use Playwright's API directly.

            Replace with: `Page.screenshot(path, full_page=True)`
            """,
            DeprecationWarning,
            stacklevel=2,
        )

        self.current_page.screenshot(path=path, full_page=True)

    def _close_popup(self, popup_tree: dict, page_url: str, timeout: int = 500):
        """Close the popup by querying AgentQL server for the close button and perform a click action with web driver.

        Parameters:
        -----------
        popup_tree (dict): The accessibility tree that has the popup node as the parent.
        page_url (str): The URL of the active page.
        timeout (int) (optional): The timeout value for the connection with AgentQL server service.
        """
        query = """
            {
                popup {
                    close_btn
                }
            }
        """
        parser = QueryParser(query)
        query_tree = parser.parse()
        try:
            response = query_agentql_server(query, popup_tree, timeout, page_url)
            agentql_response_proxy = AQLResponseProxy(response, self, query_tree)
            agentql_response_proxy.popup.close_btn.click()
        except (AgentQLServerError, ElementNotFoundError, AttributeNotFoundError) as e:
            raise UnableToClosePopupError() from e

    def _get_user_auth_session(self) -> StorageState:
        """
        Returns the user authentication session that contains the login session state of current browser. User could pass this information when starting the session to preserve previous login state.

        Returns:
        --------
        dict: User auth session in Python dictionary format.
        """
        if not self._browser or not self._context:
            raise NoOpenBrowserError()
        return self._context.storage_state()

    def _locate_interactive_element(self, response_data: dict) -> Locator:
        """
        Locates an interactive element in the web page.

        Parameters:
        -----------

        response_data (dict): The data of the interactive element from the AgentQL response.

        Returns:
        --------

        [Playwright Locator](https://playwright.dev/python/docs/api/class-locator): The web element represented by Playwright's Locator object.
        """
        return locate_interactive_element(self.current_page, response_data)  # type: ignore

    def _prepare_accessibility_tree(
        self, lazy_load_pages_count: int = 3, include_aria_hidden: bool = True
    ) -> dict:
        """Prepare the AT by modifing the dom. It will return the accessibility tree after waiting for page to load and dom modification.

        Parameters:
        -----------
        lazy_load_pages_count (int): The number of times to scroll down and up the page.
        include_aria_hidden (bool): Whether to include elements with aria-hidden attribute in the accessibility tree.

        Returns:
        --------
        dict: AT of the page
        """
        self._original_html = self.current_page.content()
        self._page_scroll(pages=lazy_load_pages_count)

        try:
            accessibility_tree = get_page_accessibility_tree(
                self.current_page, include_aria_hidden=include_aria_hidden
            )
            process_iframes(self.current_page, accessibility_tree)
            post_process_accessibility_tree(accessibility_tree)
            return accessibility_tree
        except Exception as e:
            raise AccessibilityTreeError() from e

    def _apply_stealth_mode_to_page(self, page: Page):
        """Applies stealth mode to the given page.

        Parameters:
        ----------
        page (Page): The page to which stealth mode will be applied.
        """
        # Only mask User Agent in headless mode to avoid detection for headless browsers
        mask_user_agent = self._headless

        if self._stealth_mode_config is None:
            return

        stealth_sync(
            page,
            config=StealthConfig(
                vendor=self._stealth_mode_config["vendor"],
                renderer=self._stealth_mode_config["renderer"],
                # nav_user_agent will only take effect when navigator_user_agent parameter is True
                nav_user_agent=self._stealth_mode_config["nav_user_agent"],
                navigator_user_agent=mask_user_agent,
            ),
        )

    def _open_url(self, url: str):
        """Opens a new page and navigates to the given URL. Initialize the storgage state if provided.

        Parameters:
        ----------
        url (str): The URL to navigate to.
        storgate_state_content (optional): The storage state with which user would like to initialize the browser.
        """

        url = ensure_url_scheme(url)

        if not self._browser or not self._context:
            raise NoOpenBrowserError()

        try:
            page = self._context.new_page()
            if self._stealth_mode_config is not None:
                self._apply_stealth_mode_to_page(page)
            page.goto(url, wait_until="domcontentloaded")
        except Exception as e:
            raise OpenUrlError(url) from e

    def _page_scroll(self, pages=3):
        """Scrolls the page down first and then up to load all contents on the page.

        Parameters:
        ----------
        pages (int): The number of pages to scroll down.
        """
        if pages < 1:
            return

        if self._stealth_mode_config is None:
            delta_y = 10000
            for _ in range(pages):
                self.current_page.mouse.wheel(delta_x=0, delta_y=delta_y)
                time.sleep(0.1)

            time.sleep(1)
            delta_y = -10000
            for _ in range(pages):
                self.current_page.mouse.wheel(delta_x=0, delta_y=delta_y)
                time.sleep(0.1)
        else:
            for _ in range(pages):
                self.scroll_to_bottom()
                time.sleep(0.1)

            time.sleep(1)
            for _ in range(pages):
                self.scroll_to_top()
                time.sleep(0.1)

    def _start_browser(
        self,
        user_auth_session=None,
    ):
        """Starts a new browser session and set storage state (if there is any).

        Parameters:
        ----------
        user_session_extras (optional): the JSON object that holds user session information
        headless (bool): Whether to start the browser in headless mode.
        load_media (bool): Whether to load media (images, fonts, etc.) or not.
        """
        ignored_args = ["--enable-automation", "--disable-extensions"]
        args = [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-blink-features=AutomationControlled",
        ]
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=self._headless, proxy=self._proxy, args=args, ignore_default_args=ignored_args
        )
        self._context = self._browser.new_context(
            user_agent=USER_AGENT,
            storage_state=user_auth_session,
        )

    def _determine_load_state(
        self,
        page: Page,
        monitor: PageActivityMonitor,
        timeout_seconds: int = 14,
        wait_for_network_idle: bool = True,
    ):
        determine_load_state_shared(page, monitor, timeout_seconds, wait_for_network_idle)

    def _add_event_listeners_for_page_monitor(self, page: Page):
        add_event_listeners_for_page_monitor_shared(page, self._page_monitor)

    def _remove_event_listeners_for_page_monitor(self, page: Page):
        remove_event_listeners_for_page_monitor_shared(page, self._page_monitor)
