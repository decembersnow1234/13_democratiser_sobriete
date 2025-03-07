import argparse
import os

import ollama

from wslibrary.pdfextraction import taxonomy
from wslibrary.pdfextraction.llm import prompts
from wslibrary.pdfextraction.llm.ollama_extraction import extract_ollama_from_paper
from wslibrary.pdfextraction.pdf.pymu import get_pymupdf4llm


OLLAMA_MODELS  = [m["model"] for m in ollama.list().get("models", [])]
PROMPT_FCTS = {name: obj for name, obj in prompts.__dict__.items() if callable(obj)}
TAXS = {name: obj for name, obj in taxonomy.__dict__.items() if callable(obj)}
def get_args_parser():

    parser = argparse.ArgumentParser(description="Extract taxonomy from a paper pdf file")
    parser.add_argument("--pdf-path", type=str, help="Path to the pdf file")
    parser.add_argument(
        "--model",
        type=str,
        choices=OLLAMA_MODELS,
        help="Model to use for extraction"
    )
    parser.add_argument(
        "--taxonomy",
        type=str,
        choices=list(TAXS.keys()),
        default="Paper",
        help="Taxonomy to use for extraction"
    )
    parser.add_argument(
        "--prompt-type",
        type=str,
        choices=list(PROMPT_FCTS.keys()),
        default="main_parts_prompt",
        help="Type of prompt to use for extraction"
    )
    parser.add_argument(
        "--output-folder",
        type=str,
        default=None,
        help="Name of the folder where the extracted information will be stored"
    )

    return parser.parse_args()

def get_files(path: str) -> list[str]:

    if path.endswith(".pdf"):
        return [path.split("/")[-1]]
    
    elif os.path.isdir(path):
        pdfs = [
            os.path.join(dir_name.replace(path, ""), file)
            for dir_name, _, files in os.walk(path)
            for file in files
            if file.endswith(".pdf")
        ]

        if len(pdfs) == 0:
            raise ValueError("There are no pdfs in the indicated folder.")
        
        return pdfs
    
    else:
        raise ValueError("The indicated path is not a pdf or a folder.")

def get_folders(pdf_files: list[str]) -> set[str]:
    return set(["/".join(file.split("/")[:-1]) for file in pdf_files])

     
def main():
    # get the arguments
    args = get_args_parser()
    input_path = args.pdf_path
    output_path = args.output_folder
    model_name = args.model
    print(f"Using the model: {model_name}")
    tax = TAXS.get(args.taxonomy)

    if (method := args.prompt_type) in PROMPT_FCTS:
        prompt_fct = PROMPT_FCTS.get(method)

    else:
        raise ValueError(f"{args.prompt_type} has not been implemented")
    
    # get the pdfs at the indicated path
    pdfs = get_files(input_path)

    # get the folders that we will need to build
    folders = get_folders(pdfs)

    # loop over the pdfs
    results = {}
    for pdf in pdfs:
        # get the text from the pdf
        content = get_pymupdf4llm(input_path + pdf)
        text = "\n".join([c["text"] for c in content])

        # ini the pdf_dict & save the text
        results[pdf] = {"text": text}

        # make the prompt
        prompt = prompt_fct(text)
        results[pdf]["prompt"] = prompt

        # extract the taxonomy from the extracted texts
        paper = extract_ollama_from_paper(
            prompt,
            model_name,
            tax
        )
        results[pdf]["tax"] = paper
    
    # make the needed dirs and save the information
    for f in folders:
        os.makedirs(output_path + f, exist_ok=True)
    
    for pdf, c in results.items():
        # save the extracted text
        text_path = output_path + pdf.replace(".pdf", ".md")
        with open(text_path, "w") as f:
            f.write(c["text"])

        # save the made prompt
        prompt_path = output_path + pdf.replace(".pdf", "_prompt.md")
        with open(prompt_path, "w") as f:
            f.write(c["prompt"])

        # save the extracted taxonomy
        tax_path = output_path + pdf.replace(".pdf", f"_{model_name}.json")
        with open(tax_path, "w") as f:
            f.write(c["tax"].model_dump_json())


if __name__ == "__main__":
    main()
