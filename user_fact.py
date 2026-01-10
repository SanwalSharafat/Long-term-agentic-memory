# Building Factual Memory
# Packages installed
from google import genai
import os
from dotenv import load_dotenv
from google.genai import types
import json

# Basic setup
load_dotenv ()
GEMINI_API_KEY = os.getenv ("GEMINAI_KEY")
client = genai.Client (api_key = GEMINI_API_KEY)

def llm_extract(query: str):
    config = types.GenerateContentConfig(
        system_instruction="""
        Extract stable factual information from the message.
        Ignore temporary and emotional information.

        Return ONLY valid JSON in this format:
        {
         "singular": { },
         "multi": {},
         "structured": {}
        }

        Rules:
        - singular: one-value facts (overwrite)
        - multi: multi-value facts (append, no duplicates)
        - structured: nested objects (education, work)
        """,
        response_mime_type="application/json",
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query,
            config=config,
        )

        if not response.text :
            return None
        return response.text
    
    except Exception as e:
        print("LLM extraction failed:", e)
        return None
        
def safe_load_json (jsonData : str) -> dict :
    if not jsonData:
        print ("No text json data found.")
        return {}
    
    try:
        return json.loads (jsonData)
    
    except json.JSONDecodeError as jde:
        print(f"JSON format error: {jde.msg} at line {jde.lineno}")
        return {}
    
    except Exception as e:
        print(f"Unexpected error loading JSON: {e}")
        return {}
    

def save_to_json (data, filename="factual.json"):
    if data is None:
        print("No data provided to save.")
        return False

    try:
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully saved to {filename}")
        return True

    except (TypeError, ValueError) as e:
        print(f"Data serialization error: {e}")
        return False
    except PermissionError:
        print(f"Permission denied: Cannot write to {filename}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while saving: {e}")
        return False


def load_json_file(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            if os.stat(path).st_size == 0:
                return {}
            return json.load(f)
            
    except json.JSONDecodeError as e:
        print(f"JSON format error in {path}: {e}")
        return {}
    
    except OSError as e:
        print(f"File system error reading {path}: {e}")
        return {}
 
def merge_memory (old, new) :

    if not old:
        return new
    
    if not new:
        return old
    
    else:
        # Singular -- > overwright
        for k,v in new.get ("singular", {}).items ():
            old.setdefault ("singular", {}) [k] = v

        # multi ----- > append without duplicates
        for k,v in new.get ("multi", {}).items ():
            old.setdefault ("multi", {}).setdefault (k, [])

            if isinstance (v, list):
                for item in v:
                    if item not in old ["multi"] [k]:
                        old ["multi"] [k].append (item)
            else:
                if v not in old ["multi"] [k]:
                    old ["multi"] [k].append (v)     

        # structured ----- > append objects
        for k,v in new.get ("structured", {}). items ():
            old.setdefault ("structured", {}). setdefault (k, [])
            if isinstance (v, list):
                old ["structured"][k]. extend (v)
            else:
                old ["structured"][k]. append (v)    

        return old

def main():
    print("ASSISTANT: Memory System Active. Type 'exit' to stop.")
    while True:
        try:
            user = input("\nYOU: ")

            if user.lower() in ["stop", "exit", "quit", "end"]:
                print("ASSISTANT: Goodbye!")
                break

            old_memory = load_json_file("factual.json")
            
            raw_text = llm_extract(user)
            
            new_data = safe_load_json(raw_text)

            if new_data:
                updated_memory = merge_memory(old_memory, new_data)
                
                save_to_json(updated_memory)
                print("ASSISTANT: Memory updated.")
            else:
                print("ASSISTANT: No new facts detected.")

        except (EOFError, KeyboardInterrupt):
            print("\nASSISTANT: Goodbye!")
            break
        except Exception as e:
            print(f"\nAn unhandled error occurred: {e}\n")
            break

if __name__ == "__main__":
    main ()