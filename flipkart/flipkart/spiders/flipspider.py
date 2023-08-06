import scrapy


class FlipspiderSpider(scrapy.Spider):
    name = "flipspider"
    allowed_domains = ["flipkart.com"]
    start_urls = ["https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DRealme",
                  "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DPoco",
                  "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DSamsung",
                  "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DOneplus",
                  "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DRedmi",
                  "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DOppo",
                  "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DVivo",
                  "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DMi",
                  "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DInfinix",
                  "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DApple",
                  "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DHonor",
                  "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DAsus",
                  "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DIqoo",
                  "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DMotorola"
                  ]

    def parse(self, response):
        pages = response.css('div ._2kHMtA')

        for page in pages:
            new_page = page.css('a._1fQZEK ::attr(href)').get()

            new_page_url = 'https://www.flipkart.com' + new_page
            yield response.follow(new_page_url, callback = self.parse_phone)


        next_page = response.css('a._1LKTO3 ::attr(href)').get()

        if next_page is not None:    
            next_page_url = 'https://www.flipkart.com' + next_page
        yield response.follow(next_page_url, callback = self.parse)

    def parse_phone(self, response):
        phone = response.css('div ._1YokD2')

        
        yield{
                'Name' : phone.css('h1 .B_NuCI::text').get(),
                'Price' : phone.css('div ._30jeq3::text').get(),
                'Overall Rating' : phone.css('div ._3LWZlK::text').get(),
                'Total no of rating' : phone.xpath("//span[@class='_1lRcqv']/following-sibling::span/text()")[0].extract(),
                'Total no of reviews' : phone.xpath("//span[@class='_13vcmD']/following-sibling::span/text()").get().strip(),
                '5 star rating' : phone.css('div ._1uJVNT::text')[0].extract(),
                '4 star rating' : phone.css('div ._1uJVNT::text')[1].extract(),
                '3 star rating' : phone.css('div ._1uJVNT::text')[2].extract(),
                '2 star rating' : phone.css('div ._1uJVNT::text')[3].extract(),
                '1 star rating' : phone.css('div ._1uJVNT::text')[4].extract(),
                'Camera Rating' : phone.css('svg ._2Ix0io::text')[0].extract(),
                'Battery Rating' : phone.css('svg ._2Ix0io::text')[1].extract(),
                'Display Rating' : phone.css('svg ._2Ix0io::text')[2].extract(),
                'Design Rating' : phone.css('svg ._2Ix0io::text')[3].extract(),
                'Variant' : phone.css('div ._21Ahn-::text')[0].extract(),
                'Display' : phone.css('div ._21Ahn-::text')[1].extract(),
                'Camera' : phone.css('div ._21Ahn-::text')[2].extract(),
                'Offers' : response.xpath("//span[@class='u8dYXW']/following-sibling::span/text()").extract()
            }