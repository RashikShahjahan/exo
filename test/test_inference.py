import asyncio
from pathlib import Path
from exo.download.hf.hf_shard_download import HFShardDownloader
from exo.inference.shard import Shard
from exo.inference.inference_engine import get_inference_engine

async def test_model():
    print("Starting test_model")
    # Define a test shard for llama-3.1-8b which supports tinygrad
    shard = Shard(
        model_id="mlabonne/Meta-Llama-3.1-8B-Instruct-abliterated",  
        start_layer=0,
        end_layer=31,  
        n_layers=32  
    )
    print(f"Created shard: {shard}")

    try:
        # Initialize the shard downloader
        print("Initializing shard downloader...")
        shard_downloader = HFShardDownloader()
        print("Shard downloader initialized")

        # Create the tinygrad inference engine
        print("Creating tinygrad inference engine...")
        engine = get_inference_engine("tinygrad", shard_downloader)
        print(f"Created inference engine: {engine.__class__.__name__}")

        # Test prompt
        prompt = "Write a short poem about AI:"
        print(f"Using test prompt: {prompt}")
        
        print("Starting inference...")
        result, state, is_eos = await engine.infer_prompt("test1", shard, prompt)
        print(f"Inference completed. Result shape: {result.shape}, State: {state}, EOS: {is_eos}")
        
        if result.shape == (1, 1):
            print("Decoding token...")
            next_token = await engine.tokenizer.decode(result[0])
            print(f"Input prompt: {prompt}")
            print(f"Next token: {next_token}")
            print(f"Is end of sequence: {is_eos}")
        else:
            print("Unexpected output shape:", result.shape)
    except Exception as e:
        print(f"Error in test_model: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
if __name__ == "__main__":
    asyncio.run(test_model())

