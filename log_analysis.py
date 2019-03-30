#!/usr/bin/env python3
import psycopg2


def connect_to_database():
    """
    Connect to a database

    Return:
        Cursor for db operations
    """
    try:
        database = psycopg2.connect("dbname=news")
        cursor = database.cursor()
    except psycopg2.Error as err:
        print("Failed to connect to the PSQL database: \n", err)
        return None
    else:
        return cursor


def popular_three_articles(db_cursor):
    """
     Finds the most popular three artciles.

        :param db_cursor: db cursor to perform query fetch.
    """

    query = """
        SELECT articles.title,
                   count(*) AS num
            FROM   log,
                   articles,
                   authors
            WHERE  log.path = '/article/' || articles.slug
            AND articles.author = authors.id
            GROUP BY articles.title
            ORDER BY num DESC
            LIMIT 3;
    """
    db_cursor.execute(query)
    results = db_cursor.fetchall()

    print('\n What are the most popular three articles of all time? \n')
    print('===========================================================')

    for result in results:
        print('\n"{title}" - {count} views \n'
              .format(title=result[0], count=result[1]))

    return


def most_popular_authors(db_cursor):
    """
        Finds the most popular authors.
        :param db_cursor: Cursor to perform query fetch db operation
    """
    query = """
            SELECT authors.name,
                   count(*) AS num
            FROM   log,
                   articles,
                   authors
            WHERE  log.path = '/article/' || articles.slug
            AND articles.author = authors.id
            GROUP BY authors.name
            ORDER BY num DESC;
        """
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    print('\n Who are the most popular article authors of all time? \n')
    print('===========================================================')

    for result in results:
        print('\n {author} - {count} views \n '
              .format(author=result[0], count=result[1]))
    return


def one_percent_errors(db_cursor):
    """
        Finds the day where error is more than 1%
        :param db_cursor: Cursor to perform query fetch db operation

        Note:
        Query in this function depends on views that were created in the db.
        Refer README for more details.

    """
    query = """
            SELECT * FROM err_rate WHERE percentage > 1;
            """
    db_cursor.execute(query)
    results = db_cursor.fetchall()

    print('\n On which days did more than 1% of requests lead to errors? \n')
    print('=================================================================')

    for result in results:
        print('\n {date:%B %d, %Y} - {rate:.1f}% errors\n'.format(
            date=result[0],
            rate=result[1]))

    return


if __name__ == "__main__":
    CURSOR = connect_to_database()
    if CURSOR:
        popular_three_articles(CURSOR)
        most_popular_authors(CURSOR)
        one_percent_errors(CURSOR)
        CURSOR.close()
