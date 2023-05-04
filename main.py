from booking.booking import Booking

bot = Booking()
bot.get_home_page()
bot.select_destination('Paris')
bot.select_dates('2023-05-30', '2023-05-31')
bot.select_occupants(1)
#bot.apply_filtrations() # Uncomment to apply filtrations
bot.report_results()