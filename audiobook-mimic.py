#!/usr/bin/python3
import subprocess
import os

#Enter / change below as needed
inputfilename = "to2c.txt"
author = "Charles Dickens"
title = "Tale of Two Cities"

mimicvoice = "en_US/m-ailabs_low"

#Stop Changing
outputname = author+' - '+title

outputpath = author+"/"+title
outputname = title+" - "+author #no extension

#Makes the appropriate folder structure
cwd = os.getcwd()
os.mkdir(cwd+'/'+author)
os.mkdir(cwd+'/'+outputpath)

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
        linestrip = line.strip()
        rendered = '<p>'+linestrip+'</p>'

        rendered = rendered.encode('utf-8').decode('utf-8')
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
