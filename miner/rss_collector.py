#!/usr/bin/env python
"""
    _____ is part of the miner project

    (c) Mark Menkhus, 2015 

    Licensed under the apache lincense, see LICENSE.md

"""

import sys
import collector_database


class rss_collector:
    """ rss_collector: contains the methods to use rss and isolates 
        form the implementation of the collector database

        depends on collector_database
    """

    def __init__(self):
        """ setup class for first use
        """
        self.db = collector_database
        try:
            self.db = self.db(self)
        except Exception, evalue:
            print "rss_collector: db.collector_database, do_config: %s" % (evalue,)
            sys.exit(1)
        return True

    def set_rss_data(self, rss_data=None):
        """ insert rss data into database
        """
        self.sql = r"""
        insert into rss_data values (rss_data) % r'vvv';
        """
        for each in rss_data:
            data = self.sql.replace('vvv', str(each))
            self.db.execute(data)
        self.db.commit()
        return True

    def get_rss_data(self):
        """ get data from database

        depends on collector_database and methods
        """
        return True

def main ():
    """ test the classes
    """
    rss_collection = rss_collector
    rss_collection = rss_collection()
    if rss_collection.set_rss_data():
        print "rss_collection.set_rss_data passed"
    else:
        print "rss_collection.set_rss_data failed"
    rss_data = rss_collection.get_rss_data()
    if rss_data:
        print "rss_collection.get_rss_data passed"
    else:
        print "rss_collection.get_rss_data failed"
    exit()


if __name__ == "__main__":
    main()
