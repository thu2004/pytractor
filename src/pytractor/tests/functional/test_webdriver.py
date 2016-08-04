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

from .webdriver_test_base import WebDriverTestBase
from selenium.webdriver.remote.webelement import WebElement

class FirefoxWebDriverTest(WebDriverTestBase):
    use_firefox = True

    def test_find_element_by_binding(self):
        self.driver.get(self.url + 'index.html#/form')
        element = self.driver.find_element_by_binding('greeting')
        self.assertIsInstance(element, WebElement)
        self.assertEqual(element.text, 'Hiya')


class ChromeWebDriverTest(WebDriverTestBase):
    use_firefox = False

    def test_find_element_by_binding(self):
        self.driver.get(self.url + 'index.html#/form')
        element = self.driver.find_element_by_binding('greeting')
        self.assertIsInstance(element, WebElement)
        self.assertEqual(element.text, 'Hiya')
