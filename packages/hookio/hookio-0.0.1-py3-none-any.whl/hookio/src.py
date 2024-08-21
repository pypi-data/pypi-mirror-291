import inspect
import asyncio
from dataclasses import dataclass
from typing import Callable,Awaitable,Any,TypeVar,Generic

# 定义一个泛型变量，用于表示函数的返回类型
R = TypeVar('R')

@dataclass
class FuncArgs(Generic[R]):
    func: Callable[..., Awaitable[R] | R]
    args: tuple[Any, ...]

class Flow:
    def __init__(
        self,
        main_logic: FuncArgs,
        on_start: FuncArgs|None = None,
        on_end: FuncArgs|None = None,
        on_error: FuncArgs|None = None,
    ):
        self.main_logic = main_logic
        self.on_start = on_start
        self.on_end = on_end if on_end and self.check_hook_func(on_end.func, ['state']) else None
        self.on_error = on_error if on_error and self.check_hook_func(on_error.func, ['msg']) else None
        self.context: dict[str, Any] = {}

    async def run(self):
        if self.on_start:
            result = await self.execute_func(self.on_start.func,self.on_start.args)
            self.context['result'] = result
        try:
            await self.execute_func(self.main_logic.func,self.main_logic.args)
        except Exception as e:
            if self.on_error:
                should_raise = await self.execute_func(self.on_error.func,(*self.on_error.args, {'msg': e}))
                if should_raise:
                    raise
        finally:
            if self.on_end:
                await self.execute_func(self.on_end.func,(*self.on_end.args, {'state': self.context.get('state',None)}))

    ## 检查回调函数是否还有关键字参数
    @staticmethod
    def check_hook_func(func: Callable, expected_args: list[str]):
        sig = inspect.signature(func)
        params = sig.parameters
        return all(p in params for p in expected_args)

    ## 无感的运行同步和异步代码
    @staticmethod
    async def execute_func(func,args):
        if inspect.iscoroutinefunction(func):
            await func(*args)
        else:
            func(*args)

if __name__ =='__main__':
    def main_func(x,y):
        return x/y
    
    def on_start(msg:str):
        print(f'start:{msg}')
    
    def on_error(msg:str):
        print(f'error: {msg}')
    
    def on_end(state:str):
        print(f'state: {state}')

    flow=Flow(
        main_logic = FuncArgs(main_func,(1,2)),
        on_start = FuncArgs(on_start,('---',)),
        on_end = FuncArgs(on_end,()),
        on_error=FuncArgs(on_error,())
    )

    asyncio.run(flow.run())