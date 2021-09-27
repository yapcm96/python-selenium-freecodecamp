import os
from selenium import webdriver
from booking.constants import BASE_URL
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable

class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:/SeleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        # The next two lines are for hiding the warning messages when running on the CLI
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        super(Booking, self).__init__(options=options) # this instantiate an instance of the inherited class i.e. webdriver.Chrome
        # could also have just used super() and will still work.
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb): # this is a magic method for the context manager of "with"
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(BASE_URL)

    def decline_cookies(self):
        decline_element = self.find_element_by_id('onetrust-reject-all-handler')
        self.execute_script("arguments[0].click();", decline_element)
        # decline_element.click()

    def change_currency(self, currency=None):
        currency_element = self.find_element_by_css_selector(
            'button[data-modal-aria-label="Select your currency"]'
        )
        currency_element.click()

        selected_currency_element = self.find_element_by_css_selector(
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'
        )
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        place_to_go_search_field = self.find_element_by_css_selector(
            'input[id="ss"]'
        )
        place_to_go_search_field.send_keys(place_to_go) # since we can enter a location and then pressing 'search' works, we can just send the keys

        # selected_place_to_go_element = self.find_element_by_css_selector(
        #     'li[data-i="0"]'
        # )
        # selected_place_to_go_element.click()

    def select_date(self, check_in_date, check_out_date):
        check_in_element = self.find_element_by_css_selector(
            'div[data-mode="checkin"]'
        )
        check_in_element.click()

        ## Navigate right on the calendar selection until the month of check out date is found
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        check_out_date_split = check_out_date.split('-')
        check_out_month = int(check_out_date_split[1])
        check_out_year = check_out_date_split[0]

        while True:
            second_month_value_element = self.find_elements_by_class_name("bui-calendar__month")
            second_month_value = second_month_value_element[1].text
            if second_month_value == months[check_out_month-1] + " " + check_out_year:
                break

            right_navigate_element = self.find_element_by_css_selector(
                'div[data-bui-ref="calendar-next"]'
            )
            right_navigate_element.click()

        ## Click on the check in and check out dates
        check_in_element = self.find_element_by_css_selector(
            f'td[data-date="{check_in_date}"]'
        )
        self.execute_script("arguments[0].click();", check_in_element)
        # check_in_element.click()

        check_out_element = self.find_element_by_css_selector(
            f'td[data-date="{check_out_date}"]'
        )
        self.execute_script("arguments[0].click();", check_out_element)
        # check_out_element.click()

    def select_adults(self, count=1):
        selection_element = self.find_element_by_id('xp__guests__toggle')
        selection_element.click()

        while True:
            decrease_adults_element = self.find_element_by_css_selector(
                'button[aria-label="Decrease number of Adults"]'
            )
            decrease_adults_element.click()
            #If the value of adults reaches 1, then we should get out
            #of the while loop
            adults_value_element = self.find_element_by_id('group_adults')
            adults_value = adults_value_element.get_attribute(
                'value'
            ) # Should give back the adults count

            if int(adults_value) == 1:
                break

        increase_button_element = self.find_element_by_css_selector(
            'button[aria-label="Increase number of Adults"]'
        )

        for _ in range(count - 1):
            increase_button_element.click()

    def click_search(self):
        search_button = self.find_element_by_css_selector(
            'button[type="submit"]'
        )
        search_button.click()

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self) # We pass in the self i.e. Booking instance into the BookingFiltration instance
        filtration.apply_star_rating(4, 5)
        filtration.sort_price_lowest_first()

    def report_results(self):
        hotel_boxes = self.find_element_by_id(
            'hotellist_inner'
        )

        report = BookingReport(hotel_boxes)
        table = PrettyTable()
        table.field_names = ["Hotel Name", "Total Price", "Hotel Score"]
        table.add_rows(report.pull_deal_box_attributes())
        print(table)

