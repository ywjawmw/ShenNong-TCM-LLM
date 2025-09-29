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
    system_prompt = "你需要尽可能给出多样化的，与中医(中国传统医学),中药等相关的，任务指令和对应的回答。我们将用于人工评估ChatGPT模型对指令的完成情况。要求:\n"

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
    system_prompt += "1. 根据如下症状组合进行指令生成：" + ", ".join(case[0].split(" ")) + "\n"
    # generate random tasks
    task_list = ["中医知识推理", "中药推荐", "中医诊断", "方剂推荐", "方剂点评", "治疗推荐", "中医方剂解读", ]
    system_prompt += "2. 表述多样化，结合真实问题；指令类型多样化，例如：" + "、".join(task_list) + "等。\n"
    system_prompt += "3. 中药和方剂是两个不同的概念，必须区分。方剂是由多个中药组成，中药表示的是单个草药。\n"
    # "例如：<input>包含症状组合：" + ",".join(case[0].split(" ")) + \
    # "，<output>中包含多个中药：" + ",".join(case[1].split(" ")) + "。\n"
    system_prompt += "4. 生成的内容中包含两个字段: <input>是一个适当且涉及真实情况的指令，<output>是针对指令的回复。\n"
    system_prompt += "5. <input>最后应包含以下的内容：“请使用→符号解释分析过程”。\n"
    system_prompt += "6. 要求<output>回答中第一部分是：给出中药或者方剂。\n"
    system_prompt += "7. 要求<output>回答中第二部分是：展示推理过程。要求在推理过程中详细地分析症状、证候、治法、方剂和中药信息。\n"
    system_prompt += "8. 要求<output>回答中第三部分是：总结症状、证候、治法和中药四类信息，格式举例：“症状：指令输入的症状”，四类信息之间使用→符号连接。\n"
    system_prompt += "9. 如果遇到无法处理的指令（只靠文本无法回答），给出无法处理的回复。\n"
    system_prompt += "10. 除非特别要求，请使用中文，指令可以是命令句、疑问句、或其他合适的类型。\n"
    system_prompt += "11. <input>应提供实质性的内容，具有挑战性。字数不超过" + str(
        random.randint(80, 120)) + "字。\n"
    system_prompt += "12. <output>应该是对指令的适当且真实的回应，符合中医诊疗习惯，不能只回复答应或拒绝请求。如果需要额外信息才能回复时，请努力预测用户意图并尝试回复。\n"
    system_prompt += "请给出满足条件的5条JSON格式数据：\n"

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

    MAX_EPOCHS = 1000  # number of data to generate (each prompt contains 20 JSON-formatted data)
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
