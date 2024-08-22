import sdb_connector as sdb_testing
import time

print("Hello, World!")
x = sdb_testing.sum_as_string(1, 2)
print(x)

start = time.time()
result = sdb_testing.select_measuremnt_data("192.168.2.63", "run_info:01J4XRFVTY9XSBCECW2NHWHMGK")
end = time.time()
print("Time taken: ", end - start)