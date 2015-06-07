#!/usr/bin/env python
"""
    collector_database is part of the miner project

    (c) Mark Menkhus, 2015

    Licensed under the apache lincence, see LICENSE.md

"""

import sys
import sqlite3
import re


class collector_database:
    """ collector_database: contains the methods to use the database

        defends on sqlite3 database
        depends on configuration
    """
    def __init__(self, database='/usr/local/miner/miner.db'):
        """ setup class for first use
        """
        self.conn = None
        self.cursor = None
        self.database = database
        self.miner_config = None
        try:
            """ open the database using Sqlite3, setup a connection
            and establish the SQL cursor
            """
            self.conn = sqlite3.connect(self.database)
            self.cursor = self.conn.cursor()
        except Exception, e:
            print "collector_database.__init__: %s" % (e,)
            sys.exit(1)
        return None

    def setup_database(self):
        """ set config items for database, over ride defaults

            set the schema for config, rss and mail
        """
        # sort unique items, based on date first, then CVSS score
        # change the text information inserted into the database to
        # document your database as you see fit.
        sql = r"""
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
        '7-jun-2015',
        'This database was created for the miner project to collect rss mail etc.
        This miner project is for my information security use, but you can purpose this
        for whatever you like.'
        );
        create table rss_feeds (
        rss_id text,
        rss_feed text
        );
        insert into rss_feeds (rss_feed) values
        ('http://www.slashdot.org/rss.xml');
        create table rss_stats (
        rss_id text not null references rss_feeds (rss_id),
        rss_lastread text,
        rss_lastsuccess text
        );
        create table rss_data (
        rss_data_id text,
        rss_id text references rss_feeds (rss_id),
        rss_item_guid text,
        rss_date text,
        rss_data text
        );
        create table rss_topic (
        rss_data_id text references rss_data (rss_data_id),
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
        version text,
        purpose text,
        pace text,
        directory text,
        initiation_date text,
        wrap_around text,
        topical_index text
        );
       insert into miner_configuration
        (version, purpose, pace, directory, initiation_date, wrap_around,
         topical_index)
        values
        ('.1', 'miner template values', '24', '/usr/local/miner','7-jun-2015',
         'False', 'None');
        """
        try:
            self.data = self.cursor.executescript(sql)
            self.conn.commit()
        except Exception, error:
            print "collector_database: setup_database: %s" % (error,)
            return False
        return True

    def get_config(self):
        """ return configuration

            get the most recent configuration
        """
        state_query = r"select * from miner_configuration order by config_id\
        desc limit 1;"
        try:
            state = self.cursor.execute(state_query)
        except Exception, error:
            print "collector_database: get_config: %s" % (error,)
            return False
        self.miner_config['version'] = state[0]
        self.miner_config['purpose'] = state[1]
        self.miner_config['pace'] = state[2]
        self.miner_config['directory'] = state[3]
        self.miner_config['initiation_date'] = state[4]
        self.miner_config['wrap_around'] = state[5]
        self.miner_config['topic_index'] = state[6]
        return self.miner_config

    def do_config(self, config_version=1, purpose="security miner", pace=12,
                  directory='/usr/local/miner', initiation_date="06-Jun-2015",
                  wrap_around=False, topic_index=None):
        """ setup the class based on the stored configuration
        """
        state_sql = "insert into miner_configuration \
        (version, purpose, pace, directory, initiation_date, wrap_around,\
         topical_index) values ("
        state_sql += r"'" + config_version + "', "
        state_sql += r"'" + purpose + "', "
        state_sql += r"'" + pace + "', "
        state_sql += r"'" + directory + "', "
        state_sql += r"'" + initiation_date + "', "
        state_sql += r"'" + wrap_around + "', "
        state_sql += r"'" + topic_index + "') ;"
        try:
            self.cursor.execute(state_sql)
            self.conn.commit()
        except Exception, error:
            print "collector_database: get_config: %s" % (error,)
            return False
        return True

    def get_feed(self):
        """ get rss feed list that is configured

            depends on database
        """
        self.sql = """
        select rss_feed from rss_feeds;
        """
        try:
            self.rss_feed = self.cursor.execute(self.sql)
            self.rss_feed = self.rss_feed.fetchall()
        except Exception, error:
            print "collector_database: get_feed: %s" % (error,)
            print "Since this is first use, please execute again."
            self.setup_database()
            sys.exit(1)
        return self.rss_feed

    def valid_rss_feed(self, item=''):
        """ is the item a URL and does it look URLish?
        """
        if re.search(r'^http', item, re.IGNORECASE):
            return True
        else:
            return False

    def set_feed(self, item="http://some.rss.item/rss.xml"):
        """ insert rss feed url into collection

            depends on string rss feed
            does not depend on validity of rss feed url
        """
        item = item.strip('\n')
        item = item.strip(' ')
        if self.valid_rss_feed(item):
            rss_feed_sql = r"insert into rss_feeds (rss_feed) values ("
            rss_feed_sql += r"'" + item + r"');"
            try:
                self.data = self.cursor.execute(rss_feed_sql)
                self.conn.commit()
            except Exception, error:
                print "collector_database: set_feed: failed while inserting\
                into database: %s" % (error)
                return False
        else:
            print "collector_database: set_feed: could not insert %s into db" % (item,)
            return False
        return True

    def get_rss_data(self):
        """ get rss feed data that was collected

            depends on database
            depends on optional range, default is all data
        """
        self.sql = """
        select * from rss_data;
        """
        try:
            ret_data = []
            for each in self.cursor.execute(self.sql):
                ret_data.append(each)
        except Exception, error:
            print "collector_database: get_rss_data: %s" % (error,)
            return False
        return ret_data

    def set_rss_data(self, data=None):
        """ insert rss data into collection

            depends on dict of zero or more rss items
            does not depend on correctness of rss data

        """
        if data:
            for each in data:
                sql = r"insert into rss_data (rss_data) values ('"
                sql += each + r"');"
            try:
                self.cursor.executescript(sql)
                self.conn.commit()
            except Exception, error:
                print "collector_database: set_rss_data during insert: %s" % (error,)
                print "the failing sql statement: %s" % (sql,)
                return False
        return True


def main():
    """ test the collector_database classes

    """
    rss_item = {}
    database = collector_database
    database = database()
    if database.get_feed():
        print "get_feed PASSED"
    else:
        print "get_feed: FAILED"
        sys.exit(1)
    if database.set_feed('http://this.feed.com/feed.xml'):
        print "set_feed passed"
    else:
        print "set_feed failed"
        sys.exit(1)
    print "get_rss_data: %s" % (database.get_rss_data(),)
    rss_item = ['this is an item']
    if database.set_rss_data(rss_item):
        print "set_rss_data passed"
    else:
        print "set_rss_data failed"
        sys.exit(1)
    exit()

if __name__ == "__main__":
    main()
