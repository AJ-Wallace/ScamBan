import discord
import os

from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

classifier = None

def load_model():
    global classifier
    
    model_name = "ealvaradob/bert-finetuned-phishing"
    
    try:
        print("Loading Classification Model...")
        
        try:
            print("Attempting to load from local cache...")
            tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
            model = AutoModelForSequenceClassification.from_pretrained(
                model_name, 
                local_files_only=True
            )
            print("Loaded from local cache!")
            
        except Exception as e:
            print(f"Local cache failed: {e}")
            print("Falling back to network download...")
            
            # Fallback to network download
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        # Create pipeline
        classifier = pipeline(
            "text-classification",
            model=model,
            tokenizer=tokenizer,
            device=-1
        )
        
        print("Model loaded successfully!")
        print("-"*50)
        return True
        
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

@client.event
async def on_ready():
    print(f"Successfully Logged In As {client.user}")
    
    if not load_model():
        print("Failed to load model. Shutting down...")
        await client.close()

@client.event
async def on_message(msg):
    if msg.author == client.user or classifier is None:
        return
    
    try:
        result = classifier(msg.content)
        
        print(f"Author: {msg.author}")
        print(f"Message: {msg.content}")
        print(f"Classification: {result}")
        print("-" * 50)
        
        if result and len(result) > 0:
            prediction = result[0]
            if prediction.get('label') == 'phishing' and prediction.get('score', 0) > 0.9:
                print(f"Potential phishing detected from {msg.author}")
                await msg.add_reaction("⚠️")
                
    except Exception as e:
        print(f"Error classifying message: {e}")

if __name__ == "__main__":
    client.run(TOKEN)