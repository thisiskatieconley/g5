"""openai_helper.py
Simple wrapper around the OpenAI Python client used for richer follow-up answers.

This module provides a single function `ask_openai(question, recipe, system_prompt=None)` which
returns a string answer or raises an exception on failure. If the environment variable
`OPENAI_API_KEY` is not set, the function returns None so callers can fall back to offline
behaviour.
"""
import os
from typing import Optional, Dict, Any

try:
    import openai
except Exception:
    openai = None


def ask_openai(question: str, recipe: Dict[str, Any], system_prompt: Optional[str] = None, model: str = "gpt-4o-mini") -> Optional[str]:
    """Ask OpenAI for a richer, contextual answer about a recipe.

    Args:
        question: User's free-form question
        recipe: The selected recipe dictionary (title, ingredients, steps, time, diets)
        system_prompt: Optional system prompt to guide the model
        model: Model name to use (default: compact GPT-4o-mini)

    Returns:
        Answer text when successful, or None when API key/library is missing or on error.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or openai is None:
        return None

    openai.api_key = api_key

    # Build a compact context for the model
    context = []
    sys_p = system_prompt or (
        "You are a helpful cooking assistant. Answer concisely and use numbered steps when describing actions."
    )
    context.append({"role": "system", "content": sys_p})

    # Add recipe summary as context
    recipe_summary = f"Title: {recipe.get('title')}\nTime: {recipe.get('time')}\nIngredients: {', '.join(recipe.get('ingredients', []))}\nSteps: {' | '.join(recipe.get('steps', []))}"
    context.append({"role": "user", "content": f"Recipe context:\n{recipe_summary}"})
    context.append({"role": "user", "content": f"User question: {question}"})

    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=context,
            max_tokens=500,
            temperature=0.6,
        )
        # Extract answer
        choices = resp.get("choices")
        if not choices:
            return None
        text = choices[0].get("message", {}).get("content")
        return text.strip() if text else None
    except Exception:
        return None
