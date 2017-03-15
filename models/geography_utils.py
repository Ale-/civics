import pycountry
from django.utils.translation import ugettext_lazy as _

#
# Returns a tuple (name of country, two-digit keycode of country) from a pycountry country
#
def country_as_tuple(country):
    return (country.alpha_2, country.name)

#
# Return a tuple with tuples of all countries in pycountry database,
# as returned by country_as_tuple function, valid for setting choices in a Django model
#
def countries_as_tuple():
    # Sort countries by name in alphabetic order
    countries = sorted( pycountry.countries, key = lambda country : country.name )
    return tuple( map(country_as_tuple, countries) )
