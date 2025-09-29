# ShenNong Series Models
ShenNong-TCM-LLM (the first Traditional Chinese Medicine large language model) Updated Version V2.0


[**中文**](./README.md) | [**English**](./README_EN.md)



<p align="center">
    <br>
    <img src="./pics/ShenNong-TCM_banner.png" width="355"/>
    <br>
</p>
<p align="center">
    <img alt="GitHub" src="https://img.shields.io/github/license/ymcui/Chinese-LLaMA-Alpaca.svg?color=blue&style=flat-square">
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/ymcui/Chinese-LLaMA-Alpaca">
</p>


Large Language Models (LLMs) represented by ChatGPT, GPT-4, etc., have triggered a new wave of research in the field of natural language processing, demonstrating capabilities close to Artificial General Intelligence (AGI), and attracting wide attention from industry and academia.

To promote the development and application of LLMs in the field of Traditional Chinese Medicine (TCM), enhance their knowledge and ability to answer medical consultations in TCM, and advance the inheritance of TCM empowered by large models, we hereby release the **ShenNong** large-scale language model for TCM:

- 🚀 [ShenNong-TCM] :
    - The training data comes from [ShenNong_TCM_Dataset].
    - ChatMed_TCM_Dataset is based on our open-source [TCM Knowledge Graph](https://github.com/ywjawmw/TCM_KG);
    - Using an entity-centric self-instruct method [entity-centric self-instruct](https://github.com/ywjawmw/ShenNong-TCM-LLM/blob/main/crawl_tcm_prompt_symptom_combo.py), we called ChatGPT to generate over 110,000 instruction data centered on TCM [SN-QA](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset);
    - ShenNong-L model is based on LlaMA 7B and fine-tuned with LoRA (rank=16). The fine-tuning code is the same as [ChatMed codebase](https://github.com/michael-wzhu/ChatMed).
    - ShenNong-Q model is based on Qwen 1.8B and fine-tuned with LoRA (rank=16).

We also welcome everyone to follow our other open-source medical LLM projects:
- 🚀 [Intelligent TCM Inheritance and Innovation Assistance Platform](https://github.com/ywjawmw/AI4TCM-Platform) - Intelligent TCM Inheritance and Innovation Platform;
- 🚀 [ChatMed-Consult](https://huggingface.co/michaelwzhu/ChatMed-Consult): Based on [Chinese medical online consultation dataset ChatMed_Consult_Dataset](https://huggingface.co/datasets/michaelwzhu/ChatMed_Consult_Dataset) with 500k+ consultation dialogues plus ChatGPT responses as training data. The backbone is [LlaMA-7b](https://github.com/facebookresearch/llama), integrated with [Chinese-LlaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca) LoRA weights and Chinese extended vocabulary, then fine-tuned with LoRA. We have open-sourced all code.
- 🚀 [ChatMed-MT](https://huggingface.co/michaelwzhu/ChatMed-MT): A multi-turn dialogue version of ChatMed-Consult, where existing open-source Chinese consultation datasets were auto-transformed by LLM to produce more empathetic and detailed doctor responses, improving patient/user experience.
- 🚀 [PromptCBLUE Chinese Medical LLM Benchmark](https://github.com/michaelwzhu/PromptCBLUE): Transforming [CBLUE](https://tianchi.aliyun.com/dataset/95414) into a prompt-learning benchmark to evaluate Chinese medical knowledge and medical text processing ability of LLMs. PromptCBLUE aims to enable a single generative LLM to complete various medical NLP tasks such as medical record structuring, consultation, case writing, etc.



## Updates

2025/09/29 🚀 Released [ShenNong-Q model checkpoint](https://huggingface.co/WJing123/ShenNong-Q), and updated SN-QA v0.2 self-instruct generation code along with the [inference pipeline](./reasoning_pipeline).

2023/6/25 🚀 Released [ShenNong_TCM_Dataset(SN-QA)](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset) v0.2 version with 110k+ data entries; also uploaded [ShenNong-L model checkpoint](https://huggingface.co/michaelwzhu/ShenNong-TCM-LLM). 

2023/6/21 🚀 Released [ShenNong_TCM_Dataset](https://huggingface.co/datasets/michaelwzhu/ShenNong_TCM_Dataset) v0.1, v0.2 version coming soon;




## Quick Start

If you want to fine-tune a large model using [SN-QA dataset](https://huggingface.co/datasets/WJing123/SN-QA), you can refer to the code and training scripts in [ChatMed codebase](https://github.com/michael-wzhu/ChatMed);


## Entity-Centric Self-Instruct Method

The [SN-QA dataset](https://huggingface.co/datasets/WJing123/SN-QA) is fully open-source and available for community use.

We know that compared to general domains, vertical domains are usually knowledge-intensive, and this knowledge is generally centered around entities. Therefore, we propose an entity-centric self-instruct method [entity-centric self-instruct](https://github.com/ywjawmw/ShenNong-TCM-LLM/blob/main/query_crawl_tcm_prompt_symptom_combo.py), which generates instructions around core entities and various intent scenarios in the vertical domain.
If you want to generate based on the [symptom set](https://github.com/ywjawmw/ShenNong-TCM-LLM/blob/main/all_TCM_name.txt) from the *Dictionary of Chinese Medicine Prescriptions*:

```bash
python crawl_tcm_prompt_symptom_combo.py   # Advanced version with more commands
python query_crawl_tcm_prompt_symptom_combo.py  # Paper version
```
You can choose freely, and further optimize and construct on top of this~~~

If you want to generate entity-centric self-instruct based on your local knowledge base/knowledge graph, run the following command (note: configure your own API key in the code file):
```bash
python query_crawl_tcm_KG_prompts.py

```
The “baseline_all_kg_triples.txt” file contains triples from the knowledge graph in plain text, see TCM-KG.


Launch ShenNong for inference:
```bash
sh ./reasoning_pipeline/api.sh

```
## Effect Comparison

### Example: ShenNong-L

By fine-tuning the Chinese LLaMA-7b model with the SN-QA dataset using LoRA, the model achieves significant improvement in answering TCM-related questions. Below we show 5 typical TCM questions with responses from both models. More test cases are available [here](./ShenNong-TCM-LLM-test examples.xls).
| 问诊问题 | 中文LlaMA-7b | ShenNong-TCM                                                                                                                                                                                                                                                                                                                               |
|------|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 可以给我介绍一些治疗太阳经风寒证的中药吗？    |    针灸、推拿等中医疗法，以及草药汤剂都可以用来缓解这种症状。        | 当出现太阳经风寒证时，可以考虑以下几种常用的中药进行治疗。这些药物具有温阳散寒、祛湿止痛的作用，能够缓解症状并促进身体康复。\n\n1. 当归（Angelica sinensis）-有活血化瘀和补气养血作用；\n2. 白芷 (Bai Zi) - 清热解毒，宣通鼻窍；\n3. 金银花(Honeysuckle, Jin Xin Hua)-清热解毒，凉血消肿；\n4. 陈皮 (Chen Pi) - 理气健脾，行滞化痰；\n5. 桂枝 (Gui Zhi) - 发汗解表，调和营卫。\n\n需要注意的是，在使用任何一种中药之前应该咨询医生或中医师的意见以确保安全有效性。                                                 |
| 我感觉浑身乏力，且出现壮热症状。请推荐中医诊断和治疗方法。   |      建议您到医院进行检查以确定病因并制定相应的治疗方案；同时可以采用中药调理身体、增强免疫力等方法缓解病情。     |   根据您的描述，您可能患有感冒或流感等疾病引起的身体不适。建议及时就医并进行中西医疗诊以确定确切的病因及治疗方案。以下是一些常用的中药方剂供参考：\n\n1. 金银花清瘟胶囊：具有解毒、抗病毒的作用，适用于风寒感冒或者流行性感冒等病症。\n\n2. 三黄石膏颗粒：可清热解毒、祛湿止痛，常用于暑湿伤阳所致的身体酸软无力。\n\n3. 五味子饮片：有温肺散寒、益气固表之功效，可用于体虚畏冷、易感恶风的情况。\n\n4. 当归生姜羊肉汤：有益血活络、温暖脾胃作用，适合因寒冷导致的身体疲倦以及食欲不振的人群食用。\n\n需要注意的是，以上药物仅作为辅助治疗措施，具体用药应在医生指导下使用。同时，保持充足休息、饮食清淡、多喝水也是缓解病情的重要方法之一。    |   
| 腹痛怎么办啊？    |      建议您尽快就医，并根据医生的指导进行治疗。      | 如果您感到腹部疼痛，以下是一些可能有用的建议:\n1. 首先休息一下。躺下或坐下来可以减轻症状并帮助身体恢复力量。\n2. 如果您有任何药物过敏史或者正在服用其他药品，请务必咨询医生的意见后再使用这些药膏、止疼剂等缓解痛苦的方法。\n3. 在饮食方面，避免食用辛辣食物和油腻食品，尽量选择清淡易消化的食物来减少肠胃负担。同时多喝水以保持水分平衡。\n4. 如果你的情况比较严重并且持续时间较长，最好去医院就诊寻求专业治疗。                                                                                                                        |
| 大便时带血，怎么办？    |     出现这种情况可能是由于肠道内出血或炎症引起的。建议及时就医检查确诊并进行治疗。       | 如果您的大便中出现了血液，可能是由于以下原因之一引起的：\n\n1.痔疮或肛裂 - 这种情况通常会导致排尿和排泄物的疼痛、瘙痒和其他不适症状。出血量可能会有所不同，从轻微到严重不等。\n2.肠炎或其他肠道疾病- 这些病症可能导致腹泻或者便秘以及其他胃肠道问题。出血量也可能因病情而异。\n3.直肠息肉 - 这是一种在直肠内形成的良性肿瘤状结构，可以引起不同程度的腹痛和出血。\n4.结肠癌 - 这种癌症是常见的消化系统恶性肿瘤类型之一，常常会引起严重的腹部痛苦并伴有贫血等问题。\n5.脱垂子宫颈糜烂 - 如果您正在怀孕并且出现这种情况，这很可能是由于宫颈糜烂所致。这种病变需要及时治疗以避免感染和流产的风险。\n\n建议立即就医寻求医生帮助进行诊断和治疗。  |
| 我牙齿疼痛，同时伴有口臭，有什么方法缓解？    |      建议您及时到口腔医院就诊。牙周炎、龋齿等疾病可能导致牙齿痛和口臭等问题出现     | 您可以尝试以下几种方式来减轻牙痛和减少口腔异味：\n\n1.漱口盐水。将一茶匙食醋加入一杯温水中，搅拌均匀后用来漱口即可。这有助于杀死细菌并减轻口气。\n\n2.使用含氟的洗发剂或去屑产品。这些产品的成分含有一定量的氟化物，可帮助清洁牙齿表面，防止龋齿形成。\n\n3.刷牙时用软毛刷轻轻按摩牙齿边缘以去除食物残渣。\n\n4.定期去看牙医进行检查和治疗。如果出现严重的蛀洞或其他问题，及时修复可能会避免更严重后果。\n\n5.注意饮食健康，少吃甜食、碳酸饮料等易导致蛀牙的食物。|


We can see:
	•	ShenNong-L’s answers are more humane and caring, while the Chinese LlaMA-7b model’s responses may be relatively stiff;
	•	Compared with the Chinese LlaMA-7b model, ShenNong-L’s answers are richer, with more practical suggestions, especially effectively recommending formulas/herbs based on symptoms.

## Disclaimer
	•	The resources related to this project are for academic research only and strictly prohibited for commercial use.
	•	As an intelligent assistant based on language models, ShenNong-TCM cannot replace TCM/Western medical diagnosis or provide medical advice. If needed, please consult a professional doctor or go to a hospital.
	•	The ShenNong-TCM series of models are iterating rapidly, and model weights will be updated regularly.
	•	The ShenNong-TCM series is based on open-source data, whose quality and quantity are limited; its TCM knowledge inevitably has various shortcomings. We will continue to improve and update it.

## Acknowledgments

This project is developed based on open-source projects. We would like to thank the related projects and researchers.
- [ShenNong-TCM-LLM,V1.0](https://github.com/michael-wzhu/ShenNong-TCM-LLM)
- [LlaMA](https://github.com/facebookresearch/llama)
- [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca)
- [Chinese-LlaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca)
- [ChatMed](https://github.com/michael-wzhu/ChatMed)
- [Qwen](https://huggingface.co/Qwen)

The “ShenNong” image in the logo was automatically generated by [midjourney](http://midjourney.com).

