# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re

class SmgPipeline(object):
    
    paper_list = []
    abstract_list = []

    
    def open_spider(self, spider):
        self.file = open('{}.txt'.format(spider.fn), 'wb')
        self.paper_pool = self.load_pool('paper')
        self.abst_pool = self.load_pool('abst')

    
    def process_item(self, item, spider):
        if item['paper_type'] == 1: # 1 = abstract
            abst = ""
            item['authors'] = self.process_name(item['authors']);            
            [item['publication'], abst] = self.process_pub_abst\
                                                 (item['publication'])
            if abst not in self.abst_pool:
                print abst+" not in pool, pushing to stack."
                self.abstract_list.append(item)
        elif item['doi'] not in self.paper_pool:
            item['authors'] = self.process_name(item['authors']);            
            item['publication'] = self.process_pub_paper(item['publication'])
            self.paper_list.append(item)

        return item


    def close_spider(self, spider):
        self.paper_list.sort(key=lambda x: x['paper_date'], reverse=True)
        self.abstract_list.sort(key=lambda x: x['paper_date'], reverse=True)
        paper_pool_file = open('paper.txt', 'ab');
        abst_pool_file = open('abst.txt', 'ab');
        s = ''

        for paper in self.paper_list:
            s = (', '.join(paper['authors'])+' ('+str(paper['paper_date'])+
                   '), '+paper['paper_name']+', '+paper['publication']+
                   ', doi: '+paper['doi']+'.\n')
            self.file.write(s)
            paper_pool_file.write(s)
        for abst in self.abstract_list:
            s = (', '.join(abst['authors'])+' ('+str(abst['paper_date'])+
                   '), '+abst['paper_name']+', '+abst['publication']+
                   ' ('+abst['journal']+').\n')
            self.file.write(s)
            abst_pool_file.write(s)
        self.file.close()
        paper_pool_file.close()
        abst_pool_file.close()
                            

    def process_name(self, name_list):
        result = []
        count = 0
        for name in name_list:
            [ last, first ] = name.encode('ascii', 'ignore').split(',')
            first_list = first.split('.')
            first = ''
            for l in first_list:
                if len(l) != 0:
                    if l[0] == '-':
                        first += l[0:2]+'. '
                    else:
                        first += (l[0] + '. ')
            if count == 0:
                result.append(last+', '+first.rstrip())
            else:
                result.append(first+last)
            count = count+1
        return result


    def process_pub_paper(self, publication):
        tokens = publication.split(',')
        journal = tokens[0];
        volume = ''
        page = ''
        issue = ''
        for token in tokens:
            token = token.lower()
            if(token.find('volume') > 0):
                volume = (', '+token.lstrip('volume '))
            elif(token.find('issue') > 0):
                issue = (', '+token.lstrip('issue '))
            elif(token.find('pp.') > 0):
                page = (', '+token.lstrip('pp. '))
                if page.find('(') >= 0:
                    page = page[0:page.find(' (')]
        return (journal+volume+issue+page)


    def process_pub_abst(self, publication):
        tokens = publication.split(',')
        end = len(tokens)-1
        abst = tokens[end].lower().lstrip('abstract ')
        meeting = ','.join(tokens[0:end])
        return [('Abstract '+abst+' presented at '+meeting), abst]

    
    def load_pool(self, pool_type):
        existed = set()
        
        type = 1 # which means abstract
        pattern = '.*Abstract (.*) pres'
        if pool_type.find('paper') >= 0:
            type = 0
            pattern = '.*doi: (.*).'
        pattern = re.compile(pattern)
        
        if type == 1: # must have the files existed.
            pool_file = open('abst.txt', 'r')
        else:
            pool_file = open('paper.txt', 'r')
            
        for line in pool_file:
            try:
                existed.add(pattern.match(line).group(1))
            except:
                break

        pool_file.close()
        return existed
        

        
