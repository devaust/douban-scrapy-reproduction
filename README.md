# douban-scrapy-reproduction
Reproduction of a crawler project (https://github.com/csuldw/AntSpider) for Dou Ban (www.douban.com).

## Environment
Scrapy: 2.2.0  
Python: 3.7.2  
macOS: Catalina 10.15.5  

## How to Use
You may refer to the original page of the [project](https://github.com/csuldw/AntSpide) for detailed information. If you are an experienced developer, there is no need to follow or execute .sh file. If not, please follow the instructions in the original page. This readme only describes the problems I encountered when reproducing.

## Problem Log
**Q1:** If the IP proxy is not available, chances are when you get an error page from www.douban.com.   
**Solution:** That happens because you send too many requests at a time. Try to slow down your concurrent requests and request speed.  

**Q2:** My Scrapy will examine whether all the crawlers can function correctly when any file in the ../douban/spiders is executed, whereas the code in the ../douban/spiders/movie_meta.py and ../douban/spiders/book_meta.py require data in the table 'subject' in the MySQL, that is, table 'subject' cannot be empty at the beginning, or else scrapy will report error.  
**Solution:** To solve this, run the same file in my repository for the reason I have already deleted related SQL codes. When you have done running ../douban/spiders/movie_meta.py and ../douban/spiders/book_meta.py, add SQL codes which have been deleted.

## Copy Right
I only reproduce this project for study, and do not possess any purpose for profits. If your cpoy rights are violated, please contact me and I will delete this repositary.
