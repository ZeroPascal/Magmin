
import json
import os
from pathlib import Path
import platform
from definitions import ROOT_DIR, THUMBNAIL_DIR

from .cli import cmdInterface, prepPaths

def ffmpegScan(filePath:str, st_ino, makeThubnail=True):
    root,file = prepPaths(filePath)
    info ={}
    info.update(scanAudio(root,file))
    info.update(scanVideo(root,file))
    try:
        if(makeThubnail and info['VFormat']):
            ffmpegRoot, file = prepPaths(filePath,exe='ffmpeg')
         
            generateThumbnail(ffmpegRoot,file,st_ino, THUMBNAIL_DIR)
    except Exception as e:
        pass
    return info


def generateThumbnail(root:str, filePath:str, st_ino:str, thubnailDirectory:str):
    thumbNail =os.path.join(thubnailDirectory,str(st_ino)+'_thumb.png')
    file_ext = os.path.splitext(filePath)[1].lower()
   # print('Thumbnail', thumbNail,filePath, file_ext)
    if(file_ext in {'.jpg', '.jpeg', '.png'}):
        cmd = 'cp '+filePath+' '+thumbNail
    else:
        cmd=root+' -ss 00:00:10 -i '+filePath+' -frames:v 1 '+thumbNail
   
    cmdInterface(cmd)
    
def scanVideo(root:str,filePath:str):
    cmd=''+root+' -v error -print_format json -select_streams v:0 -show_streams -sexagesimal -i '+filePath
    videoInfo={}
    try:
        info = json.loads(cmdInterface(cmd))
        vinfo =info['streams'][0] 
        videoInfo['VFormat']= vinfo['codec_name']
        videoInfo['VCodecID']=vinfo['codec_long_name']
        videoInfo['VWidth']=vinfo['width']
        videoInfo['VHeight']=vinfo['height']
        videoInfo['VFrameRateMode']=vinfo['r_frame_rate']
        videoInfo['VFrameRate']=vinfo['avg_frame_rate']
        videoInfo['VDuration']=vinfo['duration']
        videoInfo['VFrameCount']=vinfo['nb_frames']
        videoInfo['VBitRate'] =vinfo['bit_rate']
        try:
            tinfo =vinfo['tags']
            videoInfo['VEncoder']=tinfo['encoder']
            videoInfo['VCreationTime']=tinfo['creation_time']
        except:
             pass

    except Exception as e:
        pass
        # print('Error',e)
    return videoInfo

def scanAudio(root:str,filePath:str):
    cmd=''+root+' -v error -print_format json -select_streams a:0 -show_streams  -i '+filePath
    audioInfo={}
    try:
        info = json.loads(cmdInterface(cmd))
        ainfo =info['streams'][0]
        audioInfo['AFormat']=ainfo['codec_name']
        audioInfo['AFormatSettings']=ainfo['codec_type']
        audioInfo['ACodecID']=ainfo['codec_long_name']
        audioInfo['ADuration']=ainfo['duration_ts']
        audioInfo['AChannels']=ainfo['channels']
        audioInfo['AChannelsLayout']=ainfo['channel_layout']
        audioInfo['ASamplingRate']=ainfo['sample_rate']
        audioInfo['ABitDepth']=ainfo['bit_rate']

    except Exception as e:
         pass
        # print('Error',e)
    return audioInfo
    