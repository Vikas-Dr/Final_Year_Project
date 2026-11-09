import json
import os
import urllib.request
import urllib.error
from typing import Any, Dict, Iterator, Optional

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")
AI_PROVIDER = os.getenv("AI_PROVIDER", "rule-based").lower()


def check_ollama_status() -> Dict[str, Any]:
    """
    Check if local Ollama server is running and accessible.
    """
    try:
        url = f"{OLLAMA_BASE_URL}/api/tags"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                models = [m.get("name") for m in data.get("models", [])]
                return {
                    "status": "online",
                    "url": OLLAMA_BASE_URL,
                    "available_models": models,
                    "configured_model": OLLAMA_MODEL,
                }
    except Exception as err:
        return {
            "status": "offline",
            "url": OLLAMA_BASE_URL,
            "configured_model": OLLAMA_MODEL,
            "error": str(err),
            "note": "Install and run Ollama locally (`ollama serve` & `ollama pull llama3`) to enable Local LLM AI reasoning.",
        }

    return {"status": "offline", "url": OLLAMA_BASE_URL}


def generate_ollama_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    timeout: int = 15,
    options: Optional[Dict[str, Any]] = None,
    keep_alive: Optional[str] = None,
) -> Optional[str]:
    """
    Send prompt to local Ollama API (/api/generate) and return text response.
    Returns None if Ollama is unreachable.
    """
    target_model = model or OLLAMA_MODEL
    url = f"{OLLAMA_BASE_URL}/api/generate"

    payload = {
        "model": target_model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3, **(options or {})},
    }
    if system_prompt:
        payload["system"] = system_prompt
    if keep_alive:
        payload["keep_alive"] = keep_alive

    try:
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=req_data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                res_json = json.loads(response.read().decode("utf-8"))
                return res_json.get("response", "").strip()
    except Exception as err:
        print(f"[Ollama Call Warning] Failed to reach Ollama: {err}")
        return None

    return None


def llm_analyze_resume(resume_text: str, target_role: str = "General Software Engineer") -> Optional[Dict[str, Any]]:
    """
    Use local LLM to parse and extract detailed resume skills, match score, and recommendations.
    """
    system_prompt = (
        "You are an expert AI HR Recruiter and Resume Analyst. Respond strictly in valid JSON format."
    )
    prompt = f"""
Analyze the following candidate resume for the role of '{target_role}'.
Return a valid JSON object with:
- "summary": concise 2-sentence summary grounded only in evidence in the resume
- "strengths": array of specific, evidenced strengths (strings)
- "missing_skills": array of role skills that are explicitly required but not evidenced

Do not return scores, invent qualifications, or treat an absent detail as proof of a lack of ability. Scores are calculated separately using a fixed, transparent rubric.

Candidate Resume Text:
\"\"\"
{resume_text[:3000]}
\"\"\"
"""
    raw_response = generate_ollama_completion(prompt, system_prompt=system_prompt)
    if not raw_response:
        return None

    try:
        # Extract JSON block if surrounded by markdown fences
        json_match = re_extract_json(raw_response)
        if json_match:
            return json_match
    except Exception as err:
        print(f"[Ollama Parsing Error] {err}")

    return None


