from utils.Sql import Queries


def main():
    p = Queries()
    p.create_db()
    p.create_tables()


if __name__ == '__main__':
    main()
