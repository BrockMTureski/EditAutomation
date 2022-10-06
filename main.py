import modules


outPath=modules.mp4ToWav("test.mp4","testOut")
clip_segments=modules.analyzeWavFile(outPath)
modules.delFile(outPath)
modules.subclip("test.mp4",clip_segments)








