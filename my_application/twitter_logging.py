import logging


def add_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)
    handler_tweet = logging.StreamHandler()
    logger.addHandler(handler_tweet)
    logger.setLevel('DEBUG')
    formatter_twitter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)s | %(message)s')
    handler_tweet.setFormatter(formatter_twitter)
    return logger
