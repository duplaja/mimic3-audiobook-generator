#!/usr/bin/python3
import subprocess
import os

#Enter / change below as needed
inputfilename = "to2c.txt"
outputname = "tale-of-two-cities" #no spaces, no extension
mimicvoice = "en_US/m-ailabs_low"

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

tts_command = 'mimic3 --voice '+mimicvoice+' --ssml --length-scale 1.3 --noise-scale 0.667 < '+outputname+'.txt > temp-'+outputname+'.wav'
print ('Using Mimic 3 to Convert to Audio (.wav): ' + tts_command)
subprocess.call(tts_command, shell=True)

convert_command = 'ffmpeg -i temp-'+outputname+'.wav -acodec libmp3lame '+outputname+'.mp3'
print ('Converting to mp3: ' + convert_command)
subprocess.call(convert_command, shell=True)

if os.path.exists('temp-'+outputname+'.wav'):
  os.remove('temp-'+outputname+'.wav')
  
if os.path.exists(outputname+'.txt'):
  os.remove(outputname+'.txt')
