#!/usr/bin/python

import os
import fnmatch

from lxml import etree


def returns_tree(file_name) :
	tree = etree.parse(open(file_name))
	return tree 

def get_old_path(tree):
	path_list = []
	for i in tree.xpath('//xspf:location', namespaces={'xspf': "http://xspf.org/ns/0/"}) :
		path_list.append(i.text.split("/")[-1])
	return path_list

def create_new_path(dir_path, path_list):
	new_path = []
	temp_path = []

	for x in range(0, len(path_list)):
		for root, dirnames, filenames in os.walk(dir_path):
			for filename in fnmatch.filter(filenames, path_list[x]):
				temp_path.append(os.path.join(root, filename))


		if len(temp_path) > 0 :
			new_path.append(temp_path[0])
			temp_path = []
	return new_path

def replace_path(tree, new_path, file_name):
	root = tree.getroot()
	code = root.xpath("//xspf:location", namespaces={'xspf': "http://xspf.org/ns/0/"})
	for c in range(0, len(code)):
		code[c].text = "file://"+new_path[c]
	etree.ElementTree(root).write(file_name, pretty_print=True)

def main():
	file_name = input("Enter the file name \n")
	dir_path = input("Enter the path to the directory, one above all the music files \n")
	tree = returns_tree(file_name)
	path_list = get_old_path(tree)
	new_path = create_new_path(dir_path, path_list)
	replace_path = create_new_path(tree, new_path, file_name)
	print(" !!-- Your Playlist is ready to use --!!")

if __name__ == '__main__':
	main()
