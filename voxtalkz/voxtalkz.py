# __init__.py
#!/usr/bin/python3
# Text to speach online python library


from gtts import gTTS
import sys, os.path as path
import io
import time
from pydub import AudioSegment
import __builtin__
import datetime
import requests 
import json
import os
import base64

_File = 'null'

def print(args):
    with open(_File,'w') as file:
        file.write(args)
    return __builtin__.print(*args, **kwargs)

class voxTalkz():
    '''
    This function will turn a script written in this formant:

    ###Start###
    Laura:tramitized_woman
    Paul:italian_man


    Paul:Hello world
    *bang*
    Laura:Help world!
    
    ###End###

    into sound(i.e. people talking and sound effects) as an .mp3 file
    sound effects must be placed into the effects folder as .mp3, .wav, or .ogg files
    '''

    def __init__(self, file, name, debug=False, cloudKey=False, timeme=False):
        _File = file
        self.homedir = path.expanduser('~')
        self.name = name
        self.debug = debug
        self._File = _File
        self.filename = name+'.mp3'
        self.SoundFile = AudioSegment.empty()
        self.Pause = AudioSegment.empty()
        self.Actors_Effects = {}
        # List of people
        if not cloudKey:
            self.Actors = {"indian_man":"bn",
                        "american_woman":"en-us",
                        "scottish_woman":"ca",
                        "russian_woman":"sk",
                        "drawling_man":"cy",
                        "autistic_woman":"da",
                        "marika":"de",
                        "au_woman":"en-au",
                        "british_woman":"en-gb",
                        "indian_woman":"en-in",
                        "spanish_woman":"es-es",
                        #"spanishenglish_woman":"es-en",
                        #"indian_man":"et",
                        "french_woman":"fr",
                        "hindu_woman":"hi",
                        "alien_man":"is",
                        "italian_man":"it",
                        "scottish_woman":"ja",
                        "phone_woman":"kn",
                        "korean_man":"ko",
                        "dramatized_woman":"mr",
                        "dutch_woman":"nl",
                        "silly_man":"pl",
                        "robot_man":"sq",
                        "dramitized_girl":"sv",
                        "bored_teen":"te",
                        "happy_girl":"th",
                        "boss_lady":"tl",
                        "young_grandma":"vi",
                        "spoiled_girl":"zh-cn",
                        "american_woman":"en"}
        else:
            self.Actors = {
            "australian_woman":["en-AU-Wavenet-A","en-AU"],
            "australian_man":["en-AU-Wavenet-B","en-AU"],
            "personal_australian_woman":["en-AU-Wavenet-C","en-AU"],
            "personal_australian_man":["en-AU-Wavenet-D","en-AU"],

            "indian_woman":["en-IN-Wavenet-A","en-IN"],
            "indian_man":["en-IN-Wavenet-B","en-IN"],
            "personal_indian_woman":["en-IN-Wavenet-C","en-IN"],
            "personal_indian_man":["en-IN-Wavenet-D","en-IN"],

            "british_woman":["en-GB-Wavenet-A","en-GB"],
            "british_man":["en-GB-Wavenet-B","en-GB"],
            "personal_british_woman":["en-GB-Wavenet-C","en-GB"],
            "urgent_british_woman":["en-GB-Wavenet-F","en-GB"],
            "personal_british_man":["en-GB-Wavenet-D","en-GB"],

            "young_american_man":["en-US-Wavenet-A","en-US"],
            "middleage_american_man":["en-US-Wavenet-B","en-US"],
            "american_man":["en-US-Wavenet-B","en-US"],
            "middleage_american_woman":["en-US-Wavenet-C","en-US"],
            "american_woman":["en-US-Wavenet-C","en-US"],
            "middleage_personal_american_man":["en-US-Wavenet-D","en-US"],
            "middleage_personal_american_woman":["en-US-Wavenet-E","en-US"],
            "young_personal_american_woman":["en-US-Wavenet-F","en-US"],
            "distracted_middleage_american_woman":["en-US-Wavenet-G","en-US"],
            "young_american_woman":["en-US-Wavenet-H","en-US"],
            "young_personal_american_man":["en-US-Wavenet-I","en-US"],
            "cocky_american_man":["en-US-Wavenet-J","en-US"]
            }

    def ToSound(self):
        # parse the file
        parsed = self.Parse(self.file)
        # turn to sound
        if parsed:
            OutputSound = self.ListToSound(parsed)
            self.SoundFile += OutputSound
        else:
            print("Error: Could not parse!")
        # Save the file
        if OutputSound:
            self.save()
        else:
            print('Error: could not turn to sound!')

    def Parse(self,file,FILE=False):
        '''
        Fuction to parse a file into usable lists
        '''
        if not FILE:
            # Open our file
            if self.debug:
                    print('Parsing %s...'%file)
            try:
                File = open(file,'r')
                if self.debug:
                    print('done!\n')
            except Exception as e:
                print('No such file: %s'%file)
                if self.debug:
                    print(e)
                return False

            # Split it into a list, with each line being a seprate item
            List = File.readlines()
            # Close our file
            File.close()
        else:
            List = FILE
        # Split our list items into 1 or 2 item lists, using a collin
        pops = []
        for i in range(0,len(List)):
            # Don't parse if the list is blank!
            if List[i] == '\n':
                pops+=[i]
                continue
            if List[i][0] == '#':
                List[i] = '\n'
                continue
            List[i] = List[i].replace('\n','')
            # Check if it is a sound effect
            if '*' in List[i]:
                List[i]=['SOUND',(List[i].replace('*','')).replace('\n','')]
            elif ':' in List[i]:
                List[i] = (List[i].replace('\n','')).split(':')
            # If the user forgot, then add a collin
            else:
                print(f'Error on line {i}! \n {List[i]} \nNo collin or astrix. Assuming collin, Attempting to fix')
                assumedName = (List[i].replace('\n','')).split(' ')[0]
                List[i] = [assumedName, List[i].replace(assumedName, '')]

        while '\n' in List:
            List.remove('\n')
        # Return our list
        if self.debug:
            print('Parsed list is: \n %s \n'%List)
        return List

    def help(self):
        print("Usage: python3 -m voxtalkz [input file, output file] --flags\n\
            \n\
            Converts play-like script to a .mp3 file \n\
            Script file must be written in this manner: \n\
            \n\
            #The first time a unknown name is called, instead of making the person talk, the name will be assigned to a person. \n\
            Susan:american_woman\n\
            #Then the person will \"talk\"\n\
            Susan:Hello, world!\n\
            #Comments are allowed!\n\
            *soundeffect \n\
            \n\
            Effects can be applied by adding an @ symbal the the effect name, like so:\n\
            person1:hello, world!@VOLUME=8\nA second effect can be applied by using the pipe(\"|\") like so:\n\
            person1:Hello, World!@FADE|VOLUME=8\n\
            ")
        print('flags:\n\
                --debug        | the program tells you what it\'s doing\n\
                --help         | print this help message\n\
                --cloud=apiKey | use Google Cloud TextToSpeech API, must have API key after it\n\
                ')
        print("List of all effects:")
        list = ["@FADE | Fade to nothing",\
                "@FADE_IN | Fade in from silent",\
                "@OVERLAY | Overlays the sound onto what has already been recorded. Use @OVERLAY=VAR1 to START the overlay at the begining of where you assigned @VAR=1",\
                "@REPEAT= | Repeat audio segment however many times you specify. e.g. (american_woman:Hello, world!@REPEAT=10) would produce someone saying \"Hello, world!\" ten times",\
                "@VAR=    | Assign a number to a temporary table. Only used with @OVERLAY",\
                "@VOLUME= | Set volume change in decibels. A negitive number will reduce the volume",\
                "@PITCH=  | Set pitch change. e.g. \"american_woman:Hello, world!@PITCH=0.3\" would make the person sound like a little girl, while \"american_woman:Hello, world!@PITCH=-0.3\" would sound like an old woman"]
        for string in list:
            print("    "+string)
        print("\nList of all actors:")
        actors = {"indian_man | Clearly speaks":"bn",
                        "american_woman | Clearly speaks":"en-us",
                        "scottish_woman":"ca",
                        "russian_woman":"sk",
                        "drawling_man":"cy",
                        "danish_woman | Clearly speaks":"da",
                        "dutch_woman":"de",
                        "au_woman | Clearly speaks":"en-au",
                        "british_woman | Clearly speaks":"en-gb",
                        "indian_woman | Clearly speaks":"en-in",
                        "spanish_woman":"es-es",
                        #"spanishenglish_woman":"es-en",
                        #"indian_man":"et",
                        "french_woman":"fr",
                        "hindu_woman":"hi",
                        "alien_man":"is",
                        "italian_man":"it",
                        "scottish_woman":"ja",
                        "phone_woman":"kn",
                        "korean_man | Clearly speaks":"ko",
                        "dramatized_woman":"mr",
                        "dutch_woman":"nl",
                        "silly_man":"pl",
                        "robot_man":"sq",
                        "dramitized_girl":"sv",
                        "bored_teen":"te",
                        "happy_girl":"th",
                        "boss_lady":"tl",
                        "young_grandma":"vi",
                        "spoiled_girl":"zh-cn",
                        "american_woman":"en"}
        for string in actors:
            print("    "+string)
        print("\nSound effects must be in the .mp3 format and placed in /home/user/.voxtalk/soundEffects\n To use footsteps.mp3: put *footsteps in your script")

    def ListToSound(self, Lists):
        '''
        Turns text into speach or sound effects
        '''
        hold={}
        SoundFile=AudioSegment.empty()
        for List in Lists:
            effects = False
            audio_segment = False
            # Check to see if any filers should be applied
            if "@" in List[0]:
                effects=(List[0].split('@'))[1]
                List[0]=(List[0].split('@'))[0]
            if len(List)>1:
                if "@" in List[1]:
                    effects=(List[1].split('@'))[1]
                    List[1]=(List[1].split('@'))[0]
            # Check to see if it's a sound effect
            if List[0] == 'SOUND':
                if self.debug:
                    print('Makeing %s...'%List[1])
                while True:
                    try:
                        try:
                            audio_segment =  AudioSegment.from_mp3(self.homedir+'/.voxTalkz/soundEffects/'+List[1]+'.mp3')
                        except:
                            audio_segment =  AudioSegment.from_wav(self.homedir+'/.voxTalkz/soundEffects/'+List[1]+'.wav')
                        except:
                            audio_segment =  AudioSegment.from_ogg(self.homedir+'/.voxTalkz/soundEffects/'+List[1]+'.ogg')
                        if self.debug:
                            print("Done!\n")
                        break
                    except:
                        contd = input('\n !!! Could not open %s'%(self.homedir+'/.voxTalkz/soundEffects/'+List[1]+'.mp3 (or .wav, or ogg) !!! Type continue to skip the sound effect, retry to retry after you\'ve fixed the problem, or exit to quit.'))
                        if contd == 'continue':
                            break
                        elif contd == 'retry':
                            pass
                        elif contd == 'exit':
                            return False
                        else:
                            print(f'{contd} is not an applicable answer. Trying again.')
                            pass
                # Open sound to a variable

            elif List[0] in self.Actors:
                if self.debug:
                    print('Making %s say \'%s\'... '%(List[0],List[1]))

                # If us
                if not self.cloudKey:
                    utterance = gTTS(text=List[1], lang=self.Actors[List[0]], slow=False, lang_check=False)
                    if self.debug:
                        print('Done!\n')
                    # Create an empty file-like object
                    File = io.BytesIO()
                    # Write what the person 'said' to the object
                    if self.debug:
                        print("Recording what %s said..."%(List[0]))
                    while True:
                        try:
                            utterance.write_to_fp(File)
                            break
                        except Exception as E:
                            wait = input('Somthing seems to be wrong with the internet (or the file). Please type \'save\' to save file, \'help\' to display what went wrong, or \'continue\' if the internet connection is restored. Anything else will exit.')
                            if wait == "continue":
                                pass
                            elif wait == "save":
                                self.SoundFile = SoundFile
                                self.save()
                            elif wait == "pass":
                                break
                            elif wait == "help":
                                print(E)
                            else:
                                return False
                else:
                    try:
                        url = "https://texttospeech.googleapis.com/v1beta1/text:synthesize"

                        text = List[1]

                        data = {
                                "input": {"text": text},
                                "voice": {"name":  self.Actors[List[0]][0], "languageCode": self.Actors[List[0]][1]},
                                "audioConfig": {"audioEncoding": "MP3"}
                              };

                        headers = {"content-type": "application/json", "X-Goog-Api-Key": self.cloudKey }

                        r = requests.post(url=url, json=data, headers=headers)

                        content = json.loads(r.content)
                        audioIO = content['audioContent']
                        audioDecoded = base64.b64decode(audioIO)
                        File = io.BytesIO()
                        with open(File,'wb') as file:
                            file.write(audioDecoded)

                    # I think this makes the file readable? Not sure
                    File.seek(0)
                    audio_segment = AudioSegment.from_mp3(File)
                if self.debug:
                    print('Done!\n')

                try:
                    if effects:
                        effects = self.Actors_Effects[List[0]] + "|" + effects
                    else:
                        effects = self.Actors_Effects[List[0]]
                except:
                    pass
                #self.SoundFile += self.Pause.read()
                #File.close()

            else:
                try:
                    List[0] = List[0].strip()
                    List[1] = List[1].strip()

                    if effects:
                        self.Actors_Effects.__setitem__(List[0],effects)
                        effects = False
                    self.Actors.__setitem__(List[0], self.Actors[List[1]])
                    if self.debug:
                        print('%s is now a %s\n'%(List[0],List[1]))
                except:
                    print("%s is NOT a type of person! Using american_woman..."%List[1])
                    self.Actors.__setitem__(List[0], self.Actors['american_woman'])

            # Apply effects
            if effects != False:
                if "|" in effects:
                    effects=effects.split('|')
                else:
                    effects = [effects]

                for effect in effects:
                    if "=" not in effect:
                        effect += "=False"
                    parsed = effect.split('=')
                    if self.debug:
                        print(parsed)

                    if parsed[0] == "VOLUME":
                        if self.debug:
                            print("Volume is %s"%parsed[1])
                        audio_segment = audio_segment + parsed[1]
 
                    elif parsed[0] == "PITCH":
                        if self.debug:
                            pass
                        octaves = float(parsed[1])
                        new_sample_rate = int(audio_segment.frame_rate * (2.0 ** octaves))
                        audio_segment = audio_segment._spawn(audio_segment.raw_data, overrides={'frame_rate': new_sample_rate})

                    elif parsed[0] == "OVERLAY":
                        if self.debug:
                            pass
                        if "VAR" in parsed[1]:
                            try:
                                SoundFile = SoundFile.overlay(audio_segment, position=hold[parsed[1]])
                            except:
                                if self.debug:
                                    print("Key error: %s not in VAR list"%parsed[1])
                        else:
                            print(len(SoundFile),len(audio_segment))
                            SoundFile = SoundFile.overlay(audio_segment, position=(len(SoundFile)-len(audio_segment)))
                        audio_segment = False

                    elif parsed[0] == "VAR":
                        hold.__setitem__("VAR"+str(parsed[1]), len(SoundFile))

                    elif parsed[0] == "TRIM":
                        pass

                    elif parsed[0] == "REPEAT":
                        if not parsed[1]:
                            parsed[1] = 2
                        audio_segment *= int(parsed[1])

                    elif parsed[0] == "FADE":
                        audio_segment = audio_segment.fade_out(len(audio_segment))

                    elif parsed[0] == "FADE_IN":
                        audio_segment = audio_segment.fade_in(len(audio_segment))
            # Finaly, add audio segment to the sound-file
            if audio_segment != False:
                SoundFile += audio_segment
        return SoundFile


    def save(self):
        '''
        function to save compiled file
        '''
        if self.debug:
            print('Saving the file as %s...'%(self.filename))
        self.SoundFile.export(self.filename, format='mp3')
        if self.debug:
            print('Done!\n')

def say(script, filename, debug=False):
    voxTalkz(script, filename, debug).ToSound()


if __name__ == "__main__":
    args = sys.argv
    debug = False
    cloudKey = False
    if ("--debug") in args:
        args.remove("--debug")
        debug = True

    if ("--help" or "-h") in args:
        voxTalkz('', '').help()

    if ("--cloud") in args:
        try:
            cloudKey = args[args.index('--cloud')+1]
            del args[args.index('--cloud')+1]
            args.remove("--cloud")
        except:
            print('Usage: --cloud [text-to-speach API key]')
            args.remove("--cloud")

    elif len(args) != 3:
        print("Expecting two arguments! Usage: voxtalkz [input file, output file] ")

    else:
        print(args)
        script = args[1]
        print(f"Using {script} as input file")
        try:
            open(script).close()
        except:
            print(f'No such file: {script}')
            script = False
        if script:
            filename = args[2]
            print(f"Outputting to {filename}")
            voxTalkz(script, filename, debug, cloudKey=cloudKey).ToSound()

