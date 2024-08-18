#Prompt.py
from colored import Fore,Style,Back
import random
import re,os,sys
import sqlalchemy
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db as db
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DayLog as DL
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode as TM
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Unified.bareCA import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes import VERSION
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
import inspect,string
import json
from pathlib import Path
from datetime import datetime
import barcode
import pint
from collections import namedtuple

class MAP:
    def __init__(self):
        #max number of aisle, this includes wall side aisle
        self.amx=4
        #min number of aisle
        self.amn=0
        #max shadow boxes to generate names for this incudes wall side aisle
        self.max_sb=6
        print(self.generate_names())

    def generate_names(self):
        address=[]
        for i in range(self.amn,self.amx):
            address.append(f"Aisle {i}")
        for side in ['Front','Rear']:
            for i in range(self.amn,self.amx):
                address.append(f"Aisle {i} {side} : End Cap")
            for m in ['Right','Left']:
                for i in range(self.amn,self.amx):
                    address.append(f"Aisle {i} {side} : Mid-End {m}")
            for sb in range(self.amn,self.max_sb):
                address.append(f"Aisle {i} {side} : Shadow Box {sb}")
        if len(address) > 0:
            for num,i in enumerate(address):
                print(num,"->",i)
            while True:
                which=input("return which: ")
                if which == '':
                    return address[0]
                elif which.lower() in ['q','quit']:
                    exit("User Quit")
                elif which.lower() in ['b','back']:
                    return
                try:
                    ids=[i for i in range(len(address))]
                    if int(which) in ids:
                        return address[int(which)]
                    else:
                        continue
                except Exception as e:
                    print(e)
                    return address[0]
        return address


def mkb(text,self):
    try:
        if text.lower() in ['','y','yes','true','t','1']:
            return True
        elif text.lower() in ['n','no','false','f','0']:
            return False
        elif text.lower() in ['p',]:
            return text.lower()
        else:
            return bool(eval(text))
    except Exception as e:
        print(e)
        return False

