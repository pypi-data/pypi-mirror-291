#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins



#--------------------------------------------------------------------------------
# 저장소 클래스.
# - 저장소 클래스를 통해 객체를 호출하면 최초 1회 할당 이후 계속 같은 객체를 반환한다.
# - 저장소 클래스 내부에서 생성되는 탓에 생성시 인자가 없는 객체여야 한다.
# - 만일 생성시 인자가 들어간다면 최초 생성인지 사용자가 판단해서 인자를 넣어주어야 한다.
# - 혹은 Link() 를 통해 외부에서 할당한 인스턴스를 넣어둘 수 있다.
#--------------------------------------------------------------------------------
T = TypeVar("T", bound = Any)
class Repository():
	#--------------------------------------------------------------------------------
	# 클래스 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__Instances : Dict[Type[T], T] = dict()


	#--------------------------------------------------------------------------------
	# 저장소에 모든 인스턴스 제거.
	#--------------------------------------------------------------------------------
	@classmethod
	def Cleanup() -> None:
		Repository.__Instances.clear()
	

	#--------------------------------------------------------------------------------
	# 저장소에 기존 인스턴스 설정 (기존 것이 있다면 제거 후 설정).
	#--------------------------------------------------------------------------------
	@staticmethod
	def Link(instance : T) -> bool:
		if not instance:
			return False
		
		isType : bool = builtins.isinstance(instance, type)
		if isType:
			return False

		classType : Type[T] = instance.__class__
		if classType in Repository.__Instances:
			del Repository.__Instances[classType]
		Repository.__Instances[classType] = instance
		return True
	

	#--------------------------------------------------------------------------------
	# 저장소에 신규 인스턴스 생성 (기존 것이 있다면 제거 후 생성).
	# - 생성자에 값을 넣기 위해 args와 kwargs 값을 넣어주어야 한다.
	# - 물론 값을 넣지 않아도 상관없으며 그 경우 인자 없는 생성자가 호출된다. (생성자에 인자가 존재한다면 주의)
	#--------------------------------------------------------------------------------
	@staticmethod
	def Set(classType : Type[T], *args : Any, **kwargs : Any) -> T:
		if classType in Repository.__Instances:
			del Repository.__Instances[classType]
		instance = classType(*args, **kwargs)
		Repository.__Instances[classType] = instance
		return instance
	

	#--------------------------------------------------------------------------------
	# 저장소에 존재하는 인스턴스 반환.
	# - 없다면 신규 생성하며 이 때 생성자에 값을 넣기 위해 args와 kwargs 값을 넣어주어야 한다.
	# - 물론 값을 넣지 않아도 상관없으며 그 경우 인자 없는 생성자가 호출된다. 생성자에 인자가 존재한다면 주의)
	#--------------------------------------------------------------------------------
	@staticmethod
	def Get(classType : Type[T], *args : Any, **kwargs : Any) -> T:
		if classType in Repository.__Instances:
			instance = Repository.__Instances[classType]
		else:
			instance = classType(*args, **kwargs)
			Repository.__Instances[classType] = instance
		return instance