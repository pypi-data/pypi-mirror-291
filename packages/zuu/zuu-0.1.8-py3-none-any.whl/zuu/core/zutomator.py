from functools import cache
from math import e
import os
import time
from typing import TypedDict
import typing
from zuu.core.scheduling import kill_proc_after_timeout, kill_process_after_timeout, kill_window_after_timeout
from zuu.stdpkg.subprocess import open_detached
from zuu.stdpkg.time import remaining_time, sleep_until

class Step(TypedDict, total = False):
    sleep : str
    print : str
    echo : str
    exit : str
    call : str
    exec : str

class Job(TypedDict):
    help : str
    steps : typing.List[Step]

class Action(TypedDict):
    name : str
    start : str
    jobs : typing.List[Job]


class Ctx:
    def __init__(self):
        self.args = {}
        self.overwriteMain : bool = False
        self.eoMod : bool = False
        self.eoStep : bool = False

        self.maxTime = 0

class BaseMod:
    def oninit(self, ctx : Ctx, action : Action):
        pass

    def prejob(self, ctx : Ctx, job : Job):
        pass

    def postjob(self, ctx : Ctx, job : Job):
        pass

    def prestep(self, ctx : Ctx, callkey : str, value, others : dict):
        pass

    def poststep(self, ctx : Ctx, callkey : str, value, others : dict):
        pass

    def __new__(cls):
        cls.__callkeys__ = [x for x in dir(cls) if x.startswith("node_") and callable(getattr(cls, x))]
        return super().__new__(cls)
    
class Zutomator:
    def __init__(self, action : Action) -> None:
        self.__action = action
        self.__mods : typing.List[BaseMod] = []
        self.__ctx : Ctx = None

    @property
    def mods(self):
        return self.__mods

    @mods.setter
    def mods(self, mods : typing.List[BaseMod]):
        self.__mods = mods


    __builtin_calls = ["sleep", "print", "echo", "exit"]

    def handle_step(self, callkey : str, value, others : dict):
        match (callkey, value, others):
            case "sleep", str(value), _:
                sleep_until(value)
            case "print"|"echo", str(value), _:
                print(value)
            case "exit",_, _:
                if value:
                    exit(value)
                exit()
            case "call", str(value), _:
                os.system(value)
            case "exec", str(value), _:
                proc = open_detached(value, *others.get("args", []))
                timeout = others.get("timeout", None)
                window : str = others.get("window", None)
                proc_string = others.get("proc", None)
                if timeout:
                    remaining = remaining_time(timeout)
                    if window:
                        kill_window_after_timeout(window, remaining)
                    elif proc_string:
                        kill_proc_after_timeout(proc_string, remaining)
                    else:
                        kill_process_after_timeout(proc.pid, remaining)
                    self.__ctx.maxTime = max(self.__ctx.maxTime, time.time() + remaining)

            case _:
                raise ValueError(f"unknown callkey {callkey}")


    @cache
    def __has_ext_callkey(self, key : str):
        for mod in self.__mods:
            if key in mod.__callkeys__:
                return True
        return False
        
    def __handle_call(self, step : Step):
        temp = step.copy()
        for callkey, val in temp.items():
            break
        val = temp.pop(callkey)

        if not self.__has_ext_callkey(callkey) and callkey in self.__builtin_calls:
            return self.handle_step(callkey, val, temp)
        
        mods_with_keys = [mod for mod in self.__mods if callkey in mod.__callkeys__]
        index = 0
        overwrite = False
        for mod in mods_with_keys:
            self.__ctx.eoMod = False
            self.__ctx.overwriteMain = False

            mod.prestep(self.__ctx, callkey, val, temp)
            
            if self.__ctx.overwriteMain:
                overwrite = True
            if self.__ctx.eoMod:
                break

            index += 1

        if not overwrite:
            self.handle_step(callkey, val, temp)

        for i in range(index, len(mods_with_keys)):
            mod = mods_with_keys[i]
            mod.poststep(self.__ctx, callkey, val, temp)

    def run(self, tillTimeout : bool = False):
        self.__has_ext_callkey.cache_clear()

        self.__ctx = Ctx()
        print(f"Current Action: {self.__action['name']}")

        if self.__action.get("start", None):
            sleep_until(self.__action['start'])

        # init mods
        for mod in self.__mods:
            mod.oninit(self.__ctx, self.__action)

        # loop jobs
        for job in self.__action['jobs']:
            job : Job
            if job.get("help", None):
                print(f"Job: {job['help']}")

            # prejob
            for mod in self.__mods:
                mod.prejob(self.__ctx, job)    

            for step in job['steps']:
                step : Step
                self.__handle_call(step)
            
                if self.__ctx.eoStep:
                    break

            for mod in self.__mods:
                mod.postjob(self.__ctx, job)

        if tillTimeout:
            while time.time() < self.__ctx.maxTime + 10:
                time.sleep(0.1)

        print(f"Action {self.__action['name']} completed")



        
        
            