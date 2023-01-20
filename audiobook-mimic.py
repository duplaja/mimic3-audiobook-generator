#!/usr/bin/python3
import subprocess
import os
import argparse

parser = argparse.ArgumentParser()
parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
optional = parser.add_argument_group('optional arguments')

required.add_argument("-a", "--author", help="story author", type=str, required=True)
required.add_argument("-t", "--title", help="story title", type=str, required=True)
required.add_argument("-i", "--inputfile", help="story file (input txt filename)", type=str, required=True)

args = parser.parse_args()

#Input from argparse
inputfilename = args.inputfile
author = args.author
title = args.title


print(title)
print(author)

mimicvoice = "en_US/m-ailabs_low"

#Stop Changing
outputname = author+' - '+title

outputpath = author+"/"+title
outputname = title+" - "+author #no extension

#Makes the appropriate folder structure
cwd = os.getcwd()
os.mkdir(cwd+'/'+author)
os.mkdir(cwd+'/'+outputpath)

table = str.maketrans({
    "<": "&lt;",
    ">": "&gt;",
    "&": "&amp;",
    #"'": "&apos;",
    #'"': "&quot;",
})
def xmlesc(txt):
    return txt.translate(table)

#Begins the process
fin = open(inputfilename, "rt", encoding='utf-8')
fout = open(outputname+".txt", "wt", encoding='utf-8')

fout.write('<speak>')

for line in fin:
    rendered = ''

    if '\n' == line:
        continue
    else:
        #A pause after a sentence
        
        line = line.encode('utf-8', errors='ignore').decode('utf-8')
        linestrip = line.strip()
        rendered = '<p>'+xmlesc(linestrip)+'</p>'

        #rendered = rendered.encode('utf-8').decode('utf-8')
        fout.write(rendered)

fout.write('</speak>')
fin.close()
fout.close()

tts_command = 'mimic3 --voice '+mimicvoice+' --ssml --length-scale 1.3 --noise-scale 0.667 < "'+outputname+'.txt" > "temp-'+outputname+'.wav"'
print ('Using Mimic 3 to Convert to Audio (.wav): ' + tts_command)
subprocess.call(tts_command, shell=True)

#MP3 Output
#convert_command = 'ffmpeg -i "temp-'+outputname+'.wav" -metadata album="'+title+'" -metadata title="'+title+'" -metadata artist="'+author+'" -metadata album_artist="'+author+'" -acodec libmp3lame "'+outputname+'.mp3"'

#M4B Output
convert_command = 'ffmpeg -i "temp-'+outputname+'.wav" -metadata album="'+title+'" -metadata title="'+title+'" -metadata artist="'+author+'" -metadata album_artist="'+author+'" -acodec aac -ac 2 -b:a 64k -f mp4 "'+outputpath+'/'+outputname+'.m4b"'


print ('Converting filetype and tagging: ' + convert_command)
subprocess.call(convert_command, shell=True)

#-map_metadata 0:s:a:0

if os.path.exists('temp-'+outputname+'.wav'):
  os.remove('temp-'+outputname+'.wav')
  
if os.path.exists(outputname+'.txt'):
  os.remove(outputname+'.txt')
