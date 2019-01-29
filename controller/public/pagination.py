#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''


from django.core.paginator import Paginator


class Paginator_help:
    # 分页

    def __init__(self, page_num, queryset, PAGE_SIZE, current_page_total, request):
        self.page_num = self.check_page_num(page_num)  # 当前页码
        self.current_page_total = current_page_total  # 当前页下标
        self.queryset = queryset  # 需要分页的对象集合
        self.PAGE_SIZE = PAGE_SIZE  # 每页显示多少条
        self.pages = self.get_Paginator_obj()  # 获取分页对象
        self.page_range = self.get_page_range()  # 获取当前页的页面下标
        self.qstr = self.get_qstr(request)
        self.current_page = self.get_current_page()  # 获取当前页对象

    def get_Paginator_obj(self):
        # 获取分页对象
        pages = Paginator(self.queryset, self.PAGE_SIZE)
        return pages

    def check_page_num(self, page_num):
        # 检查页码
        if page_num <= 0:
            page_num = 1
        return page_num

    def get_current_page(self):
        # 获取当前页对象
        current_page = self.pages.page(self.page_num)
        return current_page

    def get_qstr(self, request):
        qstr = '&'.join(['%s=%s' % (k, v) for k, v in request.GET.items() if k != 'p'])
        return qstr

    def calculate_begin_end(self):
        # 计算当前页下标的取值范围
        page_total = self.pages.num_pages
        begin = 0
        end = 0
        if page_total <= self.current_page_total:
            begin = 0
            end = page_total
        else:
            if self.page_num <= self.current_page_total / 2:
                begin = 0
                end = self.current_page_total
            else:
                begin = self.page_num - self.current_page_total / 2
                end = self.page_num + self.current_page_total / 2
                if (self.current_page_total % 2) != 0:  # 如果分页下标为奇数
                    end += 1
                if end > page_total:
                    end = page_total
                    begin = page_total - self.current_page_total
        return begin, end

    def get_page_range(self):
        # 获取当前页的页面下标
        begin, end = self.calculate_begin_end()

        # 草了，1.9的Paginator分页类的page_range方法得到的尽然是xrange,用[begin:end]切片报错
        page_range = [i for i in self.pages.page_range]
        page_range = page_range[begin:end]

        return page_range
