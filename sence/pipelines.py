# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SencePipeline:
	def __init__(self):
		self.courses = []

	def process_item(self, item, spider):
		self.courses.append(item['course_name'])
		return item

	def close_spider(self, spider):
		with open('courses_names.txt', 'w') as f:
		    for course in self.courses:
		        f.write("%s\n" % course)
