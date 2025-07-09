import streamlit as st
import requests
import json
import random
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Page config
st.set_page_config(
    page_title="Jasper AI Clone - $1.5B in 100 Lines",
    page_icon="📝",
    layout="wide"
)

# Mock responses for free demo (no API needed)
MOCK_RESPONSES = {
    "blog_post": [
        "# The Future of {topic}\n\n{topic} is revolutionizing the way we think about {industry}. With cutting-edge innovation and groundbreaking technology, {topic} offers unprecedented opportunities for growth and success.\n\n## Why {topic} Matters\n\nIn today's fast-paced digital landscape, {topic} has emerged as a game-changer. Companies that embrace {topic} are seeing remarkable results:\n\n- Increased efficiency by 300%\n- Enhanced customer satisfaction\n- Streamlined operations\n- Competitive advantage\n\n## The Bottom Line\n\n{topic} isn't just a trend—it's the future. Don't get left behind in the {industry} revolution.",
        
        "# Unlocking the Power of {topic}\n\nDiscover how {topic} is transforming the {industry} landscape. From startups to Fortune 500 companies, everyone is talking about {topic}.\n\n## The {topic} Revolution\n\n{topic} represents a paradigm shift in how we approach {industry}. This innovative solution delivers:\n\n✅ Seamless integration\n✅ Scalable architecture\n✅ Real-time analytics\n✅ Cost-effective implementation\n\n## Ready to Get Started?\n\nThe {topic} opportunity won't wait. Join thousands of industry leaders who are already leveraging {topic} to drive unprecedented growth."
    ],
    
    "social_media": [
        "🚀 Ready to transform your {industry} game? {topic} is the secret weapon top companies use to stay ahead!\n\n#Innovation #Growth #Success #{topic}",
        
        "💡 Hot take: {topic} isn't just changing {industry}—it's completely revolutionizing it.\n\nWhat's your experience with {topic}? Drop your thoughts below! 👇\n\n#{topic} #GameChanger #FutureOfWork",
        
        "🔥 BREAKING: {topic} just hit a new milestone! \n\nThis is exactly why smart {industry} leaders are investing in {topic} NOW.\n\nDon't miss out on the {topic} revolution! 🚀"
    ],
    
    "email_marketing": [
        "Subject: Don't Miss Out on the {topic} Revolution!\n\nHey there,\n\nHave you heard about {topic}? It's completely transforming the {industry} space, and I didn't want you to miss out.\n\nHere's what makes {topic} so special:\n• Saves you 10+ hours per week\n• Increases ROI by 250%\n• Trusted by 50,000+ professionals\n\nReady to experience {topic} for yourself?\n\n[Get Started Today]\n\nBest regards,\nThe {topic} Team",
        
        "Subject: Your {industry} Success Starts Here\n\nHi {name},\n\nStruggling with {industry} challenges? You're not alone.\n\nThat's exactly why we created {topic}—to help professionals like you achieve breakthrough results.\n\n✅ Proven results in 30 days\n✅ No technical expertise required\n✅ 24/7 support included\n\nJoin thousands who've already transformed their {industry} approach with {topic}.\n\n[Start Your Journey]\n\nCheers,\nYour {topic} Team"
    ],
    
    "product_description": [
        "Introducing {topic}—the game-changing solution that's revolutionizing {industry}.\n\nDesigned for modern professionals who demand excellence, {topic} combines cutting-edge technology with user-friendly design to deliver unprecedented results.\n\n🌟 KEY FEATURES:\n• Advanced AI-powered insights\n• Seamless workflow integration\n• Real-time collaboration tools\n• Enterprise-grade security\n\nWhether you're a startup founder or Fortune 500 executive, {topic} adapts to your unique needs and scales with your success.\n\nReady to experience the future of {industry}? Try {topic} today!",
        
        "Meet {topic}: Your Secret Weapon for {industry} Success\n\nTired of outdated {industry} solutions? {topic} is here to change everything.\n\nPowerful yet simple, {topic} delivers:\n✨ Instant results\n✨ Zero learning curve\n✨ 99.9% uptime guarantee\n✨ World-class support\n\nJoin the {topic} revolution and discover why industry leaders choose us over the competition.\n\nGet started in minutes, see results in days."
    ]
}

