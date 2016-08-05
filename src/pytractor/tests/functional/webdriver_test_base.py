# Copyright 2014 Konrad Podloucky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Simple tests for Firefox and Chrome drivers. We just see if the drivers can
be instantiated and run a simple test.
"""
import unittest
import os
import platform

from selenium.webdriver.remote.webelement import WebElement

# pylint: disable=no-name-in-module
from pytractor.webdriver import Firefox, Chrome
from selenium import webdriver

# pylint: enable=no-name-in-module

from . import SimpleWebServerProcess


class WebDriverTestBase(unittest.TestCase):
    WIN_CHROME_DIR = "bin/windows"
    OSX_CHROME_DIR = "bin/osx"
    LINUX_CHROME_DIR = "bin/linux"

    @classmethod
    def setUpClass(cls):
        cls.url = 'http://localhost:{}/'.format(SimpleWebServerProcess.PORT)
        if cls.use_firefox:
            profile = webdriver.FirefoxProfile()
            profile.set_preference("network.proxy.type", 0)
            cls.driver = Firefox(firefox_profile=profile)
        else:
            system_name = platform.system()
            module_path = __file__
            if system_name == "Darwin":
                chrome_path = os.path.join(os.path.dirname(module_path), cls.OSX_CHROME_DIR)
                chrome_driver = os.path.join(chrome_path, "chromedriver")
            elif system_name == "Windows":
                chrome_path = os.path.join(os.path.dirname(module_path), cls.WIN_CHROME_DIR)
                chrome_driver = os.path.join(chrome_path, "chromedriver.exe")
            else:
                chrome_path = os.path.join(os.path.dirname(module_path), cls.LINUX_CHROME_DIR)
                chrome_driver = os.path.join(chrome_path, "chromedriver")

            cls.driver = Chrome(executable_path=chrome_driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

