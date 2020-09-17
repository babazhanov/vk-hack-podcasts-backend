import sox
# create transformer
tfm = sox.Transformer()
# trim the audio between 5 and 10.5 seconds.
tfm.trim(5, 10.5)
# apply compression
tfm.compand()
# apply a fade in and fade out
tfm.fade(fade_in_len=1.0, fade_out_len=0.5)
# create an output file.
tfm.build_file('metallic-drums.wav', 'metallic-drums.aiff')