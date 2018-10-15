a, *rest, b = range(10)


with open("Python/NewStart/Basics.py", encoding='utf-8') as f:
    first, *_, last = f.readlines()


def sum(a, b, *, biteme=False):
    if biteme:
        pass
    else:
        return a + b
#sum(1, 2, 3) # TypeError: sum() takes 2 positional arguments but 3 were given


try:
    try:
        raise Exception("Yo")
    except Exception as e:
        raise Exception("Chain preserved") from e
except Exception as e:
    print(e)

def ListIter():
    """ Instead of 
        for i in gen():
            yield i
   """
    yield from range(10)
ListIter()


from pathlib import Path
directory = Path("Python/NewStart")
filepath = directory / "Basics.py"
print(filepath.exists())


# https://docs.python.org/3/library/asyncio-task.html
import asyncio
async def ping_server(ip):  
    print("Pinging {0}".format(ip))
@asyncio.coroutine # same as above
def load_file(path):  
    pass
async def ping_local():  
    return await ping_server('192.168.1.1')
# Blocking call which returns when the ping_local() coroutine is done
loop = asyncio.get_event_loop()
loop.run_until_complete(ping_local())
loop.close()