def llm_evaluate_interview_answer(
    question: str,
    answer: str,
    question_type: str = "theory",
    expected_answer: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Use local LLM to evaluate candidate theory or coding answer.
    """
    system_prompt = "You are an expert AI Technical Interviewer. Evaluate candidate answers strictly in valid JSON format."
    prompt = f"""
Evaluate the candidate's answer for the following {question_type} question.

Question: "{question}"
Candidate Answer: "{answer}"
Expected Core Concepts: "{expected_answer or 'Technical accuracy, clarity, completeness'}"

Return a valid JSON object with:
- "score": integer score between 0 and 100
- "feedback": 1-2 sentence constructive feedback explaining the score
- "key_points_covered": array of concepts candidate mentioned correctly
- "missing_concepts": array of concepts candidate missed
"""
    raw_response = generate_ollama_completion(prompt, system_prompt=system_prompt)
    if not raw_response:
        return None

    return re_extract_json(raw_response)


def rule_based_chat_agent(user_message: str) -> Dict[str, Any]:
    """Return the local instant-response fallback when Ollama is unavailable."""
    msg_lower = user_message.lower()
    if any(k in msg_lower for k in ["resume", "cv", "ats", "upload"]):
        reply = (
            "I am your AI Resume Assistant. Upload a clear PDF or DOCX with skills, experience, projects, and education."
        )
    elif any(k in msg_lower for k in ["interview", "question", "prep", "practice", "mcq", "coding"]):
        reply = (
            "Open Take Interview to practice role-specific MCQs, technical questions, and coding exercises."
        )
    elif any(k in msg_lower for k in ["verify", "face", "id", "biometric", "security"]):
        reply = (
            "Upload a clear photo ID and selfie in Identity Check to complete verification before your interview."
        )
    else:
        reply = (
            "I can help with resume improvements, job matching, and technical interview preparation."
        )

    return {
        "reply": reply,
        "provider": "Rule-Based AI Assistant",
        "status": "fallback",
    }


def llm_chat_agent(user_message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """AI Agent powered by local Ollama, with a rule-based fallback."""
    system_prompt = (
        "You are a concise AI career assistant. Help with resumes, job matching, and interview preparation. "
        "Answer in one direct sentence of at most 18 words."
    )
    
    prompt = f"User Question: {user_message}\n"
    if context:
        prompt += f"Context: {json.dumps(context)}\n"
        
    raw_response = generate_ollama_completion(
        prompt,
        system_prompt=system_prompt,
        timeout=120,
        options={"num_predict": 24, "num_ctx": 2048},
        keep_alive="24h",
    )
    
    if raw_response:
        return {
            "reply": raw_response,
            "provider": f"ollama ({OLLAMA_MODEL})",
            "status": "online"
        }
    
    return rule_based_chat_agent(user_message)


def stream_llm_chat_agent(
    user_message: str,
    context: Optional[Dict[str, Any]] = None,
) -> Iterator[Dict[str, Any]]:
    """Stream chat tokens from Ollama, with a rule-based fallback if it is unavailable."""
    system_prompt = (
        "You are a concise AI career assistant. Help with resumes, job matching, and interview preparation. "
        "Answer in one direct sentence of at most 18 words."
    )
    prompt = f"User Question: {user_message}\n"
    if context:
        prompt += f"Context: {json.dumps(context)}\n"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "system": system_prompt,
        "stream": True,
        "keep_alive": "24h",
        "options": {
            "temperature": 0.2,
            "num_predict": 24,
            "num_ctx": 2048,
        },
    }
    request = urllib.request.Request(
        f"{OLLAMA_BASE_URL}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    emitted_tokens = False
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            for line in response:
                if not line.strip():
                    continue
                chunk = json.loads(line.decode("utf-8"))
                token = chunk.get("response", "")
                if token:
                    emitted_tokens = True
                    yield {"token": token}
                if chunk.get("done"):
                    yield {
                        "done": True,
                        "provider": f"ollama ({OLLAMA_MODEL})",
                        "status": "online",
                    }
                    return
    except (OSError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as err:
        print(f"[Ollama Stream Warning] Failed to complete chat: {err}")
        if emitted_tokens:
            yield {"error": "The AI response was interrupted. Please try again.", "done": True}
            return

    if not emitted_tokens:
        fallback = rule_based_chat_agent(user_message)
        yield {
            "reply": fallback["reply"],
            "provider": fallback["provider"],
            "status": fallback["status"],
            "done": True,
        }


def re_extract_json(text: str) -> Optional[Dict[str, Any]]:
    """Helper to extract JSON dict from LLM response text."""
    try:
        # Try direct parse
        return json.loads(text)
    except Exception:
        pass

    # Search for markdown ```json ... ``` or first { ... }
    try:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            json_str = text[start : end + 1]
            return json.loads(json_str)
    except Exception:
        pass

    return None
