from booking.booking import Booking

# inst = Booking()
# inst.land_first_page()

try:
    with Booking(teardown=False) as bot:
        bot.land_first_page()
        bot.decline_cookies()
        # bot.change_currency(currency='USD')
        bot.select_place_to_go(input("Where are you going? "))
        bot.select_date(input("When is your check-in date? Enter in format yyyy-mm-dd: "),
                        input("When is your check-out date? Enter in format yyyy-mm-dd: "))
        bot.select_adults(int(input("How many adults? ")))
        bot.click_search()
        bot.apply_filtrations()
        bot.refresh() # Let our bot grab the data after a refresh, this way it doesn't grab the data too quickly before filters are applied
        bot.report_results()

except Exception as e:
    if 'in PATH' in str(e):
        print(
            'Your are tyring to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '    PATH=$PATH:/path/toyour/folder/ \n'
        )
    else:
        raise