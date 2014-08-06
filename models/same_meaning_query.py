from models import connect_db


class QueryBuilder(object):
    def __init__(self):
        self.cursor = connect_db.Connect().make_connection().cursor
        self.query = ''
        self.from_part = ''
        self.select_part = ''
        self.where_part = ''
        self.group_by_part = ''
        self.limit_part = ''

    def show_tables(self):
        self.query = 'show tables'
        return self

    def select_all(self, table):
        self.query = 'select * from ' + table
        return self

    def desc_table(self, table):
        self.query = 'desc ' + table
        return self

    def set_query(self, query):
        self.query = query
        return self

    def set_from(self, from_):
        self.from_part = ' from ' + ', '.join(from_)
        self.from_ = ', '.join(from_)
        return self

    def set_select(self, select):
        self.select_part = 'select ' + ', '.join(select) + ' '
        return self

    def set_limit(self, limit):
        self.limit_part = ' limit ' + limit
        return self

    def set_group_by(self, group_by):
        self.group_by_part = ' group by ' + ', '.join(group_by)
        return self

    def get_fields(self):
        names = []
        for i in self.from_.split(', '):
            tmp, names_tmp = QueryBuilder().select_all(i).execute_with_meta()
            for j in range(len(names_tmp)):
                names_tmp[j] = i + '.' + names_tmp[j]
            for k in names_tmp:
                names.append(k)

        return names

    def build_query(self):
        self.query = self.select_part + self.from_part + self.where_part + self.group_by_part + self.limit_part
        return self

    def execute(self):
        print self.query
        self.cursor.execute(self.query)
        return self.cursor.fetchall()

    def execute_with_meta(self):
        print self.query
        self.cursor.execute(self.query)
        meta = []
        for i in self.cursor.description:
            meta.append(i[0])
        return self.cursor.fetchall(), meta

    def get_query_for_label(self):
        return self.select_part + self.from_part + self.where_part + self.group_by_part