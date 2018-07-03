import time
import os

from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC 

from lib.page import Page

class PagePowerGermany(Page):
    
    def __init__(self, driver):
        super(PagePowerGermany, self).__init__(driver, url='https://www.eex-transparency.com/homepage/power/germany', title='Transparency in Energy Markets - Germany')

        self.go_to()
        self.wait_to_load()
        self.set_xhr_interception()
        self.intercept_textarea_id = 'interceptedResponse' # DO NOT CHANGE THIS!!!
        self.textarea = self.driver.find_element(By.ID, self.intercept_textarea_id)

        second_chart_box = self.driver.find_element(By.CSS_SELECTOR,'.tpe-chart-teaser')
        self.planned_button = second_chart_box.find_elements(By.CSS_SELECTOR, '.tabs a.ng-binding')[1]
        self.actual_button = second_chart_box.find_elements(By.CSS_SELECTOR, '.tabs a.ng-binding')[0]

    def clear_textarea(self):
        self.driver.execute_script("""
            var textarea = document.getElementById('interceptedResponse');
            textarea.value = '';
            console.log(textarea);
        """)

    def get_actual_data(self):
        self.wait_to_load()
        self.planned_button.click()
        self.clear_textarea()
        self.actual_button.click()
        data = self.get_intercepted_data()
        self.clear_textarea()
        return data

    def get_planned_data(self):
        self.wait_to_load()
        self.actual_button.click()
        self.clear_textarea()
        self.planned_button.click()
        data = self.get_intercepted_data()
        self.clear_textarea()
        return data
 

    def get_intercepted_data(self):
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR,'div[data-ng-show="loading"]')))
        return self.textarea.get_attribute('value')

    def set_xhr_interception(self):
        self.driver.execute_script("""
            (function(XHR) {
            "use strict";

            var element = document.createElement('textarea');
            element.id = "interceptedResponse";
            document.body.appendChild(element);

            var open = XHR.prototype.open;
            var send = XHR.prototype.send;

            XHR.prototype.open = function(method, url, async, user, pass) {
                this._url = url; // want to track the url requested
                open.call(this, method, url, async, user, pass);
            };

            XHR.prototype.send = function(data) {
                var self = this;
                var oldOnReadyStateChange;
                var url = this._url;

                function onReadyStateChange() {
                if(self.status === 200 && self.readyState == 4 /* complete */) {
                    console.log(self.responseText);
                    document.getElementById("interceptedResponse").value = self.responseText;
                }
                if(oldOnReadyStateChange) {
                    oldOnReadyStateChange();
                }
                }

                if(this.addEventListener) {
                this.addEventListener("readystatechange", onReadyStateChange,
                    false);
                } else {
                oldOnReadyStateChange = this.onreadystatechange;
                this.onreadystatechange = onReadyStateChange;
                }
                send.call(this, data);
            }
            })(XMLHttpRequest);"""
        )

        