# API providers with free tiers
API_PROVIDERS = {
    "Mock (Free)": {"endpoint": "mock", "key_needed": False},
    "OpenAI": {"endpoint": "https://api.openai.com/v1/chat/completions", "key_needed": True},
    "Anthropic Claude": {"endpoint": "https://api.anthropic.com/v1/messages", "key_needed": True},
    "Google Gemini": {"endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent", "key_needed": True},
    "Hugging Face - GPT2": {"endpoint": "https://api-inference.huggingface.co/models/gpt2", "key_needed": True},
    "Hugging Face - Llama2": {"endpoint": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf", "key_needed": True},
    "Hugging Face - Flan-T5": {"endpoint": "https://api-inference.huggingface.co/models/google/flan-t5-large", "key_needed": True},
    "Hugging Face - CodeLlama": {"endpoint": "https://api-inference.huggingface.co/models/codellama/CodeLlama-7b-Instruct-hf", "key_needed": True}
}

# Content templates (the "AI innovation")
TEMPLATES = {
    "Blog Post": {
        "description": "SEO-optimized blog posts that drive traffic",
        "inputs": ["topic", "industry", "tone"],
        "mock_key": "blog_post"
    },
    "Social Media": {
        "description": "Viral social media posts that boost engagement",
        "inputs": ["topic", "industry", "platform"],
        "mock_key": "social_media"
    },
    "Email Marketing": {
        "description": "High-converting email campaigns",
        "inputs": ["topic", "industry", "audience"],
        "mock_key": "email_marketing"
    },
    "Product Description": {
        "description": "Compelling product descriptions that sell",
        "inputs": ["topic", "industry", "features"],
        "mock_key": "product_description"
    }
}

def make_api_call(provider, template_type, inputs):
    """Make API call to selected provider"""
    if provider == "Mock (Free)":
        # Return mock response
        template = TEMPLATES[template_type]
        responses = MOCK_RESPONSES[template["mock_key"]]
        response = random.choice(responses)
        
        # Replace placeholders
        for key, value in inputs.items():
            if value:
                response = response.replace(f"{{{key}}}", value)
        
        return response
    
    # For real API calls
    prompt = f"Write a {template_type.lower()} about {inputs.get('topic', 'technology')} for the {inputs.get('industry', 'business')} industry."
    
    if provider == "OpenAI":
        return call_openai(prompt, inputs.get('api_key'))
    elif provider == "Anthropic Claude":
        return call_claude(prompt, inputs.get('api_key'))
    elif provider == "Google Gemini":
        return call_gemini(prompt, inputs.get('api_key'))
    elif provider.startswith("Hugging Face"):
        # Extract the model URL from the provider name
        model_urls = {
            "Hugging Face - GPT2": "https://api-inference.huggingface.co/models/gpt2",
            "Hugging Face - Llama2": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf",
            "Hugging Face - Flan-T5": "https://api-inference.huggingface.co/models/google/flan-t5-large",
            "Hugging Face - CodeLlama": "https://api-inference.huggingface.co/models/codellama/CodeLlama-7b-Instruct-hf"
        }
        model_url = model_urls.get(provider)
        return call_huggingface(prompt, inputs.get('api_key'), model_url)
    
    return "API call failed. Try the mock version or check your API key."

def call_openai(prompt, api_key):
    """Call OpenAI API"""
    if not api_key:
        return "OpenAI API key required"
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"OpenAI API error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"OpenAI API error: {str(e)}"

def call_claude(prompt, api_key):
    """Call Anthropic Claude API"""
    if not api_key:
        return "Claude API key required"
    
    try:
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["content"][0]["text"]
        else:
            return f"Claude API error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Claude API error: {str(e)}"

def call_gemini(prompt, api_key):
    """Call Google Gemini API"""
    if not api_key:
        return "Gemini API key required"
    
    try:
        # Fix 1: Use the correct endpoint URL
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        # Fix 2: Correct request structure
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": 500,
                "temperature": 0.7
            }
        }
        
        # Fix 3: Add proper headers
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            # Fix 4: Handle the response structure properly
            if "candidates" in result and len(result["candidates"]) > 0:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return "No content generated by Gemini"
        else:
            return f"Gemini API error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Gemini API error: {str(e)}"

def call_huggingface(prompt, api_key, model_url=None):
    """Call Hugging Face API with different models"""
    if not api_key:
        return "Hugging Face API key required"
    
    # Default model if none specified
    if not model_url:
        model_url = "https://api-inference.huggingface.co/models/gpt2"
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Different models need different input formats
        if "llama" in model_url.lower():
            # Llama models prefer chat format
            data = {
                "inputs": f"<s>[INST] {prompt} [/INST]",
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "do_sample": True,
                    "top_p": 0.9,
                    "repetition_penalty": 1.1
                }
            }
        elif "flan-t5" in model_url.lower():
            # Flan-T5 is instruction-tuned
            data = {
                "inputs": f"Generate content: {prompt}",
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
        elif "codellama" in model_url.lower():
            # CodeLlama for code generation
            data = {
                "inputs": f"# {prompt}\n",
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.2,  # Lower temp for code
                    "do_sample": True
                }
            }
        else:
            # GPT2 and other general models
            data = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "do_sample": True,
                    "top_p": 0.9,
                    "repetition_penalty": 1.1
                }
            }
        
        response = requests.post(model_url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            
            # Handle different response formats
            if isinstance(result, list) and len(result) > 0:
                if "generated_text" in result[0]:
                    generated = result[0]["generated_text"]
                    # Clean up the response (remove input prompt if included)
                    if generated.startswith(prompt):
                        generated = generated[len(prompt):].strip()
                    return generated
                elif "text" in result[0]:
                    return result[0]["text"]
            elif isinstance(result, dict):
                if "generated_text" in result:
                    return result["generated_text"]
                elif "text" in result:
                    return result["text"]
            
            return "No content generated by Hugging Face"
            
        elif response.status_code == 503:
            return "Model is loading, please wait a few minutes and try again"
        else:
            return f"Hugging Face API error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Hugging Face API error: {str(e)}"

# Main UI
st.title("🚀 Jasper AI Clone - $1.5B in 100 Lines")

st.markdown("""
### The $1.5B Content Writer That's Just Templates + API Calls

**Jasper AI raised $125M for... this.** Choose your template, fill in the blanks, get "AI-generated" content.

**Spoiler alert:** It's just ChatGPT with marketing templates. Where's my $1.5B? 🤔
""")

# Sidebar for API selection
st.sidebar.title("⚙️ API Configuration")
selected_provider = st.sidebar.selectbox("Choose AI Provider:", list(API_PROVIDERS.keys()))

api_key = None
if API_PROVIDERS[selected_provider]["key_needed"]:
    api_key = st.sidebar.text_input(f"Enter {selected_provider} API Key:", type="password")
    
    if selected_provider == "OpenAI":
        st.sidebar.info("Get free API key: https://platform.openai.com/api-keys")
    elif selected_provider == "Anthropic Claude":
        st.sidebar.info("Get free API key: https://console.anthropic.com/")
    elif selected_provider == "Google Gemini":
        st.sidebar.info("Get free API key: https://makersuite.google.com/app/apikey")
    elif selected_provider == "Hugging Face":
        st.sidebar.info("Get free API key: https://huggingface.co/settings/tokens")

# Main content area
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 Choose Your Template")
    
    selected_template = st.selectbox("Content Type:", list(TEMPLATES.keys()))
    
    template_info = TEMPLATES[selected_template]
    st.info(template_info["description"])
    
    # Dynamic inputs based on template
    inputs = {}
    for input_field in template_info["inputs"]:
        if input_field == "topic":
            inputs[input_field] = st.text_input("Topic:", placeholder="AI, SaaS, Marketing, etc.")
        elif input_field == "industry":
            inputs[input_field] = st.text_input("Industry:", placeholder="Technology, Healthcare, Finance, etc.")
        elif input_field == "tone":
            inputs[input_field] = st.selectbox("Tone:", ["Professional", "Casual", "Excited", "Authoritative"])
        elif input_field == "platform":
            inputs[input_field] = st.selectbox("Platform:", ["LinkedIn", "Twitter", "Facebook", "Instagram"])
        elif input_field == "audience":
            inputs[input_field] = st.text_input("Target Audience:", placeholder="CEOs, Marketers, Developers, etc.")
        elif input_field == "features":
            inputs[input_field] = st.text_area("Key Features:", placeholder="List the main features or benefits")
    
    inputs["api_key"] = api_key
    
    generate_button = st.button("🎯 Generate Content", type="primary")

with col2:
    st.subheader("📄 Generated Content")
    
    if generate_button:
        with st.spinner(f"Generating with {selected_provider}..."):
            result = make_api_call(selected_provider, selected_template, inputs)
            
            st.markdown("**Generated Content:**")
            st.markdown(result)
            
            # Show the "innovation"
            st.markdown("---")
            st.markdown("**🔍 What Just Happened:**")
            st.code(f"""
# The "$1.5B Innovation":
template = "{selected_template}"
inputs = {str({k: v for k, v in inputs.items() if k != 'api_key'})}
api_call = "{selected_provider}"

# That's it. That's the whole business model.
""")

# Footer with reality check
st.markdown("---")
st.markdown("""
### 💡 Reality Check

**What Jasper AI Actually Is:**
- Templates with placeholder variables ✅
- API calls to OpenAI/Claude/Gemini ✅  
- Pretty UI with form inputs ✅
- Marketing buzzwords ✅

**What It's NOT:**
- Revolutionary AI technology ❌
- Proprietary models ❌
- Worth $1.5B ❌

**Time to Build This:** ~2 hours  
**Jasper's Funding:** $125M
**My clone:**  Where's MY $125M? 🤔

---
*Built by someone who sees through the AI BS.*
""")

# Add some stats for dramatic effect
st.markdown("---")
st.markdown("### 📊 The Numbers Don't Lie")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Jasper's Funding", "$125M", "💸")
    
with col2:
    st.metric("This Clone's Budget", "$0", "🎯")
    
with col3:
    st.metric("Development Time", "2 hours", "⚡")
    
with col4:
    st.metric("Lines of Code", "~500", "🔥")

# Show the source code
with st.expander("📁 View Source Code (The Real Innovation)"):
    st.code("""
# The entire "AI content generation" business model:

def jasper_ai_clone(template, inputs, api_key):
    prompt = f"Write a {template} about {inputs['topic']}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# That's it. $1.5B valuation for this function.
""")