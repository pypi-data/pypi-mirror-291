from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.RandomStringUtil import *
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Unified.Unified as unified
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import prefix_text
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.ReFormula import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FormBuilder import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FBMTXT import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Lookup2.Lookup2 import Lookup as Lookup2
from collections import namedtuple,OrderedDict
import nanoid
from password_generator import PasswordGenerator
import random
from pint import UnitRegistry
import pandas as pd
import numpy as np
from datetime import *
from colored import Style,Fore
import json,sys,math,re,calendar
def today():
    dt=datetime.now()
    return date(dt.year,dt.month,dt.day)
'''
RATE+RATE|int|float=RATE
RATE-RATE|int|float=RATE
RATE/RATE|int|float=RATE
RATE*RATE|int|float=RATE

RATE*timedelta = RATE.GROSS(float)
'''

class RATE:
    class GROSS:
        def __init__(self,value):
            self.value=value
        def __str__(self):
            return f'''{Style.underline}{Fore.orange_red_1}Gross {Style.reset}{Style.bold}{Fore.green}${Style.reset}{Fore.light_yellow}{self.value}{Style.reset}'''

    def __init__(self,value):
        self.value=value

    def __add__(self,other):
        if isinstance(other, RATE):
            return self.value + other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value + other
        else:
            raise TypeError("Unsupported operand type(s) for +")

    def __radd__(self,other):
        return self.__add__(other)

    def __sub__(self,other):
        if isinstance(other, RATE):
            return self.value - other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value - other
        else:
            raise TypeError("Unsupported operand type(s) for -")

    def __rsub__(self,other):
        return self.__sub__(other)

    def __truediv__(self,other):
        if isinstance(other, RATE):
            return self.value / other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value / other
        else:
            raise TypeError("Unsupported operand type(s) for /")

    def __rtruediv__(self,other):
        return self.__truediv__(other)

    def __floordiv__(self,other):
        if isinstance(other, RATE):
            return self.value // other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value // other
        else:
            raise TypeError("Unsupported operand type(s) for //")

    def __rfloordiv__(self,other):
        return self.__floordiv__(other)

    def __mod__(self,other):
        if isinstance(other, RATE):
            return self.value * other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value * other
        else:
            raise TypeError("Unsupported operand type(s) for *")

    def __rmod__(self,other):
        return self.__mod__(other)

    def __pow__(self,other):
        if isinstance(other, RATE):
            return self.value ** other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value ** other
        else:
            raise TypeError("Unsupported operand type(s) for **")

    def __rpow__(self,other):
        return self.__pow__(other)

    def __mul__(self,other):
        if isinstance(other, RATE):
            return self.value * other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value * other
        elif isinstance(other,timedelta):
            return self.GROSS(self.value*(other.total_seconds()/60/60))
        else:
            raise TypeError("Unsupported operand type(s) for *")

    def __rmul__(self,other):
        return self.__mul__(other)

def YT(time_string):
    dt=datetime.now()
    if dt.day == 1:
        month=dt.month
        if month == 0:
            month=12
        nd=calendar.monthrange(month,dt.year)[-1]
        dt=datetime(dt.year,month,nd,dt.day,dt.hour,dt.minute)
    else:
        dt=datetime(dt.year,dt.month,dt.day-1,dt.hour,dt.minute)
    tmp=time_string
    numbers=r"\d+"
    m=r'[p,a]m'
    whatNumbers=[int(i) for i in re.findall(numbers,tmp)]
    if len(whatNumbers) >= 2:
        d=datetime(dt.year,dt.month,dt.day,whatNumbers[0],whatNumbers[1])
        return d
    else:
        raise Exception("format must be 1..24:1..59 [h:m]")

def yt(time_string):
    return YT(time_string)

def TT(time_string):
    dt=datetime.now()
    tmp=time_string
    numbers=r"\d+"
    whatNumbers=[int(i) for i in re.findall(numbers,tmp)]
    if len(whatNumbers) >= 2:
        d=datetime(dt.year,dt.month,dt.day,whatNumbers[0],whatNumbers[1])
        print(d)
        return d
    else:
        raise Exception("format must be 1..24:1..59 [h:m]")

def tt(time_string):
    return TT(time_string)

def TD(time_string):
    tmp=time_string
    '''x is businesses month'''
    numbers=r"\d+[hmsHMSyxXdYD]*"
    whatNumbers=[i for i in re.findall(numbers,tmp)]
    seconds=0
    for i in whatNumbers:
        if 'h' in i.lower():
            p=r'\d+'
            r=re.findall(p,i)
            if len(r) > 0:
                seconds+=int(r[0])*60*60
        elif 'm' in i.lower():
            p=r'\d+'
            r=re.findall(p,i)
            if len(r) > 0:
                seconds+=int(r[0])*60
        elif 's' in i.lower():
            p=r'\d+'
            r=re.findall(p,i)
            if len(r) > 0:
                seconds+=int(r[0])
        elif 'y' in i.lower():
            p=r'\d+'
            r=re.findall(p,i)
            if len(r) > 0:
                seconds+=(int(r[0])*sum(calendar.mdays)*24*60*60)
        elif 'x' in i.lower():
            p=r'\d+'
            r=re.findall(p,i)
            if len(r) > 0:
                seconds+=(int(r[0])*30*24*60*60)
        elif 'd' in i.lower():
            p=r'\d+'
            r=re.findall(p,i)
            if len(r) > 0:
                seconds+=int(r[0])*24*60*60

    TIMEDELTA=timedelta(seconds=seconds)
    print(TIMEDELTA)
    return TIMEDELTA

def td(time_string):
    return TD(time_string)

