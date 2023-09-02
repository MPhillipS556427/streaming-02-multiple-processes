# Import from Python Standard Library
import csv
import socket
import time
import logging
import random

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Declare program constants (typically constants are named with ALL_CAPS)
HOST = "localhost"
PORT = 9999
ADDRESS_TUPLE = (HOST, PORT)
INPUT_FILE_NAME = "United-States-fertility-rates.csv"
OUTPUT_FILE_NAME = "out9.txt"

# Define program functions (bits of reusable code)
def prepare_message_from_row(row):
    """Prepare a binary message from a given row."""
    Year, Birth_Number, General_Fertility_Rate, Crude_Birth_Rate = row
    # use an fstring to create a message from our data
    # notice the f before the opening quote for our string?
    fstring_message = f"[{Year}, {Birth_Number}, {General_Fertility_Rate}, {Crude_Birth_Rate}]"

    # prepare a binary (1s and 0s) message to stream
    MESSAGE = fstring_message.encode()
    logging.debug(f"Prepared message: {fstring_message}")
    return MESSAGE

def stream_row(input_file_name, address_tuple):
    """Read from input file and stream data."""
    logging.info(f"Starting to stream data from {input_file_name} to {address_tuple}.")

    # Create a file object for input (r = read access)
    with open(input_file_name, "r") as input_file:
        reader = csv.reader(input_file, delimiter=",")  # Create a CSV reader object

        # use socket enumerated types to configure our socket object
        # Set our address family to (IPV4) for 'internet'
        # Set our socket type to UDP (datagram)
        ADDRESS_FAMILY = socket.AF_INET
        SOCKET_TYPE = socket.SOCK_DGRAM # Using UDP (datagram)

        # Call the socket constructor, socket.socket()
        # A constructor is a special method with the same name as the class
        # Use the constructor to make a socket object
        # and assign it to a variable named `sock_object`
        sock_object = socket.socket(ADDRESS_FAMILY, SOCKET_TYPE)

        rows = list(reader)
        rows.reverse()  # Reverse the order of rows

        last_processed_index = 0  # Track the index of the last processed row

        with open(OUTPUT_FILE_NAME, "w") as output_file:
            logging.info(f"Opened for writing: {OUTPUT_FILE_NAME}.")
            while last_processed_index < len(rows):  # Continue streaming until all rows are processed
                row = rows[last_processed_index]
                MESSAGE = prepare_message_from_row(row)
                sock_object.sendto(MESSAGE, address_tuple)
                output_file.write(str(MESSAGE) + "\n")
                logging.info(f"Sent and wrote: {MESSAGE} on port {PORT}.")

                last_processed_index += 1  # Update the index of the last processed row

                # Generate one record every 1-3 seconds
                sleep_time = random.uniform(1, 3)  # Random sleep between 1 and 3 seconds
                time.sleep(sleep_time)  # Sleep for the random time

# ---------------------------------------------------------------------------
# If this is the script we are running, then call some functions and execute code!
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        logging.info("===============================================")
        logging.info("Starting fake streaming process.")
        stream_row(INPUT_FILE_NAME, ADDRESS_TUPLE)
        logging.info("Streaming complete!")
        logging.info("===============================================")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
