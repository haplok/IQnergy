
import multiprocessing
import concurrent.futures
import time

import functions

class ProcessController:
   
    def __init__(self) -> None:
        self.max_processes = 1
        self.q = multiprocessing.Queue()  
        self.alive_proc = 0
    
    def set_max_proc(self, n: int) -> None:
        self.max_processes = n

    def start(self, tasks, max_exec_time) -> None:
        self.max_exec_time = max_exec_time
        
        for task in tasks:
            self.q.put(task)
        
        processes = []
        while not self.q.empty() and self.alive_proc < self.max_processes:
            task = self.q.get()
            process = multiprocessing.Process(target=task[0], args=task[1])
            process.start()
            self.alive_proc += 1
            processes.append(process)
            
        time.sleep(self.max_exec_time)  
        for process in processes:
            self.alive_proc -= 1
            if process.is_alive():
                process.terminate()
            process.join()
            

    def wait(self) -> None:
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_processes) as executor:
            while not self.q.empty():
                task = self.q.get()
                executor.submit(task[0], *task[1])

    def wait_count(self) -> int:
        return self.q.qsize()
    
    def alive_count(self) -> int:
        return self.alive_proc

if __name__ == "__main__":
    start_time = time.time()
    tasks_to_do = [(functions.function1, (1, *range(0))),
                   (functions.function2, (2, *range(1))),
                   (functions.function3, (3, *range(2))),
                   (functions.function4, (4, *range(3))),
                   (functions.function5, (5, *range(4))),
                   (functions.function6, (6, *range(5))),
                   (functions.function1, (1, *range(6))),
                   (functions.function2, (2, *range(7))),
                   (functions.function3, (3, *range(8))),
                   (functions.function4, (4, *range(9))),
                   (functions.function5, (5, *range(10))),
                   (functions.function6, (6, *range(11)))
                   ]
      
    p_c = ProcessController()
    p_c.set_max_proc(3)
    p_c.start(tasks_to_do, 3.1)
    print('осталось ' + str(p_c.wait_count()) + ' элемента в очереди')
    p_c.wait()
    print(p_c.alive_count())
    
    print(f'Общее время выполнения программы: {time.time()-start_time} секунд')


