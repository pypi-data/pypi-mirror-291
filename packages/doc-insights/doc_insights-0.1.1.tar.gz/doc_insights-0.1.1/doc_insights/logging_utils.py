def log_message(message, log_file="scan_log.txt"):
    """
    Logs a message to both the console and a file.

    This function writes the provided message to a specified log file
    and prints the message to the console. It appends the message to
    the log file, ensuring that existing log entries are preserved.

    Args:
        message (str): The message to log. This message will be both 
                       printed to the console and written to the log file.
        log_file (str, optional): The path to the log file where the message 
                                  should be written. Defaults to "scan_log.txt".

    Returns:
        None
    """
    with open(log_file, "a") as log:
        log.write(message + "\n")
    print(message)
