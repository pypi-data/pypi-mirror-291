from typing import Optional

def get_info(provider: Optional[str] = None):
    """
    Returns information about available LLM models, including descriptions and image upload support.
    
    Args:
        provider (str, optional): The LLM provider to filter by ('openai', 'anthropic', or 'google').
                                  If not provided, returns info for all providers.
    
    Returns:
        dict: Information about LLM models for the specified provider or all providers.
    """
    all_models_info = {
        "openai": {
            "gpt-3.5-turbo-0125": {
                "description": "Efficient and cost-effective model for various tasks.",
                "image_upload": False
            },
            "gpt-4-turbo-2024-04-09": {
                "description": "Advanced model with improved reasoning and broader knowledge.",
                "image_upload": True
            },
            "gpt-4o-2024-05-13": {
                "description": "Optimized GPT-4 model with enhanced performance.",
                "image_upload": True
            },
            "gpt-4o-mini-2024-07-18": {
                "description": "Compact version of GPT-4o optimized for faster responses and is the cheapest option.",
                "image_upload": True
            }
        },
        "anthropic": {
            "claude-3-5-sonnet-20240620": {
                "description": "Balanced model for general-purpose tasks.",
                "image_upload": True
            },
            "claude-3-opus-20240229": {
                "description": "Most capable Claude model for complex tasks.",
                "image_upload": True
            },
            "claude-3-sonnet-20240229": {
                "description": "Versatile model balancing performance and speed.",
                "image_upload": True
            },
            "claude-3-haiku-20240307": {
                "description": "Fastest Claude model, ideal for quick responses.",
                "image_upload": True
            }
        },
        "google": {
            "gemini-1.5-flash-latest": {
                "description": "Fast and efficient model for various applications.",
                "image_upload": False
            }
        }
    }
    
    if provider:
        return {provider: all_models_info.get(provider, {})}
    return all_models_info


# Original LLM_MODELS dictionary for backwards compatibility
LLM_MODELS = {
    "openai": {
        "gpt3_5": "gpt-3.5-turbo-0125",
        "gpt4": "gpt-4-turbo-2024-04-09",
        "gpt4_omni": "gpt-4o-2024-05-13",
        "gpt4_omni_mini": "gpt-4o-mini-2024-07-18"
    },
    "anthropic": {
        "claude3_5_sonnet": "claude-3-5-sonnet-20240620",
        "claude3_opus": "claude-3-opus-20240229",
        "claude3_sonnet": "claude-3-sonnet-20240229",
        "claude3_haiku": "claude-3-haiku-20240307"
    },
    "google": {
        "gemini1_5_flash": "gemini-1.5-flash-latest"
    }
}
