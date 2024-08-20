
from zuu.core.zutomator import Action, Zutomator


z = Zutomator(Action(
    name="test",
    start="2",
    jobs=[
        {
            "help" : "test 1",
            "steps" : [
                {
                    "echo" : "hello world"
                },
                {
                    "sleep" : "3"
                },
                {
                    "exec" : "notepad.exe",
                    "timeout" : 5,
                    "proc" : "Notepad.exe"
                }
            ]
        }
    ]
))
z.run(tillTimeout=True)