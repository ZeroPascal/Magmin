//https://stackoverflow.com/questions/15900485/correct-way-to-convert-size-in-bytes-to-kb-mb-gb-in-javascript
export function formatBytes(bytes:number, decimals = 2) {
    if (!+bytes) return '0 Bytes'

    const k = 1024
    const dm = decimals < 0 ? 0 : decimals
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
}

export function formatTime(time:number):string{
    const d=  new Date(time*1000)
    return d.toLocaleString()
    //return d.getHours()+':'+d.getMinutes()+':'+d.getSeconds()+' '+d.getMonth()+'/'+d.getDay()+'/'
  
}   

//d.getFullYear()+d.getMonth()+d.getDate+
//d.getHours()+':'+d.getMinutes()+':'+d.getSeconds()+' '+d.getMonth()+'/'+d.getDay()+'/'