#!/usr/bin/env python
import unittest
from Clict import from_Config

from unittest.mock import patch, MagicMock
from pathlib import Path
from configparser import ConfigParser
import os

# Importing the classes and functions from the given code

class TestFromConfig(unittest.TestCase):


	def test_folder(self):
		# Test handling of a file with a valid config extension
		config = from_Config(Path('./config'))
		self.assertTrue(config._self.type.folder)
		self.assertEqual(config._self.name, "config")
		print(repr(config.__opts__()))
		print(repr(config))
	# def test_ignore_dotfiles(self):
	# 	# Test that dotfiles are ignored when ignore_dotfiles is set to True
	# 	config = from_Config(self.dot_file)
	# 	self.assertTrue(config._type.file)
	# 	self.assertTrue(config._opts.ignore_dotfiles)
	# 	self.assertEqual(config._name, ".hidden_config")
	#
	# 	# Now, check if it correctly ignores the dotfile if set to ignore
	# 	config._optb.ignore_dotfiles = True
	# 	config.__read__()
	# 	self.assertNotIn(".hidden_config", config)

	# def test_strip_file_extension(self):
	# 	# Test that file extensions are stripped if strip_fileext is set to True
	# 	config = from_Config(self.test_file)
	# 	self.assertTrue(config._type.file)
	# 	self.assertTrue(config._opts.strip_fileext)
	# 	self.assertEqual(config._name, "example_config")  # No ".ini" extension
	#
	# 	# Change strip_fileext to False and test again
	# 	config._optb.strip_fileext = False
	# 	config.__read__()
	# 	self.assertIn("mockup.ini", config)
	#
	# def test_strip_folder_prefix(self):
	# 	# Test that folder prefixes are stripped if strip_folderprefix is set to True
	# 	numbered_folder = Path("001_example_folder")
	# 	numbered_folder.mkdir(exist_ok=True)
	#
	# 	try:
	# 		config = from_Config(numbered_folder)
	# 		self.assertTrue(config._type.folder)
	# 		self.assertTrue(config._opts.strip_folderprefix)
	#
	# 		# If 'strip_folderprefix' is True, '001_' should be stripped
	# 		config._optb.strip_folderprefix = True
	# 		config.__read__()
	# 		self.assertIn("example_folder", config)
	# 		self.assertNotIn("001_example_folder", config)
	#
	# 		# If 'strip_folderprefix' is False, the prefix should remain
	# 		config._optb.strip_folderprefix = False
	# 		config.__read__()
	# 		self.assertIn("001_example_folder", config)
	#
	# 	finally:
	# 		numbered_folder.rmdir()
	#
	# def test_strip_file_prefix(self):
	# 	# Test that numeric prefixes in file names are stripped if strip_fileprefix is set to True
	# 	self.numbered_prefix_file.touch()
	# 	config = from_Config(self.numbered_prefix_file)
	# 	self.assertTrue(config._type.file)
	# 	self.assertTrue(config._opts.strip_fileprefix)
	#
	# 	# If 'strip_fileprefix' is True, '001_' should be stripped
	# 	config._optb.strip_fileprefix = True
	# 	self.assertEqual(config._name, "example_config")
	#
	# 	# If 'strip_fileprefix' is False, the prefix should remain
	# 	config._optb.strip_fileprefix = False
	# 	config.__read__()
	# 	self.assertIn("001_example_config", config)
	#
	# def test_config_detection(self):
	# 	# Test that the class correctly detects config files based on name and extension
	# 	config = from_Config(Path("config/mockup.ini"))
	# 	self.assertTrue(config._type.config)
	#
	# 	config = from_Config(Path("settings.conf"))
	# 	self.assertTrue(config._type.config)
	#
	# 	non_config = from_Config(Path("readme.txt"))
	# 	self.assertFalse(non_config._type.config)
	#
	# def test_parent_relationship(self):
	# 	# Test the parent-child relationship handling within directories
	# 	config = from_Config(self.test_folder)
	# 	self.assertTrue(config._type.folder)
	# 	self.assertIsNone(config._parent)  # No parent for root config
	#
	# 	# Test with a nested folder
	# 	nested_folder = self.test_folder / "sub_folder"
	# 	nested_folder.mkdir(exist_ok=True)
	# 	try:
	# 		nested_config = from_Config(nested_folder, parent=config)
	# 		self.assertEqual(nested_config._parent._name, "example_folder")
	# 	finally:
	# 		nested_folder.rmdir()

if __name__ == '__main__':
	unittest.main()
