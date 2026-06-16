import os
import sys
import json
import subprocess
import google.genai as genai

# =====================================================================
# AGENT TOOL DEFINITIONS
# These are the actions the AI can take autonomously.
# =====================================================================

def discover_subdomains() -> str:
    """Runs the tool to discover IITM subdomains and saves them to iitm_urls.txt. Returns the execution status."""
    print("[Tool execution] discover_subdomains()...", flush=True)
    try:
        result = subprocess.run([sys.executable, "find_subdomains.py"], capture_output=True, text=True)
        return "Subdomain discovery completed successfully. File iitm_urls.txt was generated."
    except Exception as e:
        return f"Error running subdomain discovery: {str(e)}"

def run_port_scan() -> str:
    """Runs the Nmap/Port scanning tool on the discovered subdomains. Saves results to results.json."""
    print("[Tool execution] run_port_scan()...", flush=True)
    try:
        result = subprocess.run([sys.executable, "run_scan.py"], capture_output=True, text=True)
        return "Port scanning completed. File results.json was generated."
    except Exception as e:
        return f"Error running port scan: {str(e)}"

def capture_screenshots() -> str:
    """Runs the Playwright screenshot tool to capture images of all subdomains and check WAF health. Saves to website_health.json and raw_screenshots/."""
    print("[Tool execution] capture_screenshots()...", flush=True)
    try:
        result = subprocess.run([sys.executable, "take_screenshots.py"], capture_output=True, text=True)
        return "Screenshot capture completed. Data saved to website_health.json and raw_screenshots folder."
    except Exception as e:
        return f"Error running screenshot capture: {str(e)}"

def analyze_security_data() -> str:
    """Reads the website_health.json and results.json to analyze security posture. Returns a summary JSON string of the raw data to the agent."""
    print("[Tool execution] analyze_security_data()...", flush=True)
    try:
        with open("website_health.json", "r") as f:
            health_data = json.load(f)
        
        # Summarize data so it fits in the LLM context and is easy to read
        summary = []
        for site in health_data:
            summary.append({
                "domain": site.get("website"),
                "status_category": site.get("category"),
                "status_code": site.get("status_code"),
                "open_ports": site.get("open_ports", []),
                "waf_retries": site.get("retries", 0)
            })
        return json.dumps(summary)
    except Exception as e:
        return f"Error reading data: {str(e)}"

def run_vision_scanner() -> str:
    """Runs the multimodal vision scanner on captured screenshots to detect IITM logos and calculate risk scores. Saves results to vision_results.json."""
    print("[Tool execution] run_vision_scanner()...", flush=True)
    try:
        result = subprocess.run([sys.executable, "vision_scanner.py"], capture_output=True, text=True)
        return "Vision analysis completed successfully. Results saved to vision_results.json"
    except Exception as e:
        return f"Error running vision scanner: {str(e)}"

def save_report(report_content: str) -> str:
    """Saves the agent's final markdown risk report to final_risk_report.md. Use this tool once the analysis is complete."""
    print("[Tool execution] save_report()...", flush=True)
    try:
        with open("final_risk_report.md", "w", encoding="utf-8") as f:
            f.write(report_content)
        return "Report successfully saved to final_risk_report.md"
    except Exception as e:
        return f"Error saving report: {str(e)}"


# =====================================================================
# AGENT ORCHESTRATOR LOOP
# =====================================================================

def main():
    # Setup API Key
    API_KEY = os.environ.get("GEMINI_API_KEY")
    if not API_KEY:
        print("[ERROR] Please set the GEMINI_API_KEY environment variable.")
        print("Run: $env:GEMINI_API_KEY=\"your-api-key\"")
        sys.exit(1)

    print("[START] Initializing Autonomous Agent...")

    # Define the Model with Tools
    client = genai.Client()
    
    system_instruction = (
        "You are an autonomous cybersecurity AI agent responsible for protecting the IIT Madras brand. "
        "Your objective is to run the complete security pipeline by invoking the appropriate tools in this specific order:\n"
        "1. discover_subdomains()\n"
        "2. run_port_scan()\n"
        "3. capture_screenshots()\n"
        "4. run_vision_scanner()\n"
        "5. analyze_security_data()\n"
        "6. save_report(report_content)\n\n"
        "Work autonomously. Execute one tool after another based on the responses. "
        "When you analyze the data, compile a professional Security Risk Report in Markdown. "
        "Identify highly suspicious sites (e.g. non-standard open ports like 3306, down/error statuses, or high WAF retries) "
        "and save the report using the save_report tool. Do NOT make up any data."
    )
    
    tools = [
        discover_subdomains,
        run_port_scan,
        capture_screenshots,
        run_vision_scanner,
        analyze_security_data,
        save_report
    ]

    # Enable automatic function calling so the agent can run tools on its own
    chat = client.chats.create(model="gemini-2.5-flash", config=dict(tools=tools, system_instruction=system_instruction))
    
    prompt = "Please execute the full security pipeline for IIT Madras subdomains. Gather all data, analyze it, and save the final report."
    
    print(f"\n[USER DIRECTIVE] '{prompt}'")
    print("[AGENT] Agent is thinking and executing tools autonomously...\n" + "-"*60)
    
    # This will automatically trigger the tool loop
    response = chat.send_message(prompt)
    
    print("-" * 60)
    print("[SUCCESS] Agent Execution Complete!")
    print("\n[AGENT REPORT]")
    print(response.text)

if __name__ == "__main__":
    main()
