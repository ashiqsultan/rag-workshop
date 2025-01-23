# Knowledge Base added for testing
temp_kb="""
# Thread
A Thread is the actual worker in the computer. 
Think about thread like a waiter in a restaurant and customers like requests. 
The waiter is the person who does the actual work. 
When more than one waiter is present then you can term it as multithread
# Process
- A Process is Program in execution
- A Process has its own virtual memory
- Process has a memory and other resources associated to it example an open file.
- All Process has **atleast one thread** (Thread of Control)
- Threads run on the CPU on the context of a Process meaning the thread refers to the process memory.
- A Process can also have multiple threads.
- In case of multithread then all threads
    - the process memory is shared between all threads
    - so we need **Mutexes to control shared data.**
**Example** Node.js itself is a process
"""