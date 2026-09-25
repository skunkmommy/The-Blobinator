import random
import tomllib
import sys

burps = ["bworp", "ourp", "bwoarp", "bworpp", "ouarp", "bourap"]
moans = ["mmnff", "nnfn", "nmmmm", "fnnh", "mmf", "unff", "whimper", "whine"]
breaths = ["huff", "puff", "pant", "urfh", "wheeze"]

with open('config.toml','rb') as f:
    config = tomllib.load(f)

def format(text:str,italics=True,bold=False):
    mode = config['formattingMode']
    if bold and italics:
        if mode == 'telegram':
            text = text.replace('***','__')
        if mode == 'fa':
            text = text.replace('***','[b][i]',1)
            text = text.replace('***','[/b][/i]',1)
    if bold:
        if mode == 'fa':
            text = text.replace('**','[b]',1)
            text = text.replace('**','[/b]',1)
    if italics:
        if mode == 'telegram':
            text = text.replace('*','__')
        if mode == 'fa':
            text = text.replace('*','[i]',1)
            text = text.replace('*','[/i]',1)
    return(text)

def getBurp(intensity=4):
    burp = random.choice(burps)
    newburp = "***"
    for letter in burp:
        letter = letter * random.randint(1,intensity)
        if random.randint(1,intensity*2) > 3:
            letter = letter.upper()
        newburp += letter

    newburp += '***'
    return(format((''.join([newburp[0].lower(),newburp[1:]])),True,True))
def getMoan(intensity=8):
    moan = "*"
    moan += random.choice(moans)
    moan += moan[-1] * random.randint(1,round(intensity/2))  #  Add letters
    moan += ',' * random.randint(0,intensity)
    if random.randint(0,10) <= intensity:
        moan +="~"

    moan += '*'
    return(format(moan,True,False))
def getBreath():
    breath = random.choice(breaths)

    return (f"...{format('*'+breath+'*',True,False)}...")
def slur(word):
    result = []
    for char in word:
        if char.lower() in ['a','e','i','o','u']:
            char += 'h'
        if char.lower() in ['z','s']:
            char = 'th'
        result+=char
    return(''.join(result))
def stutter(word):
    if word[0].isalpha():
        return(word[0]+ "-" +word)
    else:
        return(word)

def getRates(weight,brainrot):
    rates = [0,0,0,0,0]
    if config['doBurps']:
       rates[0] = config['blobspeakModifier'] * 0.1 * (weight/8)
    else:
        rates[0] = 0

    if config['isHorny']:
        rates[1] = config['blobspeakModifier'] * 0.1 * brainrot
    else:
        rates[1] = 0

    if config['blobStuttering']:
        rates[2] = config['blobspeakModifier'] * 0.1 * brainrot
    else:
        rates[2] = 0

    if config['blobSlurring'] and weight > 5:
        rates[3] = config['blobspeakModifier'] * 0.25 * (weight/8)
    else:
        rates[3] = 0

    if config['blobBreathing']:
        rates[4] = config['blobspeakModifier'] * 0.25 * (weight/8)
    else:
        rates[4] = 0
    if weight > 7:
        rates[2] = 10
        rates[3] = 10
        rates[0] *= 4
        rates[1] *= 4
    return(rates)

def microCommands(micros:str)->list:
    out = {}
    for micro in micros.split(' '):
        if micro.replace('mod','') != micro:    #   Blobspeak modifier
            out['blobspeakModifier'] = float(micro.replace('mod',''))
        if micro.replace('ws','') != micro:     #   Weight stage
            out['weightStage'] = int(micro.replace('ws',''))
        if micro.replace('br','') != micro:     #   Brainrot
            out['brainRot'] = float(micro.replace('br',''))
            
        if micro.replace('tg','') != micro:     #   Telegram mode
            out['formattingMode'] = 'telegram'
        if micro.replace('fa','') != micro:		#	FA mode
            out['formattingMode'] = 'fa'
    config.update(out)
    return(True)
def talkBlobby(original):
    if original == "":
            return("")

    weight = config['weightStage']
    brainrot = config['brainRot']
    rates = getRates(weight, brainrot)
    return(blobSpeak(original,rates[0],rates[1],rates[2],rates[3],rates[4]))
def blobSpeak(text,burpChance=0.2,moanChance=0.2,stutterChance=0.2,breathChance=0.2,slurChance=0.2):

    result = ""
    for word in text.split():
        if word[0] == '^':  #   Angled brackets override
            #   Check for manual input
            if word[1:-1] == 'burp':
                word = getBurp()
            elif word[1:-1] == 'moan':
                word = getMoan()
            elif word[1:-1] == 'breath':
                word = getBreath()
            else:
                word = word[1:-1]
            result = result + word + ' '
            continue
        if len(word) >= 10: #   Burp interrupts
            burpCounter = round(len(word)/10)
            wordNew = ""    #   I want to die
            for char in word:
                    if random.random() < burpChance/2 and burpCounter:
                        char += getBurp()
                        wordNew += char
                        burpCounter -= 1
                    else:
                        wordNew += char
            word = wordNew


        if random.random() < stutterChance:
            word = stutter(word)
            if random.random() < 0.1:
                word = stutter(word)

        if random.random() < slurChance:
            word = slur(word)
        
        if random.random() < burpChance:
            word = ' '.join([getBurp(),word])

        if random.random() < moanChance:
            word = ' '.join([getMoan(),word])
        
        if random.random() < breathChance:
            word = ' '.join([getBreath(),word])

        result = result + word + ' '
    return(result)

def process(text: str) -> str:
    if text[0] == '[':
        try:
            #	Microcommands
            micros = microCommands(text.split(']')[0][1:])
            if not micros:
                raise ValueError("No micros present!")
            text = text.split(']')[1][1:]
        except:
            text = text
    return(talkBlobby(text))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read()
    print(process(text))
