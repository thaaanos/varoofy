#!/usr/bin/env python
"""
    _____ is part of the miner project

    (c) Mark Menkhus, 2015

    Licensed under the apache lincense, see LICENSE.md

"""

import sys


class collector_database:
    """ collector_database: contains the methods to use the database

        defends on sqlite3 database
        depends on configuration
    """

    def __init__(self):
        """ setup class for first use
        """
        try:
            do_config(self)
        except Exception, evalue:
            print "collector_database, do_config: %s" % (evalue,)
            sys.exit(1)
        return True

    def set_config(self):
        """ set config items for database, over ride defaults

            set the schema for config, rss and mail
        """
        return True

    def get_config(self):
        """ return configuration
        """
        return True

    def do_config(self):
        """ setup the class based on the stored configuration
        """
        return

    def _get_rss_schema(self):
        """ get the internal rss schema for use in the class
        """
        return True

    def _set_rss_schema(self):
        """ set the schema for use in the database, this is not
        mutable, rather part of the implementation
        """
        return True

    def _get_mail_schema(self):
        """ get the internal rss schema for use in the class
        """
        return True

    def _set_mail_schema(self):
        """ set the schema for use in the database, this is not
        mutable, rather part of the implementation
        """
        return True

    def get_feed(self):
        """ get rss feed list that is configured

            depends on database
        """
        return True

    def set_feed(self):
        """ insert rss feed url into collection

            depends on string rss feed
            does not depend on validity of rss feed url
        """
        return True


    def get_rss_data(self):
        """ get rss feed data that was collected

            depends on database
            depends on optional range, default is all data
        """
        return True

    def set_rss_data(self):
        """ insert rss data into collection

            depends on dict of zero or more rss items
            does not depend on correctness of rss data
        """
        return True


def main():
    """ test the collector_database classes

    """
    database = collector_database
    database = database()
    print "get_feed %s" % (database.get_feed())
    if database.set_feed('http://this.geed.com/feed.xml'):
        print "set_feed passed"
    else:
        print "set_feed failed"
        sys.exit(1)        
    print "get_rss_data: %s" % (database.get_rss_data(),)
    rss_item = ['item']['this is an item']
    if database.set_rss_data(rss_item):
        print "set_rss_data passed"
    else:
        print "set_rss_data failed"
        sys.exit(1)
    exit()

if __name__ == "__main__":
    main()
