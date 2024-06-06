import twitterScraper
import twitterEmailSender
import time



if __name__ == '__main__':
    twitterScraper.main()
    time.sleep(10)
    twitterEmailSender.main()
