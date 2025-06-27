import time
from src.train_loop_crf import parse_arguments, train

start_time = time.time()
train(parse_arguments())
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")
