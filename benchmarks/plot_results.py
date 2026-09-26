import matplotlib.pyplot as plt

from .run_benchmark import run,TIMEOUT


def plot(results):

    for pattern,data in results.items():

        lengths=data["lengths"]
        engine_times=data["engine_times"]
        re_times=data["re_times"]

        plt.figure(figsize=(8,5))

        plt.plot(lengths,engine_times,marker="o",label="Our DFA engine")

        valid_lengths=[]
        valid_re_times=[]

        for length,time_value in zip(lengths,re_times):

            if time_value is not None:

                valid_lengths.append(length)
                valid_re_times.append(time_value)

        plt.plot(valid_lengths,valid_re_times,marker="o",label="Python re")

        for length,time_value in zip(lengths,re_times):

            if time_value is None:

                plt.annotate("TIMEOUT",(length,TIMEOUT*1000),xytext=(5,5),textcoords="offset points")

        plt.yscale("log")

        plt.ylim(top=TIMEOUT*1000*1.5)

        plt.xlabel("Input length (n)")
        plt.ylabel("Matching time (ms)")
        plt.title(f"Regex benchmark: {pattern}")

        plt.legend()
        plt.grid(True,which="both")

        filename=(pattern.replace("(","").replace(")","").replace("|","_").replace("*","star"))

        plt.savefig(f"{filename}_benchmark.png",dpi=150,bbox_inches="tight")

        plt.show()


if __name__=="__main__":

    import multiprocessing

    multiprocessing.freeze_support()

    results=run()
    plot(results)