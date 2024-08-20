import os
import time
from typing import Optional, List, Literal, Dict, Any

import requests
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.webdriver import WebDriver

from .helpers import delay, get_screenshot
from .logging_config import logger
from .types import AppiumSessionConfig, AppiumHandler, Command, ExecuteResponse, AppiumServerConfig


class GptDriver:
    _gpt_driver_base_url = "https://api.mobileboost.io"

    def __init__(self, api_key: str, driver: Optional[WebDriver] = None, device_config: Optional[Dict] = None, appium_server_config: Optional[Dict] = None):
        self._api_key = api_key
        self._gpt_driver_session_id: Optional[str] = None
        self._appium_session_config: Optional[AppiumSessionConfig] = None
        self._device_config: Optional[Dict] = device_config
        self._appium_server_config: Optional[Dict] = appium_server_config
        self._driver: Optional[WebDriver] = driver
        self._initialize_driver()

    def _initialize_driver(self):

        port = int(os.getenv('APPIUM_PORT', 4723))
        host = os.getenv('APPIUM_HOST', 'localhost')
        appium_server_config = {'port': port, 'host': host}

        if self._driver:
            self._appium_session_config = AppiumSessionConfig(
                id=self._driver.session_id,
                platform=self._driver.capabilities['platformName'],
                device_name=self._driver.capabilities['deviceName'],
                platform_version=self._driver.capabilities['platformVersion'],
                appium_server_config=AppiumServerConfig(**appium_server_config),
            )
        elif self._device_config:
            appium_server_config = self._appium_server_config or appium_server_config
            self._appium_session_config = AppiumSessionConfig(
                **self._device_config,
                appium_server_config=AppiumServerConfig(**appium_server_config),
            )
        else:
            raise ValueError("Either provide an Appium driver or a device_config dict")

    def start_session(self):
        if not self._driver:
            platform = self._appium_session_config.platform

            if platform.lower() == "android":
                options = UiAutomator2Options()
            else:
                options = XCUITestOptions()

            # Set up the desired capabilities for Appium
            options.load_capabilities({
                'deviceName': self._appium_session_config.device_name,
                'platformVersion': self._appium_session_config.platform_version,
            })

            logger().info(">> Connecting to the Appium server...")
            self._driver = webdriver.Remote(
                command_executor=f'http://{self._appium_session_config.appium_server_config.host}:'
                                 f'{self._appium_session_config.appium_server_config.port}',
                options=options
            )
            logger().info(">> Driver initialized")

        logger().info(">> Starting session...")
        self._appium_session_config.id = self._driver.session_id
        gpt_driver_session_response = requests.post(
            f"{self._gpt_driver_base_url}/sessions/create",
            json={
                "api_key": self._api_key,
                "appium_session_id": self._appium_session_config.id,
                "device_config": {
                    "platform": self._appium_session_config.platform,
                    "device": self._appium_session_config.device_name,
                    "os": self._appium_session_config.platform_version,
                },
            },
        )
        rect_response = requests.get(
            f"http://{self._appium_session_config.appium_server_config.host}:"
            f"{self._appium_session_config.appium_server_config.port}/session/"
            f"{self._appium_session_config.id}/window/rect"
        )

        self._appium_session_config.size = {
            "width": rect_response.json()['value']['width'],
            "height": rect_response.json()['value']['height'],
        }

        gpt_driver_session_id = gpt_driver_session_response.json()['sessionId']
        if gpt_driver_session_id:
            session_link = f"https://app.mobileboost.io/gpt-driver/sessions/{gpt_driver_session_id}"
            logger().info(f">> Session created. Monitor execution at: {session_link}")
            self._gpt_driver_session_id = gpt_driver_session_id

    def stop_session(self, status: Literal["failed", "success"]):
        logger().info(">> Stopping session...")
        requests.post(
            f"{self._gpt_driver_base_url}/sessions/{self._gpt_driver_session_id}/stop",
            json={
                "api_key": self._api_key,
                "status": status,
            },
        )
        logger().info(">> Session stopped.")
        self._gpt_driver_session_id = None

    def execute(self, command: str, appium_handler: Optional[AppiumHandler] = None):
        logger().info(f">> Executing command: {command}")

        if appium_handler:
            try:
                appium_handler(self._driver)
            except Exception:
                self._gpt_handler(command)
        else:
            self._gpt_handler(command)

    def assert_condition(self, assertion: str):
        logger().info(f">> Asserting: {assertion}")
        results = self.check_bulk([assertion])

        if not list(results.values())[0]:
            raise AssertionError(f"Failed assertion: {assertion}")

    def assert_bulk(self, assertions: List[str]):
        logger().info(f">> Asserting: {assertions}")
        results = self.check_bulk(assertions)

        failed_assertions = [
            assertions[i] for i, success in enumerate(results.values()) if not success
        ]

        if failed_assertions:
            raise AssertionError(f"Failed assertions: {', '.join(failed_assertions)}")

    def check_bulk(self, conditions: List[str]) -> Dict[str, bool]:
        logger().info(f">> Checking: {conditions}")
        screenshot = get_screenshot(self._appium_session_config)

        response = requests.post(
            f"{self._gpt_driver_base_url}/sessions/{self._gpt_driver_session_id}/assert",
            json={
                "api_key": self._api_key,
                "base64_screenshot": screenshot,
                "assertions": conditions,
                "command": f"Assert: {conditions}",
            },
        )

        return response.json()['results']

    def extract(self, extractions: List[str]) -> Dict[str, Any]:
        logger().info(f">> Extracting: {extractions}")
        screenshot = get_screenshot(self._appium_session_config)

        response = requests.post(
            f"{self._gpt_driver_base_url}/sessions/{self._gpt_driver_session_id}/extract",
            json={
                "api_key": self._api_key,
                "base64_screenshot": screenshot,
                "extractions": extractions,
                "command": f"Extract: {extractions}",
            }
        )

        return response.json()['results']

    def _gpt_handler(self, command: str):
        try:
            condition_succeeded = False

            while not condition_succeeded:
                screenshot = get_screenshot(self._appium_session_config)

                logger().info(">> Asking GPT Driver for next action...")
                response = requests.post(
                    f"{self._gpt_driver_base_url}/sessions/{self._gpt_driver_session_id}/execute",
                    json={
                        "api_key": self._api_key,
                        "command": command,
                        "base64_screenshot": screenshot,
                    }
                )
                execute_status = response.json()['status']
                if execute_status == "failed":
                    raise Exception("Execution failed")

                condition_succeeded = execute_status != "inProgress"
                execute_response = ExecuteResponse(**response.json())
                for cmd in execute_response.commands:
                    self._execute_command(cmd)

                if not condition_succeeded:
                    time.sleep(1.5)

        except Exception as e:
            self.stop_session(status="failed")
            raise e

    @staticmethod
    def _execute_command(command: Command):
        logger().info(">> Performing action...")
        first_action = command.data.get('actions', [])[0] if command.data else None
        if first_action and first_action.get('type') == "pause" and first_action.get('duration'):
            delay(first_action['duration'] * 1000)
        else:
            requests.request(
                method=command.method,
                url=command.url,
                json=command.data
            )
