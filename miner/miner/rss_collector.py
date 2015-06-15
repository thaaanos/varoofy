#!/usr/bin/env python
"""
    _____ is part of the miner project

    (c) Mark Menkhus, 2015

    Licensed under the apache license, see LICENSE.md

"""

import sys
import collector_database


class rss_collector:
    """ rss_collector: contains the methods to use rss and isolates
        from the implementation of the collector database

        depends on collector_database
    """

    def __init__(self):
        """ setup class for first use
        """
        try:
            self.db = collector_database()
        except Exception, error:
            print "rss_collector.__init__ %s" % (error,)
            sys.exit(1)
        return None

    def set_rss_data(self, rss_data=None):
        """ insert rss data into database
        """
        for each in rss_data:
            try:
                self.db.set_rss_data(each)
            except Exception, error:
                print "rss_collector.set_rss_data: %s" % (error,)
                sys.exit(1)
        return True

    def get_rss_data(self):
        """ get data from database

        depends on collector_database and methods
        """
        rss_data = []
        for each in self.db.get_rss_data():
            rss_data.append(each)
        return rss_data


def main():
    """ test the classes
    """
    try:
        rss_collection = rss_collector
    except Exception, error:
        print "main test in rss_collection: rss_collector %" % (error,)
    #rss_collection = rss_collection()
    try:
        rss_collection.set_rss_data(['this is some data'])
        print "rss_collection.set_rss_data passed"
    except Exception, error:
        print "rss_collection.set_rss_data %s" % (error,)
        sys.exit(1)
    try:
        rss_data = rss_collection.get_rss_data()
        print "rss_collection.get_rss_data passed"
        for each in rss_data:
            print each
    except Exception, error:
        print "rss_collection.get_rss_data %s" % (error,)
        sys.exit(1)
    exit()


if __name__ == "__main__":
    main()
