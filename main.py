from tkinter import Tk, HORIZONTAL, Label, Button, END, PhotoImage, Listbox, LEFT, StringVar, ACTIVE
import pygame
import os
import threading
import time
from mutagen.mp3 import MP3
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from tkinter import ttk
from PIL import Image, ImageTk


class Player:
    def __init__(self, master):
        self.master = master
        pygame.init()
        pygame.mixer.init()

        self.threads = []

        # Button symbols/variables
        PLAY = "►"
        PAUSE = "||"
        RWD = "◀◀"
        FWD = "▶▶"
        STOP = "■"
        UNPAUSE = "||"
        mute = "🔇"
        unmute = u"\U0001F50A"
        vol_mute = 0.0
        vol_unmute = 1

        # Playlist
        self.play_list = Listbox(master, font="Sansarif 12 bold", bd=2, fg='white',
                                 bg="#384c6b", width=39, height=21, selectbackground="#768499")
        self.play_list.place(x=605, y=100)

        # Photo
        files = 'music1.jpg'
        self.img1 = Image.open(files)
        self.img1 = self.img1.resize((600, 470), Image.Resampling.LANCZOS)
        self.img = ImageTk.PhotoImage(self.img1)
        self.lab = Label(master, border=0, bg='#27364d')
        self.lab.grid(row=0, column=0)
        self.lab["compound"] = LEFT
        self.lab["image"] = self.img

        # Song Title
        self.var = StringVar()
        self.var.set("What's Playing?")
        self.song_title = Label(master, font="Helvetica 12 bold", bg="#27364d",
                                fg="white", width=90, textvariable=self.var)
        self.song_title.place(x=0, y=0)

        # Add Music

        def append_listbox():
            global song_list
            try:
                directory = askdirectory()
                os.chdir(directory)
                song_list = os.listdir()
                song_list.reverse()
                for item in song_list:  # Returns list of songs
                    pos = 0
                    self.play_list.insert(pos, item)
                    pos += 1

                global size
                index = 0
                size = len(song_list)
                self.play_list.selection_set(index)
                self.play_list.see(index)
                self.play_list.activate(index)
                self.play_list.selection_anchor(index)

            except:
                showerror("File selected error", "Please choose a file correctly")
                # Runs the append_listbox function on separate thread

        def add_songs_playlist():
            mythreads = threading.Thread(target=append_listbox)
            self.threads.append(mythreads)
            mythreads.start()

        # Music Duration

        def get_time():
            current_time = pygame.mixer.music.get_pos() / 1000
            formated_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
            next_one = self.play_list.curselection()
            song = self.play_list.get(next_one)
            song_timer = MP3(song)
            song_length = int(song_timer.info.length)
            format_for_length = time.strftime("%H:%M:%S", time.gmtime(song_length))
            self.label_time.config(text=f"{format_for_length} / {formated_time}")
            self.progress["maximum"] = song_length
            self.progress["value"] = int(current_time)
            master.after(100, get_time)

        # Iterates through all the songs in the playlist

        def Play_music():
            try:
                track = self.play_list.get(ACTIVE)
                pygame.mixer.music.load(track)
                self.var.set(track)
                pygame.mixer.music.play()
                get_time()


            except:
                showerror("No Music", "Please load the music you want to play")


        # Pause and Unpause

        def pause_unpause():
            if self.button_pause['text'] == PAUSE:
                pygame.mixer.music.pause()
                self.button_pause['text'] = UNPAUSE

            elif self.button_pause['text'] == UNPAUSE:
                pygame.mixer.music.unpause()
                self.button_pause['text'] = PAUSE

        # Play the music on a different thread from the gui

        def play_thread():
            mythreads = threading.Thread(target=Play_music)
            self.threads.append(mythreads)
            mythreads.start()

        master.bind("<space>", lambda x: play_thread())

        # Stop Song

        def stop():
            pygame.mixer.music.stop()

        # Volume bar

        def volume(x):
            pygame.mixer.music.set_volume(self.volume_slider.get())

        # Mute and unmute the song while the song plays

        def muted():
            if self.button_mute['text'] == unmute:
                pygame.mixer.music.set_volume(vol_mute)
                self.volume_slider.set(vol_mute)
                self.button_mute['fg'] = "red"
                self.button_mute['text'] = mute
            elif self.button_mute['text'] == mute:
                pygame.mixer.music.set_volume(vol_unmute)
                self.volume_slider.set(vol_unmute)
                self.button_mute['fg'] = "white"
                self.button_mute['text'] = unmute

        # Next song

        def nextSong():
            try:
                next_one = self.play_list.curselection()
                next_one = next_one[0] + 1
                song = self.play_list.get(next_one)
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                self.play_list.select_clear(0, END)
                self.play_list.activate(next_one)
                self.play_list.selection_set(next_one, last=None)
                self.var.set(song)
                get_time()
                self.play_list.see(next_one)
            except:
                showerror("No Next Song", "Please press the previous button")

        def next():
            mythreads = threading.Thread(target=nextSong)
            self.threads.append(mythreads)
            mythreads.start()

        # Previous song

        def prevSong():
            try:
                next_one = self.play_list.curselection()
                next_one = next_one[0] - 1
                song = self.play_list.get(next_one)
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                self.play_list.select_clear(0, END)
                self.play_list.activate(next_one)
                self.play_list.selection_set(next_one, last=None)
                self.var.set(song)
                get_time()
                self.play_list.see(next_one)
            except:
                showerror("No previous Song", "Please press the Next button")

        def prev():
            mythreads = threading.Thread(target=prevSong)
            self.threads.append(mythreads)
            mythreads.start()

        self.master.bind('<Left>', lambda x: prev())
        self.master.bind('<Right>', lambda x: next())

        # Music playlist and playback buttons
        self.separator = ttk.Separator(self.lab, orient='horizontal')
        self.separator.place(relx=0, rely=0.87, relwidth=0.996, relheight=1)
        self.button_play = Button(master, text=PLAY, width=5, bd=5, bg="#27364d",
                                  fg="#27364d", font="Helvetica, 15", command=play_thread)
        self.button_play.place(x=150, y=415)
        self.button_stop = Button(master, text=STOP, width=5, bd=5,
                                  font="Helvetica, 15", bg="#27364d", fg="#27364d", command=stop)
        self.button_stop.place(x=225, y=415)
        self.button_prev = Button(master, text=FWD, width=5, bd=5,
                                  font="Helvetica, 15", bg="#27364d", fg="#27364d", command=next)
        self.button_prev.place(x=310, y=415)

        self.button_next = Button(master, text=RWD, width=5, bd=5, bg="#27364d",
                                  fg="#27364d", font="Helvetica, 15", command=prev)
        self.button_next.place(x=10, y=415)
        self.button_pause = Button(master, text=PAUSE, width=4, bd=5,
                                   font="Helvetica, 15", bg="#27364d", fg="#27364d", command=pause_unpause)
        self.button_pause.place(x=85, y=415)

        self.button_mute = Button(master, text=unmute, width=2, bd=5,
                                  font="Helvetica, 15", bg="#27364d", fg="#27364d", command=muted)
        self.button_mute.place(x=390, y=415)

        self.label_playlist = Label(master, text=u"My Music Playlist ♫ ", bg='#768499',
                                    width=31, font="Helvetica, 15")
        self.label_playlist.place(x=625, y=21)

        self.button_load_music = Button(master, text="♫ Click Here To Load Music ♫", width=20,
                                        bd=3, font="Helvetica, 10", fg="#768499", command=add_songs_playlist)
        self.button_load_music.place(x=700, y=60)

        self.style = ttk.Style()

        self.style.configure("myStyle.Horizontal.TScale", background="#27364d")

        self.volume_slider = ttk.Scale(self.lab, from_=0, to=1, orient=HORIZONTAL,
                                       value=1, length=120, command=volume, style="myStyle.Horizontal.TScale")
        self.volume_slider.place(x=465, y=424)

        self.progress = ttk.Progressbar(self.lab, orient=HORIZONTAL, value=0, length=410, mode='determinate')
        self.progress.place(x=28, y=387)

        self.label_time = Label(master, text="00:00:00 / 00:00:00",
                                width=17, font="Helvetica, 10", bg="#768499", fg="white")
        self.label_time.place(x=460, y=387)


# Tk window function

def main():
    root = Tk()
    playerapp = Player(root)
    root.geometry("963x470+200+100")
    root.title("Mp3 Music Player")
    root.configure(bg="#27364d")
    root.resizable(width=0, height=0)
    root.mainloop()


if __name__ == "__main__":
    main()