class TasksMode:
    Lookup=Lookup2
    #extra is for future expansion
    def exportList2Excel(self,fields=False,extra=[]):
        FIELDS=['Barcode','ALT_Barcode','Code','Name','Price','CaseCount']
        cols=[i.name for i in Entry.__table__.columns]
        if fields == True:
            return FIELDS
        for i in extra:
            if i in cols:
                FIELDS.append(extra)
            else:
                print(f"{Fore.light_red}{Style.bold}Warning {Style.underline}{Style.reset}{Fore.light_yellow}'{i}' from extra={extra} is not a valid {Style.reset}{Fore.light_green}Field|Column!{Style.reset}")
       
        with Session(self.engine) as session:
            query=session.query(Entry).filter(Entry.InList==True)
            df = pd.read_sql(query.statement, query.session.bind)
            df=df[['Barcode','ALT_Barcode','Code','Name','Price','CaseCount']]
            #df.to_excel()
            def mkT(text,self):
                if text=='':
                    return 'InList-Export.xlsx'
                return text
            while True:
                try:
                    efilename=Prompt.__init2__(None,func=mkT,ptext=f"Save where[{mkT('',None)}]",helpText="save the data to where?",data=self)
                    if isinstance(efilename,str):
                        df.to_excel(efilename)
                    break
                except Exception as e:
                    print(e)
    alt=f'''
{Fore.medium_violet_red}A {Style.bold}{Fore.light_green}Honey Well Voyager 1602g{Style.reset}{Fore.medium_violet_red} was connected and transmitted a '{Fore.light_sea_green}^@{Fore.medium_violet_red}'{Style.reset}
    '''

    def getTotalwithBreakDownForScan(self,short=False):
        while True:
            color1=Fore.light_red
            color2=Fore.orange_red_1
            color3=Fore.cyan
            color4=Fore.green_yellow
            def mkT(text,self):
                return text
            if not short:
                fieldname='ALL_INFO'
            else:
                fieldname="BASIC_INFO"
            mode='LU'
            h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
            scanned=Prompt.__init2__(None,func=mkT,ptext=f'{h}{Fore.light_yellow}barcode|code[help]?',helpText='',data=self)
            if scanned in [None,]:
                return
            elif scanned in ['',]:
                print(f"Nothing was Entered! or {self.alt}")
                continue
            else:
                with Session(self.engine) as session:
                    result=session.query(Entry).filter(or_(Entry.Barcode==scanned,Entry.Code==scanned,Entry.Barcode.icontains(scanned),Entry.Code.icontains(scanned),Entry.ALT_Barcode==scanned),Entry.InList==True).first()
                    if result:
                        backroom=result.BackRoom
                        total=0
                        for f in self.valid_fields:
                            if f not in self.special:
                                if getattr(result,f) not in [None,'']:
                                    total+=float(getattr(result,f))
                        if not short:
                            print(result)
                        else:
                            print(result.seeShort())
                        print(f"{Fore.light_yellow}0 -> {color1}Amount Needed Total+BackRoom {Style.reset}{color2}{Style.bold}{total}{Style.reset}! {Fore.grey_70}#if you total everything including backroom{Style.reset}")
                        print(f"{Fore.cyan}1 -> {color1}Amount Needed Total w/o BackRoom {Style.reset}{color2}{Style.bold}{total-backroom}{Style.reset} {Fore.grey_70}#if you are totalling everything without the backroom!{Style.reset}")
                        print(f"{Fore.light_green}2 -> {color1}Amount Needed Total w/o BackRoom - BackRoom {Style.reset}{color2}{Style.bold}{(total-backroom)-backroom}{Style.reset}! {Fore.grey_70}#if you are totalling everything needed minus what was/will brought from the backroom{Style.reset}")


                        
                    else:
                        print(f"{Fore.light_red}{Style.bold}No such Barcode|Code with InList==True:{scanned}{Style.reset}\nLet's Try a Search[*]!")
                        #search_auto_insert
                        idF=self.SearchAuto(InList=True,skipReturn=False)
                        if idF:
                            result=session.query(Entry).filter(Entry.EntryId==idF).first()
                            if result:
                                backroom=result.BackRoom
                                total=0
                                for f in self.valid_fields:
                                    if f not in self.special:
                                        if getattr(result,f) not in [None,'']:
                                            total+=float(getattr(result,f))
                                if not short:
                                    print(result)
                                else:
                                    print(result.seeShort())
                                print(f"{Fore.light_yellow}0 -> {color1}Amount Needed Total+BackRoom {Style.reset}{color2}{Style.bold}{total}{Style.reset}! {Fore.grey_70}#if you total everything including backroom{Style.reset}")
                                print(f"{Fore.cyan}1 -> {color1}Amount Needed Total w/o BackRoom {Style.reset}{color2}{Style.bold}{total-backroom}{Style.reset} {Fore.grey_70}#if you are totalling everything without the backroom!{Style.reset}")
                                print(f"{Fore.light_green}2 -> {color1}Amount Needed Total w/o BackRoom - BackRoom {Style.reset}{color2}{Style.bold}{(total-backroom)-backroom}{Style.reset}! {Fore.grey_70}#if you are totalling everything needed minus what 'was', or 'will be', brought from the backroom{Style.reset}")
                            else:
                                print(f"{Fore.light_yellow}Nothing was selected!{Style.reset}")




            

    def display_field(self,fieldname,load=False,above=None,below=None):
        #for use with header
        #fieldname='ALL_INFO'
        mode='ListMode'
        h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
    
        color1=Fore.light_green
        color2=Fore.orange_red_1
        color3=Fore.cyan
        color4=Fore.green_yellow
        numColor=Fore.light_red
        eidColor=Fore.medium_violet_red
        m=f"{numColor}Item Num {Style.reset}|{color1}Name{Style.reset}|{color2}Barcode|ALT_Barcode{Style.reset}|{color3}Code{Style.reset}|{color4}{fieldname}{Style.reset}|{eidColor}EID{Style.reset}"
        hr='-'*len(m)
        print(f"{m}\n{hr}")
        if (fieldname in self.valid_fields) or (load == True and fieldname == 'ListQty'):
            with Session(self.engine) as session:
                query=session.query(Entry).filter(Entry.InList==True)
                if above == None:
                    def mkT(text,self):
                        try:
                            v=int(text)
                        except Exception as e:
                            print(e)
                            v=0
                        return v
                    above=Prompt.__init2__(None,func=mkT,ptext=f"{h}Above [{Fore.light_green}0{Style.reset}]",helpText="anything below this will not be displayed!",data=self)
                if below == None:
                    def mkTBelow(text,self):
                        try:
                            v=int(text)
                        except Exception as e:
                            print(e)
                            v=sys.maxsize
                        return v
                    below=Prompt.__init2__(None,func=mkTBelow,ptext=f"{h}Below [{Fore.light_green}{sys.maxsize}{Style.reset}]",helpText="anything above this will not be displayed!",data=self)
                if above != None:
                    print(type(above),above,fieldname)
                    query=query.filter(getattr(Entry,fieldname)>above)
                if below != None:
                    query=query.filter(getattr(Entry,fieldname)<below)
                results=query.all()
                if len(results) < 1:
                    print(f"{Fore.light_red}{Style.bold}Nothing is in List!{Style.reset}")
                for num,result in enumerate(results):
                    print(f"{numColor}{num}{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{eidColor}{getattr(result,'EntryId')}{Style.reset}")
        print(f"{m}\n{hr}")

    def SearchAuto(self,InList=None,skipReturn=False):
        while True:
            try:
                with Session(self.engine) as session:
                    def mkT(text,self):
                        return text
                    fields=[i.name for i in Entry.__table__.columns if str(i.type) == "VARCHAR"]
                    stext=Prompt.__init2__(None,func=mkT,ptext="Search[*]:",helpText="Search All(*) fields",data=self)
                    
                    query=session.query(Entry)
                    
                    if stext in [None,'']:
                        return
                    
                    q=[]
                    
                    for f in fields:
                        q.append(getattr(Entry,f).icontains(stext.lower()))

                    query=query.filter(or_(*q))
                    if InList != None:
                        query=query.filter(Entry.InList==InList)
                    results=query.all()
                    ct=len(results)
                    for num,r in enumerate(results):
                        if num < round(0.25*ct,0):
                            color_progress=Fore.green
                        elif num < round(0.50*ct,0):
                            color_progress=Fore.light_green
                        elif num < round(0.75*ct,0):
                            color_progress=Fore.light_yellow
                        else:
                            color_progress=Fore.light_red
                        if num == ct - 1:
                            color_progress=Fore.light_red
                        if num == 0:
                            color_progress=Fore.cyan    
                        msg=f"{color_progress}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} ->{r}"
                        print(msg)
                    print(f"{Fore.light_yellow}There are {Fore.light_red}{ct}{Fore.light_yellow} Total Results for search {Fore.medium_violet_red}'{stext}'{Style.reset}{Fore.light_yellow}.{Style.reset}")
                    print(f"{Fore.light_red}Fields Searched in {Fore.cyan}{fields}{Style.reset}")
                    def mklint(text,data):
                        try:    
                            if text.lower() in ['r','rs','rst','reset']:
                                return True
                            index=int(text)
                            if index in [i for i in range(data)]:
                                return index
                            else:
                                raise Exception("out of bounds!")
                        except Exception as e:
                            print(e)
                            return None
                    if skipReturn:
                        return
                    ct=len(results)-1
                    if ct+1 > 0:
                        reset=False
                        while True:
                            which=Prompt.__init2__(None,func=mklint,ptext=f"Which {Fore.light_red}entry # {Style.reset}{Fore.light_yellow}do you wish to use?",helpText="number of entry to use [0..{ct}]\nUse 'r'|'rs'|'rst'|'reset' to reset search\n",data=ct+1)
                            print(which)
                            if which in [None,]:
                                return
                            elif which in [True,] and not isinstance(which,int):
                                reset=True
                                break

                            return results[which].EntryId
                        if reset == False:
                            break
            except Exception as e:
                print(e)
    def next_barcode(self):
        with Session(ENGINE) as session:
            next_barcode=session.query(SystemPreference).filter(SystemPreference.name=="next_barcode").first()
            
            state=False
            
            if next_barcode:
                    try:
                        state=json.loads(next_barcode.value_4_Json2DictString).get("next_barcode")
                    except Exception as e:
                        print(e)
                        next_barcode.value_4_Json2DictString=json.dumps({'next_barcode':False})
                        session.commit()
                        session.refresh(next_barcode)
                        state=json.loads(next_barcode.value_4_Json2DictString).get("next_barcode")
            else:
                next_barcode=db.SystemPreference(name="next_barcode",value_4_Json2DictString=json.dumps({'next_barcode':False}))
                session.add(next_barcode)
                session.commit()
                session.refresh(next_barcode)
                state=json.loads(next_barcode.value_4_Json2DictString).get("next_barcode")
            f=deepcopy(state)
            print(f,"NEXT BARCODE")
            next_barcode.value_4_Json2DictString=json.dumps({'next_barcode':False})
            session.commit()
            return f

    def reset_next_barcode(self):
        print(f"{Fore.red}Resetting Next Barcode...{Style.reset}")
        with Session(ENGINE) as session:
            next_barcode=session.query(SystemPreference).filter(SystemPreference.name=="next_barcode").delete()
            session.commit()
            next_barcode=db.SystemPreference(name="next_barcode",value_4_Json2DictString=json.dumps({'next_barcode':False}))
            session.add(next_barcode)
            session.commit()


    def NewEntrySchematic(self):
        master_tag=sys._getframe().f_code.co_name
        def mkT(text,self):
                return str(text)
        section=Prompt.__init2__(None,func=mkT,ptext="Section Name, if any [This sets Tags, may be commma separated]?",helpText=" the h2 header of the schematic",data=self)
        if section in [None,]:
            return
        while True:
            code=''
                                
            fieldname="NewEntryFromSchematic"
            code=Prompt.__init2__(None,func=mkT,ptext=f"{Fore.grey_70}[{Fore.light_steel_blue}ListMode{Fore.medium_violet_red}@{Fore.light_green}{fieldname}{Fore.grey_70}]{Style.reset}{Fore.light_yellow} Barcode",helpText=self.helpText_barcodes,data=self)
            if code == None:
                return
            with Session(self.engine) as session:
                check=session.query(Entry).filter(Entry.Barcode==code).first()
                data=OrderedDict({'Code':code,'Name':code,'Facings':1,'CaseCount':1})
                if not check:
                    newEntry=self.mkNew(code=code,data=data)
                    if self.next_barcode():
                        continue
                    if newEntry == None:
                        print(f"{Fore.orange_red_1}User canceled!{Style.reset}")
                        return
                    newEntry['Barcode']=code
                    newEntry['InList']=True
                    newEntry['ListQty']=1
                    ne=Entry(**newEntry)
                    tags=getattr(ne,"Tags")
                    if tags in ['',None]:
                        tags_tmp=[master_tag,]
                        tags_tmp.extend(section.split(","))
                        setattr(ne,"Tags",json.dumps(tags_tmp))
                    else:
                        try:
                            tags_tmp=list(json.loads(getattr(ne,"Tags")))
                            for s in section.split(","):
                                    if s not in tags_tmp:
                                        tags_tmp.append(s)
                            if master_tag not in tags_tmp:
                                tags_tmp.append(master_tag)
                            setattr(ne,"Tags",json.dumps(tags_tmp))
                        except Exception as e:
                            tags_tmp=[master_tag,]
                            tags_tmp.extend(section.split(","))
                            setattr(ne,"Tags",json.dumps(tags_tmp))
                    session.add(ne)
                    session.commit()
                    session.flush()
                    session.refresh(ne)

                    print(ne)
                else:
                    data['Name']=check.Name
                    data['Code']=check.Code
                    data['Facings']=check.Facings
                    data['CaseCount']=check.CaseCount
                    print(f"{Fore.light_red}Barcode: {Fore.light_yellow}{check.Barcode}{Style.reset}")
                    for k in data:
                        msg=f"{Fore.light_red}{k}: {Fore.light_yellow}{data[k]}{Style.reset}"
                        print(msg)
                    print(f"{Fore.light_red}Item Exists please use '{Fore.light_yellow}ni{Fore.light_red}' to {Fore.light_sea_green}bypass... {Fore.light_magenta}prompting now for {Style.bold}updates...{Style.reset}")
                    updates=self.mkNew(code=check.Barcode,data=data)
                    if self.next_barcode():
                        continue
                    if updates != None:
                        if 'EntryId' in list(updates.keys()):
                            eid=updates.pop("EntryId")
                        updates['InList']=True
                        updates['ListQty']=1
                        query=session.query(Entry).filter(Entry.Barcode==check.Barcode)
                        e=query.first()
                        for k in updates:
                            setattr(e,k,updates[k])
                            session.commit()
                        tags=getattr(e,"Tags")
                        if tags in ['',None]:
                            tags_tmp=[master_tag,]
                            tags_tmp.extend(section.split(","))
                            setattr(e,"Tags",json.dumps(tags_tmp))
                        else:
                            try:
                                tags_tmp=list(json.loads(getattr(e,"Tags")))
                                for s in section.split(","):
                                    if s not in tags_tmp:
                                        tags_tmp.append(s)
                                if master_tag not in tags_tmp:
                                    tags_tmp.append(master_tag)
                                setattr(e,"Tags",json.dumps(tags_tmp))
                            except Exception as e:
                                tags_tmp=[master_tag,]
                                tags_tmp.extend(section.split(","))
                                setattr(e,"Tags",json.dumps(tags_tmp))
                        session.commit()
                        session.flush()
                        session.refresh(check)
                    else:
                        continue
                    print(check)

    def NewEntryMenu(self):
        def mkTl(text,self):
            return text
        fieldname='NewItemMenu'
        mode='TaskMode'
        expo_color=Fore.light_green
        h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
        htext=f'''{Fore.grey_70}Add an Entry using available data directly,
checking for new item by barcode
{Fore.grey_50}Entry that exists will prompt for updates
to fields) based off of mode
{Fore.light_steel_blue}Each mode will also add a tag designating which 
mode was used to create the entry {Fore.grey_70}This corresponds to the method() used!{Fore.light_steel_blue}:
 {Fore.light_yellow}nfst='NewEntryShelf'
 {Fore.light_sea_green}nfsc='NewEntrySchematic'
 {Fore.light_green}ucs='update_ShelfCount_CaseCount'
 {Fore.light_magenta}nfa='NewEntryAll'
{Fore.grey_84}The 'Entry' added/updated will have InList=True and ListQty=1,
Unless you use {Fore.light_steel_blue}nfst|new entry from shelf|new_entry_from_shelf{Fore.grey_84}
Which instead of {Fore.cyan}ListQty=1, {Fore.light_red}sets {Fore.orange_red_1}Shelf=1{Style.reset}
so use {Fore.orange_red_1}ls-lq/ls Shelf {Fore.light_yellow}from {Fore.light_magenta}previous menu{Fore.light_yellow} to view items added{Style.reset}
{Fore.light_red}nfa|nefa|new entry from all|new_entry_from_all - {expo_color}new from all{Style.reset}
{Fore.light_steel_blue}nfst|new entry from shelf|new_entry_from_shelf - {expo_color}new from shelf{Style.reset}
{Fore.light_red}nfsc|new entry from schematic|new_entry_from_schematic - {expo_color}new from aisle
{Fore.light_steel_blue}ucs|update casecount shelfcount|update_casecount_shelfcount - {expo_color}update casecount and shelf count
{Fore.light_steel_blue}en|edit note|edit_note - {expo_color}edit note of product by barcode/code/id
{Style.reset}'''
        while True:
            try:
                doWhat=Prompt.__init2__(None,func=mkTl,ptext=f"{h}Do What?",helpText=htext,data=self)
                if doWhat in [None,]:
                    return
                elif doWhat.lower() in ['nfa',f"nfa","new entry from all","new_entry_from_all","nefa"]:
                    self.NewEntryAll()
                elif doWhat.lower() in ['nfsc',"new entry from schematic","new_entry_from_schematic"]:
                    self.NewEntrySchematic()
                elif doWhat.lower() in ['nfst',"new entry from shelf","new_entry_from_shelf"]:
                    self.NewEntryShelf()
                elif doWhat.lower() in ['update casecount shelfcount','update_casecount_shelfcount','ucs']:
                    self.update_ShelfCount_CaseCount()
                elif doWhat.lower() in 'find_dupes|fd|cleanup'.split('|'):
                    self.findDupes()
                elif doWhat.lower() in 'en|edit note|edit_note'.split("|"):
                    self.editNotes()
            except Exception as e:
                print(e)

    def editNotes(self):
        while True:
            code=''
                                
            def mkT(text,self):
                return str(text)
            fieldname="EditNote"
            code=Prompt.__init2__(None,func=mkT,ptext=f"{Fore.grey_70}[{Fore.light_steel_blue}ListMode{Fore.medium_violet_red}@{Fore.light_green}{fieldname}{Fore.grey_70}]{Style.reset}{Fore.light_yellow} Barcode",helpText=self.helpText_barcodes,data=self)
            if code == None:
                return
            with Session(self.engine) as session:
                check=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code)).first()
                if not check:
                    print("No Such Item By Barcode!")
                else:
                    print(f'Note: {check.Note}')
                    data_l=check.Note.split("\n")
                    if len(data_l) > 0:
                        data_dict={num:{'type':'string','default':i} for num,i in enumerate(data_l)}
                        test=FormBuilder(data=data_dict,extra_tooling=True)
                        lines='\n'.join([i for i in test.values()])
                        setattr(check,'Note',lines)
                        session.commit()
                        session.refresh(check)
                        print('New Note:',check.Note)


    def NewEntryShelf(self):
        master_tag=sys._getframe().f_code.co_name
        while True:
            code=''
                                
            def mkT(text,self):
                return str(text)
            fieldname="NewEntryFromShelf"
            code=Prompt.__init2__(None,func=mkT,ptext=f"{Fore.grey_70}[{Fore.light_steel_blue}ListMode{Fore.medium_violet_red}@{Fore.light_green}{fieldname}{Fore.grey_70}]{Style.reset}{Fore.light_yellow} Barcode",helpText=self.helpText_barcodes,data=self)
            if code == None:
                return
            with Session(self.engine) as session:
                check=session.query(Entry).filter(Entry.Barcode==code).first()
                data=OrderedDict({'Code':code,'Name':code,'Price':1,'CaseCount':1})
                if not check:
                    newEntry=self.mkNew(code=code,data=data)
                    if self.next_barcode():
                        continue
                    if newEntry == None:
                        print(f"{Fore.orange_red_1}User canceled!{Style.reset}")
                        return
                    newEntry['Barcode']=code
                    newEntry['InList']=True
                    newEntry['Shelf']=1
                    ne=Entry(**newEntry)
                    tags=getattr(ne,"Tags")
                    tags_tmp=master_tag
                    if tags in ['',None]:
                        tags_tmp=[master_tag,]
                        setattr(ne,"Tags",json.dumps(tags_tmp))
                    else:
                        try:
                            tags_tmp=list(json.loads(getattr(ne,"Tags")))
                            if master_tag not in tags_tmp:
                                tags_tmp.append(master_tag)
                            tags_tmp.append(master_tag)
                            setattr(ne,"Tags",json.dumps(tags_tmp))
                        except Exception as e:
                            tags_tmp=[section,]
                            setattr(ne,"Tags",json.dumps(tags_tmp))
                    session.add(ne)
                    session.commit()
                    session.flush()
                    session.refresh(ne)
                    print(ne)
                else:
                    data['Name']=check.Name
                    data['Code']=check.Code
                    data['Price']=check.Price
                    data['CaseCount']=check.CaseCount
                    print(f"{Fore.light_red}Barcode: {Fore.light_yellow}{check.Barcode}{Style.reset}")
                    for k in data:
                        msg=f"{Fore.light_red}{k}: {Fore.light_yellow}{data[k]}{Style.reset}"
                        print(msg)
                    print(f"{Fore.light_red}Item Exists please use '{Fore.light_yellow}ni{Fore.light_red}' to {Fore.light_sea_green}bypass... {Fore.light_magenta}prompting now for {Style.bold}updates...{Style.reset}")
                    updates=self.mkNew(code=check.Barcode,data=data)
                    if self.next_barcode():
                        continue
                    if updates != None:
                        if 'EntryId' in list(updates.keys()):
                            eid=updates.pop("EntryId")
                        updates['InList']=True
                        updates['ListQty']=1
                        #session.query(Entry).filter(Entry.Barcode==check.Barcode)
                        query=session.query(Entry).filter(Entry.Barcode==check.Barcode)
                        e=query.first()
                        for k in updates:
                            setattr(e,k,updates[k])
                            session.commit()
                        tags=getattr(e,"Tags")
                        section=master_tag
                        if tags in ['',None]:
                            tags_tmp=[section,]
                            setattr(e,"Tags",json.dumps(tags_tmp))
                        else:
                            try:
                                tags_tmp=list(json.loads(getattr(e,"Tags")))
                                if section not in tags_tmp:
                                    tags_tmp.append(section)
                                setattr(e,"Tags",json.dumps(tags_tmp))
                            except Exception as e:
                                tags_tmp=[section,]
                                setattr(e,"Tags",json.dumps(tags_tmp))
                        #.update(updates)
                        session.commit()
                        session.flush()
                        session.refresh(check)
                    else:
                        continue
                    print(check)

    def update_ShelfCount_CaseCount(self):
        master_tag=sys._getframe().f_code.co_name
        while True:
            code=''
                                
            def mkT(text,self):
                return str(text)
            fieldname="NewEntryFromAllFields"
            code=Prompt.__init2__(None,func=mkT,ptext=f"{Fore.grey_70}[{Fore.light_steel_blue}ListMode{Fore.medium_violet_red}@{Fore.light_green}{fieldname}{Fore.grey_70}]{Style.reset}{Fore.light_yellow} Barcode",helpText=self.helpText_barcodes,data=self)
            if code == None:
                return
            with Session(self.engine) as session:
                check=session.query(Entry).filter(Entry.Barcode==code).first()
                if not check:
                    fields={'CaseCount':'integer','ShelfCount':'integer'}
                    
                    flds={}
                    for k in fields:
                        if k in ['Timestamp','EntryId']:
                            continue
                        if fields[k].lower() in ["varchar","string"]:
                            if k not in ['Size','TaxNote','Note','Tags','Location','Image','ALT_Barcode','DUP_Barcode','CaseID_BR','CaseID_LD','CaseID_6W',]:
                                flds[k]=code
                            else:
                                if k == 'Location':
                                    flds[k]='///'
                                elif k == 'Tags':
                                    flds[k]='[]'
                                else:
                                    flds[k]=''
                        elif fields[k].lower() in ["float","integer","boolean"]:
                            flds[k]=0
                        else:
                            flds[k]=None
                    print(flds)
                    newEntry=self.mkNew(code=code,data=flds)
                    flds['Code']=code
                    flds['Barcode']=code
                    flds['Name']=code
                    #{'Name':code,'Code':code,'CaseCount':1,'Price':1})
                    if self.next_barcode():
                        continue
                    if newEntry == None:
                        print(f"{Fore.orange_red_1}User canceled!{Style.reset}")
                        return
                    newEntry['Barcode']=code
                    newEntry['InList']=True
                    newEntry['InList']=1
                    ne=Entry(**newEntry)
                    tags=getattr(ne,"Tags")
                    tags_tmp=[]
                    if tags in ['',None]:
                        tags_tmp.append(master_tag)
                        setattr(ne,"Tags",json.dumps(tags_tmp))
                    else:
                        try:
                            tags_tmp=list(json.loads(getattr(ne,"Tags")))
                            tags_tmp.append(master_tag)
                            if master_tags not in tags_tmp:
                                tags_tmp.append(master_tags)
                            setattr(ne,"Tags",json.dumps(tags_tmp))
                        except Exception as e:
                            tags_tmp=[master_tag,]
                            setattr(ne,"Tags",json.dumps(tags_tmp))
                    session.add(ne)
                    session.commit()
                    session.flush()
                    session.refresh(ne)
                    print(ne)
                else:
                    '''
                    data={
                    'Name':check.Name,
                    'Code':check.Code,
                    'Price':check.Price,
                    'CaseCount':check.CaseCount,
                    }
                    '''
                    #d1=[i.name for i in check.__table__.columns]
                    d1=['CaseCount','ShelfCount']
                    data={i:getattr(check,i) for i in d1}
                    print(f"{Fore.light_red}Item Exists please use '{Fore.light_yellow}ni{Fore.light_red}' to {Fore.light_sea_green}bypass... {Fore.light_magenta}prompting now for {Style.bold}updates...{Style.reset}")
                    updates=self.mkNew(code=check.Barcode,data=data)
                    if self.next_barcode():
                        continue
                    if updates != None:
                        if 'EntryId' in list(updates.keys()):
                            eid=updates.pop("EntryId")
                        updates['InList']=True
                        updates['ListQty']=1
                        #session.query(Entry).filter(Entry.Barcode==check.Barcode)

                        query=session.query(Entry).filter(Entry.Barcode==check.Barcode)
                        e=query.first()
                        for k in updates:
                            setattr(e,k,updates[k])
                            session.commit()
                        tags=getattr(e,"Tags")
                        section=master_tag
                        if tags in ['',None]:
                            tags_tmp=[section,]
                            setattr(e,"Tags",json.dumps(tags_tmp))
                        else:
                            try:
                                tags_tmp=list(json.loads(getattr(e,"Tags")))
                                if section not in tags_tmp:
                                    tags_tmp.append(section)
                                setattr(e,"Tags",json.dumps(tags_tmp))
                            except Exception as e:
                                tags_tmp=[section,]
                                setattr(e,"Tags",json.dumps(tags_tmp))

                        #.update(updates)
                        session.commit()
                        session.flush()
                        session.refresh(check)
                    else:
                        continue
                    print(check)

    def NewEntryAll(self):
        master_tag=sys._getframe().f_code.co_name
        while True:
            code=''
                                
            def mkT(text,self):
                return str(text)
            fieldname="NewEntryFromAllFields"
            code=Prompt.__init2__(None,func=mkT,ptext=f"{Fore.grey_70}[{Fore.light_steel_blue}ListMode{Fore.medium_violet_red}@{Fore.light_green}{fieldname}{Fore.grey_70}]{Style.reset}{Fore.light_yellow} Barcode",helpText=self.helpText_barcodes,data=self)
            if code == None:
                return
            with Session(self.engine) as session:
                check=session.query(Entry).filter(Entry.Barcode==code).first()
                if not check:
                    fields={i.name:str(i.type) for i in Entry.__table__.columns}
                    fields.pop('Timestamp')
                    fields.pop('EntryId')
                    flds={}
                    for k in fields:
                        if k in ['Timestamp','EntryId']:
                            continue
                        if fields[k].lower() in ["varchar","string"]:
                            if k not in ['Size','TaxNote','Note','Tags','Location','Image','ALT_Barcode','DUP_Barcode','CaseID_BR','CaseID_LD','CaseID_6W',]:
                                flds[k]=code
                            else:
                                if k == 'Location':
                                    flds[k]='///'
                                elif k == 'Tags':
                                    flds[k]='[]'
                                else:
                                    flds[k]=''
                        elif fields[k].lower() in ["float","integer","boolean"]:
                            flds[k]=0
                        else:
                            flds[k]=None
                    flds['Code']=code
                    flds['Barcode']=code
                    flds['Name']=code

                    newEntry=self.mkNew(code=code,data=flds)
                    if self.next_barcode():
                        continue
                    #{'Name':code,'Code':code,'CaseCount':1,'Price':1})
                    if newEntry == None:
                        print(f"{Fore.orange_red_1}User canceled!{Style.reset}")
                        return
                    newEntry['Barcode']=code
                    newEntry['InList']=True
                    newEntry['InList']=1
                    ne=Entry(**newEntry)
                    tags=getattr(ne,"Tags")
                    tags_tmp=[]
                    if tags in ['',None]:
                        tags_tmp.append(master_tag)
                        setattr(ne,"Tags",json.dumps(tags_tmp))
                    else:
                        try:
                            tags_tmp=list(json.loads(getattr(ne,"Tags")))
                            if master_tag not in tags_tmp:
                                tags_tmp.append(master_tag)
                            setattr(ne,"Tags",json.dumps(tags_tmp))
                        except Exception as e:
                            tags_tmp=[master_tag,]
                            setattr(ne,"Tags",json.dumps(tags_tmp))
                    session.add(ne)
                    session.commit()
                    session.flush()
                    session.refresh(ne)
                    print(ne)
                else:
                    '''
                    data={
                    'Name':check.Name,
                    'Code':check.Code,
                    'Price':check.Price,
                    'CaseCount':check.CaseCount,
                    }
                    '''
                    d1=[i.name for i in check.__table__.columns]
                    data={i:getattr(check,i) for i in d1}
                    print(f"{Fore.light_red}Barcode: {Fore.light_yellow}{check.Barcode}{Style.reset}")
                    for k in data:
                        msg=f"{Fore.light_red}{k}: {Fore.light_yellow}{data[k]}{Style.reset}"
                        print(msg)
                    print(f"{Fore.light_red}Item Exists please use '{Fore.light_yellow}ni{Fore.light_red}' to {Fore.light_sea_green}bypass... {Fore.light_magenta}prompting now for {Style.bold}updates...{Style.reset}")
                    updates=self.mkNew(code=check.Barcode,data=data)
                    if self.next_barcode():
                        continue
                    print(updates)
                    if updates != None:
                        if 'EntryId' in list(updates.keys()):
                            eid=updates.pop("EntryId")
                        updates['InList']=True
                        updates['ListQty']=1
                        #session.query(Entry).filter(Entry.Barcode==check.Barcode)

                        query=session.query(Entry).filter(Entry.Barcode==check.Barcode)
                        e=query.first()
                        for k in updates:
                            setattr(e,k,updates[k])
                            session.commit()
                        tags=getattr(e,"Tags")
                        section=master_tag
                        if tags in ['',None]:
                            tags_tmp=[section,]
                            setattr(e,"Tags",json.dumps(tags_tmp))
                        else:
                            try:
                                tags_tmp=list(json.loads(getattr(e,"Tags")))
                                if section not in tags_tmp:
                                    tags_tmp.append(section)
                                setattr(e,"Tags",json.dumps(tags_tmp))
                            except Exception as e:
                                tags_tmp=[section,]
                                setattr(e,"Tags",json.dumps(tags_tmp))

                        #.update(updates)
                        session.commit()
                        session.flush()
                        session.refresh(check)
                    else:
                        continue
                    print(check)

    def mkNew(self,code,data=None):
        if data != None:
            if 'Tags' in list(data.keys()):
                data.pop('Tags')
        if data == None:
            data={
            'Name':code,
            'Code':code,
            'Price':0,
            'CaseCount':1,
            }
        self.skipTo=None
        while True:  
            #print(self.skipTo,"#loop top")
            for num,f in enumerate(data):
                #print(self.skipTo,'#2',"1 loop for")
                if self.skipTo != None and num < self.skipTo:
                    continue
                else:
                    self.skipTo=None
                keys=['e','p','d']
                otherExcludes=['EntryId','Timestamp',]
                while True:
                    try:
                        if str(f) == 'Tags':
                            print(f"Please use '#38' for this! '{f}'")
                        elif str(f) in otherExcludes:
                            print(f"Not working on this one RN! '{f}'")
                        elif str(f) == 'Location':
                            def lclg(text,data):
                                try:
                                    if text.lower() in keys:
                                        return text.lower()
                                    if text in ['',]:
                                        return '///'
                                    else:
                                        return text
                                except Exception as e:
                                    print(e)
                                    return 
                            dtmp=Prompt.__init2__(None,func=lclg,ptext=f"Entry[default:{data[f]}] {f}",helpText=f"{Fore.light_steel_blue}Enter a value for {f}, or leave blank to use scanned code; 'b' goes back to 'TaskMode'; 'e' to skip/exit entry altogether! 'p' for previous ; 'd' to use default stored value, if you entered a value, then 'd' will use that value when coming back from 'p'{Style.reset}",data=self)
                            if dtmp in [None,]:
                                print(f"{Fore.orange_red_1}User Canceled!{Style.reset}")
                                return


                        elif str(f) == 'Price':
                            def lclf(text,data):
                                try:
                                    if text.lower() in keys:
                                        return text.lower()
                                    return float(eval(text))
                                except Exception as e:
                                    return float(0)
                            dtmp=Prompt.__init2__(None,func=lclf,ptext=f"Entry[default:{data[f]}] {f}",helpText=f"{Fore.light_steel_blue}Enter a value for {f}, or leave blank to use scanned code; 'b' goes back to 'TaskMode'; 'e' to skip/exit entry altogether! 'p' for previous ; 'd' to use default stored value, if you entered a value, then 'd' will use that value when coming back from 'p'{Style.reset}",data=self)
                            if dtmp in [None,]:
                                print(f"{Fore.orange_red_1}User Canceled!{Style.reset}")
                                return

                        elif str(f) == 'CaseCount':
                            def lcli(text,data):
                                try:
                                    if text.lower() in keys:
                                        return text.lower()
                                    return int(eval(text))
                                except Exception as e:
                                    return int(1)
                            dtmp=Prompt.__init2__(None,func=lcli,ptext=f"Entry[default:{data[f]}] {f}",helpText=f"{Fore.light_steel_blue}Enter a value for {f}, or leave blank to use scanned code; 'b' goes back to 'TaskMode'; 'e' to skip/exit entry altogether! 'p' for previous ; 'd' to use default stored value, if you entered a value, then 'd' will use that value when coming back from 'p'{Style.reset}",data=self)
                            if dtmp in [None,]:
                                print(f"{Fore.orange_red_1}User Canceled!{Style.reset}")
                                return
                        else:
                            def lclt(text,data):
                                return text
                            dtmp=Prompt.__init2__(None,func=lclt,ptext=f"Entry[default:{data[f]}] {f}",helpText=f"{Fore.light_steel_blue}Enter a value for {f}, or leave blank to use scanned code; 'b' goes back to 'TaskMode'; 'e' to skip/exit entry altogether! 'p' for previous ; 'd' to use default stored value, if you entered a value, then 'd' will use that value when coming back from 'p'{Style.reset}",data=self)
                            if dtmp in [None,]:
                                print(f"{Fore.orange_red_1}User Canceled!{Style.reset}")
                                return
                        
                        if dtmp in ['',None] and f not in ['Price','CaseCount']:
                            fields={i.name:str(i.type) for i in Entry.__table__.columns}
                            if f in fields.keys():
                                if fields[f].lower() in ["string",]:
                                    data[f]=code
                                elif fields[f].lower() in ["float",]:
                                    data[f]=1.0
                                elif fields[f].lower() in ["integer",]:
                                    data[f]=1
                                elif fields[f].lower() in ["boolean",]:
                                    data[f]=False
                                else:
                                    data[f]=code
                            else:
                                raise Exception(f"{Fore.red}{Style.bold}Unsupported Field {Fore.light_red}'{f}'{Style.reset}")
                            #data[f]=code
                        elif dtmp in ['',None] and f in ['Price','CaseCount']:
                            continue
                        elif isinstance(dtmp,str):
                            if str(dtmp).lower() in ['e',]:
                                return
                            elif str(dtmp).lower() in ['p',]:
                                #print(num,num-1,"#3 loop while")
                                self.skipTo=num-1
                                break
                            elif str(dtmp).lower() in ['d',]:
                                print(f'{Fore.light_green}{data[f]}{Style.reset}',f'{Fore.orange_red_1}using default{Style.reset}')
                                pass
                            else:
                                fields={i.name:str(i.type) for i in Entry.__table__.columns}
                                if f in fields.keys():
                                    if fields[f].lower() in ["string",]:
                                        data[f]=dtmp
                                    elif fields[f].lower() in ["float",]:
                                        data[f]=float(eval(dtmp))
                                    elif fields[f].lower() in ["integer",]:
                                        data[f]=int(eval(dtmp))
                                    elif fields[f].lower() in ["boolean",]:
                                        data[f]=bool(eval(dtmp))
                                    else:
                                        data[f]=dtmp
                                else:
                                    raise Exception(f"{Fore.red}{Style.bold}Unsupported Field {Fore.light_red}'{f}'{Style.reset}")
                                #data[f]=dtmp
                        else:
                            data[f]=dtmp
                        self.skipTo=None
                        break
                    except Exception as e:
                        print(e)
                        break
                if self.skipTo != None:
                    break
            if self.skipTo == None:
                break
        return data

    entrySepStart=f'{Back.grey_30}{Fore.light_red}\\\\{Fore.light_green}{"*"*10}{Fore.light_yellow}|{Fore.light_steel_blue}#REPLACE#{Fore.light_magenta}|{Fore.orange_red_1}{"+"*10}{Fore.light_yellow}{Style.bold}({today()}){Fore.light_red}//{Style.reset}'
    entrySepEnd=f'{Back.grey_30}{Fore.light_red}\\\\{Fore.orange_red_1}{"+"*10}{Fore.light_yellow}|{Fore.light_steel_blue}#REPLACE#{Fore.light_magenta}|{Fore.light_green}{"*"*10}{Fore.light_yellow}{Style.bold}({today()}){Fore.light_red}//{Style.reset}'
    def setFieldInList(self,fieldname,load=False,repack_exec=None,barcode=None):
        tmp_fieldname=fieldname
        while True:
            if (fieldname not in self.special or fieldname in ['Facings'] )or (load==True and fieldname in ['ListQty',]):
                m=f"Item Num |Name|Barcode|ALT_Barcode|Code|{fieldname}|EID"
                hr='-'*len(m)
                if (fieldname in self.valid_fields) or (load==True and fieldname in ['ListQty',]) or fieldname == None:
                    with Session(self.engine) as session:
                        if not barcode:
                            code=''
                            
                            def mkT(text,self):
                                return str(text)
                            code=Prompt.__init2__(None,func=mkT,ptext=f"{Fore.grey_70}[{Fore.light_steel_blue}ListMode{Fore.medium_violet_red}@{Fore.light_green}{fieldname}{Fore.grey_70}]{Style.reset}{Fore.light_yellow} Barcode|Code",helpText=self.helpText_barcodes,data=self)
                            if code in [None,]:
                                break
                            elif code in ['',]:
                                print(f"Nothing was Entered! or {self.alt}")
                                continue
                        else:
                            code=barcode
                        print(self.entrySepStart.replace('#REPLACE#',f'{code}@{fieldname}'))

                        pc.PossibleCodes(scanned=code)
                        pc.PossibleCodesEAN13(scanned=code)
                            
                        value=0
                        def processQtyRe(code,MODE):
                            print(fieldname)
                            try:
                                with Session(ENGINE) as session:
                                    replace_case=['c','C','cs','case']
                                    replace_case.sort(key=len,reverse=True)
                                    replace_unit=['e','u','eaches','each','unit']
                                    replace_unit.sort(key=len,reverse=True)
                                    replace_load=['l','ld','load','lod']
                                    replace_load.sort(key=len,reverse=True)
                                    replace_pallet=['p','pallet']
                                    replace_pallet.sort(key=len,reverse=True)
                                    replace_shelf=['s','sf','shlf','shelf']
                                    replace_shelf.sort(key=len,reverse=True)
                                    replace_this=['current','x',]
                                    replace_this.sort(key=len,reverse=True)
                                    replace_facings=['facings','f']
                                    replace_facings.sort(key=len,reverse=True)

                                    multipliers={
                                    'l':1,
                                    'u':1,
                                    'p':1,
                                    's':1,
                                    'c':1,
                                    'x':1,
                                    'f':1,
                                    }
                                    result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.ALT_Barcode==code)).first()
                                    if result:
                                        if result.CaseCount==0:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.LoadCount==0:
                                            result.LoadCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.PalletCount==0:
                                            result.PalletCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.ShelfCount==0:
                                            result.ShelfCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.Facings==0:
                                            setattr(result,'Facings',1)
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if getattr(result,fieldname) == None:
                                            setattr(result,fieldname,0)

                                        multipliers['x']=getattr(result,fieldname)
                                        multipliers['c']=result.CaseCount
                                        multipliers['l']=result.LoadCount
                                        multipliers['p']=result.PalletCount
                                        multipliers['s']=result.ShelfCount
                                        multipliers['f']=result.Facings
                                    else:
                                        pass
                                    def mkV(text,data):
                                        return text
                                    local_htxt=f'''{Fore.green_yellow}
using similar functionality to the primary mode, call it Legacy,
ReParseFormula mode uses formulas like so
c.1.1|1.c+2.u|u.2=1 unit + 2 cases based on the Entry related,
where the suffix can be on either side of the number, with similar 
results to advanced mode, with the exception this mode is meant to
guarantee 1.c == (1.0*c); whatever c is
so this boils down to if you have a case count of 7,
then the formula will result in:{Fore.light_yellow}
    1*1+2*7=result
    1+14=result
    result=15
{Fore.grey_70}No suffixes are needed
Take note that the suffixes must follow their quantity
number
you may use python3 built-in's to process numbers as this is 
done with {Fore.light_red}eval(){Fore.grey_70}
so you may also input below:{Fore.light_yellow}
    round(1@/2#,2) and get a valued result
    if invalid, an exception is thrown
    but will not end the programme
use of the python3.x module math is valid

{Fore.medium_violet_red}{Style.bold}Valid numeric-multiplier suffixes are{Style.reset}
{Fore.light_green}{Style.underline}Case Numeric-Multiplier Suffixes{Style.reset}
{Fore.green_yellow}{'|'.join(replace_case)}{Style.reset}
{Fore.light_magenta}{Style.underline}Unit/Eaches Numeric-Multiplier Suffixes{Style.reset}
{Style.bold}{Fore.orange_red_1}Special Suffixes{Style.reset}
{Fore.medium_violet_red}ShelfCount{Style.reset}
{Fore.light_steel_blue}{'|'.join(replace_shelf)}{Style.reset}
{Fore.medium_violet_red}LoadCount{Style.reset}
{Fore.light_magenta}{Style.underline}{'|'.join(replace_load)}{Style.reset}
{Fore.medium_violet_red}PalletCount{Style.reset}
{Fore.light_steel_blue}{'|'.join(replace_pallet)}{Style.reset}
{Fore.light_magenta}{Style.underline}{'|'.join(replace_facings)}{Style.reset}'''
                                    text=Prompt.__init2__(None,func=mkV,ptext="ReFormulated Qty using NUM@=Units,NUM#=Cases (Enter==1)",helpText=local_htxt,data=code)
                                    if text in [None,]:
                                        return
                                    elif text in ['',]:
                                        return 1

                                    textO=ReParseFormula(formula=text,casecount=multipliers.get('c'),suffixes=replace_case)
                                    textO=ReParseFormula(formula=str(textO),casecount=multipliers.get('u'),suffixes=replace_unit)
                                    textO=ReParseFormula(formula=str(textO),casecount=multipliers.get('l'),suffixes=replace_load)
                                    textO=ReParseFormula(formula=str(textO),casecount=multipliers.get('s'),suffixes=replace_shelf)
                                    textO=ReParseFormula(formula=str(textO),casecount=multipliers.get('p'),suffixes=replace_pallet)
                                    textO=ReParseFormula(formula=str(textO),casecount=multipliers.get('x'),suffixes=replace_this)
                                    textO=ReParseFormula(formula=str(textO),casecount=multipliers.get('f'),suffixes=replace_facings)

                                    textO=str(textO)
                                    print(textO)
                                    if MODE.startswith("+"):
                                        return float(eval(textO))
                                    elif MODE.startswith("-"):
                                        return float(eval(textO))*-1
                                    return float(eval(textO))
                            except Exception as e:
                                print(e)
                                if MODE.startswith("+"):
                                    return float(1)
                                elif MODE.startswith("-"):
                                    return float(-1)
                                else:
                                    return float(1)

                        def processQty(code,MODE):
                            try:
                                with Session(ENGINE) as session:
                                    replace_case=['#','.c','.C','.cs','.case']
                                    replace_unit=['@','.e','.u','.eaches','.each','.unit']
                                    replace_load=['^','~','.l','.ld','.load','.lod']
                                    replace_pallet=['$','\\','.p','.pallet']
                                    replace_shelf=['%','?','.s','.sf','.shlf','.shelf']
                                    multipliers={
                                    '@':1,
                                    '#':1,
                                    '$':1,
                                    '^':1,
                                    '%':1,
                                    }
                                    result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.ALT_Barcode==code)).first()
                                    if result:
                                        if result.CaseCount==0:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.LoadCount==0:
                                            result.LoadCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.PalletCount==0:
                                            result.PalletCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.ShelfCount==0:
                                            result.ShelfCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)

                                        multipliers['#']=result.CaseCount
                                        multipliers['^']=result.LoadCount
                                        multipliers['$']=result.PalletCount
                                        multipliers['%']=result.ShelfCount
                                    else:
                                        pass
                                    def mkV(text,data):
                                        return text
                                    local_htxt=f'''{Fore.grey_70}
using similar functionality to the primary mode, call it Legacy,
advanced mode uses formulas like so
1@+2#=1 unit + 2 cases based on the Entry related
so this boils down to if you have a case count of 7,
then the formula will result in:{Fore.light_yellow}
    1*1+2*7=result
    1+14=result
    result=15
{Fore.grey_70}No suffixes are needed
Take note that the suffixes must follow their quantity
number
you may use python3 built-in's to process numbers as this is 
done with {Fore.light_red}eval(){Fore.grey_70}
so you may also input below:{Fore.light_yellow}
    round(1@/2#,2) and get a valued result
    if invalid, an exception is thrown
    but will not end the programme
use of the python3.x module math is valid

{Fore.medium_violet_red}{Style.bold}Valid numeric-multiplier suffixes are{Style.reset}
{Fore.light_green}{Style.underline}Case Numeric-Multiplier Suffixes{Style.reset}
{Fore.green_yellow}{'|'.join(replace_case)}{Style.reset}
{Fore.light_magenta}{Style.underline}Unit/Eaches Numeric-Multiplier Suffixes{Style.reset}
{Style.bold}{Fore.orange_red_1}Special Suffixes{Style.reset}
{Fore.medium_violet_red}ShelfCount{Style.reset}
{Fore.light_steel_blue}{'|'.join(replace_shelf)}{Style.reset}
{Fore.medium_violet_red}LoadCount{Style.reset}
{Fore.light_magenta}{Style.underline}{'|'.join(replace_load)}{Style.reset}
{Fore.medium_violet_red}PalletCount{Style.reset}
{Fore.light_steel_blue}{'|'.join(replace_pallet)}{Style.reset}'''
                                    text=Prompt.__init2__(None,func=mkV,ptext="Formulated Qty using NUM@=Units,NUM#=Cases (Enter==1)",helpText=local_htxt,data=code)
                                    if text in [None,]:
                                        return
                                    elif text in ['',]:
                                        return 1
                                    for r in replace_case:
                                        text=text.lower().replace(r,f"*{multipliers.get('#')}")
                                    for r in replace_unit:
                                        text=text.lower().replace(r,f"*{multipliers.get('@')}")
                                    for r in replace_load:
                                        text=text.lower().replace(r,f"*{multipliers.get('^')}")
                                    for r in replace_shelf:
                                        text=text.lower().replace(r,f"*{multipliers.get('%')}")
                                    for r in replace_pallet:
                                        text=text.lower().replace(r,f"*{multipliers.get('$')}")

                                    if MODE.startswith("+"):
                                        return float(eval(text))
                                    elif MODE.startswith("-"):
                                        return float(eval(text))*-1
                                    return float(eval(text))
                            except Exception as e:
                                print(e)
                                if MODE.startswith("+"):
                                    return float(1)
                                elif MODE.startswith("-"):
                                    return float(-1)
                                else:
                                    return float(1)

                        def mkT(text,code):
                            try:
                                if text not in ['',]:
                                    if text in ['a','+a','-a']:
                                        #value,text,suffix
                                        return float(processQty(code,text)),text,''
                                    if text in ['r','+r','-r']:
                                        #value,text,suffix
                                        return float(processQtyRe(code,text)),text,''
                                    else:
                                        tmp=text.split(',')
                                        if len(tmp) == 2:
                                            text,suffix=tmp
                                            if suffix.lower() not in ['s','e','u',' ','','c']:
                                                suffix=''
                                        else:
                                            suffix=''
                                            for i in ['s','e','u','c']:
                                                if text.endswith(i):
                                                    suffix=i
                                                    text=text[:-1]
                                                    break

                                        return float(eval(text)),text,suffix
                                else:
                                    return float(1),text,''
                            except Exception as e:
                                print(e)
                                return float(0),text,''
                        if fieldname == None:
                            color_1=Fore.light_red
                            color_2=Fore.light_magenta
                            hstring=f'''
Location Fields:
{Fore.deep_pink_3b}Shelf - {color_1}{Style.bold}0{Style.reset}
{Fore.light_steel_blue}BackRoom - {color_2}{Style.bold}1{Style.reset}
{Fore.cyan}Display_1 - {color_1}{Style.bold}2{Style.reset}
{Fore.cyan}Display_2 - {color_2}{Style.bold}3{Style.reset}
{Fore.cyan}Display_3 - {color_1}{Style.bold}4{Style.reset}
{Fore.cyan}Display_4 - {color_2}{Style.bold}5{Style.reset}
{Fore.cyan}Display_5 - {color_1}{Style.bold}6{Style.reset}
{Fore.cyan}Display_6 - {color_2}{Style.bold}7{Style.reset}
{Fore.cyan}SBX_WTR_DSPLY - {color_1}{Style.bold}8{Style.reset}
{Fore.cyan}SBX_CHP_DSPLY - {color_2}{Style.bold}9{Style.reset}
{Fore.cyan}SBX_WTR_KLR - {color_1}{Style.bold}10{Style.reset}
{Fore.violet}FLRL_CHP_DSPLY - {color_2}{Style.bold}11{Style.reset}
{Fore.violet}FLRL_WTR_DSPLY - {color_1}{Style.bold}12{Style.reset}
{Fore.grey_50}WD_DSPLY - {color_2}{Style.bold}13{Style.reset}
{Fore.grey_50}CHKSTND_SPLY - {color_1}{Style.bold}14{Style.reset}
{Fore.grey_50}InList - {color_2}{Style.bold}15{Style.reset}'''

                            def mkfields(text,data):
                                def print_selection(selected):
                                    print(f"{Fore.light_yellow}Using selected {Style.bold}{Fore.light_green}'{selected}'{Style.reset}!")
                                try:
                                    selected=None
                                    #use upper or lower case letters/words/fieldnames
                                    fields=tuple([i.name for i in Entry.__table__.columns])
                                    fields_lower=tuple([i.lower() for i in fields])
                                    if text.lower() in fields_lower:
                                        index=fields_lower.index(text.lower())
                                        selected=fields[index]
                                        print_selection(selected)
                                        return fields[index]
                                    else:
                                        #use numbers
                                        mapped={
                                            '0':"Shelf",
                                            '1':"BackRoom",
                                            '2':"Display_1",
                                            '3':"Display_2",
                                            '4':"Display_3",
                                            '5':"Display_4",
                                            '6':"Display_5",
                                            '7':"Display_6",
                                            '8':"SBX_WTR_DSPLY",
                                            '9':"SBX_CHP_DSPLY",
                                            '10':"SBX_WTR_KLR",
                                            '11':"FLRL_CHP_DSPLY",
                                            '12':"FLRL_WTR_DSPLY",
                                            '13':"WD_DSPLY",
                                            '14':"CHKSTND_SPLY",
                                            '15':"ListQty"
                                        }
                                        #print(text,mapped,text in mapped,mapped[text])
                                        if text in mapped:
                                            selected=mapped[text]
                                            print_selection(selected)
                                            return mapped[text]
                                except Exception as e:
                                    print(e)
                            while True:
                                fieldname=Prompt.__init2__(None,func=mkfields,ptext="Location Field(see h|help)",helpText=hstring,data=self)
                                if fieldname in [None,]:
                                    break
                                break
                            if fieldname in [None,]:
                                continue
                            m=f"Item Num |Name|Barcode|ALT_Barcode|Code|{fieldname}|EID"
                            hr='-'*len(m)
                        palletcount=1
                        shelfcount=1
                        loadcount=1
                        casecount=1
                        facings=1
                        Name=''
                        CD=''
                        BCD=''
                        ABCD=''
                        ci=''

                        result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.ALT_Barcode==code,Entry.Barcode.icontains(code),Entry.Code.icontains(code)),Entry.InList==True).first()
                        if result == None:
                            result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.ALT_Barcode==code,Entry.Barcode.icontains(code),Entry.Code.icontains(code))).first()
                            #print(isinstance(result,Entry))
                            hafnhaf=f'''{Fore.grey_70}[{Fore.light_steel_blue}ListMode Entry Info{Fore.grey_70}]
    {Style.reset}{Fore.light_green}CaseCount={Fore.cyan}{casecount}{Style.reset}|{Fore.medium_violet_red}ShelfCount={Fore.light_magenta}{shelfcount}{Style.reset}|{Fore.orange_red_1}Facings={Fore.turquoise_4}{facings}{Style.reset}
    {Fore.green_yellow}LoadCount={Fore.dark_goldenrod}{loadcount}{Style.reset}|{Fore.light_red}PalletCount={Fore.orange_red_1}{palletcount}|{Fore.spring_green_3a}{fieldname}={Fore.light_sea_green}{ci}{Style.reset}
    {Fore.cyan}Name{Fore.light_steel_blue}={Name}{Style.reset}
    {Fore.dark_goldenrod}Barcode={Fore.light_green}{BCD}|{Style.reset}{Fore.light_sea_green}ALT_Barcode={Fore.turquoise_4}{ABCD}{Style.reset}
    {Style.bold}{Fore.orange_red_1}Code={Fore.spring_green_3a}{CD}{Style.reset}'''
                            if isinstance(result,Entry):
                                for k in ['PalletCount','ShelfCount','LoadCount','CaseCount','Facings']:
                                    if getattr(result,k) < 1 or getattr(result,k) == None:
                                        setattr(result,k,1)
                                        session.commit()
                                        session.flush()
                                        session.refresh(result)
                                palletcount=result.PalletCount
                                facings=result.Facings
                                shelfcount=result.ShelfCount
                                loadcount=result.LoadCount
                                casecount=result.CaseCount
                                Name=result.Name
                                BCD=result.Barcode
                                CD=result.Code
                                ABCD=result.ALT_Barcode 
                                ci=getattr(result,fieldname)
                                code=result.Barcode
                                hafnhaf=f'''{Fore.grey_70}[{Fore.light_steel_blue}ListMode Entry Info{Fore.grey_70}]
    {Style.reset}{Fore.light_green}CaseCount={Fore.cyan}{casecount}{Style.reset}|{Fore.medium_violet_red}ShelfCount={Fore.light_magenta}{shelfcount}{Style.reset}|{Fore.orange_red_1}Facings={Fore.turquoise_4}{facings}{Style.reset}
    {Fore.green_yellow}LoadCount={Fore.dark_goldenrod}{loadcount}{Style.reset}|{Fore.light_red}PalletCount={Fore.orange_red_1}{palletcount}|{Fore.spring_green_3a}{fieldname}={Fore.light_sea_green}{ci}{Style.reset}
    {Fore.cyan}Name{Fore.light_steel_blue}={Name}{Style.reset}
    {Fore.dark_goldenrod}Barcode={Fore.light_green}{BCD}|{Style.reset}{Fore.light_sea_green}ALT_Barcode={Fore.turquoise_4}{ABCD}{Style.reset}
    {Style.bold}{Fore.orange_red_1}Code={Fore.spring_green_3a}{CD}{Style.reset}'''

                            print(hafnhaf)
                            results=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Barcode.icontains(code),Entry.Code.icontains(code),Entry.Code==code,Entry.ALT_Barcode==code)).all()
                            results_ct=len(results)
                            resultsName=session.query(Entry).filter(or_(Entry.Name.icontains(code))).all()
                            resultsName_ct=len(resultsName)
                            if results_ct > 0:
                                select=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.white}{Back.dark_red_1}Do you wish to select an alternative to the first?",helpText="yes or no, default=no",data="boolean")
                                if select in [False,'d']:
                                    pass
                                elif select in [True,]:
                                    for num,i in enumerate(results):
                                        msg=f'''{Fore.light_green}{num}/{Fore.light_red}{results_ct} -> {i.seeShort()}{Style.reset}'''
                                        print(msg)
                                    which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.white}{Back.dark_red_1}Which number?",helpText="number in yellow",data="integer")
                                    if which in [None,]:
                                        continue
                                    elif which in ['d',]:
                                        result=results[0]
                                    else:
                                        result=results[which]
                                elif select in [None,]:
                                    continue

                            if resultsName_ct > 0:
                                warn=', this will overwrite the other yes?'
                                if results_ct < 1:
                                    warn=''
                                select=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.white}{Back.dark_red_1}Do you wish to select an alternative to the first {warn}",helpText="yes or no, default=no",data="boolean")
                                if select in [False,'d']:
                                    pass
                                elif select in [True,]:
                                    for num,i in enumerate(resultsName):
                                        msg=f'''{Fore.light_green}{num}/{Fore.light_red}{resultsName_ct} -> {i.seeShort()}{Style.reset}'''
                                        print(msg)
                                    which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{Fore.white}{Back.dark_red_1}Which number?",helpText="number in yellow",data="integer")
                                    if which in [None,]:
                                        continue
                                    elif which in ['d',]:
                                        result=resultsName[0]
                                    else:
                                        result=resultsName[which]
                                elif select in [None,]:
                                    continue
                        
                        if isinstance(result,Entry):
                            for k in ['PalletCount','ShelfCount','LoadCount','CaseCount','Facings']:
                                if getattr(result,k) < 1 or getattr(result,k) == None:
                                    setattr(result,k,1)
                                    session.commit()
                                    session.flush()
                                    session.refresh(result)
                            palletcount=result.PalletCount
                            facings=result.Facings
                            shelfcount=result.ShelfCount
                            loadcount=result.LoadCount
                            casecount=result.CaseCount
                            Name=result.Name
                            BCD=result.Barcode
                            CD=result.Code
                            ABCD=result.ALT_Barcode 
                            ci=getattr(result,fieldname)
                            code=result.Barcode

                            hafnhaf=f'''{Fore.grey_70}[{Fore.light_steel_blue}ListMode Entry Info{Fore.grey_70}]
{Style.reset}{Fore.light_green}CaseCount={Fore.cyan}{casecount}{Style.reset}|{Fore.medium_violet_red}ShelfCount={Fore.light_magenta}{shelfcount}{Style.reset}|{Fore.orange_red_1}Facings={Fore.turquoise_4}{facings}{Style.reset}
{Fore.green_yellow}LoadCount={Fore.dark_goldenrod}{loadcount}{Style.reset}|{Fore.light_red}PalletCount={Fore.orange_red_1}{palletcount}|{Fore.spring_green_3a}{fieldname}={Fore.light_sea_green}{ci}{Style.reset}
{Fore.cyan}Name{Fore.light_steel_blue}={Name}{Style.reset}
{Fore.dark_goldenrod}Barcode={Fore.light_green}{BCD}|{Style.reset}{Fore.light_sea_green}ALT_Barcode={Fore.turquoise_4}{ABCD}{Style.reset}
{Style.bold}{Fore.orange_red_1}Code={Fore.spring_green_3a}{CD}{Style.reset}'''

                        ptext=f'''{hafnhaf}
{Fore.light_red}Enter {Style.bold}{Style.underline}{Fore.orange_red_1}Quantity/Formula{Style.reset} amount|+amount|-amount|a,+a,-a(advanced)|r,+r,-r(ReParseFormula) (Enter==1)'''
                        p=Prompt.__init2__(None,func=mkT,ptext=f"{ptext}",helpText=self.helpText_barcodes,data=code)
                        if self.next_barcode():
                            continue
                        if p in [None,]:
                            continue
                        if p:
                            value,text,suffix=p
                        else:
                            continue
                        def mkLT(text,data):
                            return text

                        note=Prompt.__init2__(None,func=mkLT,ptext=f"Note's? ",helpText="temporary note about item, if any.",data=code)
                        if note in [None,]:
                            continue

                        try:
                            color1=Fore.light_red
                            color2=Fore.orange_red_1
                            color3=Fore.cyan
                            color4=Fore.green_yellow 
                            if text.startswith("-") or text.startswith("+"):
                                #result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.ALT_Barcode==code)).first()
                                #sore
                                if result:
                                    if suffix.lower() in ['c',]:
                                        if result.CaseCount in [None,]:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.CaseCount < 1:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        value=float(value)*result.CaseCount
                                    setattr(result,fieldname,getattr(result,fieldname)+float(value))
                                    setattr(result,'Note',getattr(result,"Note")+"\n"+note)
                                    result.InList=True
                                    session.commit()
                                    session.flush()
                                    session.refresh(result)
                                    if callable(repack_exec):
                                        repack_exec(result)
                                    print(f"{Fore.light_red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")
                                    print(f"{m}\n{hr}")
                                    print(self.entrySepEnd.replace('#REPLACE#',f'{code}@{fieldname}'))
                                else:
                                    replacement=self.SearchAuto()
                                    if self.next_barcode():
                                            continue
                                    if isinstance(replacement,int):
                                        result=session.query(Entry).filter(Entry.EntryId==replacement).first()
                                        if result:
                                            setattr(result,fieldname,getattr(result,fieldname)+float(value))
                                            result.InList=True
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                            if callable(repack_exec):
                                                repack_exec(result)
                                            print(f"{Fore.light_red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")
                                            print(f"{m}\n{hr}")
                                            print(self.entrySepEnd.replace('#REPLACE#',f'{code}@{fieldname}'))
                                        else:
                                            raise Exception(f"result is {result}")
                                    else:
                                        data=self.mkNew(code=code)
                                        if self.next_barcode():
                                            continue
                                        if data in [None,]:
                                            return
                                        
                                        name=data['Name']
                                        icode=data['Code']
                                        iprice=data['Price']
                                        icc=data['CaseCount']
                                        n=Entry(Barcode=code,Code=icode,Price=iprice,Note=note+"\nNew Item",Name=name,CaseCount=icc,InList=True)
                                        setattr(n,fieldname,value)
                                        session.add(n)
                                        session.commit()
                                        session.flush()
                                        session.refresh(n)
                                        n.copySrc()
                                        result=n
                                        print(f"{Fore.light_red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")

                                        print(f"{m}\n{hr}")
                                        print(self.entrySepEnd.replace('#REPLACE#',f'{code}@{fieldname}'))
                                        if callable(repack_exec):
                                            repack_exec(n)
                            else:
                                #result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.ALT_Barcode==code)).first()
                                #sore
                                if result:
                                    if suffix.lower() in ['c',]:
                                        if result.CaseCount in [None,]:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.CaseCount < 1:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        value=float(value)*result.CaseCount
                                    setattr(result,fieldname,value)
                                    setattr(result,'Note',getattr(result,"Note")+"\n"+note)
                                    result.InList=True
                                    session.commit()
                                    session.flush()
                                    session.refresh(result)
                                    if callable(repack_exec):
                                        repack_exec(result)
                                    print(f"{Fore.light_red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")

                                    print(f"{m}\n{hr}")
                                    print(self.entrySepEnd.replace('#REPLACE#',f'{code}@{fieldname}'))

                                else:
                                    replacement=self.SearchAuto()
                                    if self.next_barcode():
                                            continue
                                    if isinstance(replacement,int):
                                        result=session.query(Entry).filter(Entry.EntryId==replacement).first()
                                        if result:
                                            setattr(result,fieldname,getattr(result,fieldname)+float(value))
                                            result.InList=True
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                            if callable(repack_exec):
                                                repack_exec(n)
                                            print(f"{Fore.light_red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")
                                            print(f"{m}\n{hr}")
                                            print(self.entrySepEnd.replace('#REPLACE#',f'{code}@{fieldname}'))
                                        else:
                                            raise Exception(f"result is {result}")
                                    else:
                                        data=self.mkNew(code=code)
                                        #print(data)
                                        if self.next_barcode():
                                            continue
                                        if data in [None,]:
                                            return
                                        name=data['Name']
                                        icode=data['Code']
                                        iprice=data['Price']
                                        icc=data['CaseCount']
                                        n=Entry(Barcode=code,Code=icode,Note=note+"\nNew Item",Name=name,Price=iprice,CaseCount=icc,InList=True)
                                        setattr(n,fieldname,value)
                                        session.add(n)
                                        session.commit()
                                        session.flush()
                                        session.refresh(n)
                                        n.copySrc()
                                        session.commit()
                                        session.flush()
                                        session.refresh(n)
                                        result=n
                                        if callable(repack_exec):
                                            repack_exec(n)
                                        print(f"{Fore.light_red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")

                                        print(f"{m}\n{hr}")
                                        print(self.entrySepEnd.replace('#REPLACE#',f'{code}@{fieldname}'))

                                    #raise Exception(result)
                        except Exception as e:
                            print(e)
                if repack_exec:
                    return
            else:
                #code for tags,caseId[br,6w,ld],
                self.processSpecial(fieldname)
                break
            if tmp_fieldname == None:
                fieldname=None
        
    helpText_barcodes=f"""
1. Enter the EntryId into the prompt
2. if an entry is found you will be prompted for a code to be saved
Quantity Modifiers:
(SEP=',' or No Sep) Suffixes Singles: s|e|u|' '|'' == units/singles/eaches/no multipliers
(SEP=',' or No Sep) Suffixes CaseCount: c == (qty*casecount+old_value_if_any
Valid Examples:
+1-2u - do operation in units and remove from qty 
-1+2c - do operation in cases and remove from qty
1c - cases set
1u - units set
remember, formula is calculated first, then that value is removed from qty if -/+
if CaseCount is less than 1, or not set, assume casecount == 1
    """
    def setBarcodes(self,fieldname):
         while True:
            try:
                def mkT(text,self):
                    return text
                cmd=Prompt.__init2__(None,func=mkT,ptext='Do What[help/q/b/$EntryId]?',helpText=self.helpText_barcodes,data=self)
                if not cmd:
                    break
                else:
                    with Session(self.engine) as session:
                        r=session.query(Entry).filter(Entry.EntryId==int(cmd)).first()
                        if r:
                            def mkT(text,self):
                                return text
                            code=Prompt.__init2__(None,func=mkT,ptext=f'{fieldname}[help]?',helpText=self.helpText_barcodes,data=self)
                            if not code:
                                break
                            else:
                                setattr(r,fieldname,code)
                                session.commit()
                                session.flush()
                                session.refresh(r)
                                print(r)
            except Exception as e:
                print(e)



    def processSpecial(self,fieldname):
        if fieldname.lower() == "tags":
            self.editTags()
        elif 'Barcode' in fieldname:
            self.setBarcodes(fieldname)
        else:
            print("SpecialOPS Fields! {fieldname} Not Implemented Yet!")
            self.editCaseIds()


    helpText_caseIds=f'''
{Fore.green_yellow}$WHERE,$EntryId,exec()|$ID{Style.reset}
#[ld,6w,br,all],$EntryId,generate - create a synthetic id for case and save item to and save qrcode png of $case_id in $WHERE
#[ld,6w,br,all],$EntryId,$case_id - set case id for item in $WHERE
#[ld,6w,br,all],$EntryId - display item case id in $WHERE
[ld,6w,br,all],s|search,$case_id - display items associated with $case_id in $WHERE
#[ld,6w,br,all],$EntryId,clr_csid - set $case_id to '' in $WHERE
where:
 ld is for Load
 6w is 6-Wheeler or U-Boat
 br is BackRoom
 
 all will apply to all of the above fields
    '''
    def editCaseIds(self):
         while True:
            def mkT(text,self):
                return text
            cmd=Prompt.__init2__(None,func=mkT,ptext='Do What[help]?',helpText=self.helpText_tags,data=self)
            if not cmd:
                break
            else:
                print(cmd)
                split_cmd=cmd.split(",")
                if len(split_cmd)==3:
                    mode=split_cmd[0]
                    eid=split_cmd[1]
                    ex=split_cmd[2]
                    if eid.lower() in ['s','search']:
                        #search
                        with Session(self.engine) as session:
                            results=[]
                            if split_cmd[0].lower() == '6w':
                                results=session.query(Entry).filter(Entry.CaseID_6W==ex).all()
                            elif split_cmd[0].lower() == 'ld':
                                results=session.query(Entry).filter(Entry.CaseID_LD==ex).all()
                            elif split_cmd[0].lower() == 'br':
                                results=session.query(Entry).filter(Entry.CaseID_BR==ex).all()
                            elif split_cmd[0].lower() == 'all':
                                results=session.query(Entry).filter(or_(Entry.CaseID_BR==ex,Entry.CaseID_LD==ex,Entry.CaseID_6W==ex)).all()
                            if len(results) < 1:
                                print(f"{Fore.dark_goldenrod}No Items to display!{Style.reset}")
                            for num,r in enumerate(results):
                                print(f"{Fore.light_red}{num}{Style.reset} -> {r}")
                    else:
                        with Session(self.engine) as session:
                            query=session.query(Entry).filter(Entry.EntryId==int(eid)).first()
                            if query:
                                if ex.lower() in ['clr_csid',]:
                                    if split_cmd[0].lower() == '6w':
                                        query.CaseID_6W=''
                                    elif split_cmd[0].lower() == 'ld':
                                        query.CaseID_LD=''
                                    elif split_cmd[0].lower() == 'br':
                                        query.CaseID_BR=''
                                    elif split_cmd[0].lower() == 'all':
                                        query.CaseID_6W=''
                                        query.CaseID_LD=''
                                        query.CaseID_BR=''
                                elif ex.lower() in ['generate','gen','g']:
                                    if split_cmd[0].lower() == '6w':
                                        query.CaseID_6W=query.synthetic_field_str()
                                    elif split_cmd[0].lower() == 'ld':
                                        query.CaseID_LD=query.synthetic_field_str()
                                    elif split_cmd[0].lower() == 'br':
                                        query.CaseID_BR=query.synthetic_field_str()
                                    elif split_cmd[0].lower() == 'all':
                                        query.CaseID_6W=query.synthetic_field_str()
                                        query.CaseID_LD=query.synthetic_field_str()
                                        query.CaseID_BR=query.synthetic_field_str()
                                else:
                                    if split_cmd[0].lower() == '6w':
                                        query.CaseID_6W=ex
                                    elif split_cmd[0].lower() == 'ld':
                                        query.CaseID_LD=ex
                                    elif split_cmd[0].lower() == 'br':
                                        query.CaseID_BR=ex
                                    elif split_cmd[0].lower() == 'all':
                                        query.CaseID_6W=ex
                                        query.CaseID_LD=ex
                                        query.CaseID_BR=ex
                                session.commit()
                                session.flush()
                                session.refresh(query)
                                print(f"""
    Name: {query.Name}
    Barcode: {query.Barcode}
    Code: {query.Code}
    EntryId: {query.EntryId}
    CaseId 6W: {query.CaseID_6W}
    CaseId LD: {query.CaseID_LD}
    CaseId BR: {query.CaseID_BR}
    """)
                elif len(split_cmd)==2:
                    with Session(self.engine) as session:
                        query=session.query(Entry).filter(Entry.EntryId==int(split_cmd[1]))
                        r=query.first()
                        if r:
                            if split_cmd[0].lower() == '6w':
                                print(r.CaseID_6W)
                            elif split_cmd[0].lower() == 'ld':
                                print(r.CaseID_LD)
                            elif split_cmd[0].lower() == 'br':
                                print(r.CaseID_BR)
                                #self.CaseID_BR=CaseID_BR
                                #self.CaseID_LD=CaseID_LD
                                #self.CaseID_6W=CaseID_6W
                        else:
                            print(f"{Fore.dark_goldenrod}No Such Item!{Style.reset}")
                else:
                    print(self.helpText_caseIds)


    helpText_tags=f'''{prefix_text}
{Fore.green_yellow}$mode[=|R,+,-],$TAG_TEXT,$fieldname,$id|$code|$barcode|$fieldData_to_id{Style.reset}
{Fore.orange_red_1}Valid Fieldnames to use are:{Fore.light_green}Barcode,{Fore.green_yellow}Code,{Fore.spring_green_3a}ALT_Barcode,{Fore.light_sea_green} and EntryId{Style.reset}
{Fore.cyan}=|R{Style.reset} -> {Fore.orange_red_1}{Style.bold}set Tag to $TAG_TEXT{Style.reset}
{Fore.cyan}+{Style.reset} -> {Fore.orange_red_1}{Style.bold}add $TAG_TEXT to Tag{Style.reset}
{Fore.cyan}pa|prompted_add|prompted add|auto_add|auto add|aa{Style.reset} -> {Fore.orange_red_1}{Style.bold}Prompted add tags to Entry{Style.reset}
{Fore.cyan}-{Style.reset} -> {Fore.orange_red_1}{Style.bold}remove $TAG_TEXT from Tag{Style.reset}
{Fore.cyan}pr|prompted_rm|prompted rm|auto_rm|auto rm|arm ->{Fore.orange_red_1}{Style.bold} prompted remove Tags, comma separated Tags are allowed{Style.reset}
{Fore.cyan}s|search{Style.reset} -> {Fore.orange_red_1}{Style.bold}search for items containing Tag{Style.reset}
{Fore.cyan}l|list{Style.reset} -> {Fore.orange_red_1}{Style.bold}List All Tags{Style.reset}
{Fore.light_red}{Style.bold}This performs operations on all results found without confirmation for mass tag-edits{Style.reset}
{Fore.cyan}ba|bta|bulk_tag_add{Style.reset} -> {Fore.orange_red_1}{Style.bold}Bulk add Tags to {Fore.light_magenta}{Style.underline}#code{Style.reset}
{Fore.cyan}br|btr|bulk_tag_rem{Style.reset} -> {Fore.orange_red_1}{Style.bold}Bulk remove Tags from {Fore.light_magenta}{Style.underline}#code{Style.reset}
{Fore.light_red}{Style.bold}reset_all_tags|clear_all_tags|cat|rat -> {Fore.orange_red_1}{Style.underline} reset all tags to []{Style.reset}
{Fore.light_red}{Style.bold}dedup_all_tags|ddat -> {Fore.orange_red_1}{Style.underline} remove all duplicate tags from Entry's{Style.reset}
    '''
    def editTags(self):
        while True:
            #cmd=input("Do What[help]?: ")
            #PROMPT
            def mkT(text,self):
                return text
            fieldname='TaskMode'
            mode='EditTags'
            h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
            cmd=Prompt.__init2__(None,func=mkT,ptext=f'{h}Do What[help]?',helpText=self.helpText_tags,data=self)
            if not cmd:
                break

            if cmd.lower() in ['l','list']:
                with Session(self.engine) as session:
                    tags=[]
                    allTags=session.query(Entry).all()
                    for i in allTags:
                        if i.Tags and i.Tags != '':
                            try:
                                tl=json.loads(i.Tags)
                                for t in tl:
                                    if t not in tags:
                                        tags.append(t)
                            except Exception as e:
                                print(e)
                    tagCt=len(tags)
                    for num,t in enumerate(tags):
                        print(f"{Fore.green}{num}{Style.reset}/{Fore.light_red}{tagCt-1}{Style.reset} -> {Fore.light_magenta}'{Style.reset}{Fore.grey_70}{t}{Style.reset}{Fore.light_magenta}'{Style.reset}")
            elif cmd.lower() in ['pa','prompted_add','prompted add','auto_add','auto add','aa']:
                while True:
                    try:
                        with Session(self.engine) as session:
                            query=session.query(Entry)
                            def mkT(text,self):
                                return text
                            tag=Prompt.__init2__(None,func=mkT,ptext="Tag(s)[Comma separated]",helpText="Tag to add to code")
                            try:
                                #code=Prompt.__init2__(None,func=mkT,ptext="Code|Barcode",helpText=f"Code|Barcode to add Tag:'{tag}' to.")
                                #if code in [None,]:
                                #    break
                                def addTag(session,entry,tag):
                                    try:
                                        old=list(json.loads(entry.Tags))
                                        for t in tag.split(","):
                                            if t not in old:
                                                old.append(t)
                                        entry.Tags=json.dumps(old)
                                    except Exception as e:
                                        print(e)
                                        entry.Tags=json.dumps(list(tag.split(",")))
                                    session.commit()
                                    session.flush()
                                    session.refresh(entry)
                                    
                                def e_do(self,code,tag):
                                    with Session(self.engine) as session:
                                        try:
                                            code=int(code)
                                            query=session.query(Entry).filter(Entry.EntryId==code)
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                addTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                        except Exception as e:
                                            print(e)

                                def b_do(self,code,tag):
                                    with Session(self.engine) as session:
                                        query=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Barcode.icontains(code)))
                                        results=query.all()
                                        ct=len(results)
                                        if len(results)==0:
                                            print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")                                            
                                        for num,r in enumerate(results):
                                            if num%2==0:
                                                colorEntry=Style.bold
                                            else:
                                                colorEntry=Fore.grey_70+Style.underline
                                            addTag(session,r,tag)
                                            session.refresh(r)
                                            compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                            if num == 0:
                                                color1=Fore.light_green
                                            elif num > 0 and num%2==0:
                                                color1=Fore.green_yellow
                                            elif num > 0 and num%2!=0:
                                                color1=Fore.dark_goldenrod
                                            elif num+1 == ct:
                                                color1=Fore.light_red
                                            print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")

                                def c_do(self,code,tag):
                                    with Session(self.engine) as session:
                                        query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Code.icontains(code)))
                                        results=query.all()
                                        ct=len(results)
                                        if len(results)==0:
                                            print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                        for num,r in enumerate(results):
                                            if num%2==0:
                                                colorEntry=Style.bold
                                            else:
                                                colorEntry=Fore.grey_70+Style.underline
                                            addTag(session,r,tag)
                                            session.refresh(r)
                                            compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                            if num == 0:
                                                color1=Fore.light_green
                                            elif num > 0 and num%2==0:
                                                color1=Fore.green_yellow
                                            elif num > 0 and num%2!=0:
                                                color1=Fore.dark_goldenrod
                                            elif num+1 == ct:
                                                color1=Fore.light_red
                                            print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                def do(self,code,tag):
                                    with Session(self.engine) as session:
                                        query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Barcode==code,Entry.Code.icontains(code),Entry.Barcode.icontains(code)))
                                        results=query.all()
                                        ct=len(results)
                                        if len(results)==0:
                                            print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                        for num,r in enumerate(results):
                                            if num%2==0:
                                                colorEntry=Style.bold
                                            else:
                                                colorEntry=Fore.grey_70+Style.underline
                                            addTag(session,r,tag)
                                            compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                            if num == 0:
                                                color1=Fore.light_green
                                            elif num > 0 and num%2==0:
                                                color1=Fore.green_yellow
                                            elif num > 0 and num%2!=0:
                                                color1=Fore.dark_goldenrod
                                            elif num+1 == ct:
                                                color1=Fore.light_red
                                            print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                                
                                ex={
                                    'delim':'.',
                                    'e_do':lambda code,tag=tag,self=self:e_do(self,code,tag),
                                    'c_do':lambda code,tag=tag,self=self:c_do(self,code,tag),
                                    'b_do':lambda code,tag=tag,self=self:b_do(self,code,tag),
                                    'do':lambda code,tag=tag,self=self:do(self,code,tag)
                                }
                                status=Prompt.__init2__(None,func=prefix_filter,ptext="Code|Barcode|(e|B|c).$code) ",helpText="Code|Barcode|EntryId to have tag applied to prefix will use the specified field e. == EntryID, c. == Code, B. == Barcode.",data=ex)
                                if status in [None,]:
                                    break
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)
            elif cmd.lower() in ['pr','prompted_rm','prompted rm','auto_rm','auto rm','arm']:
                while True:
                    try:
                        with Session(self.engine) as session:
                            query=session.query(Entry)
                            def mkT(text,self):
                                return text
                            tag=Prompt.__init2__(None,func=mkT,ptext="Tag(s)[Comma separated]",helpText="Tag to add to code")
                            try:
                                #code=Prompt.__init2__(None,func=mkT,ptext="Code|Barcode",helpText=f"Code|Barcode to add Tag:'{tag}' to.")
                                #if code in [None,]:
                                #    break
                                def rmTag(session,entry,tag):
                                    try:
                                        old=list(json.loads(entry.Tags))
                                        tmp=[]
                                        for t in old:
                                            if t not in tag.split(","):
                                                tmp.append(t)
                                            else:
                                                print(f"{Fore.grey_70}Removing Tag '{Fore.light_yellow}{t}{Fore.grey_70}'{Style.reset}")

                                        entry.Tags=json.dumps(tmp)
                                    except Exception as e:
                                        print(e)
                                        entry.Tags=json.dumps([])
                                    session.commit()
                                    session.flush()
                                    session.refresh(entry)
                                    
                                def e_do(self,code,tag):
                                    with Session(self.engine) as session:
                                        try:
                                            code=int(code)
                                            query=session.query(Entry).filter(Entry.EntryId==code)
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                rmTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                        except Exception as e:
                                            print(e)

                                def b_do(self,code,tag):
                                    with Session(self.engine) as session:
                                        query=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Barcode.icontains(code)))
                                        results=query.all()
                                        ct=len(results)
                                        if len(results)==0:
                                            print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")                                            
                                        for num,r in enumerate(results):
                                            if num%2==0:
                                                colorEntry=Style.bold
                                            else:
                                                colorEntry=Fore.grey_70+Style.underline
                                            rmTag(session,r,tag)
                                            session.refresh(r)
                                            compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                            if num == 0:
                                                color1=Fore.light_green
                                            elif num > 0 and num%2==0:
                                                color1=Fore.green_yellow
                                            elif num > 0 and num%2!=0:
                                                color1=Fore.dark_goldenrod
                                            elif num+1 == ct:
                                                color1=Fore.light_red
                                            print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")

                                def c_do(self,code,tag):
                                    with Session(self.engine) as session:
                                        query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Code.icontains(code)))
                                        results=query.all()
                                        ct=len(results)
                                        if len(results)==0:
                                            print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                        for num,r in enumerate(results):
                                            if num%2==0:
                                                colorEntry=Style.bold
                                            else:
                                                colorEntry=Fore.grey_70+Style.underline
                                            rmTag(session,r,tag)
                                            session.refresh(r)
                                            compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                            if num == 0:
                                                color1=Fore.light_green
                                            elif num > 0 and num%2==0:
                                                color1=Fore.green_yellow
                                            elif num > 0 and num%2!=0:
                                                color1=Fore.dark_goldenrod
                                            elif num+1 == ct:
                                                color1=Fore.light_red
                                            print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                def do(self,code,tag):
                                    with Session(self.engine) as session:
                                        query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Barcode==code,Entry.Code.icontains(code),Entry.Barcode.icontains(code)))
                                        results=query.all()
                                        ct=len(results)
                                        if len(results)==0:
                                            print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                        for num,r in enumerate(results):
                                            if num%2==0:
                                                colorEntry=Style.bold
                                            else:
                                                colorEntry=Fore.grey_70+Style.underline
                                            rmTag(session,r,tag)
                                            compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                            if num == 0:
                                                color1=Fore.light_green
                                            elif num > 0 and num%2==0:
                                                color1=Fore.green_yellow
                                            elif num > 0 and num%2!=0:
                                                color1=Fore.dark_goldenrod
                                            elif num+1 == ct:
                                                color1=Fore.light_red
                                            print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                                
                                ex={
                                    'delim':'.',
                                    'e_do':lambda code,tag=tag,self=self:e_do(self,code,tag),
                                    'c_do':lambda code,tag=tag,self=self:c_do(self,code,tag),
                                    'b_do':lambda code,tag=tag,self=self:b_do(self,code,tag),
                                    'do':lambda code,tag=tag,self=self:do(self,code,tag)
                                }
                                status=Prompt.__init2__(None,func=prefix_filter,ptext="Code|Barcode|(e|B|c).$code) ",helpText="Code|Barcode|EntryId to have tag applied to prefix will use the specified field e. == EntryID, c. == Code, B. == Barcode.",data=ex)
                                if status in [None,]:
                                    break
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)
            elif cmd.lower() in ['s','search']:
                def mkT(text,self):
                    return text
                tag=Prompt.__init2__(None,func=mkT,ptext='Tag[help]?',helpText=self.helpText_tags,data=self)
                if not tag:
                    break
               
                with Session(self.engine) as session:
                    results=session.query(Entry).all()
                    ct=len(results)
                    t=[]
                    print(f"{Fore.cyan}Checking all Entries for exact match with JSON parsing Enabled!{Style.reset}")
                    for num,r in enumerate(results):
                        #print(r.Tags)
                        try:
                            if r.Tags not in ['',None]:

                                if tag in list(json.loads(r.Tags)):
                                    t.append(r)
                        except Exception as e:
                            pass
                    print(f"{Fore.light_sea_green}Checking Entries via IContains from SQLAlchemy!{Style.reset}")
                    dble_t=session.query(Entry).filter(Entry.Tags.icontains(tag)).all()
                    t.extend(dble_t)
                    t=set(t)
                    ct=len(t)
                    for num,rr in enumerate(t):
                        print(f"{Fore.green}{num}{Style.reset}/{Fore.light_red}{ct}{Style.reset} -> {rr}")
                    print(f"{Fore.light_yellow}there was/were {Style.reset}{Fore.light_blue}{len(t)} Results.{Style.reset}")
                    inlist=Prompt.__init2__(None,func=mkT,ptext='Set Results to Have InList=True[help] and ListQty=-1?',helpText=self.helpText_tags,data=self)
                    if not inlist:
                        break
                    if inlist.lower() in ['y','yes']:
                        ct2=len(t)
                        for num,x in enumerate(t):
                            x.InList=True
                            x.ListQty=-1
                            print(f"{Fore.light_green}{num}{r.EntryId}={Style.reset}{Fore.light_yellow}{r.InList}{Style.reset}/{Fore.light_red}{ct2}{Style.reset}")
                            if num%50 ==0:
                                session.commit()
                        session.commit()
            elif cmd.lower() in ['ba','bulk_tag_add']:
                while True:
                    try:
                        with Session(self.engine) as session:
                            query=session.query(Entry)
                            def mkT(text,self):
                                return text
                            tag=Prompt.__init2__(None,func=mkT,ptext="Tag",helpText="Tag to add to code")
                            while True:
                                try:
                                    #code=Prompt.__init2__(None,func=mkT,ptext="Code|Barcode",helpText=f"Code|Barcode to add Tag:'{tag}' to.")
                                    #if code in [None,]:
                                    #    break
                                    def addTag(session,entry,tag):
                                        try:
                                            old=list(json.loads(entry.Tags))
                                            if tag not in old:
                                                old.append(tag)
                                            entry.Tags=json.dumps(old)
                                        except Exception as e:
                                            print(e)
                                            entry.Tags=json.dumps([tag,])
                                        session.commit()
                                        session.flush()
                                        session.refresh(entry)
                                        
                                    def e_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            try:
                                                code=int(code)
                                                query=session.query(Entry).filter(Entry.EntryId==code)
                                                results=query.all()
                                                ct=len(results)
                                                if len(results)==0:
                                                    print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                                for num,r in enumerate(results):
                                                    if num%2==0:
                                                        colorEntry=Style.bold
                                                    else:
                                                        colorEntry=Fore.grey_70+Style.underline
                                                    addTag(session,r,tag)
                                                    session.refresh(r)
                                                    compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                    if num == 0:
                                                        color1=Fore.light_green
                                                    elif num > 0 and num%2==0:
                                                        color1=Fore.green_yellow
                                                    elif num > 0 and num%2!=0:
                                                        color1=Fore.dark_goldenrod
                                                    elif num+1 == ct:
                                                        color1=Fore.light_red
                                                    print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                            except Exception as e:
                                                print(e)
                                        return True

                                    def b_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Barcode.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")                                            
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                addTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                        return True

                                    def c_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Code.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                addTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                        return True
                                    def do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Barcode==code,Entry.Code.icontains(code),Entry.Barcode.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                addTag(session,r,tag)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                        return True
                                                    
                                    ex={
                                        'delim':'.',
                                        'e_do':lambda code,tag=tag,self=self:e_do(self,code,tag),
                                        'c_do':lambda code,tag=tag,self=self:c_do(self,code,tag),
                                        'b_do':lambda code,tag=tag,self=self:b_do(self,code,tag),
                                        'do':lambda code,tag=tag,self=self:do(self,code,tag)
                                    }
                                    status=Prompt.__init2__(None,func=prefix_filter,ptext="Code|Barcode|(e|B|c).$code) ",helpText="Code|Barcode|EntryId to have tag applied to prefix will use the specified field e. == EntryID, c. == Code, B. == Barcode.",data=ex)
                                    if status in [None,]:
                                        break   
                                except Exception as e:
                                    print(e)

                        break
                    except Exception as e:
                        print(e)
            elif cmd.lower() in ['br','btr','bulk_tag_rem']:
                while True:
                    try:
                        with Session(self.engine) as session:
                            query=session.query(Entry)
                            def mkT(text,self):
                                return text
                            tag=Prompt.__init2__(None,func=mkT,ptext="Tag",helpText="Tag to remove from code")
                            while True:
                                try:
                                    #code=Prompt.__init2__(None,func=mkT,ptext="Code|Barcode",helpText=f"Code|Barcode to add Tag:'{tag}' to.")
                                    #if code in [None,]:
                                    #    break
                                    def remTag(session,entry,tag):
                                        try:
                                            old=list(json.loads(entry.Tags))
                                            if tag not in old:
                                                return
                                            tmp=[]
                                            for t in old:
                                                if t != tag:
                                                    tmp.append(t)
                                            entry.Tags=json.dumps(tmp)
                                        except Exception as e:
                                            print(e)
                                            entry.Tags=json.dumps([])
                                        session.commit()
                                        session.flush()
                                        session.refresh(entry)

                                    def e_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            try:
                                                code=int(code)
                                                query=session.query(Entry).filter(Entry.EntryId==code)
                                                results=query.all()
                                                ct=len(results)
                                                if len(results)==0:
                                                    print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                                for num,r in enumerate(results):
                                                    results=query.all()
                                                    if num%2==0:
                                                        colorEntry=Style.bold
                                                    else:
                                                        colorEntry=Fore.grey_70+Style.underline
                                                    remTag(session,r,tag)
                                                    session.refresh(r)
                                                    compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                    if num == 0:
                                                        color1=Fore.light_green
                                                    elif num > 0 and num%2==0:
                                                        color1=Fore.green_yellow
                                                    elif num > 0 and num%2!=0:
                                                        color1=Fore.dark_goldenrod
                                                    elif num+1 == ct:
                                                        color1=Fore.light_red
                                                    print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                                    
                                            except Exception as e:
                                                print(e)
                                        return True
                                    def b_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Barcode.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")                                            
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                remTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                                    
                                                #print(f"{Fore.light_yellow}{num}{Style.reset}/{Fore.light_red}{ct}{Style.reset} -> {r}")
                                                #remTag(session,r,tag)
                                        return True
                                    def c_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Code.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                remTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                        return True   
                                    def do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Barcode==code,Entry.Code.icontains(code),Entry.Barcode.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                remTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                        return True  
                                    ex={
                                        'delim':'.',
                                        'e_do':lambda code,tag=tag,self=self:e_do(self,code,tag),
                                        'c_do':lambda code,tag=tag,self=self:c_do(self,code,tag),
                                        'b_do':lambda code,tag=tag,self=self:b_do(self,code,tag),
                                        'do':lambda code,tag=tag,self=self:do(self,code,tag)
                                    }
                                    status=Prompt.__init2__(None,func=prefix_filter,ptext="Code|Barcode|(e|B|c).$code) ",helpText="Code|Barcode|EntryId to have tag remove from (prefix will use the specified field e. == EntryID, c. == Code, B. == Barcode.)",data=ex)
                                    if status in [None,]:
                                        break   
                                except Exception as e:
                                    print(e)

                        break
                    except Exception as e:
                        print(e)
            elif cmd.lower() in ['reset_all_tags','clear_all_tags','cat','rat']:
                with Session(self.engine) as session:
                    query=session.query(Entry)
                    results=query.all()
                    ct=len(results)
                    if ct == 0:
                        print(f"{Fore.light_red}No Entry's with Tags to reset!{Style.reset}")
                    for num,r in enumerate(results):
                        setattr(r,'Tags',json.dumps([]))
                        if num%200==0:
                            session.commit()
                            session.flush()
                        if num%2==0:
                            colorEntry=Style.bold
                        else:
                            colorEntry=Fore.grey_70+Style.underline
                        compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                        if num == 0:
                            color1=Fore.light_green
                        elif num > 0 and num%2==0:
                            color1=Fore.green_yellow
                        elif num > 0 and num%2!=0:
                            color1=Fore.dark_goldenrod
                        elif num+1 == ct:
                            color1=Fore.light_red

                        print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                    session.commit()
                    session.flush()
            elif cmd.lower() in ['dedup_all_tags','ddat',]:
                with Session(self.engine) as session:
                    query=session.query(Entry)
                    results=query.all()
                    ct=len(results)
                    if ct == 0:
                        print(f"{Fore.light_red}No Entry's with Tags to reset!{Style.reset}")
                    for num,r in enumerate(results):
                        #processHERE
                        try:
                            if r.Tags in ['',None]:
                                r.Tags=json.dumps([])
                            else:
                                t=json.loads(r.Tags)
                                tt=Tags=list(t)
                                ttt=list(set(tt))
                                setattr(r,'Tags',json.dumps(ttt))
                        except Exception as e:
                            print(e)
                            #print(r,r.Tags,type(r.Tags))
                            #exit()
                            #setattr(r,'Tags',json.dumps([]))
                        #setattr(r,'Tags',json.dumps([]))
                        if num%200==0:
                            session.commit()
                            session.flush()
                        if num%2==0:
                            colorEntry=Style.bold
                        else:
                            colorEntry=Fore.grey_70+Style.underline
                        compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                        if num == 0:
                            color1=Fore.light_green
                        elif num > 0 and num%2==0:
                            color1=Fore.green_yellow
                        elif num > 0 and num%2!=0:
                            color1=Fore.dark_goldenrod
                        elif num+1 == ct:
                            color1=Fore.light_red

                        print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                    session.commit()
                    session.flush()
            else:
                split_cmd=cmd.split(",")
                if len(split_cmd) == 4:
                    #$mode,$search_fieldname,$EntryId,$tag
                    mode=split_cmd[0]
                    tag=[split_cmd[1],] 
                    search_fieldname=split_cmd[2]
                    eid=split_cmd[3]
                    with Session(self.engine) as session:
                        #print(split_cmd,type(eid),search_fieldname)
                        if search_fieldname == 'Barcode':
                            rs=session.query(Entry).filter(Entry.Barcode==eid).all()
                        elif search_fieldname == 'Code':
                            rs=session.query(Entry).filter(Entry.Code==eid).all()
                        elif search_fieldname == 'ALT_Barcode':
                            rs=session.query(Entry).filter(Entry.ALT_Barcode==eid).all()
                        elif search_fieldname == 'EntryId':
                            rs=session.query(Entry).filter(Entry.ALT_Barcode==int(eid)).all()
                        else:
                            print(self.helpText_tags)
                            return
                        #result=session.query(Entry).filter(getattr(Entry,search_fieldname)==eid).all()
                        result=rs
                        #print(len(result))
                        for num,r in enumerate(result):
                            msg=''
                            if r.Tags == '':
                                 r.Tags=json.dumps(list(tag))
                            session.commit()
                            session.refresh(r)
                            
                            if mode in ['=','r','R']:
                                r.Tags=json.dumps(list(tag))
                            elif mode == '+':
                                try:
                                    old=json.loads(r.Tags)
                                    if tag[0] not in old:
                                        old.append(tag[0])
                                        r.Tags=json.dumps(old)
                                    else:
                                        msg=f"{Fore.light_yellow}Tag is Already Applied Nothing will be Done!{Style.reset}"
                                except Exception as e:
                                    print(e)
                            elif mode == '-':
                                try:
                                    old=json.loads(r.Tags)
                                    if tag[0] in old:
                                        i=old.index(tag[0])
                                        old.pop(i)
                                        r.Tags=json.dumps(old)
                                    else:
                                        msg=f"{Fore.light_red}No Such Tag in Item...{Fore.light_yellow} Nothing will be done!{Style.reset}"
                                except Exception as e:
                                    print(e)
                                

                            
                            session.commit()
                            session.flush()
                            session.refresh(r)
                            print(r)
                            print(msg)
                else:
                    print(self.helpText_tags)


    def setName(self):
        with Session(self.engine) as session:
            def mkT(text,self):
                    return text
            fieldname='SetName'
            mode='TaskMode'
            h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
            code=Prompt.__init2__(None,func=mkT,ptext=f'{h}Code|Barcode[help]?',helpText='',data=self)
            if not code:
                return
            
            value=Prompt.__init2__(None,func=mkT,ptext='Name[help]?',helpText='',data=self)
            if not value:
                return
           
            result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code)).first()
            if result:
                result.Name=value
                session.commit()
                session.flush()
                session.refresh(result)
                print(result)
            else:
                print(f"{Fore.light_red}{Style.bold}No Such Item Identified by '{code}'{Style.reset}")
    
    def printLastGenerated(self):
        of=Path("GeneratedString.txt")
        if not of.exists():
            print(f"{Fore.orange_red_1}{of} {Fore.cyan}EXISTS{Style.bold}{Fore.green}={Style.reset}{Fore.light_red}{of.exists()}{Style.reset}")
            return
        try:
            with open(of,"r") as ifile:
                print(f"'{Fore.light_yellow}{ifile.read()}{Style.reset}'")
        except Exception as e:
            print(e)


    def GenPassMenu(self):
        print(f"{Fore.orange_red_1}The File Genrated will automatically be deleted when its age is over 15-days old, so back it up else where if you really need it!{Style.reset}")
        pwo=PasswordGenerator()
        pwo.minlen=16
        # All properties are optional
        '''
        pwo.minlen = 30 # (Optional)
        pwo.maxlen = 30 # (Optional)
        pwo.minuchars = 2 # (Optional)
        pwo.minlchars = 3 # (Optional)
        pwo.minnumbers = 1 # (Optional)
        pwo.minschars = 1 # (Optional)
        '''
        n=pwo.generate()
        of=Path("GeneratedString.txt")
        print(f"'{Fore.light_yellow}{n}{Style.reset}'")
        with open(of,"w+") as out:
            out.write(n)
        print(f"{Fore.light_green}Written to {Fore.light_steel_blue}{of.absolute()}{Style.reset}")

    def list_total(self):
        with Session(self.engine) as session:
            results=session.query(Entry).filter(Entry.InList==True).all()
            ct=len(results)
            total=0
            total_case=0
            total_units=0
            total_units_br=0
            for num,r in enumerate(results):
                print(f"{Fore.green}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} -> {r}")
                total+=r.total_value(CaseMode=False)
                total_case+=r.total_value(CaseMode=True)
                total_units+=r.total_units()
                total_units_br+=r.total_units(BackRoom=False)
            #print(total_units,total_units_br)
            print(f"""
{Fore.light_green}Total By Units: ${Fore.light_red}{total}{Style.reset}{Fore.green_yellow} for{Fore.light_red} {total_units} w/BackRoom{Fore.light_green} | {total_units_br} {Fore.light_magenta}wo/BackRoom{Style.reset}
{Fore.light_green}Total By Case: ${Fore.light_red}{total_case}{Style.reset}{Fore.green_yellow} for{Fore.light_red} {total_units} w/BackRoom{Fore.light_green} | {total_units_br} {Fore.light_magenta}wo/BackRoom{Style.reset} 
""")
    def clear_system_tags(self,tags):
        ct=len(tags)
        for num,tag in enumerate(tags):
            print(f"removing tag {num}/{ct-1} '{tag}'")
            tagList(engine=self.engine,state=False,tag=tag)

    def __init__(self,engine,parent):
        self.reset_next_barcode()
        of=Path("GeneratedString.txt")
        if of.exists():
            age=datetime.now()-datetime.fromtimestamp(of.stat().st_ctime)
            days=float(age.total_seconds()/60/60/24)
            if days > 15:
                print(f"{Fore.light_yellow}Time is up, removeing old string file! {Fore.light_red}{of}{Style.reset}")
                of.unlink()
            else:
                print(f"{Fore.light_yellow}{of} {Fore.light_steel_blue}is {round(days,2)} {Fore.light_red}Days old!{Fore.light_steel_blue} you have {Fore.light_red}{15-round(days,2)} days{Fore.light_steel_blue} left to back it up!{Style.reset}")

        self.engine=engine
        self.parent=parent
        self.special=['Tags','ALT_Barcode','DUP_Barcode','CaseID_6W','CaseID_BR','CaseID_LD','Facings']
        self.valid_fields=['Shelf',
        'BackRoom',
        'Display_1',
        'Display_2',
        'Display_3',
        'Display_4',
        'Display_5',
        'Display_6',
        'ALT_Barcode',
        'DUP_Barcode',
        'CaseID_BR',
        'CaseID_LD',
        'CaseID_6W',
        'Tags',
        'Facings',
        'SBX_WTR_DSPLY',
        'SBX_CHP_DSPLY',
        'SBX_WTR_KLR',
        'FLRL_CHP_DSPLY',
        'FLRL_WTR_DSPLY',
        'WD_DSPLY',
        'CHKSTND_SPLY',
        ]
        '''
        ALT_Barcode=Column(String)
        DUP_Barcode=Column(String)
        CaseID_BR=Column(String)
        CaseID_LD=Column(String)
        CaseID_6W=Column(String)
        Tags=Column(String)
        Facings=Column(Integer)
        SBX_WTR_DSPLY=Column(Integer)
        SBX_CHP_DSPLY=Column(Integer)
        SBX_WTR_KLR=Column(Integer)
        FLRL_CHP_DSPLY=Column(Integer)
        FLRL_WTR_DSPLY=Column(Integer)
        WD_DSPLY=WD_DSPLY=Column(Integer)
        CHKSTND_SPLY=CHKSTND_SPLY=Column(Integer)
        '''
        #self.display_field("Shelf")
        self.options={
                '1':{
                    'cmds':['q','quit','#1'],
                    'desc':"quit program",
                    'exec':lambda: exit("user quit!"),
                    },
                '2':{
                    'cmds':['b','back','#2'],
                    'desc':'go back menu if any',
                    'exec':None
                    },
                }
        #autogenerate duplicate functionality for all valid fields for display
        count=3
        location_fields={
            "Shelf":None,
            "BackRoom":None,
            "Display_1":None,
            "Display_2":None,
            "Display_3":None,
            "Display_4":None,
            "Display_5":None,
            "Display_6":None,
            "ListQty":None,
            "SBX_WTR_DSPLY":None,
            "SBX_CHP_DSPLY":None,
            "SBX_WTR_KLR":None,
            "FLRL_CHP_DSPLY":None,
            "FLRL_WTR_DSPLY":None,
            "WD_DSPLY":None,
            "CHKSTND_SPLY":None,

            "set Shelf":None,
            "set BackRoom":None,
            "set Display_1":None,
            "set Display_2":None,
            "set Display_3":None,
            "set Display_4":None,
            "set Display_5":None,
            "set Display_6":None,
            "set ListQty":None,
            "set ListQty":None,
            "set SBX_WTR_DSPLY":None,
            "set SBX_CHP_DSPLY":None,
            "set SBX_WTR_KLR":None,
            "set FLRL_CHP_DSPLY":None,
            "set FLRL_WTR_DSPLY":None,
            "set WD_DSPLY":None,
            "set CHKSTND_SPLY":None,
        }
        def print_location_fields(location_fields):
            for num,k in enumerate(location_fields):
                if num%2==0:
                    color1_field=Fore.sea_green_1a
                    cmd_alter=Fore.light_steel_blue
                else:
                    color1_field=Fore.spring_green_1
                    cmd_alter=Fore.cyan
                if 'set ' in k:
                    tmp=f'{Fore.orange_red_1}{Style.bold}*{Style.reset}'
                else:
                    tmp=''
                #print(location_fields[k],f'"{k}"')
                msg=f"{tmp}{color1_field}{k}{Style.reset} - {'|'.join([f'{cmd_alter}{i}{Style.reset}' for i in location_fields[k]])}"
                print(msg)

        for entry in self.valid_fields:
            self.options[entry]={
                    'cmds':["#"+str(count),f"ls {entry}"],
                    'desc':f'list needed @ {entry}',
                    'exec':lambda self=self,entry=entry: self.display_field(f"{entry}"),
                    }
            if entry in list(location_fields.keys()):
                location_fields[entry]=self.options[entry]['cmds']
            count+=1

        #setoptions
        #self.setFieldInList("Shelf")
        for entry in self.valid_fields:
            self.options[entry+"_set"]={
                    'cmds':["#"+str(count),f"set {entry}"],
                    'desc':f'set needed @ {entry}',
                    'exec':lambda self=self,entry=entry: self.setFieldInList(f"{entry}"),
                    }
            if f"set {entry}" in list(location_fields.keys()):
                location_fields[f"set {entry}"]=self.options[entry+"_set"]['cmds']
            count+=1
        self.options["lu"]={
                    'cmds':["#"+str(count),f"lookup","lu","check","ck"],
                    'desc':f'get total for valid fields',
                    'exec':lambda self=self,entry=entry: self.getTotalwithBreakDownForScan(),
                    }
        count+=1
        self.options["setName"]={
                    'cmds':["#"+str(count),f"setName","sn"],
                    'desc':f'set name for item by barcode!',
                    'exec':lambda self=self,entry=entry: self.setName(),
                    }
        count+=1
        self.options["setListQty"]={
                    'cmds':["#"+str(count),f"setListQty","slq"],
                    'desc':f'set ListQty for Values not wanted to be included in totals.',
                    'exec':lambda self=self: self.setFieldInList("ListQty",load=True),
                    }
        location_fields["set ListQty"]=self.options["setListQty"]['cmds']
        count+=1
        self.options["lsListQty"]={
                    'cmds':["#"+str(count),f"lsListQty","ls-lq"],
                    'desc':f'show ListQty for Values not wanted to be included in totals.',
                    'exec':lambda self=self: self.display_field("ListQty",load=True),
                    }
        location_fields["ListQty"]=self.options["lsListQty"]['cmds']
        count+=1
        self.options["listTotal"]={
                    'cmds':["#"+str(count),f"listTotal","list_total"],
                    'desc':f'show list total value.',
                    'exec':lambda self=self: self.list_total(),
                    }
        count+=1
        self.options["lus"]={
                    'cmds':["#"+str(count),f"lookup_short","lus","lu-","check","ck-","ls"],
                    'desc':f'get total for valid fields short view',
                    'exec':lambda self=self,entry=entry: self.getTotalwithBreakDownForScan(short=True),
                    }
        count+=1
        self.options["b1"]={
                    'cmds':["#"+str(count),f"barcode_first","b1"],
                    'desc':f'list mode where barcode is asked first',
                    'exec':lambda self=self: self.setFieldInList(None,load=True),
                    }
        count+=1
        self.options["el2e"]={
                    'cmds':["#"+str(count),f"export-list-2-excel","el2e"],
                    'desc':f'export fields {self.exportList2Excel(fields=True)} to Excel file',
                    'exec':lambda self=self: self.exportList2Excel(),
                    }
        count+=1
        self.options["formula"]={
                    'cmds':["#"+str(count),f"formula","eval"],
                    'desc':f'solve an equation | same tool as "c"|"calc"',
                    'exec':lambda self=self: self.evaluateFormula(),
                    }
        count+=1
        self.options["tag_reverse_inventory_1"]={
                    'cmds':["#"+str(count),f"tag_reverse_inventory_1","tri1",],
                    'desc':f'add Tag "ReverseInventory" to Entry\'s with InList==True',
                    'exec':lambda self=self: tagList(engine=self.engine,state=True,tag="ReverseInventory",removeTag=['have/has',]),
                    }
        count+=1
        self.options["tag_reverse_inventory_0"]={
                    'cmds':["#"+str(count),f"tag_reverse_inventory_0","tri0",],
                    'desc':f'remove Tag "ReverseInventory" to Entry\'s with InList==True',
                    'exec':lambda self=self: tagList(engine=self.engine,state=False,tag="ReverseInventory"),
                    }
        count+=1
        self.options["tag_have/has_1"]={
                    'cmds':["#"+str(count),f"tag_have/has_1","th1",],
                    'desc':f'add Tag "have/has" to Entry\'s with InList==True',
                    'exec':lambda self=self: tagList(engine=self.engine,state=True,tag="have/has",removeTag=["ReverseInventory",]),
                    }
        count+=1
        self.options["tag_have/has_0"]={
                    'cmds':["#"+str(count),f"tag_have/has_0","th0",],
                    'desc':f'remove Tag "have/has" to Entry\'s with InList==True',
                    'exec':lambda self=self: tagList(engine=self.engine,state=False,tag="have/has"),
                    }
        count+=1
        self.options["clear_system_tags"]={
                    'cmds':["#"+str(count),f"clear_system_tags","cst",],
                    'desc':f'remove/clear system tags',
                    'exec':lambda self=self: self.clear_system_tags(["have/has","ReverseInventory",])
                    }
        count+=1
        self.options["addPersonalTags"]={
                    'cmds':["#"+str(count),f"pt1","personal_tag_1",],
                    'desc':f'add a personal tag to list',
                    'exec':lambda self=self: tagList(engine=self.engine,state=True,tag=None,removeTag=['',])
                    }
        count+=1
        self.options["remPersonalTags"]={
                    'cmds':["#"+str(count),f"pt0","personal_tag_0",],
                    'desc':f'remove a personal tag from list',
                    'exec':lambda self=self: tagList(engine=self.engine,state=False,tag=None,removeTag=['',])
                    }
        count+=1
        self.options["list location fields"]={
                    'cmds':["#"+str(count),f"llf","list location fields","list_location_fields"],
                    'desc':f'list location fields cmds',
                    'exec':lambda self=self: print_location_fields(location_fields),
                    }
        count+=1
        self.options["New Entry Menu"]={
                    'cmds':["#"+str(count),f"nem","new entry menu","new_entry_menu"],
                    'desc':f'menu of options to add new Entry\' to the system',
                    'exec':lambda self=self: self.NewEntryMenu(),
                    }
        count+=1
        self.options["New Password Menu"]={
                    'cmds':["#"+str(count),f"gpwd","gen passwd","gen_passwd","gpass","genpass","gen pass","gen_pass"],
                    'desc':f'create a new random string, not backed up',
                    'exec':lambda self=self: self.GenPassMenu(),
                    }
        count+=1
        self.options["Print Old Password Menu"]={
                    'cmds':["#"+str(count),f"ppwd","print passwd","print_passwd","ppass","p_pass","gen pass","pass","lpass","last pass","last pwd","lst pwd"],
                    'desc':f'print last random string',
                    'exec':lambda self=self: self.printLastGenerated(),
                    }
        count+=1
        self.options["RandomString Menu"]={
                    'cmds':["#"+str(count),f"rs","rsm","random string","random_string","random string menu","random_string_menu",],
                    'desc':f'random string menu',
                    'exec':lambda self=self: RandomStringUtilUi(parent=self,engine=self.engine),
                    }
        count+=1
        '''
        self.options["Find Duplicates"]={
                    'cmds':["#"+str(count),f"fd","find_dupes"],
                    'desc':f'find duplicate Entry by Barcode',
                    'exec':lambda self=self: self.findDupes(),
                    }
        count+=1
        '''
        self.options["FB"]={
                    'cmds':["#"+str(count),f"fb","formBuilder"],
                    'desc':f'build new mappings',
                    'exec':lambda self=self: print(FormBuilder(data=fm_data))   ,
                    }
        count+=1
        
        '''
        self.options["new entry from schematic"]={
                    'cmds':["#"+str(count),f"nfsc","new entry from schematic","new_entry_from_schematic"],
                    'desc':f'add a new entry from schematic directly, checking for new item by barcode(Entry that exists will prompt for updates to fields); the Entry added will have InList=True and ListQty=1, so use {Fore.orange_red_1}ls-lq{Style.reset}{Fore.light_yellow} to view items added{Style.reset}',
                    'exec':lambda self=self: self.NewEntrySchematic(),
                    }
        count+=1
        self.options["new entry from shelf"]={
                    'cmds':["#"+str(count),f"nfst","new entry from shelf","new_entry_from_shelf"],
                    'desc':f'add a new entry from shelf available data directly, checking for new item by barcode(Entry that exists will prompt for updates to fields); the Entry added will have InList=True and ListQty=1, so use {Fore.orange_red_1}ls-lq{Style.reset}{Fore.light_yellow} to view items added{Style.reset}',
                    'exec':lambda self=self: self.NewEntryShelf(),
                    }
        count+=1
        self.options["new entry with all fields"]={
                    'cmds':["#"+str(count),f"nfa","new entry from all","new_entry_from_all"],
                    'desc':f'add a new entry from all fields, checking for new item by barcode(Entry that exists will prompt for updates to fields); the Entry added will have InList=True and ListQty=1, so use {Fore.orange_red_1}ls-lq{Style.reset}{Fore.light_yellow} to view items added{Style.reset}',
                    'exec':lambda self=self: self.NewEntryAll(),
                    }
        count+=1
        '''

        while True:
            def mkT(text,self):
                return text
            command=Prompt.__init2__(None,func=mkT,ptext=f'{Fore.grey_70}[{Fore.light_steel_blue}TaskMode{Fore.grey_70}] {Fore.light_yellow}Do What[help/??/?]',helpText=self.parent.help(print_no=True),data=self)
            if not command:
                break
            #command=input(f"{Style.bold}{Fore.green}do what[??/?]:{Style.reset} ")
            if self.parent != None and self.parent.Unified(command):
                print("ran a Unified CMD")
            elif command == "??":
                for num,option in enumerate(self.options):
                    color=Fore.dark_goldenrod
                    color1=Fore.cyan
                    if (num%2)==0:
                        color=Fore.green_yellow
                        color1=Fore.magenta
                    print(f"{color}{self.options[option]['cmds']}{Style.reset} - {color1}{self.options[option]['desc']}{Style.reset}")
            else:
                for option in self.options:
                    if self.options[option]['exec'] != None and (command.lower() in self.options[option]['cmds'] or command in self.options[option]['cmds']):
                        self.options[option]['exec']()
                    elif self.options[option]['exec'] == None and (command.lower() in self.options[option]['cmds'] or command in self.options[option]['cmds']):
                        return
    def promptForOp(self,n,total,entryIdList,barcode):
        with Session(ENGINE) as session:
            try:
                while True:
                    if len(entryIdList) <= 0:
                        return True
                    os.system("clear")
                    results=[]
                    digits=12
                    formula=round((round((os.get_terminal_size().columns/2))-1)-(digits/2))-4
                    footer=f"\n{Style.bold}{Fore.grey_70}+{'-'*formula}{Back.grey_30}{Fore.white}DIGITS{Back.black}{Fore.grey_70}{'-'*formula}+{Style.reset}"
                    fields=['Barcode','Code','Name','EntryId','Price','CRV','Tax','TaxNote','Note','Size','CaseCount','Location','Tags','ALT_Barcode','DUP_Barcode']
                    for num,i in enumerate(entryIdList):
                        entry=session.query(Entry).filter(Entry.EntryId==i).first()
                        if entry:
                            if entry not in results:
                                results.append(entry)
                                msg=f'{Fore.light_steel_blue}Select No.:{num}|Group {Fore.orange_red_1}{n}{Fore.grey_70} of {Fore.light_red}{total-1}{Fore.grey_70} -> {Fore.light_green}{f"{Style.reset} {Fore.magenta}|{Style.reset} {Fore.light_green}".join([i+f"={Fore.light_yellow}"+str(getattr(entry,i)) for i in fields])}{Style.reset}'
                                print(msg+footer.replace('DIGITS',str(num).zfill(digits)))
                    x=f"""Total duplicates in Batch of Barcode({barcode}): {len(entryIdList)}
Do What? [rms,rma,edit/e,<ENTER>/next,prev]"""
                    cmd=Prompt.__init2__(self,func=FormBuilderMkText,ptext=x,helpText="what you will be able to do soon!",data="string")
                    if cmd in [None,]:
                        return
                    print(cmd,f'"{cmd}"')
                    if cmd.lower() in 'prev':
                        return False
                    if cmd.lower() in 'da|deleta_all|rma|rm_all'.split("|"):
                        selected=deepcopy(entryIdList)
                        ct=len(selected)
                        for num,s in enumerate(selected):
                            print(f"deleting {num}/{ct} - {s}")
                            session.query(Entry).filter(Entry.EntryId==s).delete()
                            if num % 100 == 0:
                                session.commit()
                        session.commit()

                        for i in selected:
                            try:
                                entryIdList.remove(i)
                            except Exception as e:
                                print(e,'#')
                        return True
                    elif cmd.lower() in ['d','next']:
                        return True
                    ####Functionality Here
                    else:
                        selected=Prompt.__init2__(self,func=FormBuilderMkText,ptext="select No(s) separated by $CHAR; you will be asked for $CHAR",helpText="returns a list!",data="list")
                        if selected in [None,]:
                            return
                        selected=[entryIdList[int(i)] for i in selected]
                        if cmd.lower() in ['ds','rms','rm selected','del selected']:
                            ct=len(selected)
                            for num,s in enumerate(selected):
                                print(f"deleting {num}/{ct} - {s}")
                                session.query(Entry).filter(Entry.EntryId==s).delete()
                                if num % 100 == 0:
                                    session.commit()
                            session.commit()

                            for i in selected:
                                try:
                                    entryIdList.remove(i)
                                except Exception as e:
                                    print(e,'#')
                        elif cmd.lower() in ['ed','edit',]:
                            ct=len(selected)
                            for num,s in enumerate(selected):
                                print(f"editing {num}/{ct} - {s}")
                                ft={i.name:{'type':str(i.type)} for i in entry.__table__.columns}
                                entry=session.query(Entry).filter(Entry.EntryId==s).first()
                                data={
                                i:{
                                    'default':getattr(entry,i),
                                    'type':ft.get(i)['type'].lower(),
                                    } for i in fields                        
                                }
                                #print(data)
                                updated=FormBuilder(data=data)
                                #print(updated)
                                for k in updated:
                                    setattr(entry,k,updated[k])
                                    if num % 1== 0:
                                        session.commit()
                                session.commit()
                                print("Saved!")
                    done=Prompt.__init2__(self,func=FormBuilderMkText,ptext="Next Batch?",helpText="yes or no",data="bool")
                    if done in [None,]:
                        return
                    elif done == True:
                        return True
            except Exception as e:
                print(e)


    def findDupes(self):
        with Session(ENGINE) as session:
            bcd2eid={}
            results=session.query(Entry).order_by(Entry.Barcode).all()
            for r in results:
                if not bcd2eid.get(r.Barcode):
                    bcd2eid[r.Barcode]=[]
                    bcd2eid[r.Barcode].append(r.EntryId)
                else:
                    if r.EntryId not in bcd2eid[r.Barcode]:
                        bcd2eid[r.Barcode].append(r.EntryId)
            tmp={}
            for k in bcd2eid:
                if len(bcd2eid[k]) > 1:
                    tmp[k]=bcd2eid[k]
            total=0
            index=None
            ready=False
            while True:
                if index == None and ready == True:
                    break
                for n,barcode in enumerate(tmp):
                    print(index)
                    if index != None and n < index:
                        continue
                    index=None
                    for num,eid in enumerate(tmp[barcode]):
                        ct=len(tmp[barcode])
                        total+=1
                        entry=session.query(Entry).filter(Entry.EntryId==eid).first()
                        print(entry,f"Duplicate of {barcode} : {num+1}/{ct} : Total Duplicates = {total}")
                    status=self.promptForOp(n,len(tmp),tmp[barcode],barcode)
                    if status == None:
                        return
                    if status == False:
                        index=n-1
                        break
                ready=True

    def evaluateFormula(self,fieldname='TaskMode',mode='Calculator',fromPrompt=False,oneShot=False):
        if fromPrompt == True:
            return
        while True:
            try:
                accro=Style.bold+Style.underline+Fore.light_red
                p1=Fore.light_magenta
                p2=Fore.light_yellow
                p3=Fore.light_green
                p4=Fore.cyan
                p5=Fore.sea_green_1a
                p6=Fore.green_yellow
                p7=Fore.dark_goldenrod
                symbol=Fore.magenta
                color=[Fore.light_green,Fore.cyan]
                math_methods='\n'.join([f'{color[num%2]}math.{i}{Fore.orange_red_1}(){Style.reset}' for num,i in enumerate(dir(math)) if callable(getattr(math,i))])
                helpText=f'''
{accro}Operator Symbol -> {symbol}()|**|*|/|+|-{Style.reset}
{accro}CVT(value,fromUnit,toUnit) -> {symbol}Convert a value from one to another{Style.reset}
{accro}datetime()+|-datetime()|timedelta() -> {symbol}Add or Subtract datetimes{Style.reset}
{accro}if you know a tool in pandas use pd, or numpy use np ->{symbol}module support for advanced math operations on a single line{Style.reset}
{accro}PEMDAS{Style.reset} - {p1}Please {p2}Excuse {p4}My {p5}Dear {p6}Aunt {p7}Sallie{Style.reset}
{accro}PEMDAS{Style.reset} - {p1}{symbol}({Style.reset}{p1}Parantheses{symbol}){Style.reset} {p3}Exponents{symbol}** {p4}Multiplication{symbol}* {p5}Division{symbol}/ {p6}Addition{symbol}+ {p7}Subtraction{symbol}-{Style.reset}
{math_methods}
yt('12:48') - military time for yesterday
tt('12:48') - military time for today
td('1y1x1d1h30m20s') - timedelta for 1 year 1 month 1 day 1 hour 30 minutes 20 seconds; as long as the number is followed by its hand designator, i.e. h=hour,m=minute,s=second, it will return
a timedelta to use with tt() and yt()
so  `yt('22:30')+td('8h') == tt('6:30')`
    `tt('6:30')-td('8h') == yt('22:30')`
RATE(float value) can be used directly with td() to get gross
`RATE(26.75)*td('8h') == Rate.Gross(value=214.0)||Gross=$(float_value) -> Gross is a generic holder-class for the display
(a/b)*%=F - get F from a fraction times a custom percent, default %=100
a/b=F/d - if 3.76 dollars is used every 22.32 hours, then in 1 hour F is consumed/WHAT?
{Style.reset}'''
                def mkValue(text,self):
                    try:
                        CVT=UnitRegistry().convert
                        fields_dflt={
                        'A':1,
                        'B':2,
                        'D':6,
                        'F':3,
                        'Round To':2,
                        '%':100,
                        }
                        fields=deepcopy(fields_dflt)
                        if text in ['a/b=F/d',]:
                            fields.pop('F')
                            fields.pop('%')

                        if text in ['(a/b)*%=F',]:
                            fields.pop('F')
                            fields.pop('D')

                        if text in ['(a/b)*%=F','a/b=F/d']:
                            for k in fields:
                                fields[k]=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"what is {k}?",helpText=text,data="float")
                                if fields[k] in [None,]:
                                    fields[k]=fields_dflt[k]
                        
                        if text in ['a/b=F/d',]:
                            r=(fields['A']*fields['D'])/fields['B']
                            return round(r,int(fields['Round To']))
                        elif text in ['(a/b)*%=F',]:
                            v=(fields['A']/fields['B'])*fields['%']
                            r=round(v,int(fields['Round To']))
                            return r

                        return eval(text)
                    except Exception as e:
                        print(e)
                        return None,e
                
                h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
                formula=Prompt.__init2__(None,func=mkValue,ptext=f"{h}Type|Tap your equation and remember PEMDAS",helpText=helpText,data=self)

                if formula in [None,]:
                    break
                print(formula)
                if oneShot:
                    return formula
            except Exception as e:
                print(e)




if __name__ == "__main__":
    TasksMode(parent=None,engine=ENGINE)
