import re
import time
import multiprocessing

from regexlib.matcher import Regex
from .redos_patterns import patterns


TIMEOUT=2


def run_re(pattern,string,result):

    re.fullmatch(pattern,string)

    start=time.perf_counter()

    re.fullmatch(pattern,string)

    elapsed=time.perf_counter()-start

    result["time"]=elapsed


def benchmark_re(pattern,string):

    result=multiprocessing.Manager().dict()

    process=multiprocessing.Process(target=run_re,args=(pattern,string,result))

    process.start()
    process.join(TIMEOUT)

    if process.is_alive():

        process.terminate()
        process.join()

        return None

    return result.get("time")


def benchmark_engine(regex,string):

    start=time.perf_counter()

    regex.match(string)

    return time.perf_counter()-start


def run():

    lengths=[5,10,15,20,25,30]

    results={}

    for item in patterns:

        pattern=item["pattern"]
        generate=item["generate"]

        regex=Regex(pattern)

        results[pattern]={"lengths":[],"engine_times":[],"re_times":[]}

        print()
        print("Pattern:",pattern)
        print("n | engine | re")

        for n in lengths:

            string=generate(n)

            engine_time=benchmark_engine(regex,string)
            re_time=benchmark_re(pattern,string)

            engine_ms=engine_time*1000

            if re_time is None:

                re_result="TIMEOUT"
                re_ms=None

            else:

                re_ms=re_time*1000
                re_result=f"{re_ms:.3f} ms"

            results[pattern]["lengths"].append(n)
            results[pattern]["engine_times"].append(engine_ms)
            results[pattern]["re_times"].append(re_ms)

            print(f"{n} | {engine_ms:.3f} ms | {re_result}")

    return results


if __name__=="__main__":

    multiprocessing.freeze_support()
    results=run()