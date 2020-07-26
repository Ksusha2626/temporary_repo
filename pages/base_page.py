import math

from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.locators import BasePageLocators


class BasePage:
    def __init__(self, app, url):
        self.app = app
        self.url = url

    def open(self):
        self.app.get(self.url)

    def go_to_login_page(self):
        link = self.app.find_element(*BasePageLocators.LOGIN_LINK)
        link.click()

    def should_be_login_link(self):
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "Login link is not presented"

    def should_be_authorized_user(self):
        assert self.is_element_present(*BasePageLocators.USER_ICON), "User icon is not presented," \
                                                                     " probably unauthorised user"

    def solve_quiz_and_get_code(self, ):
        alert = self.app.switch_to.alert
        x = alert.text.split(" ")[2]
        answer = str(math.log(abs((12 * math.sin(float(x))))))
        alert.send_keys(answer)
        alert.accept()
        try:
            alert = self.app.switch_to.alert
            alert_text = alert.text
            print(f"Your code: {alert_text}")
            alert.accept()
        except NoAlertPresentException:
            print("No second alert presented")

    def is_element_present(self, selector, locator, timeout=4):
        try:
            WebDriverWait(self.app, timeout).until_not(EC.presence_of_element_located((selector, locator)))
        except TimeoutException:
            return True

        return False

    def is_disappeared(self, selector, locator, timeout=4):
        try:
            WebDriverWait(self.app, timeout, 1, TimeoutException). \
                until_not(EC.presence_of_element_located((selector, locator)))
        except TimeoutException:
            return False

        return True