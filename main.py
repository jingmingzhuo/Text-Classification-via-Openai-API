import argparse
import json
import os
import threading
import queue
from model import get_response
from tasks.task import get_task


def run(args, task, id):
    info = {}
    info["id"] = id
    input = task.get_input(args.prompt, id)
    response = get_response(input, args.model, args.temperature)
    info["output"] = task.extract_output(args.prompt, response["content"])
    info["acc"] = task.test_output(id, info["output"])
    info["prompt_tokens"] = response["prompt_tokens"]
    info["completion_tokens"] = response["completion_tokens"]
    return info 


def activity(args, task, infos):
    while True:
        global q
        id = q.get()
        if id is None:
            break

        info = run(args, task, id)
        lock.acquire()
        infos.append(info)
        lock.release()
        q.task_done()


def single_test(args, task, save_path, infos, start_id, end_id):    
    for id in range(start_id, end_id):
        info = run(args, task, id)
        infos.append(info)
        if (id + 1) % 500 == 0 or id == end_id - 1: 
            with open(save_path, 'w') as f:
                f.write(json.dumps(infos, indent=4))


def multi_test(args, task, save_path, infos, start_id, end_id):
    global lock
    lock = threading.Lock()
    threads = []
    for id in range(args.thread_num):
        threads.append(threading.Thread(target=activity, args=(args, task, infos)))
    global q
    q = queue.Queue()
    for id in range(start_id, end_id):
        q.put(id)
    for thread in threads:
        thread.start()
    q.join()
    for id in range(args.thread_num):
        q.put(None)
    for thread in threads:
        thread.join()
    with open(save_path, 'w') as f:
        f.write(json.dumps(infos, indent=4))

def evaluate(infos):
    accs = 0
    num = len(infos)
    for id in range(num):
        if infos[id]["acc"]:
            accs += 1
    accuracy = accs/num
    print("-"*50)
    print("The Accuracy is %.3f." % accuracy)

def test(args):
    task = get_task(args.task_name)

    if args.save_path:
        save_path = args.save_path
    else:
        task_path = f'logs/{args.task_name}'
        if not os.path.isdir(task_path):
            os.makedirs(task_path)
        save_path = f'logs/{args.task_name}/{args.model}_{args.temperature}_{args.prompt}.json'
    
    if args.test_method == 'continue' and os.path.isfile(save_path):
        with open(save_path) as f:
            infos = json.load(f)
    else:
        infos = []

    task_length = len(task)
    start_id = len(infos)
    if args.test_num == 0:
        end_id = task_length
    elif start_id + args.test_num > task_length:
        end_id = task_length
    else:
        end_id = start_id + args.test_num

    if args.thread == 'single':
        single_test(args, task, save_path, infos, start_id, end_id)
    else:
        multi_test(args, task, save_path, infos, start_id, end_id)

    evaluate(infos)


def parse_args():
    args = argparse.ArgumentParser()
    # model
    args.add_argument('--model', type=str, choices=['gpt-3.5-turbo', 'gpt-4'], default='gpt-3.5-turbo')
    args.add_argument('--temperature', type=float, default=0)
    # task
    args.add_argument('--task_name', type=str, default='mmlu')
    args.add_argument('--prompt', type=str, choices=['pure', 'few_shot', 'cot'], default='pure')
    # test
    args.add_argument('--thread', type=str, choices=['single', 'multi'], default='single')
    args.add_argument('--thread_num', type=int, default=4)
    args.add_argument('--save_path', type=str, default=None)
    args.add_argument('--test_method', type=str, choices=['renew','continue'], default='renew')
    args.add_argument('--test_num', type=int, default=0)

    args = args.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    test(args)
