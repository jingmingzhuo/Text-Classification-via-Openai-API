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
    print(response["content"][0])
    info["output"] = task.extract_output(args.prompt, response["content"][0])
    info["acc"] = task.test_output(id, info["output"])
    info["prompt_tokens"] = response["prompt_tokens"]
    info["completion_tokens"] = response["completion_tokens"]
    return info 


def tot_run(args, task, id):
    input = task.get_input(args.prompt, id)
    best_thought = ""
    info = {}
    info["id"] = id
    info["step"] = []
    prompt_tokens, completion_tokens = 0, 0

    for step in range(task.steps):
        step_info = {}
        response = get_response(input, temperature=args.generate_temperature, n=args.generate_num, stop=task.stop[step])
        thoughts = [best_thought + thought for thought in response["content"]]
        vote_input = task.get_input_vote(id, thoughts)
        vote_response = get_response(prompt=vote_input, temperature=args.temperature, n=1)
        choice = task.extract_vote(vote_response["content"][0]) - 1
        best_thought += thoughts[choice]
        input += best_thought + task.stop[step] + ' '
        step_info["step"] = step
        step_info["generate"] = response["content"]
        step_info["choice"] = choice
        step_info["best_thought"] = best_thought
        info["step"].append(step_info)
        prompt_tokens += response["prompt_tokens"] + vote_response["prompt_tokens"]
        completion_tokens += response["completion_tokens"] + vote_response["completion_tokens"]

    input = task.get_input_after_tot(id, best_thought)
    response = get_response(input, temperature=args.temperature)
    info["output"] = task.extract_output(args.prompt, response["content"][0])
    info["acc"] = task.test_output(id, info["output"])
    info["prompt_tokens"] = prompt_tokens + response["prompt_tokens"]
    info["completion_tokens"] =  completion_tokens + response["completion_tokens"]
    return info


def activity(args, task, infos, start_id, end_id, save_path):
    while True:
        global q
        id = q.get()
        if id is None:
            break

        if args.prompt == 'tot':
            info = tot_run(args, task, id)
        else:
            info = run(args, task, id)
        
        lock.acquire()
        print("-"*100)
        global cnt
        print("Test Progress %d / %d ." % (cnt-start_id+1, end_id-start_id))
        cnt += 1
        print(info)
        infos.append(info)
        if (id + 1) % 100 == 0 or id == end_id - 1: 
            with open(save_path, 'w') as f:
                f.write(json.dumps(infos, indent=4))
        lock.release()

        q.task_done()


def single_test(args, task, save_path, infos, start_id, end_id):    
    for id in range(start_id, end_id):
        if args.prompt == 'tot':
            info = tot_run(args, task, id)
        else:
            info = run(args, task, id)
        print("-"*100)
        print("Test Progress %d / %d ." % (id-start_id+1, end_id-start_id))
        print(info)
        infos.append(info)
        if (id + 1) % 100 == 0 or id == end_id - 1: 
            with open(save_path, 'w') as f:
                f.write(json.dumps(infos, indent=4))


def multi_test(args, task, save_path, infos, start_id, end_id):
    global lock, q, cnt
    lock = threading.Lock()
    q = queue.Queue()
    cnt = 0
    threads = []
    for id in range(args.thread_num):
        threads.append(threading.Thread(target=activity, args=(args, task, infos, start_id, end_id, save_path)))
    for id in range(start_id, end_id):
        q.put(id)
    for thread in threads:
        thread.start()
    q.join()
    for id in range(args.thread_num):
        q.put(None)
    for thread in threads:
        thread.join()


def evaluate(infos):
    accs = 0
    num = len(infos)
    for id in range(num):
        if infos[id]["acc"]:
            accs += 1
    accuracy = accs/num
    print("-"*100)
    print("The Accuracy is %.3f ." % accuracy)


def test(args):
    task = get_task(args)
    if args.save_path:
        save_path = args.save_path
    else:
        task_path = f'logs/{args.task_name}'
        if not os.path.isdir(task_path):
            os.makedirs(task_path)
        if args.prompt == 'tot':
            save_path = f'logs/{args.task_name}/{args.model}_{args.temperature}_{args.prompt}_{args.generate_temperature}_{args.generate_num}.json'
        else:
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

    print("-"*100)
    print("The test is over .")


def parse_args():
    args = argparse.ArgumentParser()
    # model
    args.add_argument('--model', type=str, choices=['gpt-3.5-turbo', 'gpt-4'], default='gpt-3.5-turbo')
    args.add_argument('--temperature', type=float, default=0)
    args.add_argument('--generate_temperature', type=float, default=1.5)
    # task
    args.add_argument('--task_name', type=str, default='mmlu')
    args.add_argument('--task_file_path', type=str)
    args.add_argument('--prompt', type=str, choices=['pure', 'few-shot', 'cot', 'tot'], default='pure')
    # test
    args.add_argument('--thread', type=str, choices=['single', 'multi'], default='single')
    args.add_argument('--thread_num', type=int, default=4)
    args.add_argument('--save_path', type=str, default=None)
    args.add_argument('--test_method', type=str, choices=['renew','continue'], default='renew')
    args.add_argument('--test_num', type=int, default=0)
    args.add_argument('--generate_num', type=int, default=5)

    args = args.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    print("-"*100)
    print(args)
    test(args)
