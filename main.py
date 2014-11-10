import os
import ConfigParser

cfg_file=os.getcwd()+r'\config.ini'
cf = ConfigParser.ConfigParser()
cf.read(cfg_file)

KEY=cf.get('key', 'key')
FRAME=cf.get('frame','frame')
print 'configuration file is:'
print cfg_file
print 'key section in config.ini is(will use first 64bits only):'
print KEY
print 'frame section in config.ini is(will use first 22bits only)'
print FRAME

#LFSR, 64bits
LFSR1=['0']*19
LFSR2=['0']*22
LFSR3=['0']*23

#LFSR[-1]
reg_temp1='0'
reg_temp2='0'
reg_temp3='0'

#key, 64bits
key=['0']*64
#initialize key according to config.ini
for i in range(64):
    key[i]=KEY[i]

print "key(64bits)(LSB->MSB):"
print ''.join(key)
#frame, 22bits
frame=['0']*22
#initialize frame according to config.ini
for i in range(22):
    frame[i]=FRAME[i]

print "frame(22bits)(LSB->MSB):"
print ''.join(frame)
#output key stream, 228bits
key_stream=['0']*228

def XOR(input1, input2):
    if(input1==input2):
        return '0'
    if(input1!=input2):
        return '1'

def Shift_LFSR1():
    reg_temp1=XOR(LFSR1[18],XOR(LFSR1[17],XOR(LFSR1[16],LFSR1[13])))
    for i in range(18): #i change from 0 to 17
        LFSR1[18-i]=LFSR1[17-i]    
    LFSR1[0]=reg_temp1
    
def Shift_LFSR2():    
    reg_temp2=XOR(LFSR2[21],LFSR2[20])
    for i in range(21):
        LFSR2[21-i]=LFSR2[20-i]
    LFSR2[0]=reg_temp2
    
def Shift_LFSR3():    
    reg_temp3=XOR(LFSR3[22],XOR(LFSR3[21],XOR(LFSR3[20],LFSR3[7])))
    for i in range(22):
        LFSR3[22-i]=LFSR3[21-i]
    LFSR3[0]=reg_temp3

def Clock_Control():
    if((LFSR2[10]==LFSR3[10]) and (LFSR3[10]!=LFSR1[8])):
        Shift_LFSR2()
        Shift_LFSR3()
    if((LFSR1[8]==LFSR3[10]) and (LFSR3[10]!=LFSR2[10])):
        Shift_LFSR1()
        Shift_LFSR3()
    if((LFSR1[8]==LFSR2[10]) and (LFSR2[10]!=LFSR3[10])):
        Shift_LFSR1()
        Shift_LFSR2()
    if((LFSR1[8]==LFSR2[10]) and (LFSR2[10]==LFSR3[10])):
        Shift_LFSR1()
        Shift_LFSR2()
        Shift_LFSR3()
        
def Init():
    for i in range(64):
        LFSR1[0]=XOR(LFSR1[0],key[i])
        LFSR2[0]=XOR(LFSR2[0],key[i])
        LFSR3[0]=XOR(LFSR3[0],key[i])
        Shift_LFSR1()
        Shift_LFSR2()
        Shift_LFSR3()
        
    for i in range(22):
        LFSR1[0]=XOR(LFSR1[0],frame[i])
        LFSR2[0]=XOR(LFSR2[0],frame[i])
        LFSR3[0]=XOR(LFSR3[0],frame[i])
        Shift_LFSR1()
        Shift_LFSR2()
        Shift_LFSR3()
  
Init()
for i in range(100):
    Clock_Control()
    
for i in range(228):
    Clock_Control()
    key_stream[i]=XOR(LFSR1[18],XOR(LFSR2[21],LFSR3[22]))
 
print "key stream(228bits)(LSB->MSB):"    
print ''.join(key_stream)

raw_input("Press <enter> to exit ...")
