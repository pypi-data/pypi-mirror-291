#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
import os


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
ROOTMARKERS : list[str] = [
	# 저장소.
	".svn",				# Subversion (SVN) version control system folder.
	".p4config",		# Perforce configuration file.
	".p4ignore",		# Perforce ignore patterns file.
	".git",				# Git version control system folder.
	".hg",				# Mercurial version control system folder.

	# 개발환경.
	".vscode",			# Visual Studio Code settings directory.
	".vs",				# Visual Studio settings directory.
	".idea",			# JetBrains IDE (PyCharm, IntelliJ IDEA, etc.) settings directory.

	# 파이썬 루트 파일.
	"setup.py",			# Python project setup script.
	"requirements.txt",	# Python project dependencies file.
	"Pipfile",			# Python project Pipenv dependency management file.
	"pyproject.toml",	# Python project configuration file.
	
	# "package.json",  # Node.js project configuration file.
	# "composer.json", # PHP project Composer configuration file.
	# "CMakeLists.txt",# CMake project configuration file.
	# "Makefile",      # Unix/Linux project build automation script.
	# "Cargo.toml",    # Rust project configuration file.
	# "gradle.build",  # Gradle project build script.
	# "pom.xml",       # Maven project configuration file.
	# ".terraform",    # Terraform configuration directory.
	# "Gemfile",       # Ruby project dependency management file.
	# "Rakefile",      # Ruby project build automation script.
	# "config.yml",    # Common YAML configuration file.
	# "config.yaml",   # Common YAML configuration file.
	# ".circleci",     # CircleCI configuration directory.
	# ".travis.yml",   # Travis CI configuration file.
]



#--------------------------------------------------------------------------------
# 프로젝트.
#--------------------------------------------------------------------------------
class Project:
	#--------------------------------------------------------------------------------
	# 프로젝트 루트 경로 찾기.
	#--------------------------------------------------------------------------------
	@staticmethod
	def FindRootPath(start : str, rootMarkers : list[str] = None) -> str:
		current = os.path.abspath(start)
		if os.path.isfile(current):
			current = os.path.dirname(current)

		if not rootMarkers: rootMarkers = ROOTMARKERS

		while True:
			if any(os.path.exists(os.path.join(current, marker)) for marker in rootMarkers):
				return current			
			parent = os.path.dirname(current)
			if parent == current: break
			current = parent
		raise FileNotFoundError("Project root not found.")