#!/usr/bin/env python3
"""
Gemini API Test Script
Test your API key and see available models
"""

import google.generativeai as genai
from config import GEMINI_API_KEY

def test_gemini_api():
    """Test Gemini API connectivity and list available models"""
    
    print("🧪 Testing Gemini API Configuration...")
    print(f"📋 API Key: {GEMINI_API_KEY[:10]}...{GEMINI_API_KEY[-5:]}")
    print()
    
    try:
        # Configure API
        genai.configure(api_key=GEMINI_API_KEY)
        print("✅ API configured successfully")
        
        # List available models
        print("\n📊 Available Models:")
        models = genai.list_models()
        compatible_models = []
        
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                compatible_models.append(model.name)
                # Mark free tier vs paid models
                if '2.5-pro' in model.name.lower():
                    tier_info = "💰 Paid Only (Premium)"
                elif '2.5-flash-lite' in model.name.lower():
                    tier_info = "🟢 Free Tier (Lite)"
                elif '2.5-flash' in model.name.lower():
                    tier_info = "🟢 Free Tier (Latest)"
                elif any(x in model.name.lower() for x in ['flash', '1.5-pro']):
                    tier_info = "🟢 Free Tier"
                else:
                    tier_info = "❓ Unknown"
                print(f"  ✅ {model.name} ({tier_info})")
            else:
                print(f"  ❌ {model.name} (not compatible)")
        
        if not compatible_models:
            print("  ⚠️  No compatible models found!")
            return False
        
        # Test with preferred model or first available (Updated to use free models)
        preferred_models = [
            'models/gemini-2.5-flash',      # Free tier - latest
            'models/gemini-2.0-flash',      # Free tier - alternative
            'models/gemini-1.5-flash',      # Free tier - reliable
            'models/gemini-1.5-pro'         # Free tier - capable
        ]
        test_model = None
        
        for preferred in preferred_models:
            for available in compatible_models:
                if preferred in available:
                    test_model = available
                    break
            if test_model:
                break
        
        if not test_model:
            test_model = compatible_models[0]
        
        print(f"\n🧪 Testing model: {test_model}")
        
        # Check if this is a paid model and warn user
        if '2.5-pro' in test_model.lower():
            print("⚠️  Warning: This is a premium paid model.")
            print("💡 If you encounter quota errors, the app will fallback to free models.")
        
        model = genai.GenerativeModel(test_model)
        
        # Simple test prompt
        test_prompt = "Say 'API test successful' if you can read this."
        response = model.generate_content(test_prompt)
        
        print(f"📤 Test prompt: {test_prompt}")
        print(f"📥 Response: {response.text}")
        
        print("\n✅ API test completed successfully!")
        print(f"🎯 Using model: {test_model}")
        return True
        
    except Exception as e:
        print(f"\n❌ API test failed: {str(e)}")
        
        if "API_KEY" in str(e) or "api_key" in str(e):
            print("\n🔧 Possible solutions:")
            print("1. Check your API key is correct")
            print("2. Verify the API key has proper permissions")
            print("3. Make sure the API key is not expired")
            
        elif "quota" in str(e).lower() or "limit" in str(e).lower() or "429" in str(e):
            print("\n🔧 Quota/Rate limit issue:")
            print("1. You're trying to use a PAID model (gemini-2.5-pro)")
            print("2. The app will automatically fallback to free models")
            print("3. Wait a few minutes and try again")
            print("4. Check your API usage in Google AI Studio")
            print("5. Consider upgrading to paid tier for premium models")
            
        elif "404" in str(e) or "not found" in str(e).lower():
            print("\n🔧 Model availability issue:")
            print("1. The API might be using a different model version")
            print("2. Try updating google-generativeai package")
            print("3. Check Google AI documentation for current model names")
            
        return False

def main():
    """Main test function"""
    success = test_gemini_api()
    
    if success:
        print("\n🚀 Your API is ready for the Sustainability Compass app!")
        print("📊 The app will use the best available model from your priority list.")
    else:
        print("\n🔧 Please fix the API issues before running the main application.")
        print("\n💡 Note: If gemini-2.5-pro fails (paid model), the app will use free alternatives.")

if __name__ == "__main__":
    main() 