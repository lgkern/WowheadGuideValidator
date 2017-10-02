import urllib
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import URLError
import json

class SEOValidator:    

    def __init__(self):
        self.file = 'options.json'
        self.options = {}
        self.loadOptions()
        self.loop = 0
      
    def loadOptions(self):
        try:
            with open(self.file, 'r') as f:
                s = f.read()
                self.options = json.loads(s)
        except Exception:
            print(self.file+' not found')
            return

    def seoAnalysis(self, charClass, charSpec):
    
        # Retrieves all guides that it should analyze
        guideTypes = self.options['guidesTypes']
        guides = guideTypes.split(',')
        
        result = ''
        issues = []
        
        # For each guide, call its own analysis method 
        for guide in guides:
            analysis = getattr(self, 'seoGuideAnalysis_'+guide)
            res, iss = analysis(charClass, charSpec)
            result += res + ','
            issues += iss
        
        return result, issues
        
    def seoGuideAnalysis_guide(self, charClass, charSpec):
        expansion = self.options['expansion']
        patch = self.options['patch']
        
        issues = []
        
        # Fetch the guide from Wowhead
        title, content = self.dataFetch(charClass, charSpec, 'guide')
        
        # Verifies if it was found
        if title is None:
            return 'x', issues.append('{0} {1} Overview Guide wasn\'t found.'.format(charClass, charSpec)
        
        # Checks if the Guide title is well formatted
        expectedTitle = '{0} {1} Guide – {2} {3}' .format(charSpec, charClass, expansion, patch)
        
        if title != expectedTitle:
            issues.append('{0} {1} Overview Title has the wrong format. <{2}> instead of <{3}> '.format(charClass, charSpec, title, expectedTitle))
            
        # Checks if the body has the expected attributes
        
        
        # Returns ['ok',None] if there are no issues, or ['x',issues[]] if there are issues
        if not issues:
            return 'ok', issues
        else:
            return 'x', issues
        
    def dataFetch(self, charClass, charSpec, guide):
        print('>Fetching {1} {0} {2}'.format(charClass, charSpec, guide))
        
        charClass = '-'.join(charClass.lower().split(' '))
        charSpec = '-'.join(charSpec.lower().split(' '))
        url = 'https://www.wowhead.com/{1}-{0}-{2}'.format(charClass, charSpec, guide)
                
        req = Request(url)
        try:
            response = urlopen(req)
        except URLError as e:
            if hasattr(e, 'reason'):
                print('   We failed to reach a server.')
                print('   Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('    The server couldn\'t fulfill the request.')
                print('    Error code: ', e.code)
            return None, None
        else:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            lines = text.split('\n')
            
            # Finds the title in the text
            title = lines[0].replace(' - Guides - Wowhead','')
            
            # Finds the Context - It is the line after "ReportLinks"
            content = ''
            nextIsContent = False
                                    
            for line in lines:
                if nextIsContent:
                    content = line
                    break
                if 'ReportLinks' in line:
                    nextIsContent = True
                    
            return title, content
            
    def classSpecCombos(self):
        combos = []
        combos.append(['Blood', 'Death Knight'])
        combos.append(['Frost', 'Death Knight'])
        combos.append(['Unholy', 'Death Knight'])
        combos.append(['Havoc', 'Demon Hunter'])
        combos.append(['Vengeance', 'Demon Hunter'])
        combos.append(['Balance', 'Druid'])
        combos.append(['Guardian', 'Druid'])
        combos.append(['Feral', 'Druid'])
        combos.append(['Restoration', 'Druid'])
        combos.append(['Beast Mastery', 'Hunter'])
        combos.append(['Masrksmanship', 'Hunter'])
        combos.append(['Survival', 'Hunter'])
        combos.append(['Arcane', 'Mage'])
        combos.append(['Fire', 'Mage'])
        combos.append(['Frost', 'Mage'])
        combos.append(['Brewmaster', 'Monk'])
        combos.append(['Mistweaver', 'Monk'])
        combos.append(['Windwalker', 'Monk'])
        combos.append(['Holy', 'Paladin'])
        combos.append(['Protection', 'Paladin'])
        combos.append(['Retribution', 'Paladin'])
        combos.append(['Discipline', 'Priest'])
        combos.append(['Holy', 'Priest'])
        combos.append(['Shadow', 'Priest'])
        combos.append(['Assassination', 'Rogue'])
        combos.append(['Outlaw', 'Rogue'])
        combos.append(['Subtlety', 'Rogue'])
        combos.append(['Elemental', 'Shaman'])
        combos.append(['Enhancement', 'Shaman'])
        combos.append(['Restoration', 'Shaman'])
        combos.append(['Affliction', 'Warlock'])
        combos.append(['Destruction', 'Warlock'])
        combos.append(['Demonology', 'Warlock'])
        combos.append(['Arms', 'Warrior'])
        combos.append(['Fury', 'Warrior'])
        combos.append(['Protection', 'Warrior'])
        return combos
        