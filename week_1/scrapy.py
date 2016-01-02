# -*- coding:utf-8 -*-
__author__ = 'cy'

import requests

class Scrapy:
    def __init__(self,type):
        self.sum = 0
        self.counts = 0
        self.size = 10
        self.type = type
        self.product_dict = {'carLoans':'CAR_LOAN_REQUEST',
                             'enterpriseLoans':'ENTERPRISE_ACCOUNTS_RECEIVABLE',
                             'products':'products'}
        self.session = requests.session()

    def get_num(self,url):
        r = self.session.request('head',url)
        self.counts = r.headers['X-Record-Count']

    def get_invest(self,url,type,index):
        sum = 0
        data = {'from':index,'productType':type,'size':self.size} if type != 'products' else {'from':index,'size':self.size}
        r = self.session.request('get',url,headers = { 'Content-Type':'application/json'},params = data)
        for i in r.json():
            sum += i['currentInvestmentAmount']
        return sum

    def cal_sum(self):
        sum = 0
        url = 'https://www.madailicai.com/p2p/service/'+self.type
        self.get_num(url)
        for i in range(0,int(self.counts),self.size):
            sum += self.get_invest(url,self.product_dict[self.type],i)
        self.sum = sum

    def __str__(self):
        return '%s counts: %s sum: %d' % (self.type,self.counts,self.sum)

if __name__ == '__main__':
    sum = 0
    for i in ('carLoans','enterpriseLoans','products'):
        product = Scrapy(i)
        product.cal_sum()
        print(product)
        sum += product.sum
    print('-'*40+'\n'+'sum: '+str(sum))

