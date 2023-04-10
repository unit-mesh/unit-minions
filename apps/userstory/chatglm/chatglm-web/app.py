from transformers import AutoTokenizer, AutoModel, TrainingArguments, AutoConfig, GenerationConfig
import torch
import torch.nn as nn
from peft import get_peft_model, LoraConfig, TaskType, PeftModel
 
import gradio as gr
 
class CastOutputToFloat(nn.Sequential):
    def forward(self, x): return super().forward(x).to(torch.float32)
 
def format_example(example: dict) -> dict:
    context = f"Instruction: {example['instruction']}\n"
    if example.get("input"):
        context += f"Input: {example['input']}\n"
    context += "Answer: "
    return {"context": context}
 
BASE_MODEL = "/openbayes/input/input1"
LORA_WEIGHTS = "/output/models/lora/chatglm/userstory_detail"
 
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
model = AutoModel.from_pretrained(BASE_MODEL, load_in_8bit=True, trust_remote_code=True, device_map='auto')
model = PeftModel.from_pretrained(model, LORA_WEIGHTS, force_download=True)
# model.supports_gradient_checkpointing = True
# model.gradient_checkpointing_enable()
# model.enable_input_require_grads()
model.lm_head = CastOutputToFloat(model.lm_head)
# model.config.use_cache = False  # silence the warnings. Please re-enable for inference!
 
# peft_config = LoraConfig(
#     task_type=TaskType.CAUSAL_LM, inference_mode=False,
#     r=8,
#     lora_alpha=32, lora_dropout=0.1,
# )
 
# model = get_peft_model(model, peft_config)
# model.is_parallelizable = True
# model.model_parallel = True
 
 
# model.eval()
# if torch.__version__ >= "2":
#     model = torch.compile(model)
 
 
def evaluate(
    instruction,
    input=None,
    temperature=0.1,
    top_p=0.75,
    top_k=40,
    num_beams=4,
    max_new_tokens=128,
    **kwargs,
):
    feature = format_example({"instruction":instruction, "input":input})
    input_text = feature["context"]
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to("cuda")
    with torch.no_grad():
        out = model.generate(
            input_ids=input_ids,
            max_length=150,
            temperature=0
        )
    answer = tokenizer.decode(out[0])
    print("answer:",answer)
    return answer
 
g = gr.Interface(
    fn=evaluate,
    inputs=[
        gr.components.Textbox(
            lines=2, label="Instruction", placeholder="Tell me about alpacas."
        ),
        gr.components.Textbox(lines=2, label="Input", placeholder="none"),
        gr.components.Slider(minimum=0, maximum=1, value=0.1, label="Temperature"),
        gr.components.Slider(minimum=0, maximum=1, value=0.75, label="Top p"),
        gr.components.Slider(minimum=0, maximum=100, step=1, value=40, label="Top k"),
        gr.components.Slider(minimum=1, maximum=4, step=1, value=4, label="Beams"),
        gr.components.Slider(
            minimum=1, maximum=512, step=1, value=128, label="Max tokens"
        ),
    ],
    outputs=[
        gr.inputs.Textbox(
            lines=5,
            label="Output",
        )
    ],
    title="🐘🚿💧 ChatGLM-LoRA",
    description="fintune ChatGLM-6b using low-rank adaptation (LoRA)..",
)
g.queue(concurrency_count=1)
g.launch(server_name="0.0.0.0")
 
# Old testing code follows.
 
"""
if __name__ == "__main__":
    # testing code for readme
    for instruction in [
        "Tell me about alpacas.",
        "Tell me about the president of Mexico in 2019.",
        "Tell me about the king of France in 2019.",
        "List all Canadian provinces in alphabetical order.",
        "Write a Python program that prints the first 10 Fibonacci numbers.",
        "Write a program that prints the numbers from 1 to 100. But for multiples of three print 'Fizz' instead of the number and for the multiples of five print 'Buzz'. For numbers which are multiples of both three and five print 'FizzBuzz'.",
        "Tell me five words that rhyme with 'shock'.",
        "Translate the sentence 'I have no mouth but I must scream' into Spanish.",
        "Count up from 1 to 500.",
    ]:
        print("Instruction:", instruction)
        print("Response:", evaluate(instruction))
        print()
"""