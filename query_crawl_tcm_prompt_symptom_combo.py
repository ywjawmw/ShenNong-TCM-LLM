import openai
import json
import sys
import random
import time

openai.api_key = "sk-XXX"  # you must provide your OpenAI API key before crawling
openai.proxy = "http://127.0.0.1:33210"

if not openai.api_key:
    raise ValueError("OpenAI API key not provided. Please set the 'openai.api_key' variable.")


def return_random_prompt():
    system_prompt = "你需要尽可能给出多样化的，与中医(中国传统医学),中药等相关的任务指令并生成问题。要求:\n"

    # generate random topics

    sym_list, prescription_list = [], []
    sym_prescription_list = []  # source data
    sym_combine_list, prescription_list = [], []
    with open("all_TCM_name.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().split("\t")
            sym_prescription_list.append(line)
            sym_combine, prescription = line[0], line[1]
            if sym_combine not in sym_combine_list:
                sym_combine_list.append(sym_combine)

            sym_new = []
            for sym in sym_combine.split(" "):
                if sym not in sym_new:
                    sym_new.append(sym)
            sym_new = ",".join(sym_new)
            sym_list.append(sym_new)

            prescription_new = []
            for herb in prescription.split(" "):
                if herb not in prescription_new:
                    prescription_new.append(herb)
            prescription_new = ",".join(prescription_new)
            prescription_list.append(prescription_new)

    pres = random.sample(sym_list, 1)[0]
    case = random.sample(sym_prescription_list, 1)[0]
    system_prompt += "1. 根据如下症状组合进行问题生成：" + ", ".join(case[0].split(" ")) + "\n"
    # generate random tasks
    task_list = ["中医知识推理", "中药推荐", "中医诊断", "方剂推荐", "方剂点评", "治疗推荐", "中医方剂解读", ]
    system_prompt += "2. 表述多样化，结合真实问题，问题类型多样化，例如：" + "、".join(task_list) + "等。\n"
    system_prompt += "请给出满足条件的5个严格满足输出格式的问题，不要有其他内容的输出：\n"
    system_prompt += '以下是输出格式的示例："query": "根据症状，中医如何诊断病情？"\n'

    print(system_prompt)
    return system_prompt


def make_openai_request():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # here we use `gpt-3.5-turbo` model, while Stanford-Alpaca uses `text-davinci-003`
            messages=[
                {"role": "user", "content": return_random_prompt()},
            ]
        )
        return response
    except Exception as e:
        print(e)
        print("RateLimitError: API rate limit exceeded. Retrying after delay...")
        time.sleep(5)  # 等待一段时间后重试
        return make_openai_request()  # 递归调用自身进行重试


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python crawl_prompt.py <output_file>")
        exit(1)

    output_file = open(sys.argv[1], 'w', encoding="utf-8")

    MAX_EPOCHS = 10000 # number of data to generate (each prompt contains 20 JSON-formatted data)
    for k in range(MAX_EPOCHS):
        response = make_openai_request()
        print(response["choices"])
        output_file.write(response["choices"][0]["message"]["content"] + '\n')
    output_file.close()

    # nohup python3 -u self_instruct/crawl_tcm_prompts.py self_instruct/file_5.txt > file_5_log.log &
    # nohup python3 -u self_instruct/crawl_tcm_prompts.py self_instruct/file_6.txt > file_6_log.log &
    # nohup python3 -u self_instruct/crawl_tcm_prompts.py self_instruct/file_7.txt > file_7_log.log &

    # nohup python3 -u self_instruct/crawl_tcm_prompts.py self_instruct/file_8.txt > file_8_log.log &
    #
