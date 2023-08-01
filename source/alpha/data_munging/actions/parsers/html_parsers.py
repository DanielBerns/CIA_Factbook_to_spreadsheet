from bs4 import BeautifulSoup
from actions.logs import LOGS

class HTMLParser:
    
    def __init__(self, identifier: str = 'HTMLParser')
       super().__init__(identifier=identifier)
       self._table: Optional[str] = None
    
    @property
    def table(self) -> str:
        return self._table
    
    @table.setter
    def table(self, value: str) -> None:
        self._table = value

    def process(self, source: Source) -> bool:
        assert LOGS is not None
        matched = True
        soup = BeautifulSoup(source.content, 'html.parser')
        title = soup.title.string
       
        # 2002
        #    2001.html: /html/body/div[2]/table/tbody/tr[5]/td/table
        #    2002.html: /html/body/div[2]/table/tbody/tr[5]/td/table
        #               /html/body/div[2]/table/tbody/tr[5]/td/table
        step_0 = soup.find_all('div')[1] # the second div
        step_1 = step_0.find_all('table')[0]
        step_2 = step_1.find_all('table')[2]
        step_3 = step_2.find_all('tr')
        self.table = step_3.text
        matched = bool(self.table)
        
        LOGS.info(f'HTMLParser.process: {self.identifier:s} == {str(matched):s}')
        return matched
    
    def report(self, target: TextIO) -> None:
        target.write(f'## {self.identifier:s}\n')
        target.write('\n')
 
