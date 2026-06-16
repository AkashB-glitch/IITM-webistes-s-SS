import os
import json
import time
import google.genai as genai
from PIL import Image

def run_vision_analysis():
    print("Starting AI Vision Analysis on all screenshots...")
    
    API_KEY = os.environ.get("GEMINI_API_KEY")
    if not API_KEY:
        print("ERROR: GEMINI_API_KEY is not set.")
        return "Failed: Missing API Key"

    client = genai.Client()
    
    # We use flash because it is much faster and cheaper for bulk image processing
    model_id = 'gemini-2.5-flash'
    
    screenshot_dir = "raw_screenshots"
    if not os.path.exists(screenshot_dir):
        print(f"ERROR: {screenshot_dir} directory not found.")
        return "Failed: No screenshots directory found."

    vision_results = []
    image_files = [f for f in os.listdir(screenshot_dir) if f.endswith('.png')]
    
    print(f"Found {len(image_files)} screenshots to analyze.")

    for i, filename in enumerate(image_files, 1):
        filepath = os.path.join(screenshot_dir, filename)
        domain = filename.replace(".png", "")
        print(f"[{i}/{len(image_files)}] Analyzing {domain}...", end=" ", flush=True)
        
        try:
            img = Image.open(filepath)
            
            prompt = (
                "You are a cybersecurity brand-protection agent. Look at this website screenshot. "
                "1. Does it contain the IIT Madras (IITM) logo? "
                "2. Does it look like a legitimate university page, a student blog, or a suspicious/phishing site? "
                "Respond in a strict JSON format exactly like this: "
                "{\"has_iitm_logo\": true/false, \"site_type\": \"legitimate/suspicious/blog/unknown\", \"risk_score\": 1-10, \"reasoning\": \"brief explanation\"}"
            )
            
            response = client.models.generate_content(
                model=model_id,
                contents=[prompt, img]
            )
            
            # Simple JSON extraction
            resp_text = response.text.strip()
            if resp_text.startswith("```json"):
                resp_text = resp_text[7:-3]
            elif resp_text.startswith("```"):
                resp_text = resp_text[3:-3]
                
            result_data = json.loads(resp_text)
            result_data["domain"] = domain
            vision_results.append(result_data)
            
            risk = result_data.get("risk_score", 0)
            print(f"Done (Risk: {risk}/10)")
            
            # Small sleep to prevent rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"Error analyzing: {str(e)}")
            vision_results.append({
                "domain": domain,
                "error": str(e)
            })

    with open("vision_results.json", "w") as f:
        json.dump(vision_results, f, indent=4)
        
    print("Vision Analysis complete! Saved to vision_results.json")
    return "Vision analysis completed successfully. Results saved to vision_results.json"

if __name__ == "__main__":
    run_vision_analysis()
