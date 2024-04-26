class Configs:
    BASE_URL = "<base_url_of_the_website>"
    PAGE_URL = "<Initial_page_url_where you want to start crawling>"
    PAGE_COMMON_ID = "<Selenium_will_wait_till_this_Id_is_Visible>"
    CONTENT_COMMON_ID = "<ID_containing_the_content_that_needs_to_be_crawled>"
    MAX_WAITING_TIME = 20
    DATA_DIR = "page_content" # data will be daved here
    TOP_ELEMENT = "div" # top element tag
    PERSIST_DIR = "./storage" 
    IMAGE_DIR = "static"
