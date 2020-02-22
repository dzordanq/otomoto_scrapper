import scrapy
from otomoto.items import CarItem

class OtomotoSpider(scrapy.Spider):
    allowed_domains = ['www.otomoto.pl']
    name = "otomoto"
    start_urls = ["https://www.otomoto.pl/osobowe/"]
    make = ''
    
    # def start_requests(self):
    #     url = "https://www.otomoto.pl/osobowe/"
    #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        makes_list = response.xpath("//select[@id='param571']/option/@value").getall()[1:]
        
        for make in makes_list:
            self.make = make
            page = self.start_urls[0] + self.urljoin(make)
            yield scrapy.Request(url=page, callback=self.parse_page)
            
                
    
    def parse_page(self, response):
        for i in range(1, self.get_last_page_number(response)):
            page = self.urljoin(response.url,'?page={0}'.format(i))
            yield scrapy.Request(url=page, callback=self.parse_url)

    def parse_url(self, response):          
        car_urls = response.xpath("//div[@class='offers list']/article/div[@class='offer-item__photo  ds-photo-container']/a/@href").getall()
        for car_url in car_urls:
            yield response.follow(url=car_url, callback=self.get_car_parameters)
            
    
            
    @staticmethod
    def get_car_parameters(response):
        car_item = CarItem()
        
        adv_data = response.xpath("//span[@class='offer-meta__value']/text()").getall()  
        car_price = response.xpath("//div[@class='offer-price']/@data-price").get()
        car_details = response.xpath("//ul[@class='offer-params__list']/li/span/text()").getall()
      
        car_details_values = response.xpath("//ul[@class='offer-params__list']/li[@class='offer-params__item']/div[@class='offer-params__value']/a/text()[normalize-space()] | //ul[@class='offer-params__list']/li[@class='offer-params__item']/div[@class='offer-params__value']/text()[normalize-space()]").getall()
        car_details_values = [x.strip() for x in car_details_values]

        car_item['Data'] = adv_data[0]
        car_item['Id'] = adv_data[1]
        car_item['Cena'] = car_price
        for item, value in zip(car_details, car_details_values):
            car_item[item] = value
        
        return car_item
            
    @staticmethod
    def get_current_page_number(response):
        return int(response.xpath("//input[@id='pageParam']/@data-currentpage").get())
        
    @staticmethod
    def get_last_page_number(response):
        try:
            last_page_number = int(response.xpath("//ul[@class='om-pager rel']//span[@class='page']/text()").getall()[-1])
            return last_page_number
        except:
            return 1
        
    
    @staticmethod
    def urljoin(*args):
        return "/".join(map(lambda x: str(x).rstrip('/'), args))