#coding: utf-8
import info
from views import main_window
from views import search_table
from views import input_window
from models import same_meaning_query
from models import utils


class ViewTypeLabels(object):
    SELECT_SELECT = 0
    FROM_SELECT = 1
    WHERE_SELECT = 2
    DEFAULT_SELECT = 3
    DESC_TABLE = 4
    ORDER_BY = 5
    PURE_QUERY = 6
    LIMIT_SELECT = 7
    GROUP_BY = 8
    AGGREGATE = 9


class WindowChooser(object):
    def __init__(self):
        self.query_builder = same_meaning_query.QueryBuilder()
        self.main_win = main_window.MainWindow(self)
        # self.info_con = info.Info(self.main_win.window)
        self.key_sequence = []
        self.keys = {'f': self.from_select,
                     'd': self.default_select,
                     's': self.show_tables,
                     'e': self.desc_table,
                     'l': self.order_by,
                     'o': self.group_by,
                     'r': self.reverse_sorting,
                     'u': self.pure_query,
                     'i': self.select_select,
                     'a': self.execute_query,
                     'x': self.limit_select}
        # mainloop must be the last method in init
        self.main_win.window.mainloop()

    def key_pressed_event(self, key):
        if key in self.keys:
            self.keys[key]()

    def set_tmp_data(self, data):
        if self.view_type == ViewTypeLabels.DEFAULT_SELECT:
            # TODO rewrite without index
            result, self.meta = self.query_builder.select_all(
                data.get(data.curselection()[0])[0]).execute_with_meta()
            dct = utils.tuple_to_dict_with_meta(result, self.meta)
            self.main_win.set_data_to_table(dct)

            self.main_win.label_value = self.query_builder.get_query_for_label()
            return

        if self.view_type == ViewTypeLabels.FROM_SELECT:
            tmp = []
            for i in data.curselection():
                tmp.append(data.get(i)[0])
            self.query_builder.set_from(tmp)

            self.main_win.label_value = self.query_builder.get_query_for_label()
            print self.main_win.label_value
            self.main_win.window.update_idletasks()
            return

        if self.view_type == ViewTypeLabels.DESC_TABLE:
            result, self.meta = self.query_builder.desc_table(
                data.get(data.curselection()[0])[0]).execute_with_meta()
            dct = utils.tuple_to_dict_with_meta(result, self.meta)
            self.main_win.set_data_to_table(dct)

            self.main_win.label_value = self.query_builder.get_query_for_label()
            return

        if self.view_type == ViewTypeLabels.ORDER_BY:
            self.sort_column = data.get(data.curselection()[0])
            self.main_win.sort_table(self.sort_column)
            return

        if self.view_type == ViewTypeLabels.PURE_QUERY:
            result, self.meta = self.query_builder.set_query(data).execute_with_meta()
            dct = utils.tuple_to_dict_with_meta(result, self.meta)
            self.main_win.set_data_to_table(dct)

            self.main_win.label_value = self.query_builder.get_query_for_label()
            return

        if self.view_type == ViewTypeLabels.SELECT_SELECT:
            tmp = []
            for i in data.curselection():
                tmp.append(data.get(i))
            self.query_builder.set_select(tmp)

            self.main_win.label_value = self.query_builder.get_query_for_label()
            return

        if self.view_type == ViewTypeLabels.LIMIT_SELECT:
            self.query_builder.set_limit(data)
            return

        if self.view_type == ViewTypeLabels.GROUP_BY:
            tmp = []
            for i in data.curselection():
                tmp.append(data.get(i))
            self.query_builder.set_group_by(tmp)

            # TODO without slices
            select_tpl = self.query_builder.select_part[7:].split(', ')
            diff = utils.group_select_diff(tmp, select_tpl)

            for i in diff:
                if i in select_tpl:
                    select_tpl.remove(i)
            self.query_builder.set_select(select_tpl)

            if len(diff) > 0:
                print 'diff not null'
                view = input_window.InputWindow(self, manual_input=False)
                view.add(', '.join(diff))
                view.calculate_string_gaps()
                self.view_type = ViewTypeLabels.AGGREGATE

            self.main_win.label_value = self.query_builder.get_query_for_label()
            return

        if self.view_type == ViewTypeLabels.AGGREGATE:
            self.query_builder.select_part = self.query_builder.select_part + ', ' + data
            print self.query_builder.build_query().query
            return

    # different select methods
    def from_select(self):
        self.view_type = ViewTypeLabels.FROM_SELECT
        view = search_table.SearchTableView(self)
        self.query_result = self.query_builder.show_tables().execute()
        view.add(self.query_result).window.mainloop()
        self.key_sequence.append('f')

    def default_select(self):
        self.view_type = ViewTypeLabels.DEFAULT_SELECT
        view = search_table.SearchTableView(self, selectmode='')
        self.query_result = self.query_builder.show_tables().execute()
        view.add(self.query_result).window.mainloop()
        self.key_sequence.append('d')

    def show_tables(self):
        result, meta = self.query_builder.show_tables().execute_with_meta()
        self.main_win.set_data_to_table(utils.tuple_to_dict_with_meta(result, meta))
        self.key_sequence.append('s')

    def desc_table(self):
        self.view_type = ViewTypeLabels.DESC_TABLE
        view = search_table.SearchTableView(self, selectmode='')
        self.query_result = self.query_builder.show_tables().execute()
        view.add(self.query_result).window.mainloop()
        self.key_sequence.append('e')

    def order_by(self):
        self.view_type = ViewTypeLabels.ORDER_BY
        view = search_table.SearchTableView(self, selectmode='')
        view.add(self.meta)
        self.key_sequence.append('l')

    def group_by(self):
        self.view_type = ViewTypeLabels.GROUP_BY
        view = search_table.SearchTableView(self)
        # TODO no slices
        self.query_result = self.query_builder.select_part[7:].split(', ')
        view.add(self.query_result)
        self.key_sequence.append('o')

    def reverse_sorting(self):
        self.main_win.sort_table(self.sort_column)
        self.key_sequence.append('r')

    def pure_query(self):
        self.view_type = ViewTypeLabels.PURE_QUERY
        input_window.InputWindow(self)
        self.key_sequence.append('u')

    def select_select(self):
        self.view_type = ViewTypeLabels.SELECT_SELECT
        view = search_table.SearchTableView(self)
        self.query_result = self.query_builder.get_fields()
        view.add(self.query_result)
        self.key_sequence.append('i')

    def execute_query(self):
        self.query_result, self.meta = self.query_builder.build_query().execute_with_meta()
        dct = utils.tuple_to_dict_with_meta(self.query_result, self.meta)
        self.main_win.set_data_to_table(dct)
        self.key_sequence.append('a')

    def limit_select(self):
        self.view_type = ViewTypeLabels.LIMIT_SELECT
        input_window.InputWindow(self)
        self.key_sequence.append('x')
