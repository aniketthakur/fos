__author__ = 'prathvi'
import mailchimp
from esthenos  import mainapp
@mainapp.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    native = date.replace(tzinfo=None)
    format='%b %d, %Y'
    return native.strftime(format)

def subscribe(name,email_ad, list_id= "93c1a74cac"):
    try:
        m = get_mailchimp_api()
        m.lists.subscribe(list_id, email = {'email':email_ad},merge_vars={'DNAME':name})
        print  "The email has been successfully subscribed"
    except mailchimp.ListAlreadySubscribedError:
        print  "That email is already subscribed to the list"
    except mailchimp.Error, e:
        print  'An error occurred: %s - %s' % (e.__class__, e)

class ordered_dict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self._order = self.keys()

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        if key in self._order:
            self._order.remove(key)
        self._order.append(key)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._order.remove(key)

    def order(self):
        return self._order[:]

    def ordered_items(self):
        return [(key,self[key]) for key in self._order]


from random import randint
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def get_mailchimp_api():
    return mailchimp.Mailchimp('6e73868dbf17cff787d3b9dab5a4f396-us5') #your api key here


from flask import request

def request_wants_json():
    best = request.accept_mimetypes\
    .best_match(['application/json', 'text/html'])
    return best == 'application/json' and\
           request.accept_mimetypes[best] >\
           request.accept_mimetypes['text/html']