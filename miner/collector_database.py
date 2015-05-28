#!/usr/bin/env python
"""
    collector_database is part of the miner project

    (c) Mark Menkhus, 2015

    Licensed under the apache lincence, see LICENSE.md

"""

import sys
import sqlite3


class collector_database:
    """ collector_database: contains the methods to use the database

        defends on sqlite3 database
        depends on configuration
    """
    def __init__(self):
        """ setup class for first use
        """
        self.conn = None
        self.cursor = None
        self.database = '/usr/local/miner/minder.db'
        self.miner_state = {}
        try:
            """ open the database using Sqlite3, setup a connection
            and establish the SQL cursor
            """
            self.conn = sqlite3.connect(self.database)
            self.cursor = self.conn.cursor()
            self.set_config()
        except Exception, e:
            print "collector_database.__init__: %s" % (e,)
            sys.exit(1)
        try:
            self.do_config(config_version=1, purpose="security miner", pace=12,
                           directory='/usr/local/miner', initiation_date="27 May 2015",
                           wrap_around=False, topic_index=False)
        except Exception, evalue:
            print "collector_database, do_config: %s" % (evalue,)
            sys.exit(1)
        return None

    def set_config(self):
        """ set config items for database, over ride defaults

            set the schema for config, rss and mail
        """
        # sort unique items, based on date first, then CVSS score
        self.sql = r"""
        create table version (
        database_author text,
        database_version text,
        database_date test,
        about text
        );
        insert into version (
        database_author, database_version, database_date, about)
        values (
        'Mark Menkhus, mark.menkhus@gmail.com',
        '1.0',
        'May 25, 2015'
        'This database was created for the miner project to collect rss mail etc.'
        );
        create table rss_feeds (
        rss_id text not null,
        rss_feed text
        );
        create table rss_stats (
        rss_id text not null references rss_feeds (rss_id),
        rss_lastread text,
        rss_lastsuccess text
        );
        create table rss_data (
        rss_data_id text not null,
        rss_id text not null references rss_feeds (rss_id),
        rss_item_guid text,
        rss_date text,
        rss_data text
        );
        create table rss_topic (
        rss_data_id text not null references rss_data (rss_data_id),
        filter_id text,
        topic_extract_type text,
        topic_extract text
        );
        create table filter_words (
        filter_id text,
        filter_name text,
        filter_regex
        );
        create table miner_configuration (
        config_id text,
        miner_version text,
        miner_purpose text,
        miner_pace text,
        miner_directory text,
        miner_initiation_date text,
        miner_wrap_around text,
        miner_topical_index text
        );
        """
        self.data = self.cursor.execute(self.sql)
        self.commit()
        return True

    def get_config(self):
        """ return configuration
        """
        self.state_query = r"select * from miner_configuration order by config_id\
        desc limit 1;"
        self.state = self.cursor.execute(self.state_query)
        self.miner_state['version'] = self.state[0]
        self.miner_state['purpose'] = self.state[1]
        self.miner_state['pace'] = self.state[2]
        self.miner_state['directory'] = self.state[3]
        self.miner_state['initiation_date'] = self.state[4]
        self.miner_state['wrap_around'] = self.state[5]
        self.miner_state['topic_index'] = self.state[6]
        return True

    def do_config(self, config_version=1, purpose="security miner", pace=12,
                  directory='/usr/local/miner', initiation_date="27 May 2015",
                  wrap_around=False, topic_index=False):
        """ setup the class based on the stored configuration
        """
        self.state_query = r"insert into miner_configuration values "
        self.miner_state['version'] = config_version
        self.miner_state['purpose'] = purpose
        self.miner_state['pace'] = pace
        self.miner_state['directory'] = directory
        self.miner_state['initiation_date'] = initiation_date
        self.miner_state['wrap_around'] = wrap_around
        self.miner_state['topic_index'] = topic_index
        return self.miner_state

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
        self.sql = """
        select rss_feed from rss_feeds;
        """
        self.rss_feed = self.cursor.execute(self.sql)
        self.rss_feed = self.rss.findall()
        return self.rss_feed

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
        self.sql = """
        select * from rss_data;
        """
        self.rss_data = self.cursor.execute(self.sql)
        self.rss_data = self.rss.findall()
        return self.rss_data

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