class Prompt:
    '''
            #for use with header
            fieldname='ALL_INFO'
            mode='LU'
            h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
    '''
    header='{Fore.grey_70}[{Fore.light_steel_blue}{mode}{Fore.medium_violet_red}@{Fore.light_green}{fieldname}{Fore.grey_70}]{Style.reset}{Fore.light_yellow} '
    state=True
    status=None
    def cleanup_system(self):
        try:
            print("Cleanup Started!")
            s=namedtuple(field_names=['ageLimit',],typename="self")
            s.ageLimit=db.AGELIMIT

            db.ClipBoordEditor.autoClean(s)

            def deleteOutDated(RID):
                with Session(db.ENGINE) as session:
                    q=session.query(db.RandomString).filter(db.RandomString.RID==RID).first()
                    print(f"Deleting {q}")
                    session.delete(q)
                    session.commit()
                    session.flush()

            def checkForOutDated():
                try:
                    ageLimit=ageLimit=float(pint.UnitRegistry().convert(2,"years","seconds"))
                    with Session(db.ENGINE) as session:
                        results=session.query(db.RandomString).all()
                        ct=len(results)
                        print(f"{Fore.light_green}RandomString len({Fore.light_salmon_3a}History{Fore.light_green}){Fore.medium_violet_red}={Fore.green_yellow}{ct}{Style.reset}")
                        for num,i in enumerate(results):
                            if i:
                                if i.AgeLimit != ageLimit:
                                    i.AgeLimit= ageLimit
                                    session.commit()
                                    session.flush()
                                    session.refresh(i)
                                if (datetime.now()-i.CDateTime).total_seconds() >= i.AgeLimit:
                                    print("need to delete expired! -> {num+1}/{ct} -> {i}")
                                    deleteOutDated(i.RID)
                except sqlalchemy.exc.OperationalError as e:
                    print(e)
                    print("Table Needs fixing... doing it now!")
                    reset()
            
            def reset():
                db.RandomStringPreferences.__table__.drop(ENGINE)
                db.RandomStringPreferences.metadata.create_all(ENGINE)

                db.RandomString.__table__.drop(ENGINE)
                db.RandomString.metadata.create_all(ENGINE)
                print(f"{Fore.orange_red_1}A restart is required!{Style.reset}")
                exit("User Quit For Reboot!")
            checkForOutDated()
        except Exception as e:
            print(e)
        exit('User Quit')

    def __init__(self,func,ptext='do what',helpText='',data={}):
        while True:
            cmd=input(f'{Fore.light_yellow}{ptext}{Style.reset}:{Fore.light_green} ')
            print(Style.reset,end='')
            
            if cmd.lower() in ['q','quit']:
                Prompt.cleanup_system(None)
            elif cmd.lower() in ['b','back']:
                self.status=False
                DayLogger(engine=ENGINE).addToday()
                return
            elif cmd.lower() in ['?','h','help']:
                print(helpText)
            else:
                #print(func)
                func(cmd,data)
                break

    def passwordfile(self):
        of=Path("GeneratedString.txt")
        if of.exists():
            age=datetime.now()-datetime.fromtimestamp(of.stat().st_ctime)
            days=float(age.total_seconds()/60/60/24)
            if days > 15:
                print(f"{Fore.light_yellow}Time is up, removeing old string file! {Fore.light_red}{of}{Style.reset}")
                of.unlink()
            else:
                print(f"{Fore.light_yellow}{of} {Fore.light_steel_blue}is {round(days,2)} {Fore.light_red}Days old!{Fore.light_steel_blue} you have {Fore.light_red}{15-round(days,2)} days{Fore.light_steel_blue} left to back it up!{Style.reset}")
                try:
                    print(f"{Fore.medium_violet_red}len(RandomString)={Fore.deep_pink_1a}{len(of.open().read())}\n{Fore.light_magenta}RandomString={Fore.dark_goldenrod}{Fore.orange_red_1}{of.open().read()}{Style.reset}")
                except Exception as e:
                    print(e)
                    print(f"{Fore.light_red}Could not read {of}{Style.reset}!")
        else:
            print(f"{Fore.orange_red_1}{of}{Fore.light_steel_blue} does not exist!{Style.reset}")

    def shortenToLen(text,length=os.get_terminal_size().columns-10):
        tmp=''
        for num,i in enumerate(text):
            if num%8==0 and num > 0:
                tmp+="\n"
            tmp+=i
        return tmp

    def __init2__(self,func,ptext='do what',helpText='',data={}):
        while True:
            color1=Style.bold+Fore.medium_violet_red
            color2=Fore.sea_green_2
            color3=Fore.pale_violet_red_1
            color4=color1
            split_len=int(os.get_terminal_size().columns/2)
            whereAmI=[str(Path.cwd())[i:i+split_len] for i in range(0, len(str(Path.cwd())), split_len)]
            helpText2=f'''
{Fore.light_salmon_3a}DT:{Fore.light_salmon_1}{datetime.now()}{Style.reset}
{Fore.orchid}PATH:{Fore.dark_sea_green_5a}{'#'.join(whereAmI)}{Style.reset}
{Fore.light_salmon_1}System Version: {Back.grey_70}{Style.bold}{Fore.red}{VERSION}{Style.reset}'''.replace('#','\n')
            
            default_list=''
            with db.Session(db.ENGINE) as session:
                    results=session.query(db.SystemPreference).filter(db.SystemPreference.name=="DefaultLists").all()
                    ct=len(results)
                    n=None
                    if ct <= 0:
                        pass
                        #print("no default tags")
                    else:
                        for num,r in enumerate(results):
                            try:
                                if r.default:
                                    default_list=','.join(json.loads(r.value_4_Json2DictString).get("DefaultLists"))
                                    break
                            except Exception as e:
                                print(e)

            #{Back.dark_orange_3b}
            cmd=input(f'''{Fore.light_sea_green+os.get_terminal_size().columns*'*'}
{Back.dark_red_1}{Fore.light_yellow}{ptext}{Style.reset}
{Fore.light_steel_blue+os.get_terminal_size().columns*'*'}
{color1}Prompt CMDS | {Fore.light_magenta}#RPLC#={Fore.tan}replace {Fore.light_magenta}#RPLC#{Fore.tan} from {Fore.light_red}CB{Fore.orange_3}.{Fore.light_green}default={Fore.light_yellow}True{Fore.light_steel_blue} or by {Fore.light_red}CB{Fore.orange_3}.{Fore.light_green}doe={Fore.light_yellow}Newest{Style.reset}
{Fore.green}q={Fore.green_yellow}quit|{Fore.light_sea_green}qb={Fore.green_yellow}backup & quit{Fore.cyan}|{Fore.light_salmon_1}c2c=calc2cmd={Fore.sky_blue_2}calculator result to input of cmd{Style.reset}
b={color2}back|{Fore.light_red}h={color3}help{color4}|{Fore.light_red}h+={color3}help+{color4}|{Fore.light_magenta}i={color3}info|
{Fore.light_green}{Fore.light_steel_blue}CMD#c2cb[{Fore.light_red}e{Fore.light_steel_blue}]{Fore.light_green}{Fore.light_red}|{Fore.orange_3}c2cb[{Fore.light_red}e{Fore.orange_3}]#CMD{Fore.light_green} - copy CMD to cb and set default
Note: optional [{Fore.light_red}e{Fore.light_green}] executes after copy{Style.reset} 
{Fore.light_steel_blue}Note: cmdline endswith/startswith [{Fore.light_red}#clr|clr#{Fore.light_green}{Fore.light_steel_blue}] clears current line for a retry{Style.reset}
{Fore.orange_red_1}c{Fore.light_steel_blue}=calc|{Fore.spring_green_3a}cb={Fore.light_blue}clipboard{Style.reset}|{Fore.light_salmon_1}cdp={Fore.green_yellow}clipboard default paste
{Fore.light_red+os.get_terminal_size().columns*'.'}
{Back.grey_35}:{Fore.light_green}{Back.grey_15} ''')
            print(f"{Fore.medium_violet_red}{os.get_terminal_size().columns*'.'}{Style.reset}",end='')

            def preProcess_RPLC(cmd):
                if '#RPLC#' in cmd:
                    with db.Session(db.ENGINE) as session:
                        dflt=session.query(db.ClipBoord).filter(db.ClipBoord.defaultPaste==True).order_by(db.ClipBoord.doe.desc()).first()
                        if dflt:
                            print(f"""{Fore.orange_red_1}using #RPLC#='{Fore.light_blue}{dflt.cbValue}{Fore.orange_red_1}'
    in {Fore.light_yellow}'{cmd.replace('#RPLC#',dflt.cbValue)}'{Style.reset}""")
                            return cmd.replace('#RPLC#',dflt.cbValue)
                        else:
                            return cmd
                            print(f"{Fore.orange_red_1}nothing to use to replace {Fore.orange_4b}#RPLC#!{Style.reset}")
                else:
                    return cmd
            cmd=preProcess_RPLC(cmd)
            def shelfCodeDetected(code):
                try:
                    with db.Session(db.ENGINE) as session:
                        results=session.query(db.Entry).filter(db.Entry.Code==code).all()
                        ct=len(results)
                except Exception as e:
                    print(e)
                    ct=0
                return f"{Fore.light_red}[{Fore.light_green}{Style.bold}Shelf{Style.reset}{Fore.light_green} CD FND{Fore.light_red}] {Fore.orange_red_1}{Style.underline}{code}{Style.reset} {Fore.light_green}{ct}{Fore.light_steel_blue} Found!{Style.reset}"
            
            def shelfBarcodeDetected(code):
                try:
                    with db.Session(db.ENGINE) as session:
                        results=session.query(db.Entry).filter(db.Entry.Barcode==code).all()
                        ct=len(results)
                except Exception as e:
                    print(e)
                    ct=0
                if ct > 0:
                    return f"{Fore.light_red}[{Fore.light_green}{Style.bold}Entry{Style.reset}{Fore.light_green} BCD FND{Fore.light_red}] {Fore.orange_red_1}{Style.underline}{code}{Style.reset} {Fore.light_green}{ct}{Fore.light_steel_blue} Found!{Style.reset}"
                else:
                    return ''
            def shelfPCCodeDetected(code):
                try:
                    with db.Session(db.ENGINE) as session:
                        results=session.query(db.PairCollection).filter(db.PairCollection.Code==code).all()
                        ct=len(results)
                except Exception as e:
                    print(e)
                    ct=0
                return f"{Fore.light_red}[{Fore.light_green}{Style.bold}Shelf{Style.reset}{Fore.light_green} CD FND in PC{Fore.light_red}] {Fore.orange_red_1}{Style.underline}{code}{Style.reset} {Fore.light_green}{ct}{Fore.light_steel_blue} Found!{Style.reset}"
            
            def shelfPCBarcodeDetected(code):
                try:
                    with db.Session(db.ENGINE) as session:
                        results=session.query(db.PairCollection).filter(db.PairCollection.Barcode==code).all()
                        ct=len(results)
                except Exception as e:
                    print(e)
                    ct=0
                if ct > 0:
                    return f"{Fore.light_red}[{Fore.light_green}{Style.bold}PC{Style.reset}{Fore.light_green} BCD FND{Fore.light_red}] {Fore.orange_red_1}{Style.underline}{code}{Style.reset} {Fore.light_green}{ct}{Fore.light_steel_blue} Found!{Style.reset}"
                else:
                    return ''



            def detectShelfCode(cmd):
                if cmd.startswith('*') and cmd.endswith('*') and len(cmd) - 2 == 8:
                    pattern=r"\*\d*\*"
                    shelfPattern=re.findall(pattern,cmd)
                    if len(shelfPattern) > 0:
                        #extra for shelf tag code
                        scMsg=f'{shelfCodeDetected(cmd[1:-1])}:{shelfPCCodeDetected(cmd[1:-1])}'
                        print(scMsg)
                        return cmd[1:-1]
                    else:
                        return cmd
                else:
                    return cmd
            bcdMsg=f'{shelfPCBarcodeDetected(cmd)}:{shelfBarcodeDetected(cmd)}'
            print(bcdMsg)
            cmd=detectShelfCode(cmd)
            def GetAsciiOnly(cmd):
                hws='\x1bOP\x1bOP'
                #hws='OPOP'
                tmp=cmd
                stripped=''
                if cmd.startswith(hws):
                   tmp=cmd[len(hws):]

                removed=[]
                for i in tmp:
                    if i in string.printable:
                        stripped+=i
                    else:
                        print(ord(i))
                        removed.append(i.encode())
                
                
                #if stripped.startswith("OPOP"):
                #    stripped=stripped[len("OPOP"):]
                ex=f"stripped({[hws.encode(),]})\n"
                if not cmd.startswith(hws):
                    ex=''
                ex1=f"stripped('{removed}')\n"
                if len(removed) <= 0:
                    ex1=''
                msg=f'''{'.'*10}\n{Fore.grey_50}{Style.bold}Input Diagnostics
Input Data({Fore.light_green}{cmd.encode()}{Fore.grey_50}){Style.reset}{Fore.light_salmon_1}
{ex1}{ex}{Fore.light_blue}finalCmd('{stripped}')\n{'.'*10}
cmd_len={len(cmd)}{Style.reset}'''
                print(msg)
                return stripped
            cmd=GetAsciiOnly(cmd)
            def detectGetOrSet(name,length):
                with db.Session(db.ENGINE) as session:
                    q=session.query(db.SystemPreference).filter(db.SystemPreference.name==name).first()
                    value=None
                    if q:
                        try:
                            value=json.loads(q.value_4_Json2DictString)[name]
                        except Exception as e:
                            q.value_4_Json2DictString=json.dumps({name:length})
                            session.commit()
                            session.refresh(q)
                            value=json.loads(q.value_4_Json2DictString)[name]
                    else:
                        q=db.SystemPreference(name=name,value_4_Json2DictString=json.dumps({name:length}))
                        session.add(q)
                        session.commit()
                        session.refresh(q)
                        value=json.loads(q.value_4_Json2DictString)[name]
                    return value

            def Mbool(text,data):
                try:
                    for i in ['n','no','false','f']:
                        if i in text.lower():
                            return False
                    for i in ['y','yes','true','t']:
                        if i in text.lower():
                            return True
                    return None
                except Exception as e:
                    return

            #PRESET_EAN13_LEN=13
            PRESET_EAN13_LEN=detectGetOrSet(name='PRESET_EAN13_LEN',length=13)
            if PRESET_EAN13_LEN != None and len(cmd) == PRESET_EAN13_LEN:
                try:
                    EAN13=barcode.EAN13(cmd)
                    use=Prompt.__init2__(None,func=Mbool,ptext=f"{Back.dark_red_1}{Fore.white}A EAN13({cmd}) Code was Entered, use it?{Style.reset}",helpText="yes or no",data="boolean")
                    if use in [True,None]:
                        pass
                    elif use in [False,]:
                        continue
                except Exception as e:
                    msg=f'''
{Fore.dark_red_1}{Style.bold}{str(e)}{Style.reset}
{Fore.yellow}{repr(e)}{Style.reset}
{Fore.light_green}Processing Will Continue...{Style.reset}
'''
                    print(msg)
            #this will be stored in system preferences as well as an gui be made to change it
            #PRESET_UPC_LEN=12
            #PRESET_UPC_LEN=None
            PRESET_UPC_LEN=detectGetOrSet(name='PRESET_UPC_LEN',length=12)
            if PRESET_UPC_LEN != None and len(cmd) == PRESET_UPC_LEN:
                try:
                    UPCA=barcode.UPCA(cmd)
                    use=Prompt.__init2__(None,func=Mbool,ptext=f"{Back.dark_red_1}{Fore.white}len({len(cmd)})-> A UPCA({cmd}) Code was Entered, use it?{Style.reset}",helpText="[y/Y]es(will ensure full UPCA-digit), or [n/N]o(will re-prompt), or [b]/back to use current text",data="boolean_basic")
                    if use in [True,None]:
                        pass
                    elif use in [False,]:
                        continue
                except Exception as e:
                    msg=f'''
{Fore.dark_red_1}{Style.bold}{str(e)}{Style.reset}
{Fore.yellow}{repr(e)}{Style.reset}
{Fore.light_green}Processing Will Continue...{Style.reset}
'''
                    print(msg)

            PRESET_UPCA11_LEN=detectGetOrSet(name='PRESET_UPCA11_LEN',length=11)   
            if PRESET_UPCA11_LEN != None and len(cmd) == PRESET_UPCA11_LEN:
                try:
                    UPCA11=str(barcode.UPCA(cmd))
                    use=Prompt.__init2__(None,func=Mbool,ptext=f"{Back.dark_red_1}{Fore.white}len({len(cmd)})-> A UPCA({cmd}) Code was Entered, use it?{Style.reset}",helpText="[y/Y]es(will ensure full UPCA-digit), or [n/N]o(will re-prompt), or [b]/back to use current text",data="boolean_basic")
                    print(f"USED:{use}")
                    if use in [True,]:
                        cmd=UPCA11
                    elif use in [None,]:
                        pass
                    elif use in [False,]:
                        continue
                except Exception as e:
                    msg=f'''
{Fore.dark_red_1}{Style.bold}{str(e)}{Style.reset}
{Fore.yellow}{repr(e)}{Style.reset}
{Fore.light_green}Processing Will Continue...{Style.reset}
'''
                    print(msg)
            #PRESET_CODE_LEN=8
            #PRESET_CODE_LEN=None
            PRESET_CODE_LEN=detectGetOrSet(name='PRESET_CODE_LEN',length=8)
            if PRESET_CODE_LEN != None and len(cmd) == PRESET_CODE_LEN:
                try:
                    Code39=barcode.Code39(cmd,add_checksum=False)
                    use=Prompt.__init2__(None,func=Mbool,ptext=f"{Back.dark_red_1}{Fore.white}A Possible Code39({cmd}) Code was Entered, use it?{Style.reset}",helpText="[y/Y]es(will ensure full UPCA-digit), or [n/N]o(will re-prompt), or [b]/back to use current text",data="boolean_basic")
                    if use in [True,None]:
                        pass
                    elif use in [False,]:
                        continue
                except Exception as e:
                    msg=f'''
{Fore.dark_red_1}{Style.bold}{str(e)}{Style.reset}
{Fore.yellow}{repr(e)}{Style.reset}
{Fore.light_green}Processing Will Continue...{Style.reset}
'''
                    print(msg)



            if cmd.endswith("#clr") or cmd.startswith('clr#'):
                print(f"{Fore.light_magenta}Sometimes we need to {Fore.sky_blue_2}re-think our '{Fore.light_red}{cmd}{Fore.sky_blue_2}'!{Style.reset}")
                continue
            elif cmd.lower() in ["aisle map",]:
                settings=namedtuple('self',['amx','amn','max_sb'])
                settings.amx=15
                settings.amn=0
                settings.max_sb=5
                ad=MAP.generate_names(settings)
                return func(ad,data)
            elif cmd.endswith("#c2cb"):
                with db.Session(db.ENGINE) as session:
                    ncb_text=cmd.split('#c2cb')[0]
                    cb=db.ClipBoord(cbValue=ncb_text,doe=datetime.now(),ageLimit=db.ClipBoordEditor.ageLimit,defaultPaste=True)
                    results=session.query(db.ClipBoord).filter(db.ClipBoord.defaultPaste==True).all()
                    ct=len(results)
                    if ct > 0:
                        for num,r in enumerate(results):
                            r.defaultPaste=False
                            if num % 100:
                                session.commit()
                        session.commit()
                    session.add(cb)
                    session.commit()
                    continue
            elif cmd.startswith("c2cb#"):
                with db.Session(db.ENGINE) as session:
                    ncb_text=cmd.split('c2cb#')[-1]
                    cb=db.ClipBoord(cbValue=ncb_text,doe=datetime.now(),ageLimit=db.ClipBoordEditor.ageLimit,defaultPaste=True)
                    results=session.query(db.ClipBoord).filter(db.ClipBoord.defaultPaste==True).all()
                    ct=len(results)
                    if ct > 0:
                        for num,r in enumerate(results):
                            r.defaultPaste=False
                            if num % 100:
                                session.commit()
                        session.commit()
                    session.add(cb)
                    session.commit()
                    continue
            if cmd.endswith("#c2cbe"):
                with db.Session(db.ENGINE) as session:
                    ncb_text=cmd.split('#c2cbe')[0]
                    cb=db.ClipBoord(cbValue=ncb_text,doe=datetime.now(),ageLimit=db.ClipBoordEditor.ageLimit,defaultPaste=True)
                    results=session.query(db.ClipBoord).filter(db.ClipBoord.defaultPaste==True).all()
                    ct=len(results)
                    if ct > 0:
                        for num,r in enumerate(results):
                            r.defaultPaste=False
                            if num % 100:
                                session.commit()
                        session.commit()
                    session.add(cb)
                    session.commit()
                    return func(ncb_text,data)
            elif cmd.startswith("c2cbe#"):
                with db.Session(db.ENGINE) as session:
                    ncb_text=cmd.split('c2cbe#')[-1]
                    cb=db.ClipBoord(cbValue=ncb_text,doe=datetime.now(),ageLimit=db.ClipBoordEditor.ageLimit,defaultPaste=True)
                    results=session.query(db.ClipBoord).filter(db.ClipBoord.defaultPaste==True).all()
                    ct=len(results)
                    if ct > 0:
                        for num,r in enumerate(results):
                            r.defaultPaste=False
                            if num % 100:
                                session.commit()
                        session.commit()
                    session.add(cb)
                    session.commit()
                    return func(ncb_text,data)
            elif cmd.lower() in ['rob','readline on boot','readline_on_boot']:
                with db.Session(db.ENGINE) as session:
                    READLINE_PREFERECE=session.query(db.SystemPreference).filter(db.SystemPreference.name=='readline').order_by(db.SystemPreference.dtoe.desc()).all()
                    ct=len(READLINE_PREFERECE)
                    if ct <= 0:
                        try:
                            import readline
                            sp=SystemPreference(name="readline",value_4_Json2DictString=json.dumps({"readline":True}))
                            session.add(sp)
                            session.commit()
                        except Exception as e:
                            print("Could not import Readline, you might not have it installed!")
                    else:
                        try:
                            f=None
                            for num,i in enumerate(READLINE_PREFERECE):
                                if i.default == True:
                                    f=num
                                    break
                            if f == None:
                                f=0
                            cfg=READLINE_PREFERECE[f].value_4_Json2DictString
                            if cfg =='':
                                READLINE_PREFERECE[f].value_4_Json2DictString=json.dumps({"readline":True})
                                import readline
                                session.commit()
                                session.refresh(READLINE_PREFERECE[f])
                            else:
                                try:
                                    x=json.loads(READLINE_PREFERECE[f].value_4_Json2DictString)
                                    if x.get("readline") in [True,False,None]:
                                        try:
                                            if x.get("readline") == False:
                                               READLINE_PREFERECE[f].value_4_Json2DictString=json.dumps({"readline":True})
                                               session.commit()
                                               exit("Reboot is required!") 
                                            elif x.get("readline") == True:
                                                READLINE_PREFERECE[f].value_4_Json2DictString=json.dumps({"readline":False})
                                                session.commit()
                                                exit("Reboot is required!")
                                            else:
                                                READLINE_PREFERECE[f].value_4_Json2DictString=json.dumps({"readline":True})
                                                session.commit()
                                                exit("Reboot is required!")
                                            print(e)
                                        except Exception as e:
                                            print(e)
                                    else:
                                        print("readline is off")
                                except Exception as e:
                                    try:
                                        import readline
                                        print(e)
                                    except Exception as e:
                                        print(e)
                        except Exception as e:
                            print(e)
                            
            elif cmd.lower() in ['c2c','calc2cmd']:
                t=TM.Tasks.TasksMode.evaluateFormula(None,fieldname="Prompt",oneShot=True)
                return func(str(t),data)
            elif cmd.lower() in ['es']:
                TM.Tasks.TasksMode.Lookup()
            elif cmd.lower() in ['c','calc']:
                #if len(inspect.stack(0)) <= 6:
                TM.Tasks.TasksMode.evaluateFormula(None,fieldname="Prompt")
                continue
                #else:
                #print(f"{Fore.light_green}Since {Fore.light_yellow}You{Fore.light_green} are already using the {Fore.light_red}Calculator{Fore.light_green}, I am refusing to recurse{Fore.light_steel_blue}(){Fore.light_green}!")
            elif cmd.lower() in ['q','quit']:
                Prompt.cleanup_system(Prompt)
            elif cmd.lower() in ['qb','quit backup']:
                DL.DayLogger.DayLogger.addTodayP(db.ENGINE)
                Prompt.cleanup_system(Prompt)
            elif cmd.lower() in ['qbc','quit backup clear']:
                DL.DayLogger.DayLogger.addTodayP(db.ENGINE)
                bare_ca(None)
                Prompt.cleanup_system(Prompt)
            elif cmd.lower() in ['cb','clipboard']:
                ed=db.ClipBoordEditor(self)
                continue
            elif cmd.lower() in ['#b',]:
                with db.Session(db.ENGINE) as session:
                    next_barcode=session.query(db.SystemPreference).filter(db.SystemPreference.name=='next_barcode').all()
                    ct=len(next_barcode)
                    if ct > 0:
                        if next_barcode[0]:
                            setattr(next_barcode[0],'value_4_Json2DictString',str(json.dumps({'next_barcode':True})))
                            session.commit()
                            session.refresh(next_barcode[0])
                    else:
                        next_barcode=db.SystemPreference(name="next_barcode",value_4_Json2DictString=json.dumps({'next_barcode':True}))
                        session.add(next_barcode)
                        session.commit()
                        session.refresh(next_barcode)
                return
            elif cmd.lower() in ['b','back']:
                return
            elif cmd.lower() in ['h','help']:
                print(helpText)
                continue
            elif cmd.lower() in ['h+','help+']:
                print(f'''{Fore.grey_50}If a Number in a formula is like '1*12345678*1', use '1*12345678.0*1' to get around regex for '*' values; {Fore.grey_70}{Style.bold}If An Issue Arises!{Style.reset}
                {Fore.grey_50}This is due to the {Fore.light_green}Start/{Fore.light_red}Stop{Fore.grey_50} Characters for Code39 ({Fore.grey_70}*{Fore.grey_50}) being filtered with {Fore.light_yellow}Regex
{Fore.light_magenta}rob=turn readline on/off at start
{Fore.light_steel_blue}if 'b' returns to previous menu, try '#b' to return to barcode input, in ListMode@$LOCATION_FIELD, 'e' does the same{Style.reset}''')
                continue
            elif cmd.lower() in ['i','info']:
                print(helpText2)
                Prompt.passwordfile(None,)
                continue
            elif cmd.lower() in ['cdp','clipboard_default_paste','clipboard default paste']:
                with db.Session(db.ENGINE) as session:
                    dflt=session.query(db.ClipBoord).filter(db.ClipBoord.defaultPaste==True).order_by(db.ClipBoord.doe.desc()).first()
                    if dflt:
                        print(f"{Fore.orange_red_1}using '{Fore.light_blue}{dflt.cbValue}{Fore.orange_red_1}'{Style.reset}")
                        return func(dflt.cbValue,data)
                    else:
                        print(f"{Fore.orange_red_1}nothing to use!{Style.reset}")
            else:
                return func(cmd,data)   

    #since this will be used statically, no self is required 
    #example filter method
    def cmdfilter(text,data):
        print(text)

prefix_text=f'''{Fore.light_red}$code{Fore.light_blue} is the scanned text literal{Style.reset}
{Fore.light_magenta}{Style.underline}#code refers to:{Style.reset}
{Fore.grey_70}e.{Fore.light_red}$code{Fore.light_blue} == search EntryId{Style.reset}
{Fore.grey_70}B.{Fore.light_red}$code{Fore.light_blue} == search Barcode{Style.reset}
{Fore.grey_70}c.{Fore.light_red}$code{Fore.light_blue} == search Code{Style.reset}
{Fore.light_red}$code{Fore.light_blue} == search Code | Barcode{Style.reset}
'''
def prefix_filter(text,self):
    split=text.split(self.get('delim'))
    if len(split) == 2:
        prefix=split[0]
        code=split[-1]
        try:
            if prefix.lower() == 'c':
                return self.get('c_do')(code)
            elif prefix == 'B':
                return self.get('b_do')(code)
            elif prefix.lower() == 'e':
                return self.get('e_do')(code)
        except Exception as e:
            print(e)
    else:
        return self.get('do')(text)






if __name__ == "__main__":  
    Prompt(func=Prompt.cmdfilter,ptext='code|barcode',helpText='test help!',data={})
        

    