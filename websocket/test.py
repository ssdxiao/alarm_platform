from moviepy.editor import AudioFileClip, concatenate_audioclips
clip1 = AudioFileClip("abc1.wav")
clip2 = AudioFileClip("abc2.wav")
clip3 = AudioFileClip("abc3.wav")
final_clip = concatenate_audioclips([clip1,clip2,clip3])
final_clip.write_audiofile("test.wav")

