# scripts/setup.py
# Run this ONCE after pip install to download ML models

import subprocess
import sys

def run(cmd):
    print(f"\n▶ Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=False)
    if result.returncode != 0:
        print(f"⚠️  Command failed (may be ok): {cmd}")
    return result.returncode == 0

def main():
    print("=" * 55)
    print("  SkillMap AI — ML Model Setup")
    print("=" * 55)

    # 1. spaCy English model
    print("\n📥 Step 1: Downloading spaCy English model...")
    success = run(f"{sys.executable} -m spacy download en_core_web_sm")
    if success:
        print("✅ spaCy en_core_web_sm downloaded")
    else:
        print("❌ spaCy download failed. Try manually:")
        print(f"   {sys.executable} -m spacy download en_core_web_sm")

    # 2. BERT model — download via sentence-transformers
    print("\n📥 Step 2: Downloading BERT model (all-MiniLM-L6-v2)...")
    print("   This is ~80MB. Please wait...")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        test = model.encode(["Python developer"])
        print(f"✅ BERT model downloaded and tested (embedding dim: {test.shape[1]})")
    except Exception as e:
        print(f"❌ BERT download failed: {e}")
        print("   Try manually: pip install sentence-transformers")

    # 3. NLTK data
    print("\n📥 Step 3: Downloading NLTK data...")
    try:
        import nltk
        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
        nltk.download("averaged_perceptron_tagger", quiet=True)
        print("✅ NLTK data downloaded")
    except Exception as e:
        print(f"⚠️  NLTK download failed: {e}")

    # 4. Test MongoDB connection
    print("\n📥 Step 4: Testing MongoDB connection...")
    try:
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)
        client.server_info()
        print("✅ MongoDB connected at localhost:27017")
    except Exception:
        print("⚠️  MongoDB not running.")
        print("   Install MongoDB: https://www.mongodb.com/try/download/community")
        print("   Or use MongoDB Atlas (free cloud): https://www.mongodb.com/atlas")
        print("   App will still work without MongoDB (results won't be saved)")

    # 5. Create .env if missing
    import os
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            print("\n✅ .env file created from .env.example")
        else:
            with open(".env", "w") as f:
                f.write("MONGODB_URI=mongodb://localhost:27017\n")
                f.write("DB_NAME=skillmap_ai\n")
            print("\n✅ .env file created with defaults")
    else:
        print("\n✅ .env file already exists")

    print("\n" + "=" * 55)
    print("  Setup Complete!")
    print("=" * 55)
    print("\nTo start the backend:")
    print(f"  {sys.executable} -m uvicorn main:app --reload --port 8000")
    print("\nTo test the API:")
    print("  Open browser: http://127.0.0.1:8000")

if __name__ == "__main__":
    main()
