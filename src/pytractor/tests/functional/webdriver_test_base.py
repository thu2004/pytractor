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
from selenium.webdriver.remote.webelement import WebElement

# pylint: disable=no-name-in-module
from pytractor.webdriver import Firefox, Chrome
from selenium import webdriver

# pylint: enable=no-name-in-module

from . import SimpleWebServerProcess


class WebDriverTestBase(unittest.TestCase):
    WIN_CHROME_DIR = "bin/windows"

    @classmethod
    def setUpClass(cls):
        cls.url = 'http://localhost:{}/'.format(SimpleWebServerProcess.PORT)
        if cls.use_firefox:
            profile = webdriver.FirefoxProfile()
            profile.set_preference("network.proxy.type", 0)
            cls.driver = Firefox(firefox_profile=profile)
        else:
            module_path = __file__
            chrome_path = os.path.join(os.path.dirname(module_path), cls.WIN_CHROME_DIR)

            chrome_driver = os.path.join(chrome_path, "chromedriver.exe")
            cls.driver = Chrome(executable_path=chrome_driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

