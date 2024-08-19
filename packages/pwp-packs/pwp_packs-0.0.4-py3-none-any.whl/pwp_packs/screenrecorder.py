import imageio_ffmpeg
import subprocess as sp
import tkinter as tk
from datetime import datetime
from time import sleep
import threading
import pyautogui

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()



def help():
    cmd = [
        FFMPEG,
        '-h'
    ]
    # help = sp.run(cmd,stdout=sp.PIPE,stderr=sp.PIPE,text=True)
    # return help.stderr
    sp.run(cmd)

def get_audio_devices(text = False):
    """
    Returns the List of audio devices available in your device.
    Args:
        text (bool, optional): if True then return the list in text format else print the list of audio devices. Defaults to False.

    Returns:
        str : Returns str if text argument True else print
    """
    cmd = [
        FFMPEG,
        '-list_devices','true','-f','dshow','-i','audio','dummy'
    ]
    if text:
        devices = sp.run(cmd,stdout=sp.PIPE,stderr=sp.PIPE,text=text)
        return devices.stderr
    else:
        sp.run(cmd)

class ScreenRecorderErrors(Exception):
    def __init__(self,message="error"):
        super().__init__(message)
        self.message = message
    
class ScreenRecorder():
    """
        ScreenRecorder class for recording the screen with optional audio input.

        Attributes:
        -----------
        filename : str
            The name of the output file.
        overwrite : bool, optional
            Whether to overwrite the file if it already exists (default is False).
        draw_mouse : bool, optional
            Whether to capture the mouse cursor in the recording (default is True).
        video_encoding : str, optional
            The video codec to use (default is "libx264").
        video_size : str, optional
            The resolution of the video (default is "1920x1080").
        constant_frame_rate : int, optional
            The constant frame rate for the video (default is 24).
        fps : int, optional
            Frames per second for the video (default is None, which set to system performance).
        preset : str, optional
            The encoding speed preset (default is 'ultrafast').
        pix_fmt : str, optional
            Pixel format of the video (default is 'yuv420p').
        movflags : str, optional
            Flags to optimize the MP4 file (default is 'faststart').
        audio_devices : list, optional
            List of audio input devices to capture (default is an empty list).
        audio_codec : str, optional
            Audio codec to use (default is aac).
        thread_queue_size : int, optional
            Size of the thread queue (default is 4096).
        rtbufsize : str, optional
            Size of the buffer for real-time input (default is "50M").
        audio_delays : list, optional
            List of audio delay values in milli-seconds for synchronization (default is 0 milli-seconds delay).
        duration : int, optional
            Duration of the recording in seconds (default is None, which records until stop function call).

    """
    def __init__(self,filename:str,overwrite:bool = False,draw_mouse:bool=True,video_encoding:str="libx264",video_size:str="1920x1080",
                constant_frame_rate:int=24,fps:int=None,preset:str='ultrafast',pix_fmt:str = 'yuv420p',movflags:str='faststart',audio_devices:list = [],
                audio_codec:str = "aac",thread_queue_size:int = 4096,rtbufsize:str = "50M",audio_delays:list=[],duration=None)->object:
        
        self.filename = filename
        self.hide_output = False
        self.recording_started = False
        self.cmd = [
            FFMPEG
        ]
        
        if overwrite:
            self.cmd.extend(['-y'])
     
        self.cmd.extend([
            '-draw_mouse','1' if draw_mouse else '0'
        ])
        
        
        self.cmd.extend(
            ['-probesize','100M',
             '-fflags', '+genpts',
            '-f','gdigrab',
            '-thread_queue_size',str(thread_queue_size),
            '-i','desktop',
            '-video_size',video_size
            ]
        )
        for audio_device in audio_devices:
            self.cmd.extend(
                [
                    '-f','dshow',
                    '-thread_queue_size',str(thread_queue_size),
                    '-rtbufsize',rtbufsize,
                    '-i',f'audio={audio_device}',
                ]
            )
        self.cmd.extend(['-flush_packets','1'])
        filter_complex_string = ""
        i = 1
        if audio_delays!=[]:
            if len(audio_delays)==len(audio_devices):
                for audio_delay in audio_delays:
                        filter_complex_string=filter_complex_string+f'[{i}:a]adelay={audio_delay}|{audio_delay}[audioinput{i}];'
                        filter_complex_string = filter_complex_string+f'[audioinput{i}]aformat=channel_layouts=stereo[audioinput{i}];'
                        i+=1
            else:
                raise Exception("audio_delays list must match with audio_devices list, if you don't want a delay on any specific input then write 0 at that index")
        if len(audio_devices)>=1:
            if audio_delays!=[]:
                # self.cmd.extend([
                # '-filter_complex',filter_complex_string+f'{"".join(f"[audioinput{audio}]" for audio in range(1,len(audio_devices)+1))}amerge=inputs={len(audio_devices)}[a]',
                # '-map','0:v','-map','[a]'
                # ])
                merge_string = ""
                for i in range(1,len(audio_devices)+1):
                    merge_string = merge_string+f'[audioinput{i}]'
                
                # filter_complex_string = filter_complex_string+f'{"".join(f"[audioinput{audio}]" for audio in range(1,len(audio_devices)+1))}amerge=inputs={len(audio_devices)}[a]'
                filter_complex_string = filter_complex_string + f'{merge_string}amerge=inputs={len(audio_devices)}[a];'
                filter_complex_string = filter_complex_string + f'[a]aformat=channel_layouts=stereo[a]'
                
            elif len(audio_devices)>1:
                # self.cmd.extend([
                #     '-filter_complex',f'{filter_complex_string.join(f"[{audio}:a]" for audio in range(1,len(audio_devices)+1))}amerge=inputs={len(audio_devices)}[a]',
                #     '-map','0:v','-map','[a]'
                # ])
                merge_string = ""
                for i in range(1,len(audio_devices)+1):
                    filter_complex_string = filter_complex_string+f'[{i}:a]aformat=channel_layouts=stereo[audioinput{i}];'
                    merge_string = merge_string+f'[audioinput{i}]'
                    
                filter_complex_string = filter_complex_string + f'{merge_string}amerge=inputs={len(audio_devices)}[a];'
                filter_complex_string = filter_complex_string + f'[a]aformat=channel_layouts=stereo[a]'
                # filter_complex_string = filter_complex_string+f'{"".join(f"[{audio}:a]" for audio in range(1,len(audio_devices)+1))}amerge=inputs={len(audio_devices)}[a]'
        
        if audio_devices!=[]:
            if len(audio_devices)>1 or len(audio_delays)>=1:
                self.cmd.extend([
                    '-filter_complex',filter_complex_string,
                    '-map','0:v','-map','[a]'
                ])
                # self.cmd.extend([
                #     '-map','0:v','-map','[a]'
                # ])
        
        self.cmd.extend([
            '-c:v',video_encoding,
            '-crf',str(constant_frame_rate)
        ])
        if fps is not None:
            self.cmd.extend([
                '-r',str(fps)
            ])
        if audio_devices!=[]:
            self.cmd.extend([
                '-c:a',audio_codec if audio_codec is not None else "aac",
                '-async','1',
            ])
        
        self.cmd.extend([
            '-preset',preset,
            '-pix_fmt', pix_fmt,
            '-movflags', movflags
        ])
        if duration is not None:
            self.cmd.extend([
                '-t',str(duration)
            ])
        self.cmd.extend([
            filename
        ])
        
    
    def get_config(self)->list:
        return self.cmd
    
    def start(self,hide_output = False):
        if not self.recording_started:
            self.recording_started = True
            if hide_output:
                self.hide_output = True
                f = open("file.txt",'w')
                self.recorder = sp.Popen(self.cmd,stdin = sp.PIPE,stdout=f,stderr=f)
            
            else:
                self.recorder = sp.Popen(self.cmd,stdin=sp.PIPE)
        
        else:
            return("Recording already started")
        
    
    def stop(self):
        if self.recording_started:
            if self.hide_output:
                self.recorder.stdin.write(b'q')
            else:
                self.recorder.stdin.write(b'q')
                self.recorder.stdin.flush()
                self.recorder.wait()
            
            self.recording_started = False
        else:
            return("Recording isn't started yet")
        


class ScreenRecorderGUI(ScreenRecorder):
    """
        ScreenRecorderGUI class for a graphical user interface to control screen recording.

        Attributes:
        -----------
        filename_prefix : str, optional
            Prefix for the output file names (default is "PWP.mp4").
        x : int, optional
            X-coordinate of the GUI window (default gui position set to top center).
        y : int, optional
            Y-coordinate of the GUI window (default gui position set to top center).
        width : int, optional
            Width of the GUI window (default is 500).
        height : int, optional
            Height of the GUI window (default is 35).
        background_color : str, optional
            Background Color of GUI window (default is black).
        overwrite : bool, optional
            Whether to overwrite the file if it already exists (default is False).
        draw_mouse : bool, optional
            Whether to capture the mouse cursor in the recording (default is True).
        video_encoding : str, optional
            The video codec to use (default is "libx264").
        video_size : str, optional
            The resolution of the video (default is "1920x1080").
        constant_frame_rate : int, optional
            The constant frame rate for the video (default is 24).
        fps : int, optional
            Frames per second for the video (default is None, which set to system performance).
        preset : str, optional
            The encoding speed preset (default is 'ultrafast').
        pix_fmt : str, optional
            Pixel format of the video (default is 'yuv420p').
        movflags : str, optional
            Flags to optimize the MP4 file (default is 'faststart').
        audio_devices : list, optional
            List of audio input devices to capture (default is an empty list).
        audio_codec : str, optional
            Audio codec to use (default is aac).
        thread_queue_size : int, optional
            Size of the thread queue (default is 4096).
        rtbufsize : str, optional
            Size of the buffer for real-time input (default is "50M").
        audio_delays : list, optional
            List of audio delay values in milli-seconds for synchronization (default is 0 milli-seconds delay).
        duration : int, optional
            Duration of the recording in seconds (default is None, which records until stop button click).
    """
    
    def __init__(self,filename_prefix:str="PWP.mp4",x:int=None,y:int=None,width:int = 500,height:int = 35,background_color:str="black",overwrite:bool = False,draw_mouse:bool=True,video_encoding:str="libx264",video_size:str="1920x1080",
                constant_frame_rate:int=24,fps:int=None,preset:str='ultrafast',pix_fmt:str = 'yuv420p',movflags:str='faststart',audio_devices:list = [],
                audio_codec:str = None,thread_queue_size:int = 4096,rtbufsize:str = "50M",audio_delays:list=[],duration=None)->object:
        
        super().__init__(filename_prefix,overwrite,draw_mouse,video_encoding,video_size,constant_frame_rate,fps,preset,pix_fmt,movflags,
                        audio_devices,audio_codec,thread_queue_size,rtbufsize,audio_delays,duration)
        
        self.root = tk.Tk()
        self.root.withdraw()
        self.is_guiopen = True
        self.width = width
        self.height = height
        self.screen_width = x if x else self.root.winfo_screenwidth()
        self.screen_height = y if y else self.root.winfo_screenheight()
        self.x =(self.screen_width//2) - (self.width // 2)
        self.y = 0
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost',True)
        self.root.configure(background=background_color)
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Close", command=self.close_gui)

        # Bind the right-click event to show the context menu
        self.root.bind("<Button-3>", self.show_context_menu)
        
        self.label = tk.Label(self.root, text="Start...", font=("Arial", 12), fg="white", bg=background_color)
        self.label.pack(side='left',padx=150)
        self.canvas_width = 30
        self.canvas_height = self.canvas_width
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg=background_color, highlightthickness=0)
        self.canvas.pack()
        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2
        self.radius = self.canvas_width // 2 - 2
        self.oval_id = self.canvas.create_oval(self.center_x - self.radius, self.center_y - self.radius,
                                    self.center_x + self.radius, self.center_y + self.radius,fill="green") 
        
        self.button_frame = tk.Frame(self.root,bg=background_color)
        self.square_width = 30
        self.square_canvas = tk.Canvas(self.button_frame,width=self.square_width,height=self.square_width,
                                       bg="black",highlightthickness=0)
        self.square_id = self.square_canvas.create_rectangle(0,0,self.square_width,self.square_width,fill="red")
        
        self.canvas.tag_bind(self.oval_id,"<Button-1>",self.start_rec_click)
        self.canvas.tag_bind(self.oval_id,"<Enter>",self.on_mouse_hover)
        self.canvas.tag_bind(self.oval_id,"<Leave>",self.on_mouse_leave)
        
        self.square_canvas.tag_bind(self.square_id,"<Button-1>",self.stop_rec_click)
        self.square_canvas.tag_bind(self.square_id, "<Enter>", self.on_mouse_hover)
        self.square_canvas.tag_bind(self.square_id, "<Leave>", self.on_mouse_leave)
         
    
    def show_context_menu(self, event):
        self.show_window()
        self.context_menu.post(event.x_root, event.y_root)
        
    def close_gui(self):
        self.hide_window()
        self.is_guiopen = False
        self.root.quit()
        
    def on_mouse_hover(self, event):
        event.widget.config(cursor = "hand2")

    def on_mouse_leave(self, event):
        event.widget.config(cursor="")

    def update_timer(self):
        while self.recording_started:
            diff = str(datetime.now()-self.st)
            diff = diff.split(":")
            self.label.config(text=f"REC...{diff[0]}:{diff[1]}:{int(diff[2].split('.')[0])}")
        self.label.config(text="Start")
    
    def hide_window(self):
        if self.is_guiopen:
            self.root.withdraw()
        
    def show_window(self):
        if self.is_guiopen:
            self.root.deiconify()
    
    def start_rec_click(self,event):
        self.cmd.pop()
        filename = self.filename.split('.')
        self.cmd.extend([
            f'{filename[0]}_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.{filename[1]}'
        ])
        self.start()
        sleep(0.5)
        self.st = datetime.now()
        self.canvas.pack_forget()
        self.button_frame.pack()
        self.square_canvas.pack()
        self.timerthread = threading.Thread(target=self.update_timer)
        self.timerthread.daemon = True
        self.timerthread.start()
        
    
    def stop_rec_click(self,event):
        self.stop()
        self.button_frame.pack_forget()
        self.square_canvas.pack_forget()
        self.canvas.pack()
    
    def on_mouse_motion(self):
        self.show_window()
        sleep(2)
        while self.is_guiopen:
            event = pyautogui.position()
            x, y = event.x, event.y
            
            if self.screen_width//2 - self.width//2 <=x <= self.screen_width//2 + self.width//2 and y == 0:
                self.show_window()
                while True:
                    event = pyautogui.position()
                    x, y = event.x,event.y
                    if self.screen_width//2 - self.width//2 <= x <= self.screen_width//2 + self.width//2 and y <=35:
                        pass
                    else:
                        break
                    
            else:
                self.hide_window()
                
        
    def show(self,text_notif:bool = True):
        self.is_guiopen = True
        self.mousethread = threading.Thread(target=self.on_mouse_motion)
        self.mousethread.daemon = True
        self.mousethread.start()
        if text_notif:
            print("Gui Started, hover mouse on the top center positon to see GUI")
        self.root.mainloop()
        

class AudioRecorder():
    
    def __init__(self,filename:str,audio_devices:list, overwrite = False, audio_codec:str = "pcm_s16le", bitrate:str = "192k", thread_queue_size:int = 4096 , real_time_buffer:str = "50M", audio_delays:list = [], duration:int = None):
        self.filenamee = filename
        self.cmd = [FFMPEG]
        if overwrite:
            self.cmd.extend(['-y'])
        self.recording_started = False
        if audio_delays == []:
            audio_delays = [0] * len(audio_devices)
        
        if len(audio_devices) != len(audio_delays):
            raise "Audio devices list is not matching with Audio delays, if you don't want to add delay in a specific input then write 0 in their respective index in audio delays list"
        audio_devices_input_list = []
        filter_complex_string = ""
        merge_string = ""
        i = 0
        for audio_device in audio_devices:
            audio_devices_input_list.extend([
                '-f','dshow',
                '-thread_queue_size',str(thread_queue_size),
                '-rtbufsize',real_time_buffer,
                '-i',f'audio={audio_device}'
            ])

            filter_complex_string += f"[{i}:a]adelay={audio_delays[i]}|{audio_delays[i]}[audioinput{i}];[audioinput{i}]aformat=channel_layouts=stereo[audioinput{i}];"
            merge_string += f"[audioinput{i}]"
            i += 1
        
        if len(audio_devices)>1:
            merge_string += "amerge=inputs=2[a];[a]aformat=channel_layouts=stereo[a]"
            filter_complex_string += merge_string
        else:
            # filter_complex_string = filter_complex_string[:len(filter_complex_string)-1]
            filter_complex_string += "[audioinput0]aformat=channel_layouts=stereo[a]"
            
        self.cmd.extend(audio_devices_input_list)
        self.cmd.extend(['-flush_packets','1'])
        self.cmd.extend(['-filter_complex',filter_complex_string])
        self.cmd.extend(['-map','[a]'])
        self.cmd.extend([
            '-b:a',bitrate,
            '-c:a',audio_codec
        ])
        
        if duration:
            self.cmd([
                '-t',str(duration)
            ])
        
        self.cmd.extend([
            filename
        ])
    
    def start(self):
        if not self.recording_started:
            self.recorder = sp.Popen(self.cmd, stdin= sp.PIPE)
            self.recording_started  = True
        else:
            print("Recording already started, please stop before start new recording")
        
    def stop(self):
        if self.recording_started:
            self.recorder.stdin.write(b'q')
            self.recorder.stdin.flush()
            self.recorder.wait()
            self.recording_started = False
        else:
            print("recording isn't started yet")
            


class AudioRecorderGUI(AudioRecorder):
    
    def __init__(self,audio_devices:list, filename_prefix:str="PWP.wav", x:int=None, y:int=None, width:int = 500, height:int = 35, background_color:str="black", overwrite = False, audio_codec:str = "pcm_s16le", bitrate:str = "192k", thread_queue_size:int = 4096 , real_time_buffer:str = "50M", audio_delays:list = [], duration:int = None):
        super().__init__(filename_prefix,audio_devices,overwrite,audio_codec,bitrate,thread_queue_size,real_time_buffer,audio_delays,duration)
        self.obj = ScreenRecorderGUI(filename_prefix,x,y,width,height,background_color)
        self.obj.cmd = self.cmd
        self.obj.filename = self.filenamee
    
    
    def show(self):
        self.obj.show()
